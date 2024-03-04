from pydantic import BaseModel

class TimeStamp(BaseModel):
    #id: int
    week_day: int
    hour: int
    minute: int
