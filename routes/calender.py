from fastapi import APIRouter
from models.Calendar import Calendar
from models.CalendarEntry import CalendarEntry

router = APIRouter()

# All API functions regarding Calenders
def NOT_FOUND(r):
    return {}

# https://stackoverflow.com/questions/76231804/fastapi-how-to-modularize-code-into-multiple-files-with-access-to-app-decorators#:~:text=1%20Answer&text=The%20modularization%20of%20routes%20in,assembled%20into%20a%20FastAPI%20application.
# Beispielstruktur: 
# https://github.com/skatesham/fastapi-bigger-application 


@router.get("/calender/{calender_id}",summary="read all CalendarEntry instances in Calendar",
        description="Get data about a specific Calender according the given ID. Returns a Json with the Data.",
        tags=["Calender"],
        response_model=Calendar, 
        responses={
            404: NOT_FOUND("Calendar")
            })
async def Get_one_Calender(
    id: int
):
    results = {"id": 0,
            "Entries": "str"}
    return results

@router.get("/calendar/calendarentry/{calendar_id}/{calendarentry_id}",summary="get one CalendarEntry instance in Calendar",
        description="Get data about a specific Calender Entry according the given ID. Returns a Json with the Data.",
        tags=["Calender"],
        response_model=CalendarEntry, 
        responses={
            404: NOT_FOUND("CalendarEntry")
            })
async def Get_one_CalenderEntry():
    results = {"module": "str",
            "time_stamp": "str"}
    return results

@router.get("/calendar/studysemester/{calendar_id}/{studysemester_id}",summary="get all CalendarEntry instances from one studysemester",
        description="Get data about a specific Calender Entry according the given ID. Returns a Json with the Data.",
        tags=["Calender"],
        response_model=Calendar, 
        responses={
            404: NOT_FOUND("Calendar")
            })
async def Get_Calender_semester():
    results = {"id": 0,
            "Entries": "str"}
    return results

@router.get("/calendar/dozent/{calendar_id}/{dozent_id}",summary="get all CalendarEntry instances from one dozent",
        description="Get data about a specific Calender Entry according the given ID. Returns a Json with the Data.",
        tags=["Calender"],
        response_model=Calendar, 
        responses={
            404: NOT_FOUND("Calendar")
            })
async def Get_Calender_dozent():
    results = {"id": 0,
            "Entries": "str"}
    return results

@router.get("/calendar/room/{calendar_id}/{room_id}",summary=" get all CalendarEntry instances from one room",
        description="Get data about a specific Calender Entry according the given ID. Returns a Json with the Data.",
        tags=["Calender"],
        response_model=Calendar, 
        responses={
            404: NOT_FOUND("Calendar")
            })
async def Get_Calender_room():
    results = {"id": 0,
            "Entries": "str"}
    return results


@router.post("/calender",summary="add Calender",
        description="Add a Calender to the database based on the Input. Gives out a Message if successful.",
        tags=["Calender"],
        response_model=Calendar,
        responses={
            404: NOT_FOUND("Calendar")
        }
    )
async def Add_Calender(
        entries: dict
    ):
    results = {"message": "success"}
    return results

@router.post("/calendar/calendarentry/{calendar_id}",summary=" add CalendarEntry instance to Calendar",
        description="Add a Calender Entry to the database based on the Input. Gives out a Message if successful.",
        tags=["Calender"],
        response_model=CalendarEntry,
        responses={
            404: NOT_FOUND("CalendarEntry")
        }
    )
async def Add_CalenderEntry(
        module: str,
        time_stamp: str
    ):
    results = {"message": "success"}
    return results

@router.put("/calendar/calendarentry/{calendar_id}/{calendarentry_id}",summary=" update one CalendarEntry instance in Calendar",
        description="Update a Calender Entry already in the database based on the Input. Gives out a Message if successful.",
        tags=["Calender"],
        response_model=CalendarEntry,
        responses={
            404: NOT_FOUND("CalendarEntry")
        }
    )

async def Update_Calender(
        module: str,
        time_stamp: str
    ):
    results = {"message": "success"}
    return results

@router.delete("/calender/{calender_id}",summary="delete Calender by ID",
        description="Delete a Calender from the database based on the Input. Gives out a Message if successful.",
        tags=["Calender"],
        response_model=Calendar,
        responses={
            404: NOT_FOUND("Calendar")
        }
    )
async def Delete_Calender():
    results = {"message": "success"}
    return results

@router.delete("/calendar/calendarentry/{calendar_id}/{calendarentry_id}",summary="remove one CalendarEntry instance from Calendar",
        description="Delete a Calender Entry from the database based on the Input. Gives out a Message if successful.",
        tags=["Calender"],
        response_model=CalendarEntry,
        responses={
            404: NOT_FOUND("CalendarEntry")
        }
    )
async def Delete_CalenderEntry():
    results = {"message": "success"}
    return results