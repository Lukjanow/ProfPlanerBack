from typing import Optional
from pydantic import BaseModel, Field
from models.StudyCourse import StudyCourse
from models.enums.Content import Content
from models.enums.Study import Study

class StudySemester(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    studyCourse: StudyCourse
    semesterNumbers: list[int]
    content: list[str]
    
class StudySemesterResponse(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    studyCourse: str
    semesterNumbers: list[int]
    content: list[str]
