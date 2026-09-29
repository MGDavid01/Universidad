# schemas/token_schema>py
from pydantic import BaseModel
from typing import Optional
from sqlmodel import SQLModel 

class Token(BaseModel):
    """Esquema de respuesta para el endpoin tde login"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """ESQUEMA PARA LOS DATOS DECODIFICADOS DEL TOKEN """
    username: str | None = None
