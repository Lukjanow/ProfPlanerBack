from typing import Optional
from pydantic import BaseModel, Field

class StudyCourse(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    semesterCount: int
    content:list[str]