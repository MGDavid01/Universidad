# api/v1/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

#achivos creados previamente
from db.database import get_session
from models.user_model import User
from schemas.user import UserCreate, UserUpdate, UserResponse



router = APIRouter()

# === CREAR usuario ===
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, session: Session = Depends(get_session)):
    """
    Crea un nuevo usuario en la base de datos.
    """
    # Verificar si el email ya existe
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Verificar si el username ya existe
    statement = select(User).where(User.username == user_data.username)
    existing_username = session.exec(statement).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El username ya está en uso"
        )
    
    # Crear el usuario (en producción, hashear la contraseña con bcrypt)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=user_data.password,  # Aquí deberías hashear la contraseña antes de guardarla
        is_active=True
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user

# === OBTENER todos los usuarios ===
@router.get("/", response_model=List[UserResponse])
def get_users(session: Session = Depends(get_session)):
    """
    Obtiene todos los usuarios registrados.
    """
    users = session.exec(select(User)).all()
    return users

# === OBTENER usuario por ID ===
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, session: Session = Depends(get_session)):
    """
    Obtiene un usuario específico por su ID.
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    return user

# === ACTUALIZAR usuario ===
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int, 
    user_update: UserUpdate, 
    session: Session = Depends(get_session)
):
    """
    Actualiza los datos de un usuario existente.
    """
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    
    # Actualizar solo los campos que vienen en el request
    update_data = user_update.model_dump(exclude_unset=True) #"truco de magia" para permitir actualizaciones parciales (cuando el cliente solo quiere cambiar uno o dos campos, no todo el registro).


    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user

# === ELIMINAR usuario ===
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    """
    Elimina un usuario de la base de datos.
    """
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    
    session.delete(db_user)
    session.commit()
    
    return None  # 204 No Content no devuelve nada