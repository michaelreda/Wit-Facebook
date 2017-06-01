import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot
from pprint import pprint
import json
from db import db



app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAL0VIHjZAZAgBAIg0QRTxz3oEYXL6vr8crg5YCuIapca1AZAcghDCLg2QbX7epmw7WJtWSWqGZAk0KhdeTcHMBrM4cDZCZCLtzYIj04tZA4jp4XkCDWrxERZAZCmE1EZAjGOMF0ejS1zxaX4awgFZC4NZB5IaN0ZAfXTBIbF6MYQW9GWnQZDZD"

bot = Bot(PAGE_ACCESS_TOKEN)


from fbmq import Page,Template, QuickReply

PAGE_ACCESS_TOKEN = "EAAL0VIHjZAZAgBAIg0QRTxz3oEYXL6vr8crg5YCuIapca1AZAcghDCLg2QbX7epmw7WJtWSWqGZAk0KhdeTcHMBrM4cDZCZCLtzYIj04tZA4jp4XkCDWrxERZAZCmE1EZAjGOMF0ejS1zxaX4awgFZC4NZB5IaN0ZAfXTBIbF6MYQW9GWnQZDZD"

page = Page(PAGE_ACCESS_TOKEN)

page.show_persistent_menu([Template.ButtonPostBack('MENU1', 'MENU_PAYLOAD/1'),
						   Template.ButtonPostBack('MENU2', 'MENU_PAYLOAD/2')])

@page.callback(['MENU_PAYLOAD/(.+)'])
def click_persistent_menu(payload, event):
  click_menu = payload.split('/')[1]
  print("you clicked %s menu" % click_menu)


@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == "just_do_it":
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Hello world!", 200

@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	log(data)

	if data['object'] == 'page':
		for entry in data['entry']:
			for messaging_event in entry['messaging']:

				# IDs
				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']

				#managing sessions
				import datetime
				current_time= datetime.datetime.utcnow()
				db.sessions.update_one({'sender_id':sender_id}, {"$set": {"last_commit":current_time}}, upsert=True) # if-find-else-update
				session = db.sessions.find_one({'sender_id':sender_id})
				print(session)

				if messaging_event.get('message'):
					# Extracting text message
					if 'text' in messaging_event['message']:
						messaging_text = messaging_event['message']['text']
					else:
						messaging_text = 'no text'

					response = None

					entities = wit_response(messaging_text)
					# dir_path = os.path.dirname(os.path.realpath(__file__))
					# print(dir_path)
					# file = open('/app/sessions/'+sender_id+'.json', 'w+')
					# pprint(json.load(file))

					#checking for responses i am waiting for
					#checking for reminder Time
					if session.get("waiting_for_reminder_time") !=None:
						from db import set_reminder
						response,Done=set_reminder(session.get("mosalsal"),int(messaging_text),sender_id)

						if Done:
							session["waiting_for_reminder_time"]= None
					mosalsal=None
					reminder= False
					#checking for mosalsal
					for entity in entities:
						# pprint(entity)
						if entity["name"] == 'mosalsal':
							mosalsal= entity["value"]
							session["mosalsal"]=mosalsal
							# response = "Ok, mawa3id {} : kol you el sa3a 10".format(str(value))

					#checking for reminders
					for entity in entities:
						if entity["name"] == 'reminderUser':
							reminder=True
							if session.get("mosalsal") == None :
								response="please enter esm el mosalsal.."
							else:
								# response="Ok I'll remind you with mosalsal "+str(session["mosalsal"])
								from db import get_mosalsal_timing
								response="Ok please select a timing number to remind you with..\n"
								response+= get_mosalsal_timing(session.get("mosalsal"))
								session["waiting_for_reminder_time"]=True
								quick_replies = [
									{'title': 'Cancel', 'payload': 'canel_reminder'}
								]
								page.send(sender_id,
								quick_replies=quick_replies)


					#if no reminder and there is a mosalsal then show schedule

					if mosalsal!=None and not reminder:
						from db import get_mosalsal_timing
						response= get_mosalsal_timing(session.get("mosalsal"))
					else:
						for entity in entities:
							if entity["name"] == 'thanks':
								response = "you are welcome ;)"
							elif entity["name"] == 'greetings':
								response = "Hello"
							elif entity["name"] == 'bye':
								response = "bye"

					#machine learning part
					if response == None:
						#if no response then check unkonws
						message= db.unkown.find_one({'message':messaging_text});
						# print(message)
						if message==None: #if message not found insert it
							db.unkown.insert({'sender_id':sender_id,'message':messaging_text})
							response = "I have no idea what you are saying.. I'm still learning"
						elif message.get("answer")!= None: #if there is an answer then send it
							response= message['answer']
						else: #if saved but no answer then send i don't know it
							response = "I have no idea what you are saying.. I'm still learning"

					db.sessions.save(session)
					bot.send_text_message(sender_id, response)

	return "ok", 200


def log(message):
	# print(message)
	sys.stdout.flush()

#clearing sessions
import threading
def clear_sessions():
	db.sessions.remove()
	print("sessions cleared")
	threading.Timer(30*60, clear_sessions).start() #every 30minutes clear sessions

clear_sessions()


# ON_HEROKU = os.environ.get('ON_HEROKU')
#
# if ON_HEROKU:
#     # get the heroku port
#     port_num = int(os.environ.get('PORT', 33507))  # as per OP comments default is 17995
# else:
#     port_num = 3000

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=int(os.environ.get('PORT', 3000)))
