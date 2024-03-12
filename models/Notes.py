from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field

class Note(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    text: str
