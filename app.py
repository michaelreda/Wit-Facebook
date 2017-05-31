import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot
from pprint import pprint

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAL0VIHjZAZAgBAIg0QRTxz3oEYXL6vr8crg5YCuIapca1AZAcghDCLg2QbX7epmw7WJtWSWqGZAk0KhdeTcHMBrM4cDZCZCLtzYIj04tZA4jp4XkCDWrxERZAZCmE1EZAjGOMF0ejS1zxaX4awgFZC4NZB5IaN0ZAfXTBIbF6MYQW9GWnQZDZD"

bot = Bot(PAGE_ACCESS_TOKEN)


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

				if messaging_event.get('message'):
					# Extracting text message
					if 'text' in messaging_event['message']:
						messaging_text = messaging_event['message']['text']
					else:
						messaging_text = 'no text'

					response = None

					entity, value = wit_response(messaging_text)
					if entity == 'mosalsal':
						response = "Ok, mawa3id {} : kol you el sa3a 10".format(str(value))
					elif entity == 'thanks':
						response = "you are welcome ;)".format(str(value))
                    elif entity == 'greetings'
                        response = "Hello".format(str(value))

					if response == None:
						response = "I have no idea what you are saying!"

					bot.send_text_message(sender_id, response)

	return "ok", 200


def log(message):
	print(message)
	sys.stdout.flush()

# ON_HEROKU = os.environ.get('ON_HEROKU')
#
# if ON_HEROKU:
#     # get the heroku port
#     port_num = int(os.environ.get('PORT', 33507))  # as per OP comments default is 17995
# else:
#     port_num = 3000

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=int(os.environ.get('PORT', 3000)))
