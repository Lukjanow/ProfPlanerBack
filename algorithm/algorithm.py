import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

import pymongo
from algorithm.conflicts import checkTimetableForConflicts
from bson import ObjectId
from routes.modules import convertDataWithReferences
from itertools import permutations
from models.CalendarEntry import CalendarEntry
from Database.Database import db
import random

def getModuleList(modules):
    module_list = []
    print(modules)
    print(modules.find())
    for module in modules.find():
        module_list.append(module)
    print("FOUND ALL MODULES")
    print("module list:",module_list)
    return convertDataWithReferences(module_list)


def getCalendarEntryList(calendar, calendarEntries, modules):
    calendarEntryList = []
    for entry in calendar["entries"]:
        entryData = calendarEntries.find_one(ObjectId(entry))
        moduledata = modules.find_one(ObjectId(entryData["module"]))
        entryData["module"] = convertDataWithReferences([moduledata])[0]
        entryData["_id"] = str(entryData["_id"])
        calendarEntryList.append(entryData)
    return calendarEntryList


def getModuleListsByPlanned(module_list, calendar_entry_list):
    unplanned_module_list = []
    planned_module_list = []
    for module in module_list:
        isPlanned = False
        for calendarEntry in calendar_entry_list:
            if module["_id"] == calendarEntry["module"]["_id"]:
                planned_module_list.append(calendarEntry)
                isPlanned = True
        if isPlanned == False:
            unplanned_module_list.append(module)
    return planned_module_list, unplanned_module_list


def getStudyCourseList(module_list):
    study_course_list = []
    for module in module_list:
        for study_semester in module["study_semester"]:
            if study_semester["studyCourse"] not in study_course_list:
                study_course_list.append(study_semester["studyCourse"])
    return study_course_list


def main():
    # 1: Get Data

    modules = db["modules"]
    calendar_entries = db["calendarEntry"]
    calendars = db["calendar"]

    module_list = getModuleList(modules)

    calendar = calendars.find_one(ObjectId("65d61765c15324dcfc497c4f"))

    calendar_entry_list = getCalendarEntryList(calendar, calendar_entries, modules)

    planned_module_list, unplanned_module_list = getModuleListsByPlanned(module_list, calendar_entry_list)

    unplanned_study_course_list = getStudyCourseList(unplanned_module_list)

    # 2: Create Timetable
    # 3: Put planned modules in Timetable
    # 4: put unplanned modules in Timetable
    # 5: create CalendarEntries for unplanned modules
    
    
    
    pass

if __name__ == '__main__':
    main()