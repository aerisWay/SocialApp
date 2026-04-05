# ============================================================
# schemas/factura_mayor_a_casa.py — Validación de facturas
# ============================================================

from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from decimal import Decimal


class FacturaUpsert(BaseModel):
    anio:      int
    mes:       int        # 1–12
    num_casos: Optional[int]     = None
    cuantia:   Optional[Decimal] = None

    @field_validator("mes")
    @classmethod
    def mes_valido(cls, v):
        if not 1 <= v <= 12:
            raise ValueError("El mes debe estar entre 1 y 12")
        return v


class FacturaResponse(BaseModel):
    id:           int
    anio:         int
    mes:          int
    num_casos:    Optional[int]
    cuantia:      Optional[float]
    pdf_filename: Optional[str]
    created_at:   datetime

    class Config:
        from_attributes = True
