# ============================================================
# models/seguimiento_mayor_a_casa.py — Seguimiento (Entrevistas/Visitas/Informes)
# ============================================================

from sqlalchemy import Column, Integer, String, Text, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base


class SeguimientoMayorACasa(Base):
    __tablename__ = "seguimientos_mayor_a_casa"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    tipo         = Column(String(20), nullable=False)   # entrevista | visita | informe
    anio         = Column(Integer, nullable=False)
    mes          = Column(Integer, nullable=False)       # 1-12
    cantidad     = Column(Integer, default=0, nullable=True)
    hombres      = Column(Integer, default=0, nullable=True)
    mujeres      = Column(Integer, default=0, nullable=True)
    observaciones = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    __table_args__ = (
        UniqueConstraint('tipo', 'anio', 'mes', name='uq_seguimiento_tipo_anio_mes'),
    )

    def __repr__(self):
        return f"<Seguimiento {self.tipo} {self.anio}-{self.mes:02d}>"
