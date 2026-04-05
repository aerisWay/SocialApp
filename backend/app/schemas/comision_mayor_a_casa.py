# ============================================================
# schemas/comision_mayor_a_casa.py — Esquemas Pydantic
# ============================================================

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class ComisionBase(BaseModel):
    apellidos: str
    nombre: str
    dni: Optional[str] = Field(None, pattern=r"^\d{8}[A-Za-z]$")
    sip: Optional[str] = Field(None, pattern=r"^\d{8}$")
    zona: Optional[int] = None
    fecha_comision: Optional[date] = None
    num_expediente: Optional[str] = None
    estado: str = 'tramite'
    observaciones: Optional[str] = None


class ComisionCreate(ComisionBase):
    pass


class ComisionResponse(ComisionBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
