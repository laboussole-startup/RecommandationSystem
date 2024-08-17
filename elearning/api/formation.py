from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from elearning.schemas.SchemasPydantic import FormationCreate, FormationRead,FormationBase
from elearning.schemas.SchemasPydantic import UtilisateurRead,UtilisateurBase,UtilisateurCreate
from elearning.crud.formation import get_formation, get_formations,createFormation
from elearning.crud import utilisateur as crudutilisateur
from core.database import get_db
from core.dependencies import get_current_active_user, get_current_user
from typing import List

router = APIRouter()

@router.post("/formations/", response_model=FormationRead)
def create_formation(
    formation: FormationCreate,
    db: Session = Depends(get_db),
    current_user: UtilisateurRead = Depends(get_current_active_user)
    
):
    print(current_user.role)
    if current_user.role.value != 'instructeur':
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    
    return createFormation(db=db, formation=formation, instructeur_id =current_user.id_utilisateur)

@router.get("/formations/{formation_id}", response_model=FormationRead)
def read_formation(formation_id: int, db: Session = Depends(get_db)):
    db_formation = get_formation(db, formation_id=formation_id)
    if db_formation is None:
        raise HTTPException(status_code=404, detail="Formation not found")
    return db_formation

@router.get("/formations/", response_model=List[FormationRead])
def read_formations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    formations = get_formations(db, skip=skip, limit=limit)
    return formations
