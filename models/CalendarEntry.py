from typing import Optional
from pydantic import BaseModel, Field
from models.Module import *
from models.TimeStamp import TimeStamp

class CalendarEntry(BaseModel):
    id: str
    module: Module
    time_stamp: TimeStamp

class CalendarEntryResponse(CalendarEntry):
    id: Optional[str] = Field(alias="_id", default=None)
    module: int
    time_stamp: TimeStamp | None
