#models for testing.py with is providing the API
from pydantic import BaseModel

def NOT_FOUND(): 
    return {"model": Error, "error": "Could not find"}

#TestModules
class Hello_World(BaseModel):
    item_id: str | None
    test: str 

class Advice(BaseModel):
    item_id: int
    advice: str

#Real Modules
class Message(BaseModel):
    message: str

class Error(BaseModel):
    error: str

class Module(BaseModel):
    id: int 
    name: str 
    dozent_id: int 
    room_id: int 
    study_semester: str 
    need: str 
    type: str 
    selected: bool 
    

class Modules(BaseModel):
    Modules: dict[Module, Module]

#Ich habe die str werte auf int geändert - Bitte korrigieren wenn das flasch war
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

class CalenderEntry(BaseModel):
    module: Module
    time_stamp: str

class Calender(BaseModel):
    Entries: dict[CalenderEntry, CalenderEntry]

class Studysemester(BaseModel):
    name: str
    study: str
    content: str

class Studysemesters(BaseModel):
    Studysemesters: dict[Studysemester, Studysemester]

