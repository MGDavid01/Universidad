# db/database.py
import os

from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError
from sqlmodel import SQLModel, Session, create_engine

# Carga las variables del archivo .env
load_dotenv()

# Obtiene la URL de la base de datos.
# Si no existe, usa SQLite por defecto para no romper el entorno local.
DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///./willydb.db"


def _build_engine(database_url: str):
    connect_args = {}
    if "sqlite" in database_url:
        connect_args = {"check_same_thread": False}
    return create_engine(
        database_url,
        echo=False,  # En producción siempre False
        connect_args=connect_args,
    )


engine = _build_engine(DATABASE_URL)


def create_db_and_tables():
    global engine
    try:
        SQLModel.metadata.create_all(engine)
    except OperationalError:
        if "postgres" not in DATABASE_URL.lower():
            raise
        sqlite_url = "sqlite:///./willydb.db"
        engine = _build_engine(sqlite_url)
        SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
