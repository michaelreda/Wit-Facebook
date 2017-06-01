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
