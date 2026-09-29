# api/v1/user_api.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import List
from datetime import timedelta

from bd.database import get_session
from models.user_model import Usuario
from schemas.user_schema import UserCreate, UserResponse, UserUpdate
from schemas.token_schema import Token, TokenData
from core.security import verify_password, get_password_hash, create_access_token
from core.config import settings
from api.v1.dependencies import get_current_user

router = APIRouter()


# === CREAR usuario ===
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, session: Session = Depends(get_session)):
    """
    Crea un nuevo usuario en la base de datos.
    """
    statement = select(Usuario).where(Usuario.email == user_data.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado",
        )

    statement = select(Usuario).where(Usuario.username == user_data.username)
    existing_username = session.exec(statement).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El username ya está en uso",
        )

    db_user = Usuario(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        is_active=True,
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
    users = session.exec(select(Usuario)).all()
    return users


# === OBTENER usuario por ID ===
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, session: Session = Depends(get_session)):
    """
    Obtiene un usuario específico por su ID.
    """
    user = session.get(Usuario, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado",
        )
    return user


# === ACTUALIZAR usuario ===
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: Session = Depends(get_session),
):
    """
    Actualiza los datos de un usuario existente.
    """
    db_user = session.get(Usuario, user_id)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado",
        )

    update_data = user_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if field == "password":
            db_user.hashed_password = get_password_hash(value)
        else:
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
    db_user = session.get(Usuario, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado",
        )

    session.delete(db_user)
    session.commit()

    return None

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """
    Obtiene un token de acceso JWT validando el usuario y la contraseña.
    Requiere 'python-multipart' instalado para procesar el formulario.
    """
    # 1. Buscar el usuario en la base de datos por su nombre de usuario
    statement = select(Usuario).where(Usuario.username == form_data.username)
    user = session.exec(statement).first()
    
    # 2. Validar que el usuario exista y que la contraseña coincida con el hash
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Generar el token JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    # 4. Retornar el token en el formato estándar OAuth2
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/", response_model=List[UserResponse])
def get_users(sesion: Session = Depends(get_current_user)):
    users = sesion.exec(select(Usuario)).all()
    return users
