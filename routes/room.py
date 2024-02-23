from fastapi import APIRouter,  HTTPException
from models.Room import *
from models.common import *

from typing import List
import copy

from utils.result_parser import remove_mongo_ids

router = APIRouter()

from Database.Database import db

rooms = db["rooms"]

@router.get("/room",summary="read all Room",
        description="Get all Rooms from Database. Returns an Array of Json's.",
        tags=["Room"],
        response_model=List[Room], responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_all_Rooms():
    results = rooms.find().sort("id", 1)
    results = remove_mongo_ids(results)
    return results


@router.get("/room/{room_id}",summary="read Room by ID",
        description="Get data about a specific Room according the given ID. Returns a Json with the Data.",
        tags=["Room"],
        response_model=Room, 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_one_Room(
    room_id
):
    result = rooms.find_one({"id": int(room_id)})
    if result: 
        result.pop("_id")
        return result
    else:   #Module does not exist
        raise HTTPException(
        404, detail=f'Module with ID {room_id} doesn\'t exist',
    )


@router.post("/room/add",summary="add Room",
        description="Add a Room to the database based on the Input. Gives out a Message if successful.",
        tags=["Room"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Add_Room(
        data: Room
    ):
    #check if module ID already exist
    if rooms.find_one({"id": data.id}):
        return {"message": f'A Module with ID {data.id} already exist'}

    data = dict(data)

    result = str(rooms.insert_one(data))
    print(result)
    return {"message": result}

# Need to clarify if this is the way how put is used; Body?
@router.put("/room/{room_id}",summary="update complete Room by ID",
        description="Update a Room already in the database based on the Input. Gives out a Message if successful.",
        tags=["Room"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Update_Room(
        room_id,
        name: str = None,
        capacity: int = None,
        equipment: int = None
    ):
    #Check if Room Exists
    #equipment = Equipment(*equipment)
    room = rooms.find_one({"id": int(room_id)})
    if not room: 
        raise HTTPException(
            404, detail=f'Module with ID {room_id} doesn\'t exist',
        )
    
    checkdata = copy.deepcopy(room)  #Copy the entry to check if something changed
    if name:
        room["name"] = name 
    if capacity:
        room["capacity"] = capacity
    if equipment:
        room["equipment"] = equipment

    if room == checkdata:
        print("No Updates")
        raise HTTPException(
            400, detail=f'No Data send to Update the Database.',
        )
    else:
        print("Update Room")
        rooms.update_one({"id": int(room_id)}, {"$set": room})
        return {"message": f'Updated Room {room_id}'}



@router.delete("/room/{room_id}",summary="delete Room by ID",
        description="Delete a Room from the database based on the Input. Gives out a Message if successful.",
        tags=["Room"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Delete_Room(
    room_id
):
    #Check if Room Exists
    room = rooms.find_one({"id": int(room_id)})
    if room:
        res = rooms.delete_one({"id": int(room_id)})
        return {"message": f'Successfully deleted Room {room_id}'}
    else:
        # Need to Clarify if this is the right response code
        raise HTTPException(
            400, detail=f'Room with ID {room_id} doesn\'t exist',
        )
