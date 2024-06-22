import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings


env_path = Path(".") / ".env"

load_dotenv(dotenv_path=env_path)
CSV_FILE_PATH = 'recommendation/formations_with_centres_interet.csv'
class Settings(BaseSettings):
        
    # Database
    DB_USER:str ="laboussole" #str = os.getenv('POSTGRES_USER')
    DB_PASSWORD:str ="TnpAnsAhOOOXjDn7FphW6OYrKtcLk6qm" #str = os.getenv('POSTGRES_PASSWORD')
    DB_NAME:str="laboussolebd" #str = os.getenv('POSTGRES_DB')
    DB_HOST :str="dpg-co9abbq0si5c73994390-a.oregon-postgres.render.com" #str = os.getenv('POSTGRES_SERVER')
    DB_PORT:str="5432" #str = os.getenv('POSTGRES_PORT')
    DATABASE_URL: str = f"postgresql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{quote_plus(DB_HOST)}:{quote_plus(DB_PORT)}/{quote_plus(DB_NAME)}"
    # JWT 
    JWT_SECRET: str = os.getenv('JWT_SECRET', '709d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('JWT_TOKEN_EXPIRE_MINUTES', 60)
def get_settings() -> Settings:
    return Settings()



