from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    utilisateur = "Utilisateur"
    instructeur = "Instructeur"

class UtilisateurBase(BaseModel):
    Nom: str
    Prénom: str
    Email: EmailStr
    Role: RoleEnum

class UtilisateurCreate(UtilisateurBase):
    MotDePasse: str

class UtilisateurInDB(UtilisateurBase):
    IDUtilisateur: int

    class Config:
        orm_mode = True
