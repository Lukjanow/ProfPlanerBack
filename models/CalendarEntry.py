from typing import Optional
from pydantic import BaseModel, Field
from models.Module import *
from models.TimeStamp import TimeStamp

class CalendarEntry(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    module: Module
    time_stamp: TimeStamp
    comment: str | None

class CalendarEntryResponse(CalendarEntry):
    id: Optional[str] = Field(alias="_id", default=None)
    module: str
    time_stamp: TimeStamp | None
