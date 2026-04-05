import random
import sys
import os

# Añadimos el directorio actual al path para poder importar 'app'
sys.path.append(os.getcwd())

from app.database import SessionLocal
from app.models.caso_mayor_a_casa import CasoMayorACasa
from app.models.comision_mayor_a_casa import ComisionMayorACasa

def randomize():
    db = SessionLocal()
    try:
        casos = db.query(CasoMayorACasa).all()
        comisiones = db.query(ComisionMayorACasa).all()
        
        all_items = casos + comisiones
        print(f"Aleatorizando {len(all_items)} registros...")
        
        # Probabilidades: 70% >65, 20% 60-65, 10% <60
        opciones = ['mayor_65'] * 70 + ['60_65'] * 20 + ['menor_60'] * 10
        
        for item in all_items:
            item.rango_edad = random.choice(opciones)
            
        db.commit()
        print("¡Hecho!")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    randomize()
