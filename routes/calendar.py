from fastapi import APIRouter, status, HTTPException
from models.Calendar import Calendar
from models.CalendarEntry import CalendarEntry
from models.common import *

router = APIRouter()
# All API functions regarding calendars

from Database.Database import db

calendars = db["calendar"]
calendarentry = db["calendarEntry"]


# https://stackoverflow.com/questions/76231804/fastapi-how-to-modularize-code-into-multiple-files-with-access-to-app-decorators#:~:text=1%20Answer&text=The%20modularization%20of%20routes%20in,assembled%20into%20a%20FastAPI%20application.
# Beispielstruktur: 
# https://github.com/skatesham/fastapi-bigger-application 


@router.get("/calendar/{calendar_id}",summary="read all CalendarEntry instances in Calendar",
        description="Get data about a specific calendar according the given ID. Returns a Json with the Data.",
        tags=["calendar"],
        response_model=Calendar, 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_one_calendar(
    calendar_id
):
    result = calendars.find_one({"id": calendar_id})
    if result:
        #remove id set by mongodb
        result.pop("_id")
        return result
    else:   #Module does not exist
        raise HTTPException(
        404, detail=f'calendar with ID {calendar_id} doesn\'t exist',
    )


@router.get("/calendar/calendarentry/{calendar_id}/{calendarentry_id}",summary="get one CalendarEntry instance in Calendar",
        description="Get data about a specific calendar Entry according the given ID. Returns a Json with the Data.",
        tags=["calendar"],
        response_model=CalendarEntry, 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_one_CalendarEntry(
    calendar_id,
    calendarentry_id
):
    result = calendars.find_one({"id": calendar_id})
    if result:
        result = calendars.find_one({"calendarEntry": calendarentry_id})
        if result:
            #remove id set by mongodb
            result.pop("_id")
            return result
        else:   #calendarentry_id does not exist
            raise HTTPException(
            404, detail=f'calendarEntry with ID {calendarentry_id} doesn\'t exist',)
    else:   #calendar_id does not exist
        raise HTTPException(
        404, detail=f'calendar with ID {calendar_id} doesn\'t exist',
    )

@router.get("/calendar/studysemester/{calendar_id}/{studysemester_id}",summary="get all CalendarEntry instances from one studysemester",
        description="Get data about a specific calendar Entry according the given ID. Returns a Json with the Data.",
        tags=["calendar"],
        response_model=Calendar, 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_calendar_semester():
    results = {"id": 0,
            "Entries": "str"}
    return results

@router.get("/calendar/dozent/{calendar_id}/{dozent_id}",summary="get all CalendarEntry instances from one dozent",
        description="Get data about a specific calendar Entry according the given ID. Returns a Json with the Data.",
        tags=["calendar"],
        response_model=Calendar, 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_calendar_dozent():
    results = {"id": 0,
            "Entries": "str"}
    return results

@router.get("/calendar/room/{calendar_id}/{room_id}",summary=" get all CalendarEntry instances from one room",
        description="Get data about a specific calendar Entry according the given ID. Returns a Json with the Data.",
        tags=["calendar"],
        response_model=Calendar, 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_calendar_room():
    results = {"id": 0,
            "Entries": "str"}
    return results


@router.post("/calendar",summary="add calendar",
        description="Add a calendar to the database based on the Input. Gives out a Message if successful.",
        tags=["calendar"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Add_calendar(
        entries: dict
    ):
    x = {"Entries": entries}
    results = str(calendars.insert_one(x))
    return {"message": results}

@router.post("/calendar/calendarentry/{calendar_id}",summary=" add CalendarEntry instance to Calendar",
        description="Add a calendar Entry to the database based on the Input. Gives out a Message if successful.",
        tags=["calendar"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Add_calendarEntry(
        data: CalendarEntry
    ):
    data = dict(data)
    result = str(calendarentry.insert_one(data))
    print(result)
    return {"message": result}

@router.put("/calendar/calendarentry/{calendar_id}/{calendarentry_id}",summary=" update one CalendarEntry instance in Calendar",
        description="Update a calendar Entry already in the database based on the Input. Gives out a Message if successful.",
        tags=["calendar"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )

async def Update_calendar(
        module: str,
        time_stamp: str
    ):
    results = {"message": "success"}
    return results

@router.delete("/calendar/{calendar_id}",summary="delete calendar by ID",
        description="Delete a calendar from the database based on the Input. Gives out a Message if successful.",
        tags=["calendar"],
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
        return {"message": f'Successfully deleted Module {calendar_id}'}
    else:
        raise HTTPException(
        404, detail=f'Module with ID {calendar_id} doesn\'t exist',
    )

@router.delete("/calendar/calendarentry/{calendar_id}/{calendarentry_id}",summary="remove one CalendarEntry instance from Calendar",
        description="Delete a calendar Entry from the database based on the Input. Gives out a Message if successful.",
        tags=["calendar"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Delete_calendarEntry(
    calendar_id,
    calendarentry_id
):
    #TODO Refactor
    calendar = calendars.find_one({"id": int(calendar_id)})
    if calendar:
        calendarentry = calendars.find_one({"entries": int(calendarentry_id)})
        if calendarentry:
            res = calendar.delete_one({"entries": int(calendarentry_id)})
            print(res)
            return {"message": f'Successfully deleted Module {calendarentry_id}'}
        else:
            raise HTTPException(
            404, detail=f'Module with ID {calendarentry_id} doesn\'t exist',)
    else:
        raise HTTPException(
        404, detail=f'Module with ID {calendar_id} doesn\'t exist',
    )