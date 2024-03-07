from bson import ObjectId
from fastapi import APIRouter,  HTTPException
from models.Room import *
from models.common import *

from typing import List
import copy

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
    results = rooms.find()

    resultList = []

    for result in results:
        result["_id"] = str(result["_id"])
        resultList.append(result)
    print
    return resultList


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
    try:
        id = ObjectId(room_id)
    except:
        raise HTTPException(400, detail=f'{room_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string',)
    result = rooms.find_one(id)

    if result == None:
        raise HTTPException(400, detail=f'Room with ID {id} doesn\'t exist',)
    
    result["_id"] = str(result["_id"])
    return result


   
@router.post("/room/add",summary="add Room",
        description="Add a Room to the database based on the Input. Gives out a Message if successful.",
        tags=["Room"],
        response_model=Room,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Add_Room(
        data: Room
    ):
    data = dict(data)
    rooms.insert_one(data)

    data["_id"] = str(data["_id"])
    return data



@router.put("/room/{room_id}",summary="update complete Room by ID",
        description="Update a Room already in the database based on the Input. Gives out a Message if successful.",
        tags=["Room"],
        response_model=Room,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Update_Room(
        room_id,
        changes:dict
    ):
    try:
        id = ObjectId(room_id)
    except:
        raise HTTPException(400, detail=f'{room_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string',)
    result = rooms.find_one(id)

    if result == None:
        raise HTTPException(400, detail=f'Room with ID {id} doesn\'t exist',)
    for key, value in changes.items():
            result[key] = value
    try:
        new_item = Room(id=room_id, roomNumber=result["roomNumber"], capacity=result["capacity"], roomType=result["roomType"])
    except:
        raise HTTPException(status_code=400, detail="TypeError")
    rooms.update_one({"_id": ObjectId(room_id)}, {"$set": changes})
    return new_item




@router.delete("/room/{room_id}",summary="delete Room by ID",
        description="Delete a Room from the database based on the Input. Gives out a Message if successful.",
        tags=["Room"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Delete_Room(room_id):
    try:
        id = ObjectId(room_id)
    except:
        raise HTTPException(400, detail=f'{room_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string',)
    
    rooms.delete_one({"_id": id})
    return {"message": f"Successfully deleted Dozent {room_id}"}