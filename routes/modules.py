from bson import ObjectId
from fastapi import APIRouter, status, HTTPException

from typing import List
from copy import * #Allow to copy Dict
from models.common import *
from models.Module import *
import re
import uuid 

router = APIRouter()

from Database.Database import db

dozents = db["dozent"]
rooms = db["rooms"]
modules = db["modules"]
calendars = db["calendar"]
calendarentry = db["calendarEntry"]
studycourse = db["studycourse"]
# All API functions regarding Modules



# https://stackoverflow.com/questions/76231804/fastapi-how-to-modularize-code-into-multiple-files-with-access-to-app-decorators#:~:text=1%20Answer&text=The%20modularization%20of%20routes%20in,assembled%20into%20a%20FastAPI%20application.
# Beispielstruktur: 
# https://github.com/skatesham/fastapi-bigger-application 


def convertDataWithReferences(re):
    x = []
   
    for result in re:
        dozent = []
        for id in result["dozent"]:
            res = dozents.find_one({"_id": ObjectId(str(id))})
            if res != None:
                res["_id"] = str(res["_id"])
            dozent.append(res)
        result["dozent"] = dozent
        study_semester = []
        for res in result["study_semester"]:
            if res != None:
                resCourse = studycourse.find_one({"_id": ObjectId(str(res["studyCourse"]))})
                resCourse["_id"] = str(resCourse["_id"])
                res["studyCourse"] = resCourse
                res["_id"] = str(res["_id"])
            study_semester.append(res)
        result["study_semester"] = study_semester

        roomList = []
        for id in result["room"]:
            res = rooms.find_one({"_id": ObjectId(str(id))})
            if res != None:
                res["_id"] = str(res["_id"])
            roomList.append(res)
        result["room"] = roomList
        result["_id"] = str(result["_id"])
        x.append(result)
    return x

@router.get("/module",summary="read all Modules",
        description="Get all Modules from Database. Returns an Array of Json's. Response contain only Dozent ID, Room ID and studysemester ID",
        tags=["Modules"],
        response_model=List[ModuleResponse])
async def Get_all_Modules():
    results = modules.find()

    resultList = []

    for result in results:
        result["_id"] = str(result["_id"])
        resultList.append(result)
    
    return resultList


@router.get("/module/{object_id}",summary=" read one Module by ID",
        description="Get data about a Module according the given object_id. Returns a Json with the Data.",
        tags=["Modules"],
        response_model=ModuleResponse, 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_one_Module(object_id):
    re = modules.find_one(ObjectId(object_id))

    if re:
        re["_id"] = str(re["_id"])
        return re
    else:   #Module does not exist
        raise HTTPException(
        404, detail=f'Module with ID {object_id} doesn\'t exist',
    )

@router.get("/moduledata/{object_id}",summary=" read one Module by ID  and get Data from referenced Data",
        description="Get data about a Module according the given object_id. Returns a Json with the Data. Also gives Back data for Dozent, Rooms and Studysemester",
        tags=["Modules"],
        response_model=Module, 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_one_Module(object_id):
    re = modules.find_one(ObjectId(object_id))

    if re:
        re = convertDataWithReferences([re])[0]
        re["_id"] = str(re["_id"])
        return re
    else:   #Module does not exist
        raise HTTPException(
        404, detail=f'Module with ID {object_id} doesn\'t exist',
    )


@router.get("/module/basicdata/", summary="Read all Modules for basic data",
        description="Get all modules for the basic data table. Returns a list of JSONs with the selected fields.",
        tags=["Modules"],
        response_model=list[BasicModule]
    )
async def Get_BasicData_Modules():
    fields = {"name": 1, "code": 1, "dozent": 1, "room": 1, "study_semester": 1, "duration": 1}

    modules_list = modules.find({}, fields)

    selected_modules = []

    for module in modules_list:
        module["_id"] = str(module["_id"])
        selected_modules.append(module)   

    selected_modules = convertDataWithReferences(selected_modules) 
        
    if selected_modules:
        return selected_modules
    else:
        # Raise HTTPException if no modules found
        raise HTTPException(status_code=404, detail='No modules found')



@router.get("/moduledata",summary="read all Modules and get Data about referenced objects",
        description="Get all Modules from Database. Returns an Array of Json's. Response contain also Data about Dozent, Room and studysemester ",
        tags=["Modules"],
        response_model=List[Module])
async def Get_all_Modules_data():
    re = modules.find()
    x = convertDataWithReferences(re)
  
    return x



@router.get("/moduledata/module/{module_id}",summary="read all Modules with the same module_id and get Data from referenced Data",
        description="Get data about Modules according the given module_id. Returns a Json with the Data. Also gives Back data for Dozent, Rooms and Studysemester",
        tags=["Modules"],
        response_model=List[Module], 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_Modules_by_id(
    module_id
):
    re = modules.find({"module_id": module_id})
    x = convertDataWithReferences(re)
    if x:
        return x
    else:   #Module does not exist
        raise HTTPException(
        404, detail=f'Module with ID {module_id} doesn\'t exist',
    )



@router.get("/module/module/{module_id}",summary=" read Modules with the same module_id",
        description="Get data about Modules according the given module_id. Returns a Json with the Data.",
        tags=["Modules"],
        response_model=List[ModuleResponse], 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_Modules_moduleid(
    module_id
):
    re = modules.find({"module_id": module_id})
    x = []
    for result in re:
        result["_id"] = str(result["_id"])
        x.append(result)
    if x:
        return x
    else:   #Module does not exist
        raise HTTPException(
        404, detail=f'Module with ID {module_id} doesn\'t exist',
    )



@router.get("/modules/select",summary="read all selected Moduls",
        description="Read all Modules that are currently selected ",
        tags=["Modules"],
        response_model=List[ModuleResponse], 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_selected_Modules():
    x = []
    result = modules.find({"selected": True}).sort("id", 1)
    for r in result:
        r["_id"] = str(r["_id"])
        x.append(r)
    if x == []:
        raise HTTPException(
        404, detail=f'No Modules found',
    )
    return x



@router.get("/modules/unselect",summary="read all unselected Moduls",
        description="Read all Modules that are currently unselected ",
        tags=["Modules"],
        response_model=List[ModuleResponse], 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_selected_Modules():
    x = []
    result = modules.find({"selected": False}).sort("id", 1)
    for r in result:
        r["_id"] = str(r["_id"])
        x.append(r)
    if x == []:
        raise HTTPException(
        404, detail=f'No Modules found',
    )
    return x



@router.get("/modulesdata/select",summary="read all selected Moduls and get data from referenced Objects",
        description="Read all Modules that are currently selected ",
        tags=["Modules"],
        response_model=List[Module], 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_selected_Modules_data():
    re = modules.find({"selected": True}).sort("id", 1)
    x = convertDataWithReferences(re)
    
    if x == []:
        raise HTTPException(
        404, detail=f'No Modules found',
    )
    return x


@router.get("/modulesdata/unselect",summary="read all unselected Moduls and get data from referenced Objects",
        description="Read all Modules that are currently unselected ",
        tags=["Modules"],
        response_model=List[Module], 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_selected_Modules_data():
    re = modules.find({"selected": False}).sort("id", 1)
    x = convertDataWithReferences(re)
    
    if x == []:
        raise HTTPException(
        404, detail=f'No Modules found',
    )
    return x

# @router.get("/module/room/{room_id}}",summary="read all Modules by Room",
#         description="Get data about multiple specific Modules according the given Room ID. Returns a Array of Json with the Data.",
#         tags=["Modules"],
#         response_model=Modules, 
#         responses={
#             404: {"model": HTTPError, "detail": "str"}
#             })
# async def Get_selected_Modules_by_room(
#     id: int
# ):
#     results = {"id": id,
#             "name": "str",
#             "dozent_id": 0,
#             "room_id": 0,
#             "study_semester": "str",
#             "need": "enumerate",
#             "type": "enumerate",
#             "selected": True}
#     return results

@router.get("/moduledata/dozent/{dozent_id}",summary="read all Modules by Dozent and dat about referenced Objects",
        description="Get data about multiple specific Modules according the given Dozent ID. Returns a Array of Json with the Data.",
        tags=["Modules"],
        response_model=List[Module], 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_selected_Modules_by_dozent_data(
    dozent_id
):
    re = modules.find({"dozent": {"$elemMatch": {"$eq": dozent_id}}}).sort("id", 1)
    print(re)
    x = convertDataWithReferences(re)
    
    if x:
        return x
    else:
        raise HTTPException(
            404, detail=f'No Modules for Dozent {dozent_id} exist.',
        )
    
@router.get("/module/dozent/{dozent_id}",summary="read all Modules by Dozent",
        description="Get data about multiple specific Modules according the given Dozent ID. Returns a Array of Json with the Data.",
        tags=["Modules"],
        response_model=List[ModuleResponse], 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_selected_Modules_by_dozent(
    dozent_id
):
    x = []
    results = modules.find({"dozent": {"$elemMatch": {"$eq": dozent_id}}}).sort("id", 1)
    for r in results:
        r["_id"] = str(r["_id"])
        x.append(r)
    if x:
        return x
    else:
        raise HTTPException(
            404, detail=f'No Modules for Dozent {dozent_id} exist.',
        )

@router.get("/module/studysemester/{studysemester_id}",summary="read all Modules by StudySemester",
        description="Get data about multiple specific Modules according the given StudySemester. Returns a Array of Json with the Data.",
        tags=["Modules"],
        response_model=List[ModuleResponse], 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_selected_Modules_studysemester(
    studysemester_id
):
    x = []
    results = modules.find({"study_semester": {"$elemMatch": {"$eq": studysemester_id}}}).sort("id", 1)
    for r in results:
        r["_id"] = str(r["_id"])
        x.append(r)
    if x:
        return x
    else:
        raise HTTPException(
            404, detail=f'No Modules for Studysemester {studysemester_id} exist.',
        )
    
@router.get("/moduledata/studysemester/{studysemester_id}",summary="read all Modules by StudySemester and data about referenced Objects",
        description="Get data about multiple specific Modules according the given StudySemester. Returns a Array of Json with the Data.",
        tags=["Modules"],
        response_model=List[Module], 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_selected_Modules_studysemester_data(
    studysemester_id
):
    re = modules.find({"study_semester": {"$elemMatch": {"$eq": studysemester_id}}}).sort("id", 1)
    x = convertDataWithReferences(re)
    if x:
        return x
    else:
        raise HTTPException(
            404, detail=f'No Modules for Studysemester {studysemester_id} exist.',
        )

@router.post("/module",summary="add Module",
        description="Add a module to the database based on the Input. Returns a Message string.",
        tags=["Modules"],
        response_model=ModuleResponse,
        responses={
            400: {"model": HTTPError, "detail": "str"},
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Add_Modul(
        data: ModuleResponse
    ):
    #check if module ID already exist
    data = dict(data)
    if data["study_semester"] != None:
        studyList = []
        for study in data["study_semester"]:
            study = dict(study)
            study["_id"] = [len(data["study_semester"]) - 1]["_id"] + 1
            studyList.append(study)

        data["study_semester"] = studyList
    modules.insert_one(data)

    data["_id"] = str(data["_id"])
    
    return data


# TODO: Please check the Enum Update Functionality, for me this way didn't worked :) 
@router.put("/module/{object_id}",summary="update complete Module by ID",
        description="Update a module already in the database based on the Input. Gives out a Message if successful.",
        tags=["Modules"],
        response_model=Module,
        responses={
            404: {"model": HTTPError, "detail": "str"},
            400: {"model": HTTPError, "detail": "str"}
        }
    )
async def Update_Modul(
        object_id, changes:dict
    ):
    result = {}

    for key, value in changes.items():
            result[key] = value

    #check if module exists
    try:
        res = modules.find_one({"_id": ObjectId(str(object_id))})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{e} must be defined')
    if res == None:
        raise HTTPException(404, detail=f'Module with ID {object_id} and type {result["type"]} doesn\'t exist',)

    modules.update_one({"_id": ObjectId(str(object_id))}, {"$set": changes})

    x = modules.find_one(ObjectId(object_id))
    tmp = []
    tmp.append(x)
    
    return convertDataWithReferences(tmp)[0]



# @router.put("/module/{module_id}/{dozent_id}",summary="update Dozent in Module",
#         description="Update Dozent assigned to module already in the database based on the Input. Gives out a Message if successful.",
#         tags=["Modules"],
#         response_model=Message,
#         responses={
#             404: {"model": HTTPError, "detail": "str"}
#         }
#     )
# async def Update_Modul_dozent(
#         dozent_id: int
#     ):
#     results = {"message": "success"}
#     return results

@router.delete("/module/{object_id}",summary="delete Module by ID",
        description="Delete a module from the database based on the Input. Gives out a Message if successful.",
        tags=["Modules"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Delete_Module(
    object_id
):
    try:
        id = ObjectId(object_id)
    except:
        raise HTTPException(400, detail=f'{object_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string',)
    
    re = modules.find_one(ObjectId(object_id))
    
    entrys = calendarentry.find()
    entryList = []

    for entry in entrys:
        if entry["module"] == object_id:
            entryList.append(str(entry["_id"]))
            calendarentry.delete_one({"_id":entry["_id"]})
    
    calendar = calendars.find()
   
    for cal in calendar:
        for entry in entryList:
            if entry not in cal["entries"]:
                continue
            cal["entries"].remove(entry)
        calendars.update_one({"_id":cal["_id"]}, {"$set":{"entries":cal["entries"]}})

    modules.delete_one({"_id": id})
    return {"message": f"Successfully deleted Module {object_id}"}



@router.post("/moduleXLSX",summary="add multiple Modules",
        description="Add multiple module to the database based on the Input. Returns a Message string. Used to import via XLSX.",
        tags=["Modules"],
        response_model=Message,
        responses={
            400: {"model": HTTPError, "detail": "str"},
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Add_Modul_XLSX(
        data: List[dict]
    ):
    ok = True
    #check if module ID already exist
    for module in data:
        cpy = {
            "dozent": [],
            "room": [],
            "study_semester": [],
            "type": []
        }
        for key, value in module.items():
            if re.search("dozent|type|study_semester|room", key):
                if re.search("dozent", key) and value:
                    cpy.setdefault("dozent", []).append(value)
                elif re.search("type", key) and value:
                    cpy.setdefault("type", []).append(value)
                elif re.search("study_semester", key) and value:
                    cpy.setdefault("study_semester", []).append(value)
                elif re.search("room", key) and value:
                    cpy.setdefault("room", []).append(value)
            elif key == "_id":
                cpy.update({key: ObjectId(value)})
            else:
                cpy.update({key: value})
        try:
            modules.insert_one(cpy)
        except:
            ok = False
            print("error", cpy)

    return {"message": f"Okay" if ok else f'Not all Modules could be imported'}