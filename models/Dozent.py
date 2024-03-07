from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field

from models.Absence import Absence

class Dozent(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    prename: str
    lastname: str
    email: str
    title: str
    salutation: str
    absences: list[Absence]

class DozentResponse(Dozent):
    absences: Optional[list[Absence]] = None
    