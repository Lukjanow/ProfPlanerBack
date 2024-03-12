from typing import Optional
from pydantic import BaseModel, Field

from models.Dozent import Dozent
from models.Room import Room
from models.StudySemester import StudySemester
from models.enums.Frequency import Frequency


class Module(BaseModel, use_enum_values=True):
    id: Optional[str] = Field(alias="_id", default=None)
    module_id: str | None
    name: str
    code: str | None
    dozent: list[Dozent]
    room: list[Room]
    study_semester: list[StudySemester]
    duration: int
    approximate_attendance: int
    frequency: Frequency
    selected: bool
    color: str | None
    study_course: list[str]



class ModuleResponse(Module):
    dozent: list[str]
    room: list[str]
    study_semester: list[str]


class BasicModule(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    code: str | None
    dozent: list[Dozent]
    room: list[Room]
    study_semester: list[StudySemester]
    duration: int
