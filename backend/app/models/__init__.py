# Paquete 'models' — clases que representan tablas de la BD
from app.database import Base          # noqa: F401
from app.models.user import User                        # noqa: F401  ← tabla 'users'
from app.models.caso_mayor_a_casa import CasoMayorACasa # noqa: F401  ← tabla 'casos_mayor_a_casa'
