from typing import Optional
from pydantic import BaseModel, Field

class Note(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    text: str
