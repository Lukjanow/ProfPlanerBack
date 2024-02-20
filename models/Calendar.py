from pydantic import BaseModel
from models.CalendarEntry import CalendarEntry

class Calendar(BaseModel):
    id: int
    entries: list[CalendarEntry]
