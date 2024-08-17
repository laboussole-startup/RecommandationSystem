from sqlalchemy.orm import Session
from elearning.models.modelsSQLAlchemy import Formation
from elearning.schemas.SchemasPydantic import FormationCreate,FormationBase



def createFormation(db: Session, formation: FormationBase, instructeur_id: int):
    # Example implementation
    db_formation = Formation(
        titre=formation.titre,
        description=formation.description,
        url_image_formation =formation.url_image_formation,
        id_instructeur=instructeur_id,
        
    )
    db.add(db_formation)
    db.commit()
    db.refresh(db_formation)
    return db_formation


def get_formation(db: Session, formation_id: int):
    return db.query(Formation).filter(Formation.id_formation == formation_id).first()

def get_formations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Formation).offset(skip).limit(limit).all()


