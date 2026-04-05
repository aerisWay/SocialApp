# ============================================================
# schemas/comision_mayor_a_casa.py — Validación de comisiones
# ============================================================

import re
from pydantic import BaseModel, field_validator, model_validator
from datetime import date, datetime
from typing import Optional

RE_DNI = re.compile(r'^\d{8}[A-Za-z]$')
RE_SIP = re.compile(r'^\d{8}$')
ESTADOS_VALIDOS = ('en_tramite', 'aprobado', 'denegado')


class ComisionCreate(BaseModel):
    apellidos: str
    nombre:    str

    dni: Optional[str] = None
    sip: Optional[str] = None

    zona:           Optional[int] = None
    rango_edad:     Optional[str] = None
    sexo:           Optional[str] = None
    mes_renovacion: Optional[str] = None
    telefono:       Optional[str] = None
    direccion:      Optional[str] = None
    estado:         str = 'en_tramite'
    mes_comision:   Optional[str] = None
    observaciones:  Optional[str] = None

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

    @field_validator("estado")
    @classmethod
    def estado_valido(cls, v):
        if v not in ESTADOS_VALIDOS:
            raise ValueError(f"Estado debe ser uno de: {', '.join(ESTADOS_VALIDOS)}")
        return v

    @field_validator("rango_edad")
    @classmethod
    def rango_edad_valido(cls, v):
        if v is not None and v not in ('menor_60', '60_65', 'mayor_65'):
            raise ValueError("Rango de edad inválido")
        return v or None


class ComisionUpdate(BaseModel):
    apellidos:      Optional[str]  = None
    nombre:         Optional[str]  = None
    dni:            Optional[str]  = None
    sip:            Optional[str]  = None
    zona:           Optional[int]  = None
    rango_edad:     Optional[str]  = None
    sexo:           Optional[str]  = None
    mes_renovacion: Optional[str]  = None
    telefono:       Optional[str]  = None
    direccion:      Optional[str]  = None
    estado:         Optional[str]  = None
    mes_comision:   Optional[str]  = None
    observaciones:  Optional[str]  = None

    @field_validator("estado")
    @classmethod
    def estado_valido(cls, v):
        if v is not None and v not in ESTADOS_VALIDOS:
            raise ValueError(f"Estado debe ser uno de: {', '.join(ESTADOS_VALIDOS)}")
        return v

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


class ComisionResponse(BaseModel):
    id:             int
    apellidos:      str
    nombre:         str
    dni:            Optional[str]
    sip:            Optional[str]
    zona:           Optional[int]
    rango_edad:     Optional[str]
    sexo:           Optional[str]
    mes_renovacion: Optional[str]
    telefono:       Optional[str]
    direccion:      Optional[str]
    estado:         str
    mes_comision:   Optional[str]
    observaciones:  Optional[str]
    caso_id:        Optional[int]
    created_at:     datetime

    class Config:
        from_attributes = True
