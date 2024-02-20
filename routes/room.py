from fastapi import APIRouter

router = APIRouter()

from models.Models import *
# All API functions regarding Rooms


# https://stackoverflow.com/questions/76231804/fastapi-how-to-modularize-code-into-multiple-files-with-access-to-app-decorators#:~:text=1%20Answer&text=The%20modularization%20of%20routes%20in,assembled%20into%20a%20FastAPI%20application.
# Beispielstruktur: 
# https://github.com/skatesham/fastapi-bigger-application 


@router.get("/room",summary="read all Room",
        description="Get all Rooms from Database. Returns an Array of Json's.",
        tags=["Room"],
        response_model=Rooms, responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_all_Rooms():
    results = {"id": 0,
            "name": "str",
            "capacity": 100,
            "equipment": "str"}
    return results


@router.get("/room/{room_id}",summary="read Room by ID",
        description="Get data about a specific Room according the given ID. Returns a Json with the Data.",
        tags=["Room"],
        response_model=Room, 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_one_Room(
    id: int
):
    results = {"id": 0,
            "name": "str",
            "capacity": 100,
            "equipment": "str"}
    return results


@router.post("/room/add",summary="add Room",
        description="Add a Room to the database based on the Input. Gives out a Message if successful.",
        tags=["Room"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Add_Room(
        name: str,
        capacity: int,
        equipment: str
    ):
    results = {"message": "success"}
    return results

@router.put("/room/{room_id}",summary="update complete Room by ID",
        description="Update a Room already in the database based on the Input. Gives out a Message if successful.",
        tags=["Room"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Update_Room(
        name: str | None,
        capacity: int | None,
        equipment: str | None
    ):
    results = {"message": "success"}
    return results

@router.delete("/room/{room_id}",summary="delete Room by ID",
        description="Delete a Room from the database based on the Input. Gives out a Message if successful.",
        tags=["Room"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Delete_Room():
    results = {"message": "success"}
    return results