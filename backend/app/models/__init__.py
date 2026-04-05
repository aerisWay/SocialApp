# Paquete 'models' — todas las tablas de la BD
from app.database import Base                                                    # noqa: F401
from app.models.user import User                                                 # noqa: F401
from app.models.caso_mayor_a_casa import CasoMayorACasa                          # noqa: F401
from app.models.comision_mayor_a_casa import ComisionMayorACasa                  # noqa: F401
from app.models.factura_mayor_a_casa import FacturaMayorACasa                    # noqa: F401
from app.models.seguimiento_mayor_a_casa import SeguimientoMayorACasa            # noqa: F401
from app.models.documentacion_mayor_a_casa import DocumentacionMayorACasa        # noqa: F401
from app.models.departamento import Departamento                                 # noqa: F401
