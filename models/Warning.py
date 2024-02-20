from pydantic import BaseModel

from models.CalendarEntry import CalendarEntry

class Warning(BaseModel):
    id: int
    name: str
    priority: int
    description: str
    affected_calendar_entries: list[CalendarEntry]
