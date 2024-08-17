from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from elearning.schemas.SchemasPydantic import UtilisateurCreate
from elearning.crud.utilisateur import create_utilisateur
from core.database import get_db

router = APIRouter()

@router.post("/utilisateur/", response_model=UtilisateurCreate)
def create_utilisateur_endpoint(utilisateur: UtilisateurCreate, db: Session = Depends(get_db)):
    db_utilisateur = create_utilisateur(db=db, utilisateur=utilisateur)
    return db_utilisateur
