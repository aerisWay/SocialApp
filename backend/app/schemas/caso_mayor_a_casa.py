# ============================================================
# schemas/caso_mayor_a_casa.py — Validación de datos de casos
# ============================================================

import re
from pydantic import BaseModel, field_validator, model_validator
from datetime import date, datetime
from typing import Optional


RE_DNI = re.compile(r'^\d{8}[A-Za-z]$')
RE_SIP = re.compile(r'^\d{8}$')


# ── ENTRADA: crear un caso nuevo ──────────────────────────────
class CasoCreate(BaseModel):
    # Obligatorios
    apellidos: str
    nombre:    str

    # Al menos uno de estos es obligatorio (validado en model_validator)
    dni: Optional[str] = None
    sip: Optional[str] = None

    # Opcionales
    zona:           Optional[int]  = None
    sexo:           Optional[str]  = None
    mes_renovacion: Optional[str]  = None
    telefono:       Optional[str]  = None
    direccion:      Optional[str]  = None
    fecha_alta:     Optional[date] = None
    fecha_baja:     Optional[date] = None
    activo:         bool           = True
    observaciones:  Optional[str]  = None

    @model_validator(mode='after')
    def al_menos_dni_o_sip(self):
        if not self.dni and not self.sip:
            raise ValueError('Debes introducir al menos DNI o SIP')
        return self

    @field_validator("dni")
    @classmethod
    def dni_valido(cls, v):
        if v is not None and v != '':
            if not RE_DNI.match(v):
                raise ValueError("El DNI debe tener 8 dígitos y 1 letra (ej: 12345678X)")
            return v
        return None

    @field_validator("sip")
    @classmethod
    def sip_valido(cls, v):
        if v is not None and v != '':
            if not RE_SIP.match(v):
                raise ValueError("El SIP debe tener exactamente 8 dígitos")
            return v
        return None

    @field_validator("sexo")
    @classmethod
    def sexo_valido(cls, v):
        if v is not None and v not in ("hombre", "mujer", "no_define"):
            raise ValueError("El sexo debe ser 'hombre', 'mujer' o 'no_define'")
        return v or None

    @field_validator("zona")
    @classmethod
    def zona_valida(cls, v):
        if v is not None and v not in (1, 2, 3, 4):
            raise ValueError("La zona debe ser 1, 2, 3 o 4")
        return v

    @field_validator("mes_renovacion")
    @classmethod
    def mes_formato_valido(cls, v):
        if v is not None and v != "":
            parts = v.split("-")
            if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
                raise ValueError("El mes de renovación debe tener formato YYYY-MM")
        return v or None


# ── ENTRADA: actualizar un caso (todos opcionales) ────────────
class CasoUpdate(BaseModel):
    apellidos:      Optional[str]  = None
    nombre:         Optional[str]  = None
    dni:            Optional[str]  = None
    sip:            Optional[str]  = None
    zona:           Optional[int]  = None
    sexo:           Optional[str]  = None
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
    dni:            Optional[str]
    sip:            Optional[str]
    zona:           Optional[int]
    sexo:           Optional[str]
    mes_renovacion: Optional[str]
    telefono:       Optional[str]
    direccion:      Optional[str]
    fecha_alta:     Optional[date]
    fecha_baja:     Optional[date]
    activo:         bool
    observaciones:  Optional[str]
    created_at:     datetime

    class Config:
        from_attributes = True
