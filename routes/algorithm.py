from bson import ObjectId
from fastapi import APIRouter
from models.Room import *
from models.common import *
from algorithm.algorithm import main as algorithm
from models.TimeStamp import TimeStamp
from models.CalendarEntry import CalendarEntryResponse

router = APIRouter()

from Database.Database import db
calendarentry = db["calendarEntry"]
calendars = db["calendar"]

@router.post("/algorithm",summary="run the algorithm",
        description="Adds a calendarEntry to every not planned module.",
        tags=["Algorithm"],
    )
async def RunAlgorithm():
    calendar_id = ObjectId("65d61765c15324dcfc497c4f")
    calendar_entry_list = algorithm()
    # id_list = []
    # for calendar_entry in calendar_entry_list:
    #     id_list.append(calendarentry.insert_one(calendar_entry))
    id_list = calendarentry.insert_many(calendar_entry_list)
    calendar = calendars.find_one(calendar_id)

    if calendar == None:
        return "ERROR"
    
    newEntryList = []

    for entry in calendar["entries"]:
        newEntryList.append(entry)

    print("---------------------")
    print(type(id_list))
    print(id_list)
    print("-----------------------")

    for id in id_list.inserted_ids:
        newEntryList.append(str(id))

    calendars.update_one({"_id": calendar_id}, {"$set":{"entries":newEntryList}})

    return "calendar_entry_list"