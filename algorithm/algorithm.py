import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

import pymongo
from conflicts import checkTimetableForConflicts
from bson import ObjectId
from routes.modules import convertDataWithReferences
from itertools import permutations


def getPermNum(perm, module_index):
    for perm_num_index, perm_num in enumerate(perm):
        if perm_num_index == module_index:
            return perm_num


def getBlockIndex(perm, block_num):
    for index, num in enumerate(perm):
        if num == block_num:
           return index


def deletePermListElements(perm_list, block_num, block_index):
    print("CURRENT PERM LIST:",perm_list)
    # for perm_num_index, perm_num in enumerate(perm_list[perm_index]):
    #     if perm_num == block_num:
    #         block_index = perm_num_index 
    print("CONFLICT:",block_num,"at",block_index)
    new_perm_list = []
    for perm in perm_list:
        if perm[block_index] == block_num:
            print("BAD PERM:", perm)
        else:
            new_perm_list.append(perm)
    print("NEW PERM LIST:",new_perm_list)
    return new_perm_list

# while is_valid == False:
#     #perm_list_1
#     print("Starting perm list 1...")
#     print("current perm:", perm_list[perm_index])
#     for module_index, module in enumerate(b_ai_1_module_list):
#         perm_num = getPermNum(perm_list[perm_index], module_index)
#         for key, value in timetable.items():
#             if key == perm_num:
#                 value.append(module)

#     is_valid, block_num = checkTimetableForConflicts(timetable, planned_module_list)
    
#     if is_valid == False:
#         perm_list = deletePermListElements(perm_list, perm_index, block_num)
#         perm_index += 1


def getDatabaseData():
    myclient = pymongo.MongoClient("localhost", 27017)
    db = myclient.ProfPlaner

    modules = db["modules"]
    calendarentry = db["calendarEntry"]
    calendars = db["calendar"]
    return modules, calendarentry, calendars


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


def getModulesBySemester(module_list, study_course, semester_number):
    semester_module_list = []
    for module in module_list:
        for study_semester in module["study_semester"]:
            if study_semester["studyCourse"]["name"] == study_course:
                if semester_number in study_semester["semesterNumbers"]:
                    semester_module_list.append(module)
    return semester_module_list


def getModulesByContent(module_list, study_course, content):
    content_module_list = []
    for module in module_list:
        for study_semester in module["study_semester"]:
            if study_semester["studyCourse"]["name"] == study_course:
                if content in study_semester["content"]:
                    content_module_list.append(module)
    return content_module_list


def getStudyCourseList(module_list):
    study_course_list = []
    for module in module_list:
        for study_semester in module["study_semester"]:
            if study_semester["studyCourse"] not in study_course_list:
                study_course_list.append(study_semester["studyCourse"])
    return study_course_list


def filterOutNonMandatoryModules(module_list):
    # print("START MODULE LIST",module_list)
    for index, module in enumerate(module_list):
        for study_semester in module["study_semester"]:
            if len(study_semester["content"]) != 0:
                module_list.pop(index)
                break
    return module_list
        # print("MODULE LIST",module_list)

def filterOutNonMandatoryCalendarEntries(calendar_entry_list):
    # print("START MODULE LIST",module_list)

    for index, calendar_entry in enumerate(calendar_entry_list):
        module = calendar_entry["module"]
        for study_semester in module["study_semester"]:
            if len(study_semester["content"]) != 0:
                calendar_entry_list.pop(index)
                break
    return calendar_entry_list
        # print("MODULE LIST",module_list)


def getPermList(num_list):
    perm_list = []
    for perm in permutations(num_list):
        perm_list.append(perm)
    return perm_list
# print("NEW PLAN", timetable)


def algorithm(module_list, planned_module_list):
    print("Starting algorithm...")
    isValid = False

    num_list = [11, 21, 31, 41, 51]


    perm_list = getPermList(num_list)
    print("Starting perm list 1...")
    while len(perm_list) > 0:
        perm = perm_list[0]
        print("current perm:", perm)
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
        for module_index, module in enumerate(module_list):
            perm_num = getPermNum(perm, module_index)
            for key, value in timetable.items():
                if key == perm_num:
                    value.append(module)
                    break

        is_valid, block_num = checkTimetableForConflicts(timetable, planned_module_list)
        
        if is_valid == False:
            print("perm failed!")
            block_index = getBlockIndex(perm, block_num)
            for index, num in enumerate(perm):
                if num == block_num:
                    block_index = index
            perm_list = deletePermListElements(perm_list, block_num, block_index)
        else:
            print("perm succeeded!")
            return timetable


def main():
    #region initialize

    #get data from database
    modules, calendarEntries, calendars = getDatabaseData()

    #get module list with all modules
    module_list = getModuleList(modules)

    #get a calendar
    calendar = calendars.find_one(ObjectId("65d61765c15324dcfc497c4f"))

    #get a list of all calendar entries of that calendar
    calendar_entry_list = getCalendarEntryList(calendar, calendarEntries, modules)

    #split the module list to an planned an unplanned modules
    planned_module_list, unplanned_module_list = getModuleListsByPlanned(module_list, calendar_entry_list)

    unplanned_study_course_list = getStudyCourseList(unplanned_module_list)

    #endregion

    new_list = planned_module_list
    for calendar_entry in new_list:
        for study_semester in calendar_entry["module"]["study_semester"]:
            if study_semester["studyCourse"]["name"] == "AI B.Sc":
                if 4 in study_semester["semesterNumbers"]:
                    print(calendar_entry["time_stamp"])

    for study_course in unplanned_study_course_list:
        for i in range(1, study_course["semesterCount"] + 1):
            print(study_course["name"], i)
            semester_list = getModulesBySemester(unplanned_module_list, study_course["name"], i)
            semester_list = filterOutNonMandatoryModules(semester_list)
            # print(study_course["name"], i, semester_list)
            timetable = algorithm(semester_list, new_list)
            print(timetable)
            print()
            #algorithmus
        for content in study_course["content"]:
            content_list = getModulesByContent(unplanned_module_list, study_course["name"], content)
            print(study_course["name"], content, content_list)

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

    
    

if __name__ == '__main__':
    main()