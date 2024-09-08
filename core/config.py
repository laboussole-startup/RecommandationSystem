import os
from pathlib import Path
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Charger les variables d'environnement
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Chemin du fichier CSV
CSV_FILE_PATH = 'recommendation/formations_with_centres_interet.csv'
class Settings(BaseSettings):
    # Configuration de la base de données
    DB_USER: str = quote_plus(os.getenv('POSTGRES_USER', 'default_user'))
    DB_PASSWORD: str = quote_plus(os.getenv('POSTGRES_PASSWORD', 'default_password'))
    DB_NAME: str = quote_plus(os.getenv('POSTGRES_DB', 'default_db'))
    DB_HOST: str = quote_plus(os.getenv('POSTGRES_SERVER', 'localhost'))
    DB_PORT: str = quote_plus(os.getenv('POSTGRES_PORT', '5432'))

    # Configuration JWT
    JWT_SECRET: str = os.getenv('JWT_SECRET')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('JWT_TOKEN_EXPIRE_MINUTES'))
    
    # URL de la base de données
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

def get_settings() -> Settings:
    return Settings()
