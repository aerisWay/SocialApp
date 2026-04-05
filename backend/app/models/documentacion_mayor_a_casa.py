# ============================================================
# models/documentacion_mayor_a_casa.py — Documentación de referencia
# ============================================================

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class DocumentacionMayorACasa(Base):
    __tablename__ = "documentacion_mayor_a_casa"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    titulo       = Column(String(200), nullable=False)
    pdf_filename = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    def __repr__(self):
        return f"<Documentacion id={self.id} titulo={self.titulo!r}>"
