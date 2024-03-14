import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client.ProfPlaner

modules = db.modules

print(modules)
for module in modules.find():
    print(module)