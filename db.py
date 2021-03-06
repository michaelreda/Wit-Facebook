from pymongo import MongoClient

MONGO_HOST = "ds157641.mlab.com"
MONGO_PORT = 57641
MONGO_DB = "ramadan"
MONGO_USER = "admin"
MONGO_PASS = "admin"
connection = MongoClient(MONGO_HOST, MONGO_PORT)
db = connection[MONGO_DB]
db.authenticate(MONGO_USER, MONGO_PASS)

def get_mosalsal_timing(mosalsal):
	mosalsal= db.mosalsalat.find_one({'name':mosalsal})
	timings_str=""
	i=1
	for timing in mosalsal["timings"]:
		timings_str+=str(i)+")at "
		timings_str+=timing["time"]
		timings_str+=" on "
		timings_str+=timing["channel"]
		timings_str+="\n"
		i+=1
	return timings_str

def set_reminder(mosalsal_name,timing_num,sender_id):
	mosalsal= db.mosalsalat.find_one({'name':mosalsal_name})
	Done=False
	if(timing_num<=len(mosalsal["timings"]) and timing_num>0):
		timing = mosalsal["timings"][timing_num-1]
		db.reminders.save({
		"sender_id":sender_id,
		"mosalsal":mosalsal_name,
		"time":timing["time"],
		"channel":timing["channel"]
		})
		response="Ok reminder set for mosalsal "+mosalsal_name+" everyday at "+timing["time"]+" on "+timing["channel"]+"."
		response+="\nYou can check your reminders by writing my reminders."
		Done=True
	else:
		response="please enter a number from 1 to "+str(len(mosalsal["timings"]))+" .. \n"
		response+= get_mosalsal_timing(mosalsal_name)
	return (response,Done)
