# ============================================================
# models/factura_mayor_a_casa.py — Tabla de facturas Major a Casa
# ============================================================

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base


class FacturaMayorACasa(Base):
    """
    Tabla 'facturas_mayor_a_casa' en PostgreSQL.
    Almacena el resumen mensual de facturación del servicio.
    """

    __tablename__ = "facturas_mayor_a_casa"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    anio = Column(Integer, nullable=False, index=True)
    mes  = Column(Integer, nullable=False, index=True)

    num_casos = Column(Integer, default=0)
    cuantia   = Column(Float, default=0.0)

    pdf_filename = Column(String(255), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    def __repr__(self):
        return f"<Factura id={self.id} fecha={self.anio}-{self.mes} cuantia={self.cuantia}>"
