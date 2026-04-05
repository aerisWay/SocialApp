# ============================================================
# schemas/seguimiento_mayor_a_casa.py
# ============================================================

from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

TIPOS_VALIDOS = ('entrevista', 'visita', 'informe')


class SeguimientoUpsert(BaseModel):
    tipo:          str
    anio:          int
    mes:           int
    cantidad:      Optional[int] = None
    hombres:       Optional[int] = None
    mujeres:       Optional[int] = None
    observaciones: Optional[str] = None

    @field_validator('tipo')
    @classmethod
    def tipo_valido(cls, v: str) -> str:
        if v not in TIPOS_VALIDOS:
            raise ValueError(f"tipo debe ser uno de {TIPOS_VALIDOS}")
        return v

    @field_validator('mes')
    @classmethod
    def mes_valido(cls, v: int) -> int:
        if not 1 <= v <= 12:
            raise ValueError("mes debe estar entre 1 y 12")
        return v


class SeguimientoResponse(BaseModel):
    id:            int
    tipo:          str
    anio:          int
    mes:           int
    cantidad:      Optional[int] = None
    hombres:       Optional[int] = None
    mujeres:       Optional[int] = None
    observaciones: Optional[str] = None
    created_at:    datetime

    model_config = {'from_attributes': True}
