from bson import ObjectId
from fastapi import APIRouter, HTTPException
from models.Room import *
from models.common import *
from algorithm.algorithm import main as algorithm
from models.TimeStamp import TimeStamp
from models.CalendarEntry import CalendarEntryResponse
from routes.modules import convertDataWithReferences

router = APIRouter()

from Database.Database import db
calendarentry = db["calendarEntry"]
calendars = db["calendar"]
modules = db["modules"]

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
    newEntryList = []
    calendarEntryList = []

    if(calendar_entry_list is None):
        return []

    if(len(calendar_entry_list) != 0 ):
        id_list = calendarentry.insert_many(calendar_entry_list)
        for id in id_list.inserted_ids:
            newEntryList.append(str(id))
            calendarEntryList.append(str(id))
    calendar = calendars.find_one(calendar_id)

    if calendar == None:
        raise HTTPException(
        404, detail=f'calendar with ID {calendar_id} doesn\'t exist',)
    
    

    for entry in calendar["entries"]:
        calendarEntryList.append(entry)

    calendars.update_one({"_id": calendar_id}, {"$set":{"entries":calendarEntryList}})

    entryList = []

    for id in newEntryList:
        entry = calendarentry.find_one(ObjectId(id))
        entry["_id"] = str(entry["_id"])
        module = convertDataWithReferences([modules.find_one(ObjectId(entry["module"]))])[0]
        entry["module"] = module
        entryList.append(entry)

    return entryList