from typing import Optional
from pydantic import BaseModel, Field
from models.enums.Content import Content
from models.enums.Study import Study

class StudySemester(BaseModel, use_enum_values=True):
    id: Optional[str] = Field(alias="_id", default=None)
    name:str
    study: Study
    content: Content
