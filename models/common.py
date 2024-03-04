from typing import ClassVar
from pydantic import BaseModel, ConfigDict

class HTTPError(BaseModel):
    detail: str

    # class Config(ConfigDict):
    #     json_schema_extra = {
    #         "example": {"detail": "HTTPException raised."},
    #     }

    Config: ClassVar = ConfigDict(json_schema_extra={
        "example": {"detail": "HTTPException raised."}
    })




class Message(BaseModel):
    message: str