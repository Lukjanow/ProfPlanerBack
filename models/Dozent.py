from pydantic import BaseModel

from models.Absence import Absence

class Dozent(BaseModel):
    id: int
    name: str
    e_mail: str
    title: str
    absences: list[Absence]
    comment: str

class Dozents(BaseModel):
    Dozents: dict[Dozent, Dozent]