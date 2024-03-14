from typing import Optional
from pydantic import BaseModel, Field

class Room(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    roomNumber: str
    capacity: int
    roomType: str
