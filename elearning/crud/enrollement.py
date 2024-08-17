from sqlalchemy.orm import Session
from elearning.models.modelsSQLAlchemy import UserFormationLink
from elearning.schemas.SchemasPydantic import UserFormationLinkRead


from sqlalchemy.orm import Session
from fastapi import HTTPException
from elearning.models.modelsSQLAlchemy import UserFormationLink

def user_inscription_formation(db: Session, user_id: int, formation_id: int):
    # Vérifiez si l'utilisateur est déjà inscrit à la formation
    inscription_existante = db.query(UserFormationLink).filter(
        UserFormationLink.user_id == user_id,
        UserFormationLink.formation_id == formation_id
    ).first()

    if inscription_existante:
        raise HTTPException(status_code=400, detail="L'utilisateur est déjà inscrit à cette formation.")

    # Créez une nouvelle inscription
    inscription = UserFormationLink(user_id=user_id, formation_id=formation_id)
    db.add(inscription)
    db.commit()
    db.refresh(inscription)
    return inscription


def get_enrollments(db: Session, utilisateur_id: int):
    return db.query(UserFormationLink).filter(UserFormationLink.user_id == utilisateur_id).all()


def is_user_enrolled(db: Session, user_id: int, formation_id: int):
    return db.query(UserFormationLink).filter(
        UserFormationLink.user_id == user_id,
        UserFormationLink.formation_id == formation_id
    ).first() is not None