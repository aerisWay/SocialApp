# ============================================================
# models/departamento.py — Tabla de departamentos (cuentas de acceso)
# ============================================================
# Cada fila = un departamento con su usuario y contraseña compartida.
# Las trabajadoras de un departamento usan el mismo usuario/contraseña.
# ============================================================

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Departamento(Base):
    __tablename__ = "departamentos"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    nombre          = Column(String(100), nullable=False)       # "Servicio de Promoción"
    username        = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)       # Nunca en texto plano
    activo          = Column(Boolean, default=True, nullable=False)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Departamento username={self.username} nombre={self.nombre}>"
