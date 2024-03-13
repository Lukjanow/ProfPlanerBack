from bson import ObjectId
from fastapi import APIRouter, HTTPException
from models.StudyCourse import StudyCourse
from models.common import *
from Database.Database import db

router = APIRouter()

studyCourseCollection = db["studycourse"]
studySemesterCollection = db["studysemester"]
modules = db["modules"]

@router.get("/studycourse",summary="read all StudyCourses",
        description="Get all StudyCourses from Database. Returns an Array of Json's.",
        tags=["StudyCourse"],
        response_model=list[StudyCourse], responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_all_StudyCourses():
    results = studyCourseCollection.find()

    resultList = []

    for result in results:
        result["_id"] = str(result["_id"])
        resultList.append(result)

    return resultList



@router.get("/studycourse/{studycourse_id}",summary="read StudyCourse by ID",
        description="Get data about a specific StudyCourse according the given ID. Returns a Json with the Data.",
        tags=["StudyCourse"],
        response_model=StudyCourse, 
        responses={
            400: {"model": HTTPError, "detail": "str"},
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_one_StudyCourse(studycourse_id: str):
    id: ObjectId

    try:
        id = ObjectId(studycourse_id)
    except:
        raise HTTPException(400, detail=f'{studycourse_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string',)

    result = studyCourseCollection.find_one(id)
    
    if result == None:
        raise HTTPException(400, detail=f'StudyCourse with ID {studycourse_id} doesn\'t exist',)

    result["_id"] = str(result["_id"])
    return result



@router.post("/studycourse",summary="add StudyCourse",
        description="Add a StudyCourse to the database based on the Input. Gives out a Message if successful.",
        tags=["StudyCourse"],
        response_model=StudyCourse,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Add_StudyCourse(studycourse: StudyCourse):
    studycourse = dict(studycourse)
    studyCourseCollection.insert_one(studycourse)

    studycourse["_id"] = str(studycourse["_id"])
    return studycourse



@router.put("/studycourse/{studycourse_id}",summary="update complete StudyCourse by ID",
        description="Update a StudyCourse already in the database based on the Input. Gives out a Message if successful.",
        tags=["StudyCourse"],
        response_model=StudyCourse,
        responses={
            404: {"model": HTTPError, "detail": "str"},
            400: {"model": HTTPError, "detail": "str"}
        }
    )
async def Update_StudyCourse(studycourse_id:str, changes: dict):
    try:
        id = ObjectId(studycourse_id)
    except:
        raise HTTPException(400, detail=f'{studycourse_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string',)
    
    item = studyCourseCollection.find_one(id)

    if item == None:
        raise HTTPException(400, detail=f'StudyCourse with ID {studycourse_id} doesn\'t exist',)

    for key, value in changes.items():
            item[key] = value
    try:
        new_item = StudyCourse(id=studycourse_id, name=item["name"], semesterCount=item["semesterCount"], content=item["content"])
    except:
        raise HTTPException(status_code=400, detail="TypeError")
    studyCourseCollection.update_one({"_id": ObjectId(studycourse_id)}, {"$set": changes})

    new_item.id = studycourse_id

    return new_item



@router.delete("/studycourse/{studycourse_id}",summary="delete StudyCourse by ID",
        description="Delete a StudyCourse from the database based on the Input. Gives out a Message if successful.",
        tags=["StudyCourse"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"},
            400: {"model": HTTPError, "detail": "str"}
        }
    )
async def Delete_StudyCourse(studycourse_id:str):
    try:
        id_course = ObjectId(studycourse_id)
    except:
        raise HTTPException(400, detail=f'{studycourse_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string',)
    
   
    moduleList = modules.find()

    for module in moduleList:
        newStudySemester = []
        if len(module["study_semester"]) == 0:
            continue
        for study in module["study_semester"]:
            if study["studyCourse"] != studycourse_id:
                newStudySemester.append(study)
        modules.update_one({"_id":module["_id"]}, {"$set":{"study_semester":newStudySemester}})

    
    studyCourseCollection.delete_one({"_id": id_course})
    return {"message": f"Successfully deleted StudyCourse {studycourse_id}"} 