from typing import Optional
from pydantic import BaseModel, Field

from models.enums.Equipment import Equipment

class Room(BaseModel, use_enum_values=True):
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    capacity: int
    equipment: Equipment
