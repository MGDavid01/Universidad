# schemas/token_schema.py
from pydantic import BaseModel
from typing import Optional
from sqlmodel import SQLModel


class Token(BaseModel):
    """Esquema de respuesta para el endpoint de login."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Esquema para los datos decodificados del token JWT."""
    username: str | None = None