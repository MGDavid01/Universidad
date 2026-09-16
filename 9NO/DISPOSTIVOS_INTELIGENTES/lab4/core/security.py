# core/security.py

from passlib.context import CryptContext


# Configuración para Argon2
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__time_cost=2,
    argon2__memory_cost=10240,
    argon2__parallelism=2,
)


def get_password_hash(password: str) -> str:
    """Hashea la contraseña usando Argon2."""
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """Verifica si la contraseña coincide con el hash."""
    return pwd_context.verify(
        plain_password,
        hashed_password
    )