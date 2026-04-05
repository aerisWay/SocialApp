# ============================================================
# schemas/documentacion_mayor_a_casa.py
# ============================================================

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DocumentacionCreate(BaseModel):
    titulo: str


class DocumentacionUpdate(BaseModel):
    titulo: Optional[str] = None


class DocumentacionResponse(BaseModel):
    id:           int
    titulo:       str
    pdf_filename: Optional[str] = None
    created_at:   datetime

    model_config = {'from_attributes': True}
