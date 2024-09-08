from sqlalchemy.orm import Session
from elearning.models.modelsSQLAlchemy import Utilisateurtest
from elearning.schemas.SchemasPydantic import UtilisateurCreate
from elearning.schemas import util
from elearning.crud import auth
from core.database import get_db  # Importez get_db depuis database.py
from fastapi import Depends, HTTPException, status


def get_utilisateur(user_id: int, db: Session):
    return db.query(Utilisateurtest).filter(Utilisateurtest.id_utilisateur == user_id).first()




def get_utilisateur_by_email(db: Session, email: str):
    return db.query(Utilisateurtest).filter(Utilisateurtest.email == email).first()

def create_utilisateur(db: Session, utilisateur: UtilisateurCreate):
    hashed_password =util. get_password_hash(utilisateur.mot_de_passe)
    db_utilisateur = Utilisateurtest(
        email=utilisateur.email,
        mot_de_passe=hashed_password,
        nom=utilisateur.nom,
        prenom=utilisateur.prenom,
        role=utilisateur.role,
        est_actif=utilisateur.est_actif
    )
    db.add(db_utilisateur)
    db.commit()
    db.refresh(db_utilisateur)
    return db_utilisateur