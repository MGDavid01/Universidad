import uuid
import os
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import List
from datetime import timedelta
import boto3
from botocore.exceptions import ClientError

# Importaciones del proyecto
from db.database import get_session
from models.user_model import User
from schemas.user_schema import UserCreate, UserUpdate, UserResponse
from schemas.token_schema import Token, TokenData
from core.security import verify_password, create_access_token, get_password_hash
from core.config import settings
from api.v1.dependencies import get_current_user, get_minio_client, ensure_bucket_exists


router = APIRouter()

# === CREAR usuario ===
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, session: Session = Depends(get_session)):
    """
    Crea un nuevo usuario en la base de datos con la contraseña hasheada.
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
    
    # Hashear la contraseña recibida en la petición
    hashed_pwd = get_password_hash(user_data.password)

    # Crear la instancia del modelo guardando el hash
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd,
        is_active=True
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user

# === OBTENER todos los usuarios ===
@router.get("/", response_model=List[UserResponse])
def get_users(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene todos los usuarios registrados (requiere autenticación).
    """
    users = session.exec(select(User)).all()
    return users

# === NUEVO: SUBIR / ACTUALIZAR IMAGEN DE PERFIL EN MINIO ===
@router.patch("/me/profile-pic", response_model=UserResponse)
async def update_profile_picture(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    minio_client: boto3.client = Depends(get_minio_client)
):
    """
    Sube la foto de perfil a MinIO y actualiza la referencia en la base de datos.
    """
    # 1. Validar tipo de archivo
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Solo se permiten imágenes JPEG, PNG o WebP"
        )

    # 2. Asegurar que el bucket existe
    ensure_bucket_exists(minio_client)

    try:
        # 3. Generar nombre único y subir a MinIO
        file_extension = os.path.splitext(file.filename)[1] or ".jpg"
        unique_filename = f"profile_{current_user.id}_{uuid.uuid4()}{file_extension}"
    
        minio_client.upload_fileobj(
            file.file,
            settings.MINIO_BUCKET_NAME,
            unique_filename,
            ExtraArgs={'ContentType': file.content_type}
        )

        # 4. Actualizar la referencia en la Base de Datos
        current_user.profile_pic = unique_filename
        session.add(current_user)
        session.commit()
        session.refresh(current_user)

        return current_user

    except ClientError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error al subir la imagen a MinIO: {str(e)}"
        )

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
    
    # Extraer únicamente los campos enviados
    update_data = user_update.model_dump(exclude_unset=True)

    # Si se envió una nueva contraseña, la extraemos y la hasheamos antes de guardar
    if "password" in update_data:
        raw_password = update_data.pop("password")
        db_user.hashed_password = get_password_hash(raw_password)

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
    
    return None

# === LOGIN PARA OBTENER TOKEN ===
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """
    Obtiene un token de acceso JWT validando el usuario y la contraseña.
    """
    statement = select(User).where(User.username == form_data.username)
    user = session.exec(statement).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}