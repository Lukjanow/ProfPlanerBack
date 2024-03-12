import sys
import os
print("HEX")
# Get the current directory of the script
current_dir = os.path.dirname(os.path.realpath(__file__))
print("HEX")
# Get the parent directory
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
print("HEX")
# Add the parent directory to sys.path
sys.path.append(parent_dir)
print("HEX")
# Now you can import modules from the 'routes' folder

# Now you can use functions or classes from routes.modules


from conflicts import checkTimetableForConflicts
from bson import ObjectId
from routes.modules import convertDataWithReferences
from Database.Database import db
print("HEX")
modules = db["modules"]
calendarentry = db["calendarEntry"]
calendars = db["calendar"]
print("HAX")
#TODO: GET ALL NOT PLANNED MODULES
re = modules.find()
print("HOX")
module_list = convertDataWithReferences(re)
print("HOX")
result = calendars.find_one(ObjectId("65d61765c15324dcfc497c4f"))
calendarEntrys = []
print("HEX")
for entry in result["entries"]:
    entryData = calendarentry.find_one(ObjectId(entry))
    moduledata = modules.find_one(ObjectId(entryData["module"]))
    entryData["module"] = convertDataWithReferences([moduledata])[0]
    entryData["_id"] = str(entryData["_id"])

    calendarEntrys.append(entryData)
print("MODULES", module_list)
print("CALENDAR ENTRIES", calendarEntrys)
#TODO: GET ALL MODULES FROM BACHELOR AI SEMESTER 1
# b_ai_1_module_list = []
# for module in module_list:
#     for study_semester in module.study_semester:
#         if study_semester.study_course.name == "AI B.Sc":
#             if study_semester.semesterNumbers.contains(1):
#                 b_ai_1_module_list.append(module)
# print(b_ai_1_module_list)

b_ai_1_module_list = ["eins","zwei","drei","vier","fünf"]
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

print(b_ai_1_module_list)
is_valid = False
while is_valid == False:
    for index, module in enumerate(b_ai_1_module_list):
        for key, value in timetable.items():
            if ((key//10) == index + 1) & ((key%10) == 1):
                value.append(module)
    is_valid = checkTimetableForConflicts(timetable)
print(timetable)