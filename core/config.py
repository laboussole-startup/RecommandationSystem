import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings

# Définir le chemin du fichier .env
env_path = Path('.') / '.env'

# Charger les variables d'environnement depuis le fichier .env
load_dotenv(dotenv_path=env_path)

# Chemin du fichier CSV
CSV_FILE_PATH = 'recommendation/formations_with_centres_interet.csv'


class Settings(BaseSettings):
    # Database configuration
    DB_USER: str = quote_plus(os.getenv('DB_USER'))
    DB_PASSWORD: str = quote_plus(os.getenv('DB_PASSWORD'))
    DB_NAME: str = quote_plus(os.getenv('DB_NAME'))
    DB_HOST: str = quote_plus(os.getenv('DB_HOST'))
    DB_PORT: str = quote_plus(os.getenv('DB_PORT'))
    
    # Construire l'URL de la base de données
    DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # JWT configuration
    JWT_SECRET: str = os.getenv('JWT_SECRET', '709d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', 'HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('JWT_TOKEN_EXPIRE_MINUTES', 60))


def get_settings() -> Settings:
    return Settings()


# Exemple d'utilisation
settings = get_settings()

