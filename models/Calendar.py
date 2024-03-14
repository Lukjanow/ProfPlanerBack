from typing import Optional
from pydantic import BaseModel, Field
from models.CalendarEntry import *

class Calendar(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    entries: list[CalendarEntry]


class CalendarResponse(Calendar):
    id: Optional[str] = Field(alias="_id", default=None)
    entries: list[str]