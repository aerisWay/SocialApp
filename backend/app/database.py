# ============================================================
# database.py — Conexión con PostgreSQL usando SQLAlchemy
# ============================================================
# SQLAlchemy es el "puente" entre Python y tu base de datos.
# En lugar de escribir SQL a mano, escribes clases Python (modelos)
# y SQLAlchemy traduce todo por ti.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# ---- Motor de base de datos ----
# create_engine crea la conexión real con PostgreSQL usando la URL del .env
engine = create_engine(
    settings.DATABASE_URL,
    # pool_pre_ping=True  ← reactiva conexiones caídas automáticamente
    # (lo activaremos cuando conectemos la BD real)
)

# ---- Fábrica de sesiones ----
# Cada petición HTTP abre una "sesión" (conversación temporal con la BD)
# y la cierra al terminar. SessionLocal crea esas sesiones.
SessionLocal = sessionmaker(
    autocommit=False,  # Los cambios NO se guardan automáticamente
    autoflush=False,   # No envía cambios a la BD hasta que lo pedimos
    bind=engine,       # Usa el motor que acabamos de crear
)

# ---- Base de modelos ----
# Todos tus modelos (tablas) heredarán de esta clase Base
Base = declarative_base()


# ---- Dependencia de sesión ----
# FastAPI llama a esta función en cada endpoint que la necesite.
# Garantiza que la sesión siempre se cierra, aunque haya un error.
def get_db():
    """
    Generador de sesiones de base de datos.
    Uso en un endpoint:
        from app.database import get_db
        from sqlalchemy.orm import Session
        from fastapi import Depends

        @router.get("/ejemplo")
        def mi_endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db          # Entrega la sesión al endpoint
    finally:
        db.close()        # Siempre cierra la sesión al terminar
