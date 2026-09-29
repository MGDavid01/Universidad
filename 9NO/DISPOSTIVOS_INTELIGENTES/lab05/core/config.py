#  core/ config. py
from pydantic_settings import BaseSettings

class Settings (BaseSettings):
    # configuracion de base de datos
    DATABASE_URL : str

    # configuracion de Autenticacion JTW
    SECRET_KEY : str
    ALGORITHM : str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int =30

    # cpnfiguracion de Pydantic V2
    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }
settings = Settings()