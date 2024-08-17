from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from elearning.schemas import token as schematoken
from elearning.crud import utilisateur as crudutilisateur
from elearning.schemas.SchemasPydantic import UtilisateurBase,UtilisateurCreate,UtilisateurRead
from elearning.schemas import util
from core.database import get_db
from core.config import settings

router = APIRouter()

@router.post("/token", response_model=schematoken.Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = util.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = util.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/utilisateurs/", response_model=UtilisateurBase)
def create_utilisateur(utilisateur: UtilisateurCreate, db: Session = Depends(get_db)):
    db_utilisateur = crudutilisateur.get_utilisateur_by_email(db, email=utilisateur.email)
    if db_utilisateur:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crudutilisateur.create_utilisateur(db=db, utilisateur=utilisateur)
