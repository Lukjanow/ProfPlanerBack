from bson import ObjectId
from fastapi import APIRouter, HTTPException
from models.StudySemester import *
from models.common import *
from Database.Database import db

router = APIRouter()

studySemesterCollection = db["studysemester"]
modules = db["modules"]

# All API functions regarding studysemester

# https://stackoverflow.com/questions/76231804/fastapi-how-to-modularize-code-into-multiple-files-with-access-to-app-decorators#:~:text=1%20Answer&text=The%20modularization%20of%20routes%20in,assembled%20into%20a%20FastAPI%20application.
# Beispielstruktur: 
# https://github.com/skatesham/fastapi-bigger-application 


@router.get("/studysemester",summary="read all Studysemester",
        description="Get all Studysemesters from Database. Returns an Array of Json's.",
        tags=["Studysemester"],
        response_model=list[StudySemesterResponse], responses={
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
        response_model=StudySemesterResponse, 
        responses={
            400: {"model": HTTPError, "detail": "str"},
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_one_Studysemester(studysemester_id: str):
    id: ObjectId

    try:
        id = ObjectId(studysemester_id)
    except:
        raise HTTPException(400, detail=f'{studysemester_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string',)

    result = studySemesterCollection.find_one(id)
    
    if result == None:
        raise HTTPException(400, detail=f'StudySemester with ID {studysemester_id} doesn\'t exist',)

    result["_id"] = str(result["_id"])
    return result



@router.post("/studysemester",summary="add Studysemester",
        description="Add a Studysemester to the database based on the Input. Gives out a Message if successful.",
        tags=["Studysemester"],
        response_model=StudySemesterResponse,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Add_Studysemester(studysemester: StudySemesterResponse):
    studysemester = dict(studysemester)
    studySemesterCollection.insert_one(studysemester)

    studysemester["_id"] = str(studysemester["_id"])
    return studysemester



@router.put("/studysemester/{studysemester_id}",summary="update complete Studysemester by ID",
        description="Update a Studysemester already in the database based on the Input. Gives out a Message if successful.",
        tags=["Studysemester"],
        response_model=StudySemesterResponse,
        responses={
            404: {"model": HTTPError, "detail": "str"},
            400: {"model": HTTPError, "detail": "str"}
        }
    )
async def Update_Studysemester(studysemester_id:str, changes: dict):
    try:
        id = ObjectId(studysemester_id)
    except:
        raise HTTPException(400, detail=f'{studysemester_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string',)
    
    item = studySemesterCollection.find_one(id)

    if item == None:
        raise HTTPException(400, detail=f'StudySemester with ID {studysemester_id} doesn\'t exist',)

    for key, value in changes.items():
            item[key] = value
    try:
        new_item = StudySemesterResponse(id=studysemester_id, studyCourse=item["studyCourse"], semesterNumbers=item["semesterNumbers"], content=item["content"])
    except:
        raise HTTPException(status_code=400, detail="TypeError")
    studySemesterCollection.update_one({"_id": ObjectId(studysemester_id)}, {"$set": changes})

    new_item.id = studysemester_id

    return new_item



@router.delete("/studysemester/{studysemester_id}",summary="delete Studysemester by ID",
        description="Delete a Studysemester from the database based on the Input. Gives out a Message if successful.",
        tags=["Studysemester"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"},
            400: {"model": HTTPError, "detail": "str"}
        }
    )
async def Delete_Studysemester(studysemester_id:str):
    try:
        id = ObjectId(studysemester_id)
    except:
        raise HTTPException(400, detail=f'{studysemester_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string',)
    
    re = modules.find({"study_semester": {"$elemMatch": {"$eq": studysemester_id}}})

    for module in re:
        newStudysemesterList = []
        for studysemester in module["study_semester"]:
            if studysemester == studysemester_id:
                continue
            newStudysemesterList.append(studysemester)
        modules.update_one({"_id":module["_id"]}, {"$set":{"study_semester":newStudysemesterList}})
    
    studySemesterCollection.delete_one({"_id": id})
    return {"message": f"Successfully deleted StudySemester {studysemester_id}"}