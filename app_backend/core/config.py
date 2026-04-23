import os
from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    app_name: str = "Red social"
    database_url: str = Field(..., validation_alias='DATABASE_URL')
    
    secret_key: str = Field(..., validation_alias='SECRET_KEY')
    algorithm: str = Field("HS256", validation_alias='ALGORITHM')
    access_token_expire: int = Field(30, validation_alias='ACCESS_TOKEN_EXPIRE')

    model_config = {
        "env_file": os.path.join(BASE_DIR, ".env"),
        "extra": "ignore"
    }

settings = Settings()
