import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

import pymongo
from algorithm.conflicts import checkTimetableForConflicts
from bson import ObjectId
from routes.modules import convertDataWithReferences
from itertools import permutations, combinations
from models.CalendarEntry import CalendarEntry
from Database.Database import db
import random

def getModuleList(modules):
    module_list = []
    for module in modules.find():
        module_list.append(module)
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


def initTimetable(timetable, module_list):
    for calendar_entry in module_list:
        start = calendar_entry["time_stamp"]
        end = {
            "week_day": start["week_day"],
            "hour": start["hour"] + (calendar_entry["module"]["duration"] // 60),
            "minute": start["minute"] + (calendar_entry["module"]["duration"] % 60)
            }
        if end["minute"] >= 60:
            end["hour"] += 1
            end["minute"] -= 60
        
        for key, value in timetable.items():
            if start["week_day"] == key//10:
                if key%10 == 1:
                    9 - 12.15
                    if (start["hour"] < 12) or (start["hour"] == 12 and start["minute"] < 15):
                        if (end["hour"] > 9) or (end["hour"] == 9 and end["minute"] > 0):
                            value.append(calendar_entry["module"])

                else:
                    13 - 16-15
                    if (start["hour"] < 16) or (start["hour"] == 16 and start["minute"] < 15):
                        if (end["hour"] > 13) or (end["hour"] == 13 and end["minute"] > 0):
                            value.append(calendar_entry["module"])
    return timetable


def detectSemiMandatorySemester(study_course, module_list):
    semi_mandatory_semester = []
    for module in module_list:
        for study_semester in module["study_semester"]:
            if study_semester["studyCourse"] == study_course:
                if len(study_semester["semesterNumbers"]) > 1:
                    for semester_number in study_semester["semesterNumbers"]:
                        if semester_number not in semi_mandatory_semester:
                            semi_mandatory_semester.append(semester_number)
    full_mandatory_semester = []
    for i in range(1, study_course["semesterCount"] + 1):
        if i not in semi_mandatory_semester:
            full_mandatory_semester.append(i)
    return full_mandatory_semester, semi_mandatory_semester


def getSemesterModules(study_course, semester, module_list):
    semester_module_list = []
    for module in module_list:
        for study_semester in module["study_semester"]:
            if study_semester["studyCourse"] == study_course:
                if semester in study_semester["semesterNumbers"]:
                    semester_module_list.append(module)
    return semester_module_list


def filterMandatoryModules(module_list, study_course):
    filtered_list = []
    for module in module_list:
        for study_semester in module["study_semester"]:
            if study_semester["studyCourse"] == study_course:
                if len(study_semester["semesterNumbers"]) == 1:
                    filtered_list.append(module)
    return filtered_list


def filterUnplannedModules(module_list, timetable):
    filtered_list = []
    for module in module_list:
        isSet = False
        for value in timetable.values():
            if module in value:
                isSet = True
                break
        if isSet == False:
            filtered_list.append(module)
    return filtered_list


def checkPerm(timetable):
    for key, value in timetable.items():
        dozent_list = []
        semester_list = []
        for module in value:
            for dozent in module["dozent"]:
                if dozent in dozent_list:
                    return False, key
                else:
                    dozent_list.append(dozent)
            for study_semester in module["study_semester"]:
                if len(study_semester["semesterNumbers"]) == 1:
                    study_semester_object = (study_semester["studyCourse"], study_semester["semesterNumbers"][0])
                    if study_semester_object in semester_list:
                        return False, key
                    else: 
                        semester_list.append(study_semester_object)
    return True, 0


def deletePermListElements(perm_list, block_num, error_perm):
    block_index = None
    for num_index, num in enumerate(error_perm):
        if num == block_num:
            block_index = num_index 
    print("CONFLICT:",block_num,"at",block_index)

    new_perm_list = []
    for perm in perm_list:
        if perm[block_index] == block_num:
            print("BAD PERM:", perm)
            pass
        else:
            new_perm_list.append(perm)
    return new_perm_list


def brainfuck(timetable, meta_module_list, timetable_list):
    perm_list = []
    for perm in permutations(timetable_list):
        perm_list.append(perm)

    while len(perm_list) > 0:
        perm = perm_list[0]
        # print("current perm:", perm)
        permSuccess = True

        for module_list in meta_module_list:

            for module_index, module in enumerate(module_list):
                module_perm_num = perm[module_index]
                timetable[module_perm_num].append(module)

            permSuccess, block_num = checkPerm(timetable)

            for module_index, module in enumerate(module_list):
                    module_perm_num = perm[module_index]
                    timetable[module_perm_num].pop()

            if permSuccess == False:
                perm_list = deletePermListElements(perm_list, block_num, perm)
                break

        if permSuccess:
            for module_list in meta_module_list:
                for module_index, module in enumerate(module_list):
                    module_perm_num = perm[module_index]
                    timetable[module_perm_num].append(module)
            return timetable, True
        
    return timetable, False
    



def main():
    # 1: Get Data

    modules = db["modules"]
    calendar_entries = db["calendarEntry"]
    calendars = db["calendar"]

    module_list = getModuleList(modules)

    calendar = calendars.find_one(ObjectId("65d61765c15324dcfc497c4f"))

    calendar_entry_list = getCalendarEntryList(calendar, calendar_entries, modules)

    planned_calendar_entry_list, unplanned_module_list = getModuleListsByPlanned(module_list, calendar_entry_list)

    unplanned_study_course_list = getStudyCourseList(unplanned_module_list)

    # 2: Create Timetable

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
    
    timetable_list = [11, 21, 31, 41, 51, 12, 22, 42, 52, 32]

    # 3: Put planned modules in Timetable

    timetable = initTimetable(timetable, planned_calendar_entry_list)

    # 4: put unplanned modules in Timetable

    for study_course in unplanned_study_course_list:

        #detect semi mandatory semester
        full_mandatory_semester_numbers, semi_mandatory_semester_numbers = detectSemiMandatorySemester(study_course, module_list)
        print("full", full_mandatory_semester_numbers)
        print("semi", semi_mandatory_semester_numbers)

        for semester in full_mandatory_semester_numbers:
            print("Semester", semester)
            # filtering modules
            semester_module_list = getSemesterModules(study_course, semester, module_list)
            semester_module_list = filterUnplannedModules(semester_module_list, timetable)

            print(semester_module_list)

            for i in range(len(semester_module_list), 11):
                combinations_list = combinations(timetable_list, i)
                for block_list in combinations_list:
                    timetable, algoSuccess = brainfuck(timetable, [semester_module_list], block_list)
                    if algoSuccess:
                        break
                if algoSuccess:
                    break



        max_mandatory_modules = 0
        meta_module_list = []
        for semester in semi_mandatory_semester_numbers:
            print("Semester", semester)
            # filtering modules
            semester_module_list = getSemesterModules(study_course, semester, module_list)
            semester_module_list = filterMandatoryModules(semester_module_list, study_course)
            semester_module_list = filterUnplannedModules(semester_module_list, timetable)
            meta_module_list.append(semester_module_list)
            semester_count = len(semester_module_list)
            if semester_count > max_mandatory_modules:
                max_mandatory_modules = semester_count

            print(semester_module_list)

            print(max_mandatory_modules)

        for i in range(max_mandatory_modules, 11):
            combinations_list = combinations(timetable_list, i)
            for block_list in combinations_list:
                timetable, algoSuccess = brainfuck(timetable, meta_module_list, block_list)
                if algoSuccess:
                    break
            if algoSuccess:
                break

        print("timetable", timetable)
        
        # full mandatory semester
        # semi mandatory semester
        # contents

    # 5: create CalendarEntries for unplanned modules
    
    return None
    
    pass

if __name__ == '__main__':
    main()