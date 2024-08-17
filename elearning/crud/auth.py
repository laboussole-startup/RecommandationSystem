from sqlalchemy.orm import Session
from elearning.models.modelsSQLAlchemy import Utilisateur
from elearning.schemas.SchemasPydantic import UtilisateurCreate,UtilisateurRead
from elearning.schemas import util
def get_utilisateur(db: Session, user_id: int):
    return db.query(Utilisateur).filter(Utilisateur.id_utilisateur == user_id).first()

def get_utilisateur_by_email(db: Session, email: str):
    return db.query(Utilisateur).filter(Utilisateur.email == email).first()

def create_utilisateur(db: Session, utilisateur: UtilisateurCreate):
    hashed_password = util.get_password_hash(utilisateur.mot_de_passe)
    db_utilisateur = Utilisateur(email=utilisateur.email, hashed_password=hashed_password)
    db.add(db_utilisateur)
    db.commit()
    db.refresh(db_utilisateur)
    return db_utilisateur
