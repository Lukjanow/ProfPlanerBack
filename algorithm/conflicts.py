def getDozentName(dozent):
    return str(dozent["prename"] + " " + dozent["lastname"])

def overlapBlock(calendarEntry, block):
    print("BLOCK",block)
    day = calendarEntry["time_stamp"]["week_day"]
    blockDay = int(block) // 10
    if day != blockDay:
        return False
    start_hours = calendarEntry["time_stamp"]["hour"]
    start_minutes = calendarEntry["time_stamp"]["minute"]

    blockTime = int(block) % 10
    if blockTime == 1:
        blockHours = 9
    elif blockTime == 2:
        blockHours = 13
    blockMinutes = 0

    if (start_hours > blockHours + 3) | ((start_hours == blockHours + 3) & (start_minutes >= blockMinutes + 15)):
        return False
    duration_hours = calendarEntry["module"]["duration"] // 60
    duration_minutes = calendarEntry["module"]["duration"] % 60
    end_hours = start_hours + duration_hours
    end_minutes = start_minutes + duration_minutes
    if end_minutes >= 60:
        end_hours += 1
        end_minutes -= 60
    
    if (end_hours < blockHours) | ((end_hours == blockHours) & (end_minutes <= blockMinutes)):
        return False
    return True

def checkTimetableForConflicts(timetable, planned_module_list):
    for key, value in timetable.items():
        module_list = value
        dozent_dict = {}
        room_dict = {}
        for module in module_list:
            for dozent in module["dozent"]:
                dozent_name = getDozentName(dozent)
                if dozent_name in dozent_dict:
                    return False
                else:
                    dozent_dict[dozent_name] = [module]
        for key2, value in dozent_dict.items():
            for calendarEntry in planned_module_list:
                module = calendarEntry["module"]
                for dozent in module["dozent"]:
                    dozent_name = getDozentName(dozent)
                    if dozent_name == key2:
                        #check Time
                        if overlapBlock(calendarEntry, key):
                            return False
    return True