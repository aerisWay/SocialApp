# ============================================================
# models/comision_mayor_a_casa.py — Tabla de comisiones Major a Casa
# ============================================================

from sqlalchemy import Column, Integer, String, Date, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class ComisionMayorACasa(Base):
    """
    Tabla 'comisiones_mayor_a_casa' en PostgreSQL.
    Registra las solicitudes de alta en el servicio que aún no son casos activos.
    """

    __tablename__ = "comisiones_mayor_a_casa"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # ── Datos de la solicitud ─────────────────────────────────
    apellidos = Column(String(100), nullable=False)
    nombre    = Column(String(100), nullable=False)
    dni       = Column(String(9), nullable=True, index=True)
    sip       = Column(String(8), nullable=True, index=True)

    zona      = Column(Integer, nullable=True)

    fecha_comision = Column(Date, nullable=True) # Cuándo se trata en la comisión
    num_expediente = Column(String(50), nullable=True, index=True)

    # ── Estado de la comisión ───────────────────────────────
    # Valores: 'tramite' | 'aprobado' | 'denegado'
    estado = Column(String(20), default='tramite', nullable=False)

    observaciones = Column(Text, nullable=True)

    # ── Auditoría ─────────────────────────────────────────────
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    def __repr__(self):
        return f"<Comision id={self.id} dni={self.dni} estado={self.estado}>"
