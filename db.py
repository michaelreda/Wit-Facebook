from pymongo import MongoClient

MONGO_HOST = "ds157641.mlab.com"
MONGO_PORT = 57641
MONGO_DB = "ramadan"
MONGO_USER = "admin"
MONGO_PASS = "admin"
connection = MongoClient(MONGO_HOST, MONGO_PORT)
db = connection[MONGO_DB]
db.authenticate(MONGO_USER, MONGO_PASS)
