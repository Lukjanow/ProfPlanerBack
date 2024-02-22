from fastapi import APIRouter, HTTPException
from models.Dozent import *
from models.Absence import Absence
from models.common import *
from bson.objectid import ObjectId
from Database.Database import db
from typing import List

router = APIRouter()

router = APIRouter()
dozentCollection = db["dozent"]

# All API functions regarding Dozents


# https://stackoverflow.com/questions/76231804/fastapi-how-to-modularize-code-into-multiple-files-with-access-to-app-decorators#:~:text=1%20Answer&text=The%20modularization%20of%20routes%20in,assembled%20into%20a%20FastAPI%20application.
# Beispielstruktur: 
# https://github.com/skatesham/fastapi-bigger-application 


@router.get("/dozent",summary="read all Dozent",
        description="Get all Dozent from Database. Returns an Array of Json's.",
        tags=["Dozent"],
        response_model=List[DozentRespone], responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_all_Dozents():
    results = dozentCollection.find()

    resultList = []

    for result in results:
        result["_id"] = str(result["_id"])
        resultList.append(result)

    return resultList



@router.get("/dozent/{dozent_id}",summary="read Dozent by ID",
        description="Get data about a specific Dozent according the given ID. Returns a Json with the Data.",
        tags=["Dozent"],
        response_model=DozentRespone, 
        responses={
            404: {"model": HTTPError, "detail": "str"},
            400: {"model": HTTPError, "detail": "str"}
            })
async def Get_one_Dozent(dozent_id: str):
    try:
        id = ObjectId(dozent_id)
    except:
        raise HTTPException(400, detail=f'{dozent_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string',)
    result = dozentCollection.find_one(id)

    if result == None:
        raise HTTPException(400, detail=f'Dozent with ID {id} doesn\'t exist',)
    
    result["_id"] = str(result["_id"])
    return result



@router.get("/dozent/absence/{dozent_id}",summary="Read all Absences by Dozent",
        description="Gives out all absences a Dozent has. Returns an Array of Json if successful",
        tags=["Dozent"],
        response_model=list[Absence],
        responses={
            404: {"model": HTTPError, "detail": "str"},
            400: {"model": HTTPError, "detail": "str"}
        }
    )
async def get_Dozent_absences(dozent_id: str):
    try:
        id = ObjectId(dozent_id)
    except:
        raise HTTPException(400, detail=f'{dozent_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string',)
    result = dozentCollection.find_one(id)

    if result == None:
        raise HTTPException(400, detail=f'Dozent with ID {id} doesn\'t exist',)
    
    resultList = []

    for item in result["absences"]:
        resultList.append(item)

    return resultList



@router.post("/dozent",summary="add Dozent",
        description="Add a Dozent to the database based on the Input. Gives out a Message if successful.",
        tags=["Dozent"],
        response_model=DozentRespone,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Add_Dozent(dozent: DozentRespone):
    dozent_id = str(dozent.id)
    dozent = dict(dozent)

    if dozent["absences"] != None:
        absenceList = []
        for absence in dozent["absences"]:
            absence = dict(absence)
            absence["begin"] = dict(absence["begin"])
            absence["end"] = dict(absence["end"])
            absenceList.append(absence)

        dozent["absences"] = absenceList
    dozentCollection.insert_one(dozent)

    dozent["_id"] = dozent_id
    return dozent



@router.put("/dozent/{dozent_id}",summary="update complete Dozent by ID",
        description="Update a Dozent already in the database based on the Input. Gives out a Message if successful.",
        tags=["Dozent"],
        response_model=DozentRespone,
        responses={
            404: {"model": HTTPError, "detail": "str"},
            400: {"model": HTTPError, "detail": "str"}
        }
    )
async def Update_Dozent(dozent_id:str, changes:dict):
    try:
        id = ObjectId(dozent_id)
    except:
        raise HTTPException(400, detail=f'{dozent_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string',)
    result = dozentCollection.find_one(id)

    if result == None:
        raise HTTPException(400, detail=f'Dozent with ID {id} doesn\'t exist',)
    for key, value in changes.items():
            result[key] = value
    try:
        new_item = DozentRespone(id=dozent_id, name=result["name"], e_mail=result["e_mail"], title=result["title"],absences=result["absences"],intern=result["intern"])
    except:
        raise HTTPException(status_code=400, detail="TypeError")
    dozentCollection.update_one({"_id": ObjectId(dozent_id)}, {"$set": changes})
    return new_item



@router.delete("/dozent/{dozent_id}",summary="delete Dozent by ID",
        description="Delete a Dozent from the database based on the Input. Gives out a Message if successful.",
        tags=["Dozent"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"},
            400: {"model": HTTPError, "detail": "str"}
        }
    )
async def Delete_Modul(dozent_id:str):
    try:
        id = ObjectId(dozent_id)
    except:
        raise HTTPException(400, detail=f'{dozent_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string',)
    
    dozentCollection.delete_one({"_id": id})
    return {"message": f"Successfully deleted Dozent {dozent_id}"}
