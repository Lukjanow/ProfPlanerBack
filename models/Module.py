from typing import Optional
from pydantic import BaseModel, Field

from models.Dozent import Dozent
from models.Room import Room
from models.StudySemester import StudySemester
from models.enums.Equipment import Equipment
from models.enums.Type import Type
from models.enums.Frequency import Frequency


class Module(BaseModel, use_enum_values=True):
    id: Optional[str] = Field(alias="_id", default=None)
    module_id: str | None
    name: str
    code: str | None
    events: list[dict]
    qsp: list[str] | None
    frequency: Frequency
    selected: bool
    color: str | None
    note: str | None
    course: bool


class ModuleResponse(Module):
    dozent: list[str]
    room: list[str]
    study_semester: list[str]


class BasicModule(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    code: str | None
    dozent: list[str]
    room: list[str]
    study_semester: list[str]
    duration: int