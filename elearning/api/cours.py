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
   

@router.get("/cours_module/{module_id}", response_model=list[ModuleRead])
def read_modules(formation_id: int, db: Session = Depends(get_db)):
    db_formation = get_cours_module(db, formation_id=formation_id)
    if db_formation is None:
        raise HTTPException(status_code=404, detail="Formation not found")
    return db_formation

@router.get("/cours/{cours_id}", response_model=ModuleRead)
def read_cours(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    formations = get_cours(db, skip=skip, limit=limit)
    return formations
