# ============================================================
# models/user.py — La "tabla" de usuarios en la base de datos
# ============================================================
# Un modelo = una tabla en PostgreSQL.
# Cada propiedad de la clase = una columna de la tabla.
#
# Ejemplo visual de lo que creará en la BD:
#
#  ┌────┬──────────┬───────────────────────┬───────────┬───────────┬─────────────────────┐
#  │ id │ username │         email         │ full_name │ is_active │     created_at      │
#  ├────┼──────────┼───────────────────────┼───────────┼───────────┼─────────────────────┤
#  │  1 │ maria99  │ maria@ejemplo.com     │ María Gil │   true    │ 2025-04-01 10:00:00 │
#  │  2 │ juandev  │ juan@ejemplo.com      │ Juan Ruiz │   true    │ 2025-04-01 11:30:00 │
#  └────┴──────────┴───────────────────────┴───────────┴───────────┴─────────────────────┘
# ============================================================

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func           # func.now() = fecha/hora actual del servidor
from app.database import Base             # La Base que definimos en database.py


class User(Base):
    """
    Tabla 'users' en PostgreSQL.
    Cada instancia de esta clase representa UNA fila de la tabla.
    """

    __tablename__ = "users"   # Nombre real de la tabla en la base de datos

    # ── Columnas ──────────────────────────────────────────────────
    id = Column(
        Integer,
        primary_key=True,   # Clave primaria: cada usuario tiene un ID único
        index=True,         # Índice para búsquedas más rápidas
        autoincrement=True, # PostgreSQL asigna el número automáticamente
    )

    username = Column(
        String(50),
        unique=True,        # No pueden haber dos usuarios con el mismo nombre
        index=True,
        nullable=False,     # Campo obligatorio (no puede estar vacío)
    )

    email = Column(
        String(255),
        unique=True,        # Cada email es único
        index=True,
        nullable=False,
    )

    full_name = Column(
        String(100),
        nullable=True,      # Campo opcional (puede estar vacío)
    )

    is_active = Column(
        Boolean,
        default=True,       # Por defecto, el usuario está activo al crearse
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # PostgreSQL pone la fecha/hora automáticamente
        nullable=False,
    )

    # Representación legible cuando imprimes un usuario en la consola
    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"
