from bson import ObjectId
from fastapi import APIRouter, status, HTTPException

from typing import List
import copy #Allow to copy Dict
from models.common import *
from models.Module import *

router = APIRouter()

from Database.Database import db

dozents = db["dozent"]
study_semesters = db["studysemester"]
rooms = db["rooms"]
modules = db["modules"]
# All API functions regarding Modules

# TODO: Create Routes with Data send instead of IDS for example: Not dozent: "id" but dozent: [{"id": id, "name": "name"}..., {"id": id, "name": "name"...}...]

# https://stackoverflow.com/questions/76231804/fastapi-how-to-modularize-code-into-multiple-files-with-access-to-app-decorators#:~:text=1%20Answer&text=The%20modularization%20of%20routes%20in,assembled%20into%20a%20FastAPI%20application.
# Beispielstruktur: 
# https://github.com/skatesham/fastapi-bigger-application 


@router.get("/module",summary="read all Modules",
        description="Get all Modules from Database. Returns an Array of Json's. Response contain only Dozent ID, Room ID and studysemester ID",
        tags=["Modules"],
        response_model=List[ModuleResponse])
async def Get_all_Modules():
    i = 1
    x = []
    results = modules.find().sort("id", 1)
    for r in results:
        #remove id set by mongodb
        r.pop("_id")
        x.append(r)
        i = i+1
    print(x)
    return x


@router.get("/moduledata",summary="read all Modules and get Data about referenced objects",
        description="Get all Modules from Database. Returns an Array of Json's. Response contain also Data about Dozent, Room and studysemester ",
        tags=["Modules"],
        response_model=List[Module])
async def Get_all_Modules_data():
    re = modules.find()
    x = []
    for result in re:
        result.pop("_id")
        dozent = []
        for id in result["dozent"]:
            res = dozents.find_one({"_id": ObjectId(str(id))})
            res["_id"] = str(res["_id"])
            dozent.append(res)
        result["dozent"] = dozent
        study_semester = []
        for id in result["study_semester"]:
            res = study_semesters.find_one({"_id": ObjectId(str(id))})
            res["_id"] = str(res["_id"])
            study_semester.append(res)
        result["study_semester"] = study_semester
        try:
            result["room"] = rooms.find_one({"_id": ObjectId(result["room"])})
            result["room"]["_id"] = str(result["room"]["_id"])
        except:
            pass
        x.append(result)
    return x

@router.get("/moduledata/{module_id}",summary="read Module by ID and get Data from referenced Data",
        description="Get data about a specific Module according the given ID. Returns a Json with the Data. Also gives Back data for Dozent, Rooms and Studysemester",
        tags=["Modules"],
        response_model=Module, 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_one_Modules_data(
    module_id
):
    result = modules.find_one({"id": int(module_id)})
    result.pop("_id")
    dozent = []
    for id in result["dozent"]:
        res = dozents.find_one({"_id": ObjectId(str(id))})
        res["_id"] = str(res["_id"])
        dozent.append(res)
    result["dozent"] = dozent
    study_semester = []
    for id in result["study_semester"]:
        res = study_semesters.find_one({"_id": ObjectId(str(id))})
        res["_id"] = str(res["_id"])
        study_semester.append(res)
    result["study_semester"] = study_semester
    try:
        result["room"] = rooms.find_one({"_id": ObjectId(result["room"])})
        result["room"]["_id"] = str(result["room"]["_id"])
    except:
        pass
    print(result)
    return result

@router.get("/module/{module_id}",summary=" read Module by ID",
        description="Get data about a specific Module according the given ID. Returns a Json with the Data.",
        tags=["Modules"],
        response_model=ModuleResponse, 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_one_Modules(
    module_id
):
    result = modules.find_one({"id": int(module_id)})
    if result:
        #remove id set by mongodb
        result.pop("_id")
        return result
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
        r.pop("_id")
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
    x = []
    re = modules.find({"selected": True}).sort("id", 1)
    for result in re:
        result.pop("_id")
        dozent = []
        for id in result["dozent"]:
            res = dozents.find_one({"_id": ObjectId(str(id))})
            res["_id"] = str(res["_id"])
            dozent.append(res)
        result["dozent"] = dozent
        study_semester = []
        for id in result["study_semester"]:
            res = study_semesters.find_one({"_id": ObjectId(str(id))})
            res["_id"] = str(res["_id"])
            study_semester.append(res)
        result["study_semester"] = study_semester
        try:
            result["room"] = rooms.find_one({"_id": ObjectId(result["room"])})
            result["room"]["_id"] = str(result["room"]["_id"])
        except:
            pass
        x.append(result)
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
    x = []
    re = modules.find({"dozent": {"$elemMatch": {"$eq": dozent_id}}}).sort("id", 1)
    for result in re:
        result.pop("_id")
        dozent = []
        for id in result["dozent"]:
            res = dozents.find_one({"_id": ObjectId(str(id))})
            res["_id"] = str(res["_id"])
            dozent.append(res)
        result["dozent"] = dozent
        study_semester = []
        for id in result["study_semester"]:
            res = study_semesters.find_one({"_id": ObjectId(str(id))})
            res["_id"] = str(res["_id"])
            study_semester.append(res)
        result["study_semester"] = study_semester
        try:
            result["room"] = rooms.find_one({"_id": ObjectId(result["room"])})
            result["room"]["_id"] = str(result["room"]["_id"])
        except:
            pass
        x.append(result)
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
        print("Getting results")
        #remove id set by mongodb
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
    x = []
    re = modules.find({"study_semester": {"$elemMatch": {"$eq": studysemester_id}}}).sort("id", 1)
    for result in re:
        result.pop("_id")
        dozent = []
        for id in result["dozent"]:
            res = dozents.find_one({"_id": ObjectId(str(id))})
            res["_id"] = str(res["_id"])
            dozent.append(res)
        result["dozent"] = dozent
        study_semester = []
        for id in result["study_semester"]:
            res = study_semesters.find_one({"_id": ObjectId(str(id))})
            res["_id"] = str(res["_id"])
            study_semester.append(res)
        result["study_semester"] = study_semester
        try:
            result["room"] = rooms.find_one({"_id": ObjectId(result["room"])})
            result["room"]["_id"] = str(result["room"]["_id"])
        except:
            pass
        x.append(result)
    if x:
        return x
    else:
        raise HTTPException(
            404, detail=f'No Modules for Studysemester {studysemester_id} exist.',
        )

@router.post("/module",summary="add Module",
        description="Add a module to the database based on the Input. Returns a Message string.",
        tags=["Modules"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Add_Modul(
        data: ModuleResponse
    ):
    #check if module ID already exist
    if modules.find_one({"id": data.id}):
        return {"message": f'A Module with ID {data.id} already exist'}

    data = dict(data)

    result = str(modules.insert_one(data))
    print(result)
    return {"message": result}


# TODO: Please check the Enum Update Functionality, for me this way didn't worked :) 
@router.put("/module/{module_id}",summary="update complete Module by ID",
        description="Update a module already in the database based on the Input. Gives out a Message if successful.",
        tags=["Modules"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"},
            400: {"model": HTTPError, "detail": "str"}
        }
    )
async def Update_Modul(
        modules_id, changes:dict
    ):
    #check if module ID already exist
    result = modules.find_one({"id": int(modules_id)})

    if result == None:
        raise HTTPException(404, detail=f'Module with ID {modules_id} doesn\'t exist',)
    for key, value in changes.items():
            result[key] = value
    try:
        new_item = ModuleResponse(id=int(modules_id), name=result["name"], dozent=result["dozent"], room=result["room"],
                                  study_semester=result["study_semester"], need=result["need"], type=result["type"],
                                  selected=result["selected"], duration=result["duration"],  approximate_attendance=result["approximate_attendance"],
                                  frequency=result["frequency"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{e}')
    r = modules.update_one({"id": int(modules_id)}, {"$set": changes})
    return {"message": f'{r}'}



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

@router.delete("/module/{module_id}",summary="delete Module by ID",
        description="Delete a module from the database based on the Input. Gives out a Message if successful.",
        tags=["Modules"],
        response_model=Message,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Delete_Module(
    module_id
):
    #TODO Possible delete Calendar entries
    module = modules.find_one({"id": int(module_id)})
    if module:
        res = modules.delete_one({"id": int(module_id)})
        print(res)
        return {"message": f'Successfully deleted Module {module_id}'}
    else:
        raise HTTPException(
        404, detail=f'Module with ID {module_id} doesn\'t exist',
    )