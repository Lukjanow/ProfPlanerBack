from pydantic import BaseModel
from models.TimeStamp import TimeStamp

class Absence(BaseModel):
    id: int
    begin: TimeStamp
    end: TimeStamp
    comment:str
