from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base
from core.config import get_settings

settings = get_settings()

# Configuration de la base de données SQLAlchemy
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)


# Crée une instance de la classe DeclarativeBase qui sera utilisée pour la définition des modèles
Base = declarative_base()

# Créer une SessionLocal qui sera utilisée pour interagir avec la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fonction pour obtenir une session de base de données
@contextmanager
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()






