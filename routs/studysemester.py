from fastapi import APIRouter

router = APIRouter()

from models.Models import *
# All API functions regarding studysemester


# https://stackoverflow.com/questions/76231804/fastapi-how-to-modularize-code-into-multiple-files-with-access-to-app-decorators#:~:text=1%20Answer&text=The%20modularization%20of%20routes%20in,assembled%20into%20a%20FastAPI%20application.
# Beispielstruktur: 
# https://github.com/skatesham/fastapi-bigger-application 


@router.get("/studysemester",summary="read all Studysemester",
        description="Get all Studysemesters from Database. Returns an Array of Json's.",
        tags=["Studysemester"],
        response_model=Studysemesters, responses={
            404: NOT_FOUND()
            })
async def Get_all_Studysemesters():
    results = {"id": 0,
            "name": "str",
            "study": "str",
            "content": "str"}
    return results


@router.get("/studysemester/{studysemester_id}",summary="read Studysemester by ID",
        description="Get data about a specific Studysemester according the given ID. Returns a Json with the Data.",
        tags=["Studysemester"],
        response_model=Studysemester, 
        responses={
            404: NOT_FOUND()
            })
async def Get_one_Studysemester(
    id: int
):
    results = {"id": 0,
            "name": "str",
            "study": "str",
            "content": "str"}
    return results


@router.post("/studysemester/add",summary="add Studysemester",
        description="Add a Studysemester to the database based on the Input. Gives out a Message if successful.",
        tags=["Studysemester"],
        response_model=Message,
        responses={
            404: NOT_FOUND()
        }
    )
async def Add_Studysemester(
        name: str,
        study: str,
        content: str
    ):
    results = {"message": "success"}
    return results

@router.put("/studysemester/{studysemester_id}",summary="update complete Studysemester by ID",
        description="Update a Studysemester already in the database based on the Input. Gives out a Message if successful.",
        tags=["Studysemester"],
        response_model=Message,
        responses={
            404: NOT_FOUND()
        }
    )
async def Update_Studysemester(
        name: str | None,
        study: str | None,
        content: str | None
    ):
    results = {"message": "success"}
    return results

@router.delete("/studysemester/{studysemester_id}",summary="delete Studysemester by ID",
        description="Delete a Studysemester from the database based on the Input. Gives out a Message if successful.",
        tags=["Studysemester"],
        response_model=Message,
        responses={
            404: NOT_FOUND()
        }
    )
async def Delete_Studysemester():
    results = {"message": "success"}
    return results