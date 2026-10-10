# models/user_model.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone


"""

A primera vista parece un error: ¿cómo va a ser opcional la llave primaria de una tabla?
Pero en realidad, es la forma correcta y estándar de hacerlo en SQLModel. Piensa en el "ciclo de vida" de un objeto antes y 
después de guardarlo en la base de datos.


Cuando creas un usuario nuevo en tu código de Python 
(por ejemplo: nuevo_user = User(username='mike', email='...')), 
aún no lo has mandado a la base de datos. 
La base de datos es la encargada de autogenerar ese ID (usando AUTO_INCREMENT o SERIAL).


    Modelo de Usuario para la base de datos.
    Hereda de SQLModel (que combina Pydantic + SQLAlchemy)
    """

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
  
    # Nuevo campo de la imagen
    profile_pic: Optional[str] = Field(default=None, max_length=255)
    
    class Config:
        # Configuración opcional para la tabla
        table_name = "users"