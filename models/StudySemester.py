from pydantic import BaseModel
from models.enums.Content import Content

from models.enums.Study import Study

class StudySemester(BaseModel):
    id: int
    name:str
    study: Study
    content: Content
