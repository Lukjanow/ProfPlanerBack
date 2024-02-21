from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field

from models.Absence import Absence

class Dozent(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    e_mail: str
    title: str
    absences: list[Absence]
    intern: bool

class DozentRespone(Dozent):
    absences: Optional[list[Absence]] = None
    