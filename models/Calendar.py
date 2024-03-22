from typing import Optional
from pydantic import BaseModel, Field
from models.CalendarEntry import *
from models.enums.Frequency import Frequency

class Calendar(BaseModel, use_enum_values=True):
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    entries: list[CalendarEntry]
    frequency: Frequency


class CalendarResponse(Calendar):
    id: Optional[str] = Field(alias="_id", default=None)
    entries: list[str]
