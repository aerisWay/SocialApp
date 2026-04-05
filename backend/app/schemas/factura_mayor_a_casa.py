# ============================================================
# schemas/factura_mayor_a_casa.py — Esquemas Pydantic
# ============================================================

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FacturaBase(BaseModel):
    anio: int
    mes: int
    num_casos: int = 0
    cuantia: float = 0.0


class FacturaCreate(FacturaBase):
    pass


class FacturaResponse(FacturaBase):
    id: int
    pdf_filename: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
