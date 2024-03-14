from typing import Optional
from pydantic import BaseModel, Field
from models.StudyCourse import StudyCourse

class StudySemester(BaseModel):
    id: Optional[int] = Field(alias="_id", default=None)
    studyCourse: StudyCourse
    semesterNumbers: list[int]
    content: list[str]
    

class StudySemesterResponse(BaseModel):
    id: Optional[int] = Field(alias="_id", default=None)
    studyCourse: str
    semesterNumbers: list[int]
    content: list[str]
