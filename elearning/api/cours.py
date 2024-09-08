from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from elearning.schemas.SchemasPydantic import ModuleBase,ModuleCreate,ModuleRead
from elearning.schemas.SchemasPydantic import LeconVideoCreate,LeconVideoBase
from elearning.crud.cours import get_cours, get_cours_module,createCours
from elearning.crud import utilisateur as crudutilisateur
from core.database import get_db
from typing import List

router = APIRouter()

@router.post("/cours/", response_model=LeconVideoBase)
def create_cours(
    lesson: LeconVideoCreate,
    db: Session = Depends(get_db)
        
):
    
    return createCours(db=db, lesson=lesson)
   

@router.get("/modules/{module_id}/first_video", response_model=LeconVideoBase)
def read_first_video(module_id: int, db: Session = Depends(get_db)):
    video = get_cours(db, module_id=module_id)
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return video



@router.get("/modules/{module_id}/videos", response_model=List[LeconVideoBase])
def read_videos(module_id: int, db: Session = Depends(get_db)):
    videos = get_cours_module(db, module_id=module_id)
    if not videos:
        raise HTTPException(status_code=404, detail="No videos found")
    return videos

