import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017")

db = client.logindb
res = db.loginAuth.find()
for r in res:
    print(r)
