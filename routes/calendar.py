from bson import ObjectId
from fastapi import APIRouter, status, HTTPException
from models.Calendar import *
from models.CalendarEntry import *
from models.common import *

router = APIRouter()
# All API functions regarding calendars and it's entries

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


@router.get("/calendar/calendarentry/{calendar_id}/{calendarentry_id}",summary="get one CalendarEntry instance in Calendar",
        description="Get data about a specific calendar Entry according the given ID. Returns a Json with the Data.",
        tags=["Calendar"],
        response_model=CalendarEntryResponse, 
        responses={
            404: {"model": HTTPError, "detail": "str"},
            400: {"model": HTTPError, "detail": "str"}
            })
async def Get_one_CalendarEntry(
    calendar_id,
    calendarentry_id
):
    result = calendars.find_one(ObjectId(calendar_id))
    if result:  
        result = calendarentry.find_one(ObjectId(calendarentry_id))
        if result: #check if element exists in given calendar
            res = calendars.find({"entries": {"$elemMatch": {"$eq": ObjectId(calendarentry_id)}}})
            for each in res:
                if each["_id"]:
                        return result
                else:   
                    raise HTTPException(
                        400, detail=f'No Entry {calendar_id} in given Calendar',)
        raise HTTPException(    #calendarentry_id does not exist
            404, detail=f'CalendarEntry with ID {calendarentry_id} doesn\'t exist',)
    else:   #calendar_id does not exist
        raise HTTPException(
        404, detail=f'calendar with ID {calendar_id} doesn\'t exist',
    )

@router.get("/calendar/studysemester/{calendar_id}/{studysemester_id}",summary="get all CalendarEntry instances from one studysemester",
        description="Get data about a specific calendar Entry according the given ID. Returns a Json with the Data.",
        tags=["Calendar"],
        response_model=CalendarResponse, 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_calendar_semester(
    calendar_id,
    studysemester_id
):
    
     #TODO Get Calender based on Semester, wait for semester db to finish
    results = {"id": 0,
            "Entries": "str"}
    return results

@router.get("/calendar/dozent/{calendar_id}/{dozent_id}",summary="get all CalendarEntry instances from one dozent",
        description="Get data about a specific calendar Entry according the given ID. Returns a Json with the Data.",
        tags=["Calendar"],
        response_model=CalendarResponseCom, 
        responses={
            418: {"model": HTTPError, "detail": "str"},
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_calendar_dozent(
    calendar_id,
    dozent_id
):
    returncalendar = {}
    returnmodules = []
    entries = []
    returnentries = []
    moduleComplete = True
    calresult = calendars.find_one(ObjectId(calendar_id))
    if calresult:
        dozresult = dozents.find_one(ObjectId(dozent_id))
        if dozresult:
            returncalendar["_id"] = str(calresult["_id"])
            returncalendar["name"] = calresult["name"]
            #Find if dozent is assigned to any module
            modresults = modules.find({"dozent": {"$elemMatch": {"$eq": dozent_id}}})
            for r in modresults:
                print("Module: ", r)
                r.pop("_id")
                returnmodules.append(r)
            print(returnmodules)
            if returnmodules:
                 #Add entries to returncalendar
                for each in returnmodules:
                    print(each["id"])
                    #get all Entries with Module
                    entryRes = calendarentry.find({"module": each["id"]})
                    newentry = False
                    for entry in entryRes:
                        print(entry)
                        entry["_id"] = str(entry["_id"])
                        entries.append(entry)
                        newentry = True
                    if not newentry and moduleComplete:
                        moduleComplete = False
                        print("Module has no Entry")
                #check if entries are in current calendar
                for each in entries:
                    print("Found Entries")
                    #remove items not in searched calendar
                    if each["_id"] in calresult["entries"]:
                        print("Entry in Calendar")
                        each = str(each)
                        returnentries.append(each)
                print(returnentries)
                returncalendar["entries"] = returnentries  
                print("Assigned entries to Calendar")
                if moduleComplete:
                    returncalendar["details"] = None
                else:
                    returncalendar["details"] = "Not all Modules of the Dozent are in the Calendar"
                return returncalendar  
            else:
                raise HTTPException(
                418, detail=f'Dozent with ID {dozent_id} isn\'t assigned to a Module',
            )
        else:   #Dozent does not exist
            raise HTTPException(
            404, detail=f'Dozent with ID {dozent_id} doesn\'t exist',
        )
    else:   #Calendar does not exist
        raise HTTPException(
        404, detail=f'calendar with ID {calendar_id} doesn\'t exist',
    )


@router.get("/calendar/room/{calendar_id}/{room_id}",summary=" get all CalendarEntry instances from one room",
        description="Get data about a specific calendar Entry according the given ID. Returns a Json with the Data.",
        tags=["Calendar"],
        response_model=CalendarResponse, 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_calendar_room():
    #TODO Get Calender based on Room, wait for room db to finish
    results = {"id": 0,
            "Entries": "str"}
    return results


@router.post("/calendar",summary="add calendar",
        description="Add a calendar to the database based on the Input. Gives out a Message if successful.",
        tags=["Calendar"],
        response_model=CalendarResponse,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Add_calendar(
        CalendarResponse: CalendarResponse
    ):
    calendar_id = str(CalendarResponse.id)
    CalendarResponse = dict(CalendarResponse)

    calendars.insert_one(CalendarResponse)

    CalendarResponse["_id"] = calendar_id
    return CalendarResponse       

@router.post("/calendar/calendarentry/{calendar_id}",summary=" add CalendarEntry instance to Calendar",
        description="Add a calendar Entry to the database based on the Input. Gives out a Message if successful.",
        tags=["Calendar"],
        response_model=Message,
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
        resultcalendar = str(calendars.update_one({"_id": ObjectId(calendar_id)}, {"$set": res}))
        return {"message": str(resultentry) + resultcalendar}
    else:
        raise HTTPException(
        404, detail=f'Calendar with ID {calendar_id} doesn\'t exist',
    )

@router.put("/calendar/calendarentry/{calendar_id}/{calendarentry_id}",summary=" update one CalendarEntry instance in Calendar",
        description="Update a calendar Entry already in the database based on the Input. Gives out a Message if successful.",
        tags=["Calendar"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )

async def Update_calendarEntry(
        calendar_id,
        calendarentry_id,
        #TODO change to different solution to allow single line edits
        entry: CalendarEntryResponse
    ):
    res = calendars.find_one(ObjectId(calendar_id))
    #TODO check if Entry already exists(?)
    if res:
        res = calendarentry.find_one(ObjectId(calendarentry_id))
        if res:
            #Convert Model to dict
            timestamp = dict(entry.time_stamp)
            entry.time_stamp = {}
            entry = dict(entry)
            entry["time_stamp"] = timestamp
            #write to Database
            resultentry = str(calendarentry.update_one({"_id": ObjectId(calendarentry_id)}, {"$set": entry}))
            return {"message": str(resultentry)}
        else:
            raise HTTPException(
        404, detail=f'Calendar Entry with ID {calendarentry_id} doesn\'t exist',
    )
    else:
        raise HTTPException(
        404, detail=f'Calendar with ID {calendar_id} doesn\'t exist',
    )



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
    module = calendars.find_one({"id": int(calendar_id)})
    if module:
        res = calendars.delete_one({"id": int(calendar_id)})
        print(res)
        #TODO Remove Entries in Calendar
        return {"message": f'Successfully deleted Module {calendar_id}'}
    else:
        raise HTTPException(
        404, detail=f'Module with ID {calendar_id} doesn\'t exist',
    )

@router.delete("/calendar/calendarentry/{calendar_id}/{calendarentry_id}",summary="remove one CalendarEntry instance from Calendar",
        description="Delete a calendar Entry from the database based on the Input. Gives out a Message if successful.",
        tags=["Calendar"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Delete_calendarEntry(
    calendar_id,
    calendarentry_id
):
    calendar = calendars.find_one({"id": ObjectId(calendar_id)})
    if calendar:
        #TODO check if Calendar has Entry
        entry = calendarentry.find_one({"entries": ObjectId(calendarentry_id)})
        if entry:
            res = calendar.delete_one({"entries": ObjectId(calendarentry_id)})
            print(res)
            #TODO Remove Entry from Calendars
            return {"message": f'Successfully deleted Module {calendarentry_id}'}
        else:
            raise HTTPException(
            404, detail=f'Module with ID {calendarentry_id} doesn\'t exist',)
    else:
        raise HTTPException(
        404, detail=f'Module with ID {calendar_id} doesn\'t exist',
    )