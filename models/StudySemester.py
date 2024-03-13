from typing import Optional
from pydantic import BaseModel, Field
from models.StudyCourse import StudyCourse
from models.enums.Content import Content
from models.enums.Study import Study

class StudySemester(BaseModel):
    id: Optional[int] = Field(alias="_id", default=None)
    studyCourse: StudyCourse
    semesterNumbers: list[str]
    content: list[str]
    
class StudySemesterResponse(BaseModel):
    id: Optional[int] = Field(alias="_id", default=None)
    studyCourse: str
    semesterNumbers: list[str]
    content: list[str]
