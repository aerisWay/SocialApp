# ============================================================
# models/caso_mayor_a_casa.py — Tabla de casos "Major a Casa"
# ============================================================
# Esta tabla almacena las personas atendidas por el servicio.
# No es lo mismo que la tabla 'users' (que serán los trabajadores
# que usan la app). Aquí guardamos los CASOS (los beneficiarios).
# ============================================================

from sqlalchemy import Column, Integer, String, Boolean, Date, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class CasoMayorACasa(Base):
    """
    Tabla 'casos_mayor_a_casa' en PostgreSQL.
    Cada fila es una persona atendida por el servicio Major a Casa.
    """

    __tablename__ = "casos_mayor_a_casa"

    # ── Identificador ─────────────────────────────────────────
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # ── Datos personales ──────────────────────────────────────
    apellidos = Column(String(100), nullable=False)
    nombre    = Column(String(100), nullable=False)

    # DNI: 8 dígitos + 1 letra. Al menos uno de dni o sip es obligatorio.
    dni = Column(String(9), nullable=True, index=True)
    # SIP: 8 dígitos exactos
    sip = Column(String(8), nullable=True, index=True)

    # ── Datos del servicio ────────────────────────────────────

    # Zona geográfica: valores 1, 2, 3 o 4
    zona = Column(Integer, nullable=True)

    # Mes de renovación del servicio: "YYYY-MM" (ej: "2025-06")
    # Usamos String para guardar exactamente el formato mes+año
    mes_renovacion = Column(String(7), nullable=True)

    # ── Contacto ──────────────────────────────────────────────
    telefono  = Column(String(20), nullable=True)
    direccion = Column(String(255), nullable=True)

    # ── Fechas de alta y baja ─────────────────────────────────
    fecha_alta = Column(Date, nullable=True)
    fecha_baja = Column(Date, nullable=True)

    # ── Rango de edad ─────────────────────────────────────────
    # 'menor_60' | '60_65' | 'mayor_65' | None
    rango_edad = Column(String(15), nullable=True)

    # ── Sexo ──────────────────────────────────────────────────
    # Valores: 'hombre' | 'mujer' | 'no_define' | None
    sexo = Column(String(10), nullable=True)

    # ── Estado ────────────────────────────────────────────────
    activo = Column(Boolean, default=True, nullable=False)

    # ── Notas adicionales ─────────────────────────────────────
    # Text = sin límite de caracteres (a diferencia de String)
    observaciones = Column(Text, nullable=True)

    # ── Auditoría (automático) ────────────────────────────────
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    def __repr__(self):
        return f"<Caso id={self.id} dni={self.dni} sip={self.sip} nombre={self.apellidos}, {self.nombre}>"
