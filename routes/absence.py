from fastapi import APIRouter
from models.Absence import *
from models.common import *

router = APIRouter()


# All API functions regarding absence

@router.get("/dozent/{dozent_id}/absences", summary="read all absences for Dozent",
            description="Get all absences for a given Dozent. Returns a Json with Absence Data",
            tags=["Absence"],
            response_model=Absence,
            responses={
                404: {"model": HTTPError, "detail": "str"}
            })
async def Get_absences(
    dozent_id: int
):
    results = [{"begin": 90,
               "end": 180,
               "comment": "Hab kein bock zu schaffen Freitags :P"}]
    return results


@router.post("/dozent/{dozent_id}/absence/",summary="add Absence to Dozent",
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


@router.put("/dozent/{dozent_id}/absence/{absence_id}",summary="update one Absence of a Dozent",
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

@router.delete("/dozent/{dozent_id}/absence/{absence_id}",summary="delete one Absence from Dozent",
        description="Delete a Absence from the database based on the Input. Gives out a Message if successful.",
        tags=["Absence"],
        response_model=Absence, 
        responses={
            404: {"model": HTTPError, "detail": "str"}
        }
    )
async def Delete_Absence():
    results = {"message": "success"}
    return results