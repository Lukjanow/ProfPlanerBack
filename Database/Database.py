import pymongo

myclient = pymongo.MongoClient("mongodb://mongo")
db = myclient["ProfPlaner"]