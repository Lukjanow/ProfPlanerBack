from bson import ObjectId
from fastapi import APIRouter, status, HTTPException
from models.Calendar import *
from models.CalendarEntry import *
from models.common import *
from routes.modules import convertDataWithReferences

router = APIRouter()
# All API functions regarding calendars and it's entries
# TODO: Create Routes with Data send instead of IDS for example: Not dozent: "id" but dozent: [{"id": id, "name": "name"}..., {"id": id, "name": "name"...}...]

from Database.Database import db

calendars = db["calendar"]
calendarentry = db["calendarEntry"]
modules = db["modules"]
rooms = db["rooms"]
dozents = db["dozent"]
studysemester = db["studysemester"]


# https://stackoverflow.com/questions/76231804/fastapi-how-to-modularize-code-into-multiple-files-with-access-to-app-decorators#:~:text=1%20Answer&text=The%20modularization%20of%20routes%20in,assembled%20into%20a%20FastAPI%20application.
# Beispielstruktur: 
# https://github.com/skatesham/fastapi-bigger-application 

@router.get("/calendar",summary="Get all Calendars",
        description="Get data about all calendars. Returns a List with the Data.",
        tags=["Calendar"],
        response_model=list[CalendarResponse], 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_all_calendar():
    results = calendars.find()

    resultList = []

    for result in results:
        result["_id"] = str(result["_id"])
        resultList.append(result)
    
    return resultList


@router.get("/calendar/{calendar_id}",summary="Get Calendar by ID",
        description="Get data about a specific calendar according the given ID. Returns a Json with the Data.",
        tags=["Calendar"],
        response_model=CalendarResponse, 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_one_calendar(
    calendar_id
):
    result = calendars.find_one(ObjectId(calendar_id))
    if result:
        result["_id"] = str(result["_id"])
        return result
    else:   #Calendar does not exist
        raise HTTPException(
        404, detail=f'calendar with ID {calendar_id} doesn\'t exist',
    )


@router.get("/calendar/entrys/{calendar_id}",summary="Get CalendarEntrys from Calendar",
        description="Get all CalendarEntrys from a specific Calendar. Returns a Json with the Data and all reference Data.",
        tags=["Calendar"],
        response_model=list[CalendarEntry], 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def getCalendarEntriesFromCalendar(
    calendar_id
):
    result = calendars.find_one(ObjectId(calendar_id))
    if result:
        response = []
        for entry in result["entries"]:
            entryData = calendarentry.find_one(ObjectId(entry))
            moduledata = modules.find_one(ObjectId(entryData["module"]))
            entryData["module"] = convertDataWithReferences([moduledata])[0]
            entryData["_id"] = str(entryData["_id"])

            response.append(entryData)
        return response
    else:   #Calendar does not exist
        raise HTTPException(
        404, detail=f'calendar with ID {calendar_id} doesn\'t exist',
    )


@router.get("/calendar/calendarentry/{calendarentry_id}",summary="get one CalendarEntry instance in Calendar",
        description="Get data about a specific calendar Entry according the given ID. Returns a Json with the Data.",
        tags=["Calendar"],
        response_model=CalendarEntryResponse, 
        responses={
            404: {"model": HTTPError, "detail": "str"},
            400: {"model": HTTPError, "detail": "str"}
            })
async def Get_one_CalendarEntry(
    calendarentry_id
):
    result = calendarentry.find_one(ObjectId(calendarentry_id))
    if not result: 
        raise HTTPException(   
        404, detail=f'CalendarEntry with ID {calendarentry_id} doesn\'t exist',)
         
    result["_id"] = str(result["_id"])
    
    return result
           

@router.get("/calendar/studysemester/{calendar_id}/{studysemester_id}",summary="get all CalendarEntry instances from one studysemester",
        description="Get data about a specific calendar Entry according the given ID. Returns a Json with the Data.",
        tags=["Calendar"],
        response_model=list[CalendarEntry], 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_calendar_semester(
    calendar_id,
    studysemester_id
):
    calendar = calendars.find_one({"_id":ObjectId(calendar_id)})

    if not calendar:
        raise HTTPException(
        404, detail=f'calendar with ID {calendar_id} doesn\'t exist',)
    
    entryList = []

    for entry_id in calendar["entries"]:
        entryData = calendarentry.find_one({"_id": ObjectId(entry_id)})

        if not entryData:
            raise HTTPException(
            404, detail=f'CalendarEntry with ID {entry_id} doesn\'t exist',)
        
        moduleData = modules.find_one({"_id": ObjectId(entryData["module"])})

        if not moduleData:
            raise HTTPException(
            404, detail=f'Module with ID {entryData["module"]} doesn\'t exist',)
        
        if studysemester_id in moduleData["study_semester"]:
            entryData["_id"] = str(entryData["_id"])
            entryData["module"] = convertDataWithReferences([moduleData])[0]

            entryList.append(entryData)

    return entryList


@router.get("/calendar/dozent/{calendar_id}/{dozent_id}",summary="get all CalendarEntry instances from one dozent",
        description="Get data about a specific calendar Entry according the given ID. Returns a Json with the Data.",
        tags=["Calendar"],
        response_model=list[CalendarEntry], 
        responses={
            418: {"model": HTTPError, "detail": "str"},
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_calendar_dozent(
    calendar_id,
    dozent_id
):
    calendar = calendars.find_one({"_id":ObjectId(calendar_id)})

    if not calendar:
        raise HTTPException(
        404, detail=f'calendar with ID {calendar_id} doesn\'t exist',)
    
    entryList = []

    for entry_id in calendar["entries"]:
        entryData = calendarentry.find_one({"_id": ObjectId(entry_id)})

        if not entryData:
            raise HTTPException(
            404, detail=f'CalendarEntry with ID {entry_id} doesn\'t exist',)
        
        moduleData = modules.find_one({"_id": ObjectId(entryData["module"])})

        if not moduleData:
            raise HTTPException(
            404, detail=f'Module with ID {entryData["module"]} doesn\'t exist',)
        
        if dozent_id in moduleData["dozent"]:
            entryData["_id"] = str(entryData["_id"])
            entryData["module"] = convertDataWithReferences([moduleData])[0]

            entryList.append(entryData)

    return entryList



@router.get("/calendar/room/{calendar_id}/{room_id}",summary=" get all CalendarEntry instances from one room",
        description="Get data about a specific calendar Entry according the given ID. Returns a Json with the Data.",
        tags=["Calendar"],
        response_model=list[CalendarEntry], 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_calendar_room(
    calendar_id,
    room_id
):
    calendar = calendars.find_one({"_id":ObjectId(calendar_id)})

    if not calendar:
        raise HTTPException(
        404, detail=f'calendar with ID {calendar_id} doesn\'t exist',)
    
    entryList = []

    for entry_id in calendar["entries"]:
        entryData = calendarentry.find_one({"_id": ObjectId(entry_id)})

        if not entryData:
            raise HTTPException(
            404, detail=f'CalendarEntry with ID {entry_id} doesn\'t exist',)
        
        moduleData = modules.find_one({"_id": ObjectId(entryData["module"])})

        if not moduleData:
            raise HTTPException(
            404, detail=f'Module with ID {entryData["module"]} doesn\'t exist',)
        
        if moduleData["room"] == None:
            continue

        if type(moduleData["room"] == list):
            if room_id in moduleData["room"]:
                entryData["_id"] = str(entryData["_id"])
                entryData["module"] = convertDataWithReferences([moduleData])[0]

                entryList.append(entryData)
        else: 
            if room_id == moduleData["room"]:
                entryData["_id"] = str(entryData["_id"])
                entryData["module"] = convertDataWithReferences([moduleData])[0]

                entryList.append(entryData)

    return entryList


@router.post("/calendar",summary="add calendar",
        description="Add a calendar to the database based on the Input. Gives out a Message if successful.",
        tags=["Calendar"],
        response_model=CalendarResponse,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Add_calendar(
        data: CalendarResponse
    ):
    data = dict(data)
    calendars.insert_one(data)

    data["_id"] = str(data["_id"])
    return data


@router.post("/calendar/calendarentry/{calendar_id}",summary=" add CalendarEntry instance to Calendar",
        description="Add a calendar Entry to the database based on the Input. Gives out a Message if successful.",
        tags=["Calendar"],
        response_model=CalendarEntryResponse,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Add_calendarEntry(
        calendar_id,
        data: CalendarEntryResponse
    ):
    res = calendars.find_one(ObjectId(calendar_id))
    if res:
        #Convert Model to dict
        timestamp = dict(data.time_stamp)
        data.time_stamp = {}
        data = dict(data)
        data["time_stamp"] = timestamp
        #write to Database
        resultentry = calendarentry.insert_one(data)
        print(type(resultentry.inserted_id))
        res["entries"] += [str(resultentry.inserted_id)]
        calendars.update_one({"_id": ObjectId(calendar_id)}, {"$set": res})

        data["_id"] = str(data["_id"])
        return data
    else:
        raise HTTPException(
        404, detail=f'Calendar with ID {calendar_id} doesn\'t exist',
    )


@router.put("/calendar/calendarentry/{calendarentry_id}",summary=" update one CalendarEntry",
        description="Update a calendar Entry already in the database based on the Input. Gives out a Message if successful.",
        tags=["Calendar"],
        response_model=CalendarEntryResponse,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Update_calendarEntry(
        calendarentry_id,
        changes:dict
    ):
    try:
        id = ObjectId(calendarentry_id)
    except:
        raise HTTPException(400, detail=f'{calendarentry_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string',)
    result = calendarentry.find_one(id)

    if result == None:
        raise HTTPException(400, detail=f'CalendarEntry with ID {id} doesn\'t exist',)
    for key, value in changes.items():
            result[key] = value
    try:
        new_item = CalendarEntryResponse(id=calendarentry_id, module=result["module"], time_stamp=result["time_stamp"], comment=result["comment"])
    except:
        raise HTTPException(status_code=400, detail="TypeError")
    calendarentry.update_one({"_id": ObjectId(calendarentry_id)}, {"$set": changes})

    new_item.id = calendarentry_id

    return new_item


@router.delete("/calendar/{calendar_id}",summary="delete calendar by ID",
        description="Delete a calendar from the database based on the Input. Gives out a Message if successful.",
        tags=["Calendar"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Delete_calendar(
    calendar_id
):
    try:
        id = ObjectId(calendar_id)
    except:
        raise HTTPException(400, detail=f'{calendar_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string',)
    
    re = calendars.find_one({"_id": id})

    if not re:
        raise HTTPException(404, detail=f'Calendar with ID {calendar_id} not found',)
    
    for entry in re["entries"]:
        calendarentry.delete_one({"_id": entry})
        

    calendars.delete_one({"_id": id})
    return {"message": f"Successfully deleted Calendar {calendar_id}"}


@router.delete("/calendar/calendarentry/{calendarentry_id}",summary="remove one CalendarEntry instance from Calendar",
        description="Delete a calendar Entry from the database based on the Input. Gives out a Message if successful.",
        tags=["Calendar"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Delete_calendarEntry(
    calendarentry_id
):
    resultCalendars = calendars.find()

    for calendar in resultCalendars:
        if calendarentry_id not in calendar["entries"]:
            continue
        calendar["entries"].remove(calendarentry_id)
        calendars.update_one({"_id":calendar["_id"]},{"$set":{"entries":calendar["entries"]}})

    calendarentry.delete_one({"_id":ObjectId(calendarentry_id)})

    return {"message": f"Successfully deleted CalendarEntry {calendarentry_id}"}
            

@router.put("/calendar/{calendar_id}",summary=" update one Calendar",
        description="Update a calendar already in the database based on the Input. Gives out a Message if successful.",
        tags=["Calendar"],
        response_model=CalendarResponse,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Update_calendarEntry(
        calendar_id,
        changes:dict
    ):
    try:
        id = ObjectId(calendar_id)
    except:
        raise HTTPException(400, detail=f'{calendar_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string',)
    result = calendars.find_one(id)

    if result == None:
        raise HTTPException(400, detail=f'Calendar with ID {id} doesn\'t exist',)
    for key, value in changes.items():
            result[key] = value
    try:
        new_item = CalendarResponse(id=calendar_id, name=result["name"], entries=result["entries"])
    except:
        raise HTTPException(status_code=400, detail="TypeError")
    calendars.update_one({"_id": ObjectId(calendar_id)}, {"$set": changes})

    new_item.id = calendar_id

    return new_item
