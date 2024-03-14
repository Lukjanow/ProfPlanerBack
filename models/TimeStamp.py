from pydantic import BaseModel

class TimeStamp(BaseModel):
    week_day: int
    hour: int
    minute: int
