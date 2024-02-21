from pydantic import BaseModel

from models.Dozent import Dozent
from models.Room import Room
from models.StudySemester import StudySemester
from models.enums.Equipment import Equipment
from models.enums.Type import Type
from models.enums.Frequency import Frequency


class Module(BaseModel, use_enum_values=True):
    id: int
    name: str
    dozent: list[Dozent]
    room: Room | None
    study_semester: list[StudySemester]
    duration: int
    approximate_attendance: int
    need: Equipment | None
    type: Type
    frequency: Frequency
    selected: bool


class ModuleResponse(Module):
    dozent: list[str]
    room: str | None
    study_semester: list[str]
