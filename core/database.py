# core/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from core.config import get_settings

# Charger les paramètres
settings = get_settings()

# Configuration de la base de données SQLAlchemy
engine = create_engine(settings.DATABASE_URL)

# Crée une instance de la classe DeclarativeBase pour les modèles
Base = declarative_base()

# Créer une session pour interagir avec la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Gestionnaire de contexte pour ouvrir et fermer une session de la base de données
def get_db():
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()