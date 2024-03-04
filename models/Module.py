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
    module_id: str
    name: str
    code: str | None
    dozent: list[Dozent]
    room: list[Room] | Room | None
    study_semester: list[StudySemester]
    duration: int
    approximate_attendance: int
    need: Equipment | None
    type: list[Type]
    frequency: Frequency
    selected: bool
    color: str | None
    note: str | None
    groups: int | None


class ModuleResponse(Module):
    dozent: list[str]
    room: list[str] | str | None
    study_semester: list[str]


class BasicModule(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    code: str
    dozent: list[str]
    room: list[str]
    study_semester: list[str]
    duration: int