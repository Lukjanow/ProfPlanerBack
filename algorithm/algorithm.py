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

def getModuleList(modules, calendar):
    module_list = []
    for module in modules.find({"frequency":calendar["frequency"]}):
        module["isSetBefore"] = False
        module_list.append(module)
    for module in modules.find({"frequency":3}):
        module["isSetBefore"] = False
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
                calendarEntry["module"]["isSetBefore"] = True
                planned_module_list.append(calendarEntry)
                isPlanned = True
        if isPlanned == False:
            module["isSetBefore"] = False
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
            full_mandatory_semester.append(str(i))
    return full_mandatory_semester, semi_mandatory_semester


def getSemesterModules(study_course, semester, module_list):
    semester_module_list = []
    for module in module_list:
        for study_semester in module["study_semester"]:
            if study_semester["studyCourse"] == study_course:
                if semester in study_semester["semesterNumbers"]:
                    semester_module_list.append(module)
    return semester_module_list


def getContentModules(study_course, content, module_list):
    content_module_list = []
    for module in module_list:
        for study_semester in module["study_semester"]:
            if study_semester["studyCourse"] == study_course:
                if len(study_semester["content"]) > 0:
                    if content in study_semester["content"]:
                        content_module_list.append(module)
    return content_module_list


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


def checkPerm(timetable, canOverlap):
    for key, value in timetable.items():
        dozent_list = []
        semester_list = []
        for module in value:
            for dozent in module["dozent"]:
                if dozent in dozent_list:
                    if module["isSetBefore"] == False:
                        return False, key
                else:
                    dozent_list.append(dozent)
            if canOverlap == False:
                for study_semester in module["study_semester"]:
                    if len(study_semester["semesterNumbers"]) == 1:
                        study_semester_object = (study_semester["studyCourse"], study_semester["semesterNumbers"][0])
                        if study_semester_object in semester_list:
                            if module["isSetBefore"] == False:
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
            pass
        else:
            new_perm_list.append(perm)
    return new_perm_list


def algorithm(timetable, meta_module_list, timetable_list, canOverlap=False):
    perm_list = []
    for perm in permutations(timetable_list):
        perm_list.append(perm)

    while len(perm_list) > 0:
        perm = perm_list[0]
        permSuccess = True

        for module_list in meta_module_list:

            for module_index, module in enumerate(module_list):
                module_perm_num = perm[module_index % len(timetable_list)]
                timetable[module_perm_num].append(module)

            permSuccess, block_num = checkPerm(timetable, canOverlap)

            for module_index, module in enumerate(module_list):
                    module_perm_num = perm[module_index % len(timetable_list)]
                    timetable[module_perm_num].pop()

            if permSuccess == False:
                perm_list = deletePermListElements(perm_list, block_num, perm)
                break

        if permSuccess:
            for module_list in meta_module_list:
                for module_index, module in enumerate(module_list):
                    module_perm_num = perm[module_index % len(timetable_list)]
                    timetable[module_perm_num].append(module)
            return timetable, True
    print("No perms left")
    return timetable, False
    



def main(id):
    # 1: Get Data

    modules = db["modules"]
    calendar_entries = db["calendarEntry"]
    calendars = db["calendar"]

    calendar = calendars.find_one(id)

    module_list = getModuleList(modules, calendar)
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
        print("StudyCourse", study_course["name"])
        #detect semi mandatory semester
        full_mandatory_semester_numbers, semi_mandatory_semester_numbers = detectSemiMandatorySemester(study_course, module_list)

        for semester in full_mandatory_semester_numbers:
            print("Semester", semester)
            # filtering modules
            semester_module_list = getSemesterModules(study_course, semester, module_list)
            semester_module_list = filterUnplannedModules(semester_module_list, timetable)

            for i in range(len(semester_module_list), 11):
                combinations_list = combinations(timetable_list, i)
                for block_list in combinations_list:
                    timetable, algoSuccess = algorithm(timetable, [semester_module_list], block_list)
                    if algoSuccess:
                        break
                if algoSuccess:
                    break



        max_mandatory_modules = 0
        meta_module_list = []
        difference_list = []
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

        for i in range(max_mandatory_modules, 11):
            combinations_list = combinations(timetable_list, i)
            for block_list in combinations_list:
                timetable, algoSuccess = algorithm(timetable, meta_module_list, block_list)
                if algoSuccess:
                    difference_list = [block for block in timetable_list if block not in block_list]
                    break
            if algoSuccess:
                break

        
        for content in study_course["content"]:
            print("Content", content)
            # filtering modules
            content_module_list = getContentModules(study_course, content, module_list)
            content_module_list = filterUnplannedModules(content_module_list, timetable)

            print("Amount", len(content_module_list))

            contentAlgoSuccess = False
            for i in range(len(content_module_list), 11 - max_mandatory_modules):
                combinations_list = combinations(difference_list, i)
                for block_list in combinations_list:
                    timetable, algoSuccess = algorithm(timetable, [content_module_list], block_list)
                    if algoSuccess:
                        contentAlgoSuccess = True
                        break
                if algoSuccess:
                    break
            if contentAlgoSuccess == False:
                timetable, algoSuccess = algorithm(timetable, [content_module_list], difference_list, True)

    print("timetable", timetable)
    calendar_entry_list = []
    for key, value in timetable.items():
        day = key//10
        time = key%10
        hours = None
        if time == 1:
            hours = 9
        else:
            hours = 13
        minutes = 0
        for module in value:
            if module in unplanned_module_list:
                calendar_entry = {
                    "module": module["_id"],
                    "time_stamp": {
                        "week_day": day,
                        "hour": hours,
                        "minute": minutes
                    },
                    "comment": None
                    }
                calendar_entry_list.append(calendar_entry)

    return calendar_entry_list


if __name__ == '__main__':
    main()