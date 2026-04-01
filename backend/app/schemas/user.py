# ============================================================
# schemas/user.py — Formularios de entrada y salida de la API
# ============================================================
# Los schemas son como "contratos":
#   - UserCreate  → qué datos debe enviar el cliente al crear un usuario
#   - UserResponse → qué datos devuelve la API (nunca la contraseña, por ej.)
#
# Pydantic valida automáticamente los tipos. Si alguien envía un número
# donde se espera un texto, la API responderá un error claro.
# ============================================================

from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


# ── Schema de ENTRADA: lo que el cliente envía ────────────────
class UserCreate(BaseModel):
    """
    Datos necesarios para crear un nuevo usuario.
    El cliente enviará esto en el body de la petición (en formato JSON).
    """
    username: str
    email: str
    full_name: Optional[str] = None    # El nombre completo es opcional

    # Validación extra: el username no puede tener espacios
    @field_validator("username")
    @classmethod
    def username_sin_espacios(cls, v: str) -> str:
        if " " in v:
            raise ValueError("El username no puede contener espacios")
        return v.lower()   # Guardamos siempre en minúsculas

    # Validación extra: el email debe tener "@"
    @field_validator("email")
    @classmethod
    def email_valido(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("El email no es válido")
        return v.lower()


# ── Schema de ACTUALIZACIÓN: solo campos opcionales ───────────
class UserUpdate(BaseModel):
    """
    Datos que se pueden actualizar de un usuario.
    Todos son opcionales: puedes mandar solo los que quieres cambiar.
    """
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


# ── Schema de SALIDA: lo que la API devuelve ──────────────────
class UserResponse(BaseModel):
    """
    Datos que la API devuelve cuando consultas un usuario.
    Nota: nunca exponemos datos sensibles como contraseñas aquí.
    """
    id: int
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        # Permite que Pydantic lea directamente objetos SQLAlchemy (modelos de BD)
        # Sin esto, tendríamos que convertir manualmente cada objeto a diccionario
        from_attributes = True
