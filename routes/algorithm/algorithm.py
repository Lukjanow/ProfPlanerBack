from conflicts import checkTimetableForConflicts

#TODO: GET ALL NOT PLANNED MODULES
module_list = []
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