# ============================================================
# utils/auth.py — Funciones de seguridad: tokens JWT y contraseñas
# ============================================================
# Este archivo centraliza TODA la lógica de autenticación:
#   1. Hashear/verificar contraseñas (bcrypt)
#   2. Crear/decodificar tokens JWT
#   3. Dependencia que protege los endpoints
# ============================================================

from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db

# ── Contexto de contraseñas ───────────────────────────────────
# bcrypt es el algoritmo estándar para contraseñas: lento a propósito
# para que un atacante no pueda probar millones de contraseñas por segundo
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ── Esquema de seguridad ──────────────────────────────────────
# HTTPBearer espera: Authorization: Bearer <token> en la cabecera HTTP
security = HTTPBearer(auto_error=False)


# ── Contraseñas ───────────────────────────────────────────────

def hash_password(raw: str) -> str:
    """Convierte 'miContraseña' en un hash irreversible para guardar en BD."""
    return pwd_context.hash(raw)


def verify_password(raw: str, hashed: str) -> bool:
    """Comprueba si la contraseña introducida coincide con el hash guardado."""
    return pwd_context.verify(raw, hashed)


# ── Tokens JWT ────────────────────────────────────────────────

def create_token(data: dict, expires_hours: int = 8) -> str:
    """
    Crea un token JWT firmado con la SECRET_KEY.
    Válido durante `expires_hours` horas (por defecto 8 = una jornada).
    """
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(hours=expires_hours)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict:
    """
    Decodifica y verifica un JWT.
    Lanza HTTPException 401 si el token es inválido o ha expirado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Sesión expirada o inválida. Por favor, inicia sesión de nuevo.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise credentials_exception


# ── Dependencia: proteger endpoints ──────────────────────────

def get_current_dept(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Dependencia FastAPI que protege cualquier endpoint.
    Uso: añade `Depends(get_current_dept)` a un router o endpoint.

    Si el token es válido → devuelve el departamento.
    Si no hay token o es inválido → responde 401 Unauthorized.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticación requerida.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_token(credentials.credentials)
    username: str = payload.get("sub")

    # Importación local para evitar importaciones circulares
    from app.models.departamento import Departamento

    dept = db.query(Departamento).filter_by(username=username, activo=True).first()
    if not dept:
        raise HTTPException(status_code=401, detail="Departamento no encontrado o inactivo.")

    return dept
