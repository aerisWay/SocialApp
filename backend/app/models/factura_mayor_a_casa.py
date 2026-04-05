# ============================================================
# models/factura_mayor_a_casa.py — Facturación mensual Major a Casa
# ============================================================

from sqlalchemy import Column, Integer, Numeric, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base


class FacturaMayorACasa(Base):
    __tablename__ = "facturas_mayor_a_casa"

    id     = Column(Integer, primary_key=True, autoincrement=True)
    anio   = Column(Integer, nullable=False)
    mes    = Column(Integer, nullable=False)   # 1–12
    num_casos = Column(Integer, default=0, nullable=True)
    cuantia   = Column(Numeric(10, 2), nullable=True)
    pdf_filename = Column(String(255), nullable=True)   # nombre del archivo en uploads/facturas/

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    __table_args__ = (
        UniqueConstraint('anio', 'mes', name='uq_factura_anio_mes'),
    )

    def __repr__(self):
        return f"<Factura {self.anio}-{self.mes:02d} casos={self.num_casos} cuantia={self.cuantia}>"
