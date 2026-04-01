# ============================================================
# schemas/caso_mayor_a_casa.py — Validación de datos de casos
# ============================================================

from pydantic import BaseModel, field_validator
from datetime import date, datetime
from typing import Optional


# ── ENTRADA: crear un caso nuevo ──────────────────────────────
class CasoCreate(BaseModel):
    # Obligatorios
    apellidos: str
    nombre:    str
    dni_sip:   str

    # Opcionales
    zona:           Optional[int]  = None   # 1, 2, 3 o 4
    mes_renovacion: Optional[str]  = None   # "YYYY-MM"
    telefono:       Optional[str]  = None
    direccion:      Optional[str]  = None
    fecha_alta:     Optional[date] = None
    fecha_baja:     Optional[date] = None
    activo:         bool           = True
    observaciones:  Optional[str]  = None

    @field_validator("zona")
    @classmethod
    def zona_valida(cls, v):
        if v is not None and v not in (1, 2, 3, 4):
            raise ValueError("La zona debe ser 1, 2, 3 o 4")
        return v

    @field_validator("mes_renovacion")
    @classmethod
    def mes_formato_valido(cls, v):
        """Valida que el formato sea YYYY-MM (lo que devuelve <input type='month'>)"""
        if v is not None and v != "":
            parts = v.split("-")
            if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
                raise ValueError("El mes de renovación debe tener formato YYYY-MM")
        return v or None


# ── ENTRADA: actualizar un caso (todos opcionales) ────────────
class CasoUpdate(BaseModel):
    apellidos:      Optional[str]  = None
    nombre:         Optional[str]  = None
    dni_sip:        Optional[str]  = None
    zona:           Optional[int]  = None
    mes_renovacion: Optional[str]  = None
    telefono:       Optional[str]  = None
    direccion:      Optional[str]  = None
    fecha_alta:     Optional[date] = None
    fecha_baja:     Optional[date] = None
    activo:         Optional[bool] = None
    observaciones:  Optional[str]  = None


# ── SALIDA: lo que devuelve la API ────────────────────────────
class CasoResponse(BaseModel):
    id:             int
    apellidos:      str
    nombre:         str
    dni_sip:        str
    zona:           Optional[int]
    mes_renovacion: Optional[str]
    telefono:       Optional[str]
    direccion:      Optional[str]
    fecha_alta:     Optional[date]
    fecha_baja:     Optional[date]
    activo:         bool
    observaciones:  Optional[str]
    created_at:     datetime

    class Config:
        from_attributes = True   # Lee directamente objetos SQLAlchemy
