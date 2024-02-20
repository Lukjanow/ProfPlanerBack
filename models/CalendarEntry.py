from pydantic import BaseModel
from models.Module import Module
from models.TimeStamp import TimeStamp

class CalendarEntry(BaseModel):
    id: int
    module: Module
    time_stamp: TimeStamp
