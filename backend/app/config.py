# ============================================================
# config.py — Configuración centralizada de la aplicación
# ============================================================
# Pydantic lee automáticamente las variables del archivo .env
# y las valida. Si falta una variable obligatoria, el servidor
# no arranca y te avisa exactamente qué falta.

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # --- Base de datos ---
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/socialapp_db"

    # --- Seguridad / JWT ---
    SECRET_KEY: str = "cambia-esto-por-una-clave-secreta-muy-larga"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --- Entorno ---
    ENVIRONMENT: str = "development"   # "development" | "production"
    DEBUG: bool = True

    # --- Nombre de la app ---
    APP_NAME: str = "SocialApp"

    class Config:
        # Le dice a pydantic que lea las variables desde el archivo .env
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instancia única que importarás en cualquier archivo:
#   from app.config import settings
#   print(settings.DATABASE_URL)
settings = Settings()
