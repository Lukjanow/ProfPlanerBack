from fastapi import APIRouter
from models.Dozent import *
from models.Absence import Absence
from Backend.models.common import *


router = APIRouter()


# All API functions regarding Dozents


# https://stackoverflow.com/questions/76231804/fastapi-how-to-modularize-code-into-multiple-files-with-access-to-app-decorators#:~:text=1%20Answer&text=The%20modularization%20of%20routes%20in,assembled%20into%20a%20FastAPI%20application.
# Beispielstruktur: 
# https://github.com/skatesham/fastapi-bigger-application 


@router.get("/dozent",summary="read all Dozent",
        description="Get all Dozent from Database. Returns an Array of Json's.",
        tags=["Dozent"],
        response_model=Dozents, responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_all_Dozents():
    results = {"id": 0,
            "name": "str",
            "email": "str",
            "title": "str",
            "absences": "list[Absence]",
            "intern": True}
    
    return results

@router.get("/dozent/{dozent_id}",summary="read Dozent by ID",
        description="Get data about a specific Dozent according the given ID. Returns a Json with the Data.",
        tags=["Dozent"],
        response_model=Dozent, 
        responses={
            404: {"model": HTTPError, "detail": "str"}
            })
async def Get_one_Dozent(
    id: int
):
    results = {"id": 0,
            "name": "str",
            "email": "str",
            "title": "str",
            "absences": "list[Absence]",
            "intern": True}
    return results

@router.get("/dozent/absence/{dozent_id}",summary="Read all Absences by Dozent",
        description="Gives out all absences a Dozent has. Returns an Array of Json if successful",
        tags=["Dozent"],
        response_model=Absence,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def get_Dozent_absences(
        dozent_id: int
    ):
    results = {"message": "success"}
    return results

@router.post("/dozent",summary="add Dozent",
        description="Add a Dozent to the database based on the Input. Gives out a Message if successful.",
        tags=["Dozent"],
        response_model=Dozent,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Add_Dozent(
        id: int,
        name: str,
        email: str,
        title: str,
        intern: bool
    ):
    results = {"message": "success"}
    return results

@router.post("/dozent/absence/{dozent_id}",summary="add Absence to Dozent",
        description="Add Absence for a Dozent to the database based on the Input. Gives out a Message if successful.",
        tags=["Absence"],
        response_model=Absence,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Add_Abscence(
        begin: str,
        end: str,
        comment: str
    ):
    results = {"message": "success"}
    return results

@router.put("/dozent/{dozent_id}",summary="update complete Dozent by ID",
        description="Update a Dozent already in the database based on the Input. Gives out a Message if successful.",
        tags=["Dozent"],
        response_model=Dozent,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Update_Dozent(
        id: int | None,
        name: str | None,
        email: str | None,
        title: str | None,
        intern: bool | None
    ):
    results = {"message": "success"}
    return results

@router.put("/dozent/absence/{dozent_id}/{absence_id}",summary="update one Absence of a Dozent",
        description="Update a Abscences already in the database based on the Input. Gives out a Message if successful.",
        tags=["Absence"],
        response_model=Absence,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Update_Abscence(
        begin: str | None,
        end: str | None,
        comment: str | None
    ):
    results = {"message": "success"}
    return results

@router.delete("/dozent/{dozent_id}",summary="delete Dozent by ID",
        description="Delete a Dozent from the database based on the Input. Gives out a Message if successful.",
        tags=["Dozent"],
        response_model=Dozent,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Delete_Modul():
    results = {"message": "success"}
    return results

@router.delete("/dozent/absence/{dozent_id}/{absence_id}",summary="delete one Absence from Dozent",
        description="Delete a Room from the database based on the Input. Gives out a Message if successful.",
        tags=["Absence"],
        response_model=Absence,
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Delete_Absence():
    results = {"message": "success"}
    return results