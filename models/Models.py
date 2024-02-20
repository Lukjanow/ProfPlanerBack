from pydantic import BaseModel

class Message(BaseModel):
    message: str

class Error(BaseModel):
    detail: str

class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }

class Module(BaseModel):
    id: int 
    name: str 
    dozent_id: int 
    room_id: int | None
    study_semester: int 
    need: str 
    type: str 
    selected: bool 
    

class Modules(BaseModel):
    Modules: dict[int, Module]

class Absence(BaseModel):
    begin: str
    end: str
    comment: str

class Dozent(BaseModel):
    id: int
    name: str
    email: str
    title: str
    absences: list[Absence]
    intern: bool

class Dozents(BaseModel):
    Dozents: dict[Dozent, Dozent]

class Room(BaseModel):
    name: str
    capacity: int
    equipment: str

class Rooms(BaseModel):
    Rooms: dict[Room, Room]

class calendarEntry(BaseModel):
    module: Module
    time_stamp: str

class calendar(BaseModel):
    Entries: dict[calendarEntry, calendarEntry]

class Studysemester(BaseModel):
    name: str
    study: str
    content: str

class Studysemesters(BaseModel):
    Studysemesters: dict[Studysemester, Studysemester]

