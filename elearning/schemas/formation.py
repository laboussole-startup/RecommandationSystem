from pydantic import BaseModel
from typing import Optional

class FormationBase(BaseModel):
    Titre: str
    Description: str

class FormationCreate(FormationBase):
    IDInstructeur: int

class FormationInDB(FormationBase):
    IDFormation: int
    IDInstructeur: int

    class Config:
        orm_mode = True
