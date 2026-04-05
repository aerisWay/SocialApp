# ============================================================
# models/comision_mayor_a_casa.py — Comisiones pendientes de aprobación
# ============================================================
# Las comisiones son solicitudes de ingreso al servicio Major a Casa.
# Cuando una comisión es aprobada, se crea automáticamente un caso
# en la tabla casos_mayor_a_casa.
# ============================================================

from sqlalchemy import Column, Integer, String, Date, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class ComisionMayorACasa(Base):
    __tablename__ = "comisiones_mayor_a_casa"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # ── Datos personales ──────────────────────────────────────
    apellidos = Column(String(100), nullable=False)
    nombre    = Column(String(100), nullable=False)
    dni       = Column(String(9),  nullable=True, index=True)
    sip       = Column(String(8),  nullable=True, index=True)

    # ── Datos del servicio ────────────────────────────────────
    zona          = Column(Integer,    nullable=True)
    rango_edad    = Column(String(15), nullable=True)  # 'menor_60' | '60_65' | 'mayor_65'
    mes_renovacion= Column(String(7),  nullable=True)

    # ── Contacto ──────────────────────────────────────────────
    telefono  = Column(String(20),  nullable=True)
    direccion = Column(String(255), nullable=True)

    # ── Fechas ────────────────────────────────────────────────
    fecha_alta = Column(Date, nullable=True)
    fecha_baja = Column(Date, nullable=True)

    # ── Sexo ──────────────────────────────────────────────────
    sexo = Column(String(10), nullable=True)

    # ── Estado de la comisión ─────────────────────────────────
    # 'en_tramite' | 'aprobado' | 'denegado'
    estado = Column(String(20), default='en_tramite', nullable=False)

    # ── Campo nuevo solicitado ────────────────────────────────
    mes_comision = Column(String(7), nullable=True)  # '2026-04'

    # ── Notas ─────────────────────────────────────────────────
    observaciones = Column(Text, nullable=True)

    # ── Referencia al caso creado al aprobar ──────────────────
    caso_id = Column(Integer, nullable=True)

    # ── Auditoría ─────────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Comision id={self.id} estado={self.estado} nombre={self.apellidos}, {self.nombre}>"
