from fastapi import APIRouter

router = APIRouter()

from models.Models import *
# All API functions regarding Modules


# https://stackoverflow.com/questions/76231804/fastapi-how-to-modularize-code-into-multiple-files-with-access-to-app-decorators#:~:text=1%20Answer&text=The%20modularization%20of%20routes%20in,assembled%20into%20a%20FastAPI%20application.
# Beispielstruktur: 
# https://github.com/skatesham/fastapi-bigger-application 


@router.get("/module",summary="read all Modules",
        description="Get all Modules from Database. Returns an Array of Json's.",
        tags=["Modules"],
        response_model=Modules, responses={
            404: NOT_FOUND()
            })
async def Get_all_Modules():
    results = {"id": 0,
            "name": "str",
            "dozent_id": 0,
            "room_id": 0,
            "study_semester": "str",
            "need": "enumerate",
            "type": "enumerate",
            "selected": True}
    return results

@router.get("/module/{module_id}",summary=" read Module by ID",
        description="Get data about a specific Module according the given ID. Returns a Json with the Data.",
        tags=["Modules"],
        response_model=Module, 
        responses={
            404: NOT_FOUND()
            })
async def Get_one_Modules(
    id: int
):
    results = {"id": id,
            "name": "str",
            "dozent_id": 0,
            "room_id": 0,
            "study_semester": "str",
            "need": "enumerate",
            "type": "enumerate",
            "selected": True}
    return results

@router.get("/module/selected",summary="read all selected Moduls",
        description="Get data about multiple specific Modules according the given ID's. Returns a Array of Json with the Data.",
        tags=["Modules"],
        response_model=Modules, 
        responses={
            404: NOT_FOUND()
            })
async def Get_selected_Modules(
    ids: list[int]
):
    results = {"id": ids,
            "name": "str",
            "dozent_id": 0,
            "room_id": 0,
            "study_semester": "str",
            "need": "enumerate",
            "type": "enumerate",
            "selected": True}
    return results

# @router.get("/module/room/{room_id}}",summary="read all Modules by Room",
#         description="Get data about multiple specific Modules according the given Room ID. Returns a Array of Json with the Data.",
#         tags=["Modules"],
#         response_model=Modules, 
#         responses={
#             404: NOT_FOUND()
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

@router.get("/module/dozent/{dozent_id}",summary="read all Modules by Dozent",
        description="Get data about multiple specific Modules according the given Dozent ID. Returns a Array of Json with the Data.",
        tags=["Modules"],
        response_model=Modules, 
        responses={
            404: NOT_FOUND()
            })
async def Get_selected_Modules_by_dozent(
    id: int
):
    results = {"id": id,
            "name": "str",
            "dozent_id": 0,
            "room_id": 0,
            "study_semester": "str",
            "need": "enumerate",
            "type": "enumerate",
            "selected": True}
    return results

@router.get("/module/studysemester/{studysemester_id}",summary="read all Modules by StudySemester",
        description="Get data about multiple specific Modules according the given StudySemester. Returns a Array of Json with the Data.",
        tags=["Modules"],
        response_model=Modules, 
        responses={
            404: NOT_FOUND()
            })
async def Get_selected_Modules(
    id: int
):
    results = {"id": id,
            "name": "str",
            "dozent_id": 0,
            "room_id": 0,
            "study_semester": "str",
            "need": "enumerate",
            "type": "enumerate",
            "selected": True}
    return results

@router.post("/module",summary="add Module",
        description="Add a module to the database based on the Input. Gives out a Message if successful.",
        tags=["Modules"],
        response_model=Message,
        responses={
            404: NOT_FOUND()
        }
    )
async def Add_Modul(
        id: int,
        name: str,
        dozent_id: int,
        room_id: int,
        study_semester: str,
        need: str,
        type: str,
        selected: bool
    ):
    results = {"message": "success"}
    return results

@router.put("/module/{module_id}",summary="update complete Module by ID",
        description="Update a module already in the database based on the Input. Gives out a Message if successful.",
        tags=["Modules"],
        response_model=Message,
        responses={
            404: NOT_FOUND()
        }
    )
async def Update_Modul(
        id: int | None,
        name: str | None,
        dozent_id: int | None,
        room_id: int | None,
        study_semester: str | None,
        need: str | None,
        type: str | None,
        selected: bool | None
    ):
    results = {"message": "success"}
    return results

# @router.put("/module/{module_id}/{dozent_id}",summary="update Dozent in Module",
#         description="Update Dozent assigned to module already in the database based on the Input. Gives out a Message if successful.",
#         tags=["Modules"],
#         response_model=Message,
#         responses={
#             404: NOT_FOUND()
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
            404: NOT_FOUND()
        }
    )
async def Delete_Modul():
    results = {"message": "success"}
    return results