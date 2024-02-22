from bson import ObjectId
from fastapi import APIRouter, HTTPException
from models.StudySemester import *
from models.common import *
from Database.Database import db

router = APIRouter()

studySemesterCollection = db["studysemester"]


# All API functions regarding studysemester

# https://stackoverflow.com/questions/76231804/fastapi-how-to-modularize-code-into-multiple-files-with-access-to-app-decorators#:~:text=1%20Answer&text=The%20modularization%20of%20routes%20in,assembled%20into%20a%20FastAPI%20application.
# Beispielstruktur: 
# https://github.com/skatesham/fastapi-bigger-application 


@router.get("/studysemester",summary="read all Studysemester",
        description="Get all Studysemesters from Database. Returns an Array of Json's.",
        tags=["Studysemester"],
        response_model=list[StudySemester], responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_all_Studysemesters():
    results = studySemesterCollection.find()

    resultList = []

    for result in results:
        result["_id"] = str(result["_id"])
        resultList.append(result)

    return resultList



@router.get("/studysemester/{studysemester_id}",summary="read Studysemester by ID",
        description="Get data about a specific Studysemester according the given ID. Returns a Json with the Data.",
        tags=["Studysemester"],
        response_model=StudySemester, 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_one_Studysemester(studysemester_id: str):
    result = studySemesterCollection.find_one(ObjectId(studysemester_id))

    result["_id"] = str(result["_id"])
    return result



@router.post("/studysemester",summary="add Studysemester",
        description="Add a Studysemester to the database based on the Input. Gives out a Message if successful.",
        tags=["Studysemester"],
        response_model=StudySemester,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Add_Studysemester(studysemester: StudySemester):
    studysemester = dict(studysemester)
    studySemesterCollection.insert_one(studysemester)

    studysemester["_id"] = str(studysemester["_id"])
    return studysemester



@router.put("/studysemester/{studysemester_id}",summary="update complete Studysemester by ID",
        description="Update a Studysemester already in the database based on the Input. Gives out a Message if successful.",
        tags=["Studysemester"],
        response_model=StudySemester,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Update_Studysemester(studysemester_id:str, changes: dict):
    item = studySemesterCollection.find_one(ObjectId(studysemester_id))
    for key, value in changes.items():
            item[key] = value
    try:
        new_item = StudySemester(id=studysemester_id, name=item["name"], study=item["study"], content=item["content"])
    except:
        raise HTTPException(status_code=400, detail="TypeError")
    studySemesterCollection.update_one({"_id": ObjectId(studysemester_id)}, {"$set": changes})

    return new_item



@router.delete("/studysemester/{studysemester_id}",summary="delete Studysemester by ID",
        description="Delete a Studysemester from the database based on the Input. Gives out a Message if successful.",
        tags=["Studysemester"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Delete_Studysemester(studysemester_id:str):
    studySemesterCollection.delete_one({"_id": ObjectId(studysemester_id)})
    return {"message": f"Successfully deleted StudySemester {studysemester_id}"}