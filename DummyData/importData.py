import json
import os
from bson import ObjectId
import pymongo
""" 
os.system('mongoimport --db ProfPlaner --collection dozent --file "ProfPlaner.dozent.json" --jsonArray')
os.system('mongoimport --db ProfPlaner --collection calendar --file "ProfPlaner.calendar.json" --jsonArray')
os.system('mongoimport --db ProfPlaner --collection calendarEntry --file "ProfPlaner.calendarEntry.json" --jsonArray')
os.system('mongoimport --db ProfPlaner --collection modules --file "ProfPlaner.modules.json" --jsonArray')
os.system('mongoimport --db ProfPlaner --collection rooms --file "ProfPlaner.rooms.json" --jsonArray')
os.system('mongoimport --db ProfPlaner --collection studysemester --file "ProfPlaner.studysemester.json" --jsonArray') """
""" 
""" 
def importDataToCollection(collection, fileName):
    with open(fileName, 'r') as file:
        file_data = json.load(file)

    for doc in file_data:
        doc['_id'] = ObjectId(doc['_id']['$oid'])

    if isinstance(file_data, list):
        collection.insert_many(file_data)  
    else:
        collection.insert_one(file_data)



myclient = pymongo.MongoClient("mongodb://mongo:27017/")
db = myclient["ProfPlaner"]

calendars = db["calendar"]
calendarentry = db["calendarEntry"]
modules = db["modules"]
rooms = db["rooms"]
dozentCollection = db["dozent"]
studyCourseCollection = db["studycourse"]

importDataToCollection(calendars, "ProfPlaner.calendar.json")
#importDataToCollection(calendarentry, "ProfPlaner.calendarEntry.json")
importDataToCollection(modules, "ProfPlaner.modules2.json")
importDataToCollection(rooms, "ProfPlaner.rooms2.json")
importDataToCollection(dozentCollection, "ProfPlaner.dozent1.json")
importDataToCollection(studyCourseCollection, "ProfPlaner.studycourse2.json")
