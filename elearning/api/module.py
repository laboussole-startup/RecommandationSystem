from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.dependencies import get_current_active_user
from elearning.schemas.SchemasPydantic import ModuleBase,ModuleCreate,ModuleRead
from elearning.schemas.SchemasPydantic import UtilisateurRead,UtilisateurBase
from elearning.crud.module import get_modules, get_module,createModule
from elearning.crud import utilisateur as crudutilisateur
from core.database import get_db
from typing import List

router = APIRouter()

@router.post("/modules/", response_model=ModuleRead)
def create_formation(
    module: ModuleCreate,
    db: Session = Depends(get_db),
    
        
):
    
    return createModule(db=db, module=module)
   

@router.get("/modules/{formation_id}", response_model=list[ModuleRead])
def read_modules(formation_id: int, db: Session = Depends(get_db)):
    db_formation = get_modules(db, formation_id=formation_id)
    if db_formation is None:
        raise HTTPException(status_code=404, detail="Formation not found")
    return db_formation

@router.get("/module/{module_id}", response_model=ModuleRead)
def read_module(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    formations = get_module(db, skip=skip, limit=limit)
    return formations
