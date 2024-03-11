from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field

from models.Absence import Absence

class StudyCourse(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    semesterCount: int
    content:list[str]