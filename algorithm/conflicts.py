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
    #loop through every time block
    for key, value in timetable.items():
        module_list = value
        dozent_dict = {}
        #loop trough every module in this block
        for module in module_list:
            #loop through every dozent in module
            for dozent in module["dozent"]:
                #get the full name of the dozent
                dozent_name = getDozentName(dozent)
                #check if the dozent has already appeared in the time block
                if dozent_name in dozent_dict:
                    return (False, key)
                else:
                    dozent_dict[dozent_name] = [module]
        #loop through every dozent that appeares in the time block
        for key2, value in dozent_dict.items():
            #loop through every planned module
            for calendarEntry in planned_module_list:
                module = calendarEntry["module"]
                #loop through every dozent in this module
                for dozent in module["dozent"]:
                    #get the full name of the dozent
                    dozent_name = getDozentName(dozent)
                    #check if the planned module has the same dozent
                    if dozent_name == key2:
                        #check if the planned module overlaps with the current block
                        if overlapBlock(calendarEntry, key):
                            return (False, key)
    return (True, 0)