def getDozentName(dozent):
    return str(dozent.name)

def checkTimetableForConflicts(timetable):
    for key, value in timetable.items():
        module_list = value
        dozent_dict = {}
        room_dict = {}
        for module in module_list:
            for dozent in module.dozent:
                dozent_name = getDozentName(dozent)
                if dozent_name in dozent_dict:
                    return False
                else:
                    dozent_dict[dozent_name] = [module]
    return True