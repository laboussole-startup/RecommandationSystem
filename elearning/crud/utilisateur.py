
from elearning.schemas.util import get_password_hash
from sqlalchemy.orm import Session
from elearning.models.modelsSQLAlchemy import Utilisateurtest, RoleEnum
from elearning.models.modelsSQLAlchemy import Utilisateurtest
from elearning.schemas.SchemasPydantic import UtilisateurCreate,UtilisateurBase

# Fonction pour créer un utilisateur
def create_utilisateur(db: Session, utilisateur: UtilisateurCreate):
    db_utilisateur = Utilisateurtest(
        nom=utilisateur.nom,
        prenom=utilisateur.prenom,
        email=utilisateur.email,
        mot_de_passe=get_password_hash(utilisateur.mot_de_passe),
        role=RoleEnum(utilisateur.role),  # Assurez-vous que 'role' est soit 'utilisateur' soit 'instructeur'
        est_actif=utilisateur.est_actif
    )
    db.add(db_utilisateur)
    db.commit()
    db.refresh(db_utilisateur)
    return db_utilisateur




def get_utilisateur(db: Session, utilisateur_id: int):
    return db.query(Utilisateurtest).filter(Utilisateurtest.id_utilisateur == utilisateur_id).first()

def get_utilisateur_by_email(db: Session, email: str):
    return db.query(Utilisateurtest).filter(Utilisateurtest.email == email).first()
