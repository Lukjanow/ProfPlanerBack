for key, value in timetable.items():
            if ((key//10) == index + 1) & ((key%10) == 1):
                value.append(module)