from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # ... (Tus configuraciones existentes de DATABASE_URL, etc.) ...
  
    # === Configuración de MinIO ===
    MINIO_ENDPOINT: str = "http://localhost:9000"
    MINIO_ACCESS_KEY: str = "admin"
    MINIO_SECRET_KEY: str = "passwordseguro123"
    MINIO_BUCKET_NAME: str = "fastapi-images"
    MINIO_REGION: str = "us-east-1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = "super_secret_key_123456789_mugiwaras"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()