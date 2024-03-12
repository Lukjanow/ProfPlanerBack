import sys
import os
# Get the current directory of the script
current_dir = os.path.dirname(os.path.realpath(__file__))
# Get the parent directory
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
# Add the parent directory to sys.path
sys.path.append(parent_dir)
# Now you can import modules from the 'routes' folder

# Now you can use functions or classes from routes.modules

import pymongo

myclient = pymongo.MongoClient("localhost", 27017)
db = myclient.ProfPlaner

from conflicts import checkTimetableForConflicts
from bson import ObjectId
from routes.modules import convertDataWithReferences
modules = db["modules"]
calendarentry = db["calendarEntry"]
calendars = db["calendar"]
#TODO: GET ALL NOT PLANNED MODULES
module_list = []

unplanned_modul_list = []
planned_module_list = []
for modul in modules.find():
    module_list.append(modul)
module_list = convertDataWithReferences(module_list)
result = calendars.find_one(ObjectId("65d61765c15324dcfc497c4f"))
calendarEntrys = []
for entry in result["entries"]:
    entryData = calendarentry.find_one(ObjectId(entry))
    moduledata = modules.find_one(ObjectId(entryData["module"]))
    entryData["module"] = convertDataWithReferences([moduledata])[0]
    entryData["_id"] = str(entryData["_id"])

    calendarEntrys.append(entryData)
print("CALENDAR ENTRYS")
for calendarEntry in calendarEntrys:
    print(calendarEntry)

for module in module_list:
    isPlanned = False
    for calendarEntry in calendarEntrys:
        if module["_id"] == calendarEntry["module"]["_id"]:
            planned_module_list.append(calendarEntry)
            isPlanned = True
    if isPlanned == False:
        unplanned_modul_list.append(module)

#TODO: GET ALL MODULES FROM BACHELOR AI SEMESTER 1
b_ai_1_module_list = []
for module in module_list:
    for study_semester in module["study_semester"]:
        if study_semester["studyCourse"]["name"] == "AI B.Sc":
            if 1 in study_semester["semesterNumbers"]:
                b_ai_1_module_list.append(module)

# b_ai_1_module_list = ["eins","zwei","drei","vier","fünf"]
#TODO: GIVE ALL MODULES FROM BACHELOR AI SEMESTER 1 A TIMESLOT
timetable = {
    11: [], #MONDAY MORNING
    12: [], #MONDAY AFTERNOON
    21: [], #TUESDAY MORNING
    22: [], #TUESDAY AFTERNOON
    31: [], #WEDNESDAY MORNING
    32: [], #WEDNESDAY AFTERNOON
    41: [], #THURSDAY MORNING
    42: [], #THURSDAY AFTERNOON
    51: [], #FRIDAY MORNING
    52: [], #FRIDAY AFTERNOON
}

is_valid = False
while is_valid == False:
    for index, module in enumerate(b_ai_1_module_list):
        for key, value in timetable.items():
            if ((key//10) == index + 1) & ((key%10) == 1):
                value.append(module)
    is_valid = checkTimetableForConflicts(timetable, planned_module_list)
print("NEW PLAN", timetable)