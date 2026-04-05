# ============================================================
# config.py — Configuración centralizada de la aplicación
# ============================================================

import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- Base de datos ---
    # Valor por defecto para desarrollo local con Docker Compose
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/apbapp_db"

    # --- Seguridad / JWT ---
    SECRET_KEY: str = "cambia-esto-por-una-clave-secreta-muy-larga"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --- Entorno ---
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # --- Nombre de la app ---
    APP_NAME: str = "APBApp"

    # --- Credenciales de departamentos ---
    DEPT_PROMOCION_PASSWORD: str = "Promocion2026"

    # Usa model_config (la forma moderna de pydantic-settings v2)
    # env_file_sentinel='missing' evita errores si .env no existe
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",          # Ignora variables de Railway que no necesitamos
    )


# Diagnóstico de arranque
settings = Settings()
print(f"[CONFIG] DATABASE_URL = {settings.DATABASE_URL[:30]}...")
print(f"[CONFIG] ENVIRONMENT = {settings.ENVIRONMENT}")
