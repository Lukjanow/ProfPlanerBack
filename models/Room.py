from pydantic import BaseModel

from models.enums.Equipment import Equipment

class Room(BaseModel):
    id: int
    name: str
    capacity: int
    equipment: Equipment

class Rooms(BaseModel):
    Rooms: dict[Room, Room]
