from bson import ObjectId
from fastapi import APIRouter, HTTPException
from models.Absence import *
from models.common import *
from models.Dozent import DozentRespone

from routes.dozent import dozentCollection

router = APIRouter()


def create_absences_update_list(dozent):
    update_list = []
    for item in dozent["absences"]:
        item = dict(item)
        item["begin"] = dict(item["begin"])
        item["end"] = dict(item["end"])

        update_list.append(item)

    update_data = {"absences": update_list}

    return update_data


# All API functions regarding absence
@router.post("/dozent/{dozent_id}/absence/",summary="add Absence to Dozent",
        description="Add Absence for a Dozent to the database based on the Input. Gives out a Message if successful.",
        tags=["Absence"],
        response_model= DozentRespone,
        responses={
            404: {"model": HTTPError, "detail": "str"},
            400: {"model": HTTPError, "detail": "str"}
        }
    )
async def Add_Abscence(dozent_id:str, absence:Absence):
    try:
        id = ObjectId(dozent_id)
    except:
        raise HTTPException(400, detail=f'{dozent_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string',)
    dozent = dozentCollection.find_one(id)

    if dozent == None:
        raise HTTPException(400, detail=f'Dozent with ID {id} doesn\'t exist',)

    absence.id = dozent["absences"][len(dozent["absences"]) - 1]["id"] + 1
    dozent["absences"].append(absence)

    dozentCollection.update_one({"_id": ObjectId(dozent_id)}, {"$set": create_absences_update_list(dozent)})
    dozent["_id"] = str(dozent["_id"])
    
    return dozent



@router.put("/dozent/{dozent_id}/absence/{absence_id}",summary="update one Absence of a Dozent",
        description="Update a Abscences already in the database based on the Input. Gives out a Message if successful.",
        tags=["Absence"],
        response_model=Absence,
        responses={
            404: {"model": HTTPError, "detail": "str"},
            400: {"model": HTTPError, "detail": "str"}
        }
    )
async def Update_Abscence(dozent_id:str, absence_id:int, changes:dict):
    try:
        id = ObjectId(dozent_id)
    except:
        raise HTTPException(400, detail=f'{dozent_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string',)
    
    dozent = dozentCollection.find_one(id)

    if dozent == None:
        raise HTTPException(400, detail=f'Dozent with ID {id} doesn\'t exist',)

    changeItem: Absence = None
    c = 0

    for item in dozent["absences"]:
        if item["id"] == absence_id:
            changeItem = item
            for key, value in changes.items():
                changeItem[key] = value
            dozent["absences"][c] = changeItem
            break
        c += 1
    
    if changeItem == None:
        raise HTTPException(status_code=400, detail=f"Absence with ID {absence_id} doesn\'t exist")

    dozentCollection.update_one({"_id": ObjectId(dozent_id)}, {"$set": create_absences_update_list(dozent)})
    return changeItem



@router.delete("/dozent/{dozent_id}/absence/{absence_id}",summary="delete one Absence from Dozent",
        description="Delete a Absence from the database based on the Input. Gives out a Message if successful.",
        tags=["Absence"],
        response_model=Message, 
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Delete_Absence(dozent_id:str, absence_id:int):
    try:
        id = ObjectId(dozent_id)
    except:
        raise HTTPException(400, detail=f'{dozent_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string',)
    
    dozent = dozentCollection.find_one(id)

    if dozent == None:
        raise HTTPException(400, detail=f'Dozent with ID {id} doesn\'t exist',)

    absence_list = []

    new_id = 0

    for item in dozent["absences"]:
        if item["id"] == absence_id:
            continue
        item["id"] = new_id
        new_id += 1
        absence_list.append(item)


    dozent["absences"] = absence_list

    dozentCollection.update_one({"_id": ObjectId(dozent_id)}, {"$set": create_absences_update_list(dozent)})
    return {"message": f"Successfully deleted Absence {absence_id} from Dozent with ID {dozent_id}"}