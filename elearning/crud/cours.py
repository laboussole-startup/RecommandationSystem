from sqlalchemy.orm import Session
from fastapi import HTTPException
from elearning.models.modelsSQLAlchemy import LeconVideo, Module
from elearning.schemas.SchemasPydantic import LeconVideoCreate

def createCours(db: Session, lesson: LeconVideoCreate):
    # Vérifier si le module existe
    module = db.query(Module).filter(Module.id_module == lesson.id_module).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    print("dddddddddddddddddddddddddddddddddddeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    
    db_cours = LeconVideo(
        titre =lesson.titre,
        description=lesson.description,
        url_video =lesson.url_video,
        url_image_lecon=lesson.url_image_lecon,
        id_module=lesson.id_module
    )
    db.add(db_cours)
    db.commit()
    db.refresh(db_cours)
    return db_cours



def get_cours(db: Session, module_id: int):
    return db.query(LeconVideo).filter(LeconVideo.id_module == module_id).first()

def get_cours_module(db: Session, module_id):
    return db.query(LeconVideo).filter(LeconVideo.id_module==module_id).all()


