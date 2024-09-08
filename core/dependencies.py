from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from elearning.crud import auth as crudutilisateur
from elearning.models.modelsSQLAlchemy import Utilisateurtest
from elearning.schemas import util
from .database import get_db
from .config import Settings, get_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Utilisateurtest:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, get_settings().JWT_SECRET, algorithms=[get_settings().JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crudutilisateur.get_utilisateur_by_email(db, email=username)
    if user is None:
        raise credentials_exception
    return user



def get_current_active_user(current_user: Utilisateurtest = Depends(get_current_user)) -> Utilisateurtest:
    if not current_user.est_actif:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
