import pymongo

myclient = pymongo.MongoClient("mongodb://admin:passwort@pp_mongodb")
db = myclient["ProfPlaner"]