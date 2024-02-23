from pydantic import BaseModel

from models.enums.Equipment import Equipment

class Room(BaseModel, use_enum_values=True):
    id: int
    name: str
    capacity: int
    equipment: Equipment
