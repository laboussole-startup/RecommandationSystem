from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from core.database import get_db
from sqlalchemy.orm import Session
from elearning.crud import auth as crudutilisateur
from core.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def authenticate_user(email: str, password: str):
    with get_db() as db:
        user = crudutilisateur.get_utilisateur_by_email(db, email=email)
        if not user:
            return False
        if not verify_password(password, user.mot_de_passe):  # Assurez-vous que 'mot_de_passe' est bien le nom de l'attribut du mot de passe
            return False
        return user
