from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.dependencies import get_current_user  # Assurez-vous d'avoir une fonction pour obtenir l'utilisateur actuel
from elearning.crud import enrollement
from elearning.models.modelsSQLAlchemy import Utilisateur
from elearning.schemas.SchemasPydantic import UserFormationLinkRead

router = APIRouter()

# Endpoint pour inscrire un utilisateur à une formation
@router.post("/formations/{formation_id}/inscription/", response_model=UserFormationLinkRead)
def user_inscription_formation(formation_id: int, db: Session = Depends(get_db), current_user: Utilisateur = Depends(get_current_user)):
    """
    Endpoint pour inscrire un utilisateur à une formation.
    """
    try:
        inscription = enrollement.user_inscription_formation(db, current_user.id_utilisateur, formation_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    return inscription
