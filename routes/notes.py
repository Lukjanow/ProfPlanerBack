from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException
from Database.Database import db
from models.Notes import Note
from models.common import *
from bson.objectid import ObjectId
from typing import List

router = APIRouter()

notes = db["notes"]

@router.get("/notes",summary="read all Notes",
        description="Get all notes from Database. Returns an Array of Json's.",
        tags=["Notes"],
        response_model=List[Note], responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_all_Notes():
    results = notes.find()

    resultList = []

    for result in results:
        result["_id"] = str(result["_id"])
        resultList.append(result)

    return resultList



@router.get("/notes/{note_id}", summary="Get a note by ID",
        description="Get data about a specific note according the given ID. Returns a Json with the Data.",
        tags=["Notes"],
        response_model=Note, 
        responses={
            404: {"model": HTTPError, "detail": "str"},
            400: {"model": HTTPError, "detail": "str"}
            })
async def Get_one_Note(note_id):
    try:
        id = ObjectId(note_id)
    except:
        raise HTTPException(400, detail=f'{note_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string',)
    result = notes.find_one(id)

    if result == None:
        raise HTTPException(400, detail=f'Note with ID {id} doesn\'t exist',)
    
    result["_id"] = str(result["_id"])
    return result


@router.post("/notes",summary="add a Note",
        description="Add a Note to the database based on the Input. Gives out a Message if successful.",
        tags=["Notes"],
        response_model=Note,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Add_Room(
        data: Note
    ):
    data = dict(data)
    notes.insert_one(data)

    data["_id"] = str(data["_id"])
    return data



@router.delete("/notes/{note_id}", summary="Delete a Note by ID", response_model=Message, tags=["Notes"])
async def Delete_Note(note_id: str):
    try:
        id = ObjectId(note_id)
    except:
        raise HTTPException(status_code=400, detail=f'{note_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string')

    result = notes.delete_one({"_id": id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")

    return {"message": f"Successfully deleted Note {note_id}"}
    
