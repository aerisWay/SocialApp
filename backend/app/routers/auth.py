# ============================================================
# routers/auth.py — Endpoint de inicio de sesión
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.departamento import Departamento
from app.utils.auth import verify_password, create_token

router = APIRouter()


# ── Schemas de este router ─────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    dept_name:    str    # "Servicio de Promoción"


# ── Endpoint ───────────────────────────────────────────────────

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Iniciar sesión con credenciales de departamento",
)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Recibe usuario y contraseña del departamento.
    Si son correctos, devuelve un token JWT válido 8 horas.
    """
    dept = db.query(Departamento).filter_by(username=data.username, activo=True).first()

    # Comprobamos usuario Y contraseña en el mismo bloque
    # (para no revelar si el usuario existe o no)
    if not dept or not verify_password(data.password, dept.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos.",
        )

    token = create_token({
        "sub":       dept.username,
        "dept_id":   dept.id,
        "dept_name": dept.nombre,
    })

    return {"access_token": token, "token_type": "bearer", "dept_name": dept.nombre}
