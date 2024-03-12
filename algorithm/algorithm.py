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
from itertools import permutations
num_list = [11, 21, 31, 41, 51]
perm_list = []

for perm in permutations(num_list):
    perm_list.append(perm)
print(perm_list)

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
for module in unplanned_modul_list:
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

# def getPermNum(perm_list, perm_index, module_index):
#     perm_num = None
#     for perm_num_index, perm_num in enumerate(perm_list[0]):
#         if perm_num_index == module_index:
#             block_num = perm_num
#     for perm_num_index, perm_num in enumerate(perm_list[perm_index]):
#         if perm_num == block_num:
#             return perm_num_index
        
def getPermNum(perm, module_index):
    for perm_num_index, perm_num in enumerate(perm):
        if perm_num_index == module_index:
            return perm_num

def deletePermListElements(perm_list, perm_index, block_num):
    block_index = None
    for perm_num_index, perm_num in enumerate(perm_list[perm_index]):
        if perm_num == block_num:
            block_index = perm_num_index 
    for index, perm in enumerate(perm_list):
        if index >= perm_index:
            if perm[block_index] == block_num:
                perm_list.drop(perm)
                index -= 1
    return perm_list


while is_valid == False:
    #perm_list_1

    num_list = [11, 21, 31, 41, 51]
    perm_list = []
    for perm in permutations(num_list):
        perm_list.append(perm)
    perm_index = 0

    for module_index, module in enumerate(b_ai_1_module_list):
        perm_num = getPermNum(perm_list[perm_index], module_index)
        for key, value in timetable.items():
            if key == perm_num:
                value.append(module)

    is_valid, block_num = checkTimetableForConflicts(timetable, planned_module_list)
    
    if is_valid == False:
        perm_list = deletePermListElements(perm_list, perm_index, block_num)
        perm_index += 1


print("NEW PLAN", timetable)