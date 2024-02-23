import os

os.system('mongoimport --db ProfPlaner --collection dozent --file "ProfPlaner.dozent.json" --jsonArray')
os.system('mongoimport --db ProfPlaner --collection calendar --file "ProfPlaner.calendar.json" --jsonArray')
os.system('mongoimport --db ProfPlaner --collection calendarEntry --file "ProfPlaner.calendarEntry.json" --jsonArray')
os.system('mongoimport --db ProfPlaner --collection modules --file "ProfPlaner.modules.json" --jsonArray')
os.system('mongoimport --db ProfPlaner --collection rooms --file "ProfPlaner.rooms.json" --jsonArray')
os.system('mongoimport --db ProfPlaner --collection studysemester --file "ProfPlaner.studysemester.json" --jsonArray')