# ============================================================
# main.py — El corazón de tu aplicación FastAPI
# ============================================================

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import engine
from app import models as _models  # noqa: F401

from app.routers import users, mayor_a_casa, auth
from app.utils.auth import hash_password
from app.config import settings


@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("\U0001f680 Arrancando APBApp API...")

    try:
        # 1. Crea todas las tablas si no existen
        _models.Base.metadata.create_all(bind=engine)
        print("\u2705 Tablas verificadas/creadas en PostgreSQL")

        # 2. Migraciones manuales
        from sqlalchemy import text, inspect
        from app.database import SessionLocal
        _db = SessionLocal()
        try:
            inspector = inspect(engine)
            if "casos_mayor_a_casa" in inspector.get_table_names():
                cols = [c["name"] for c in inspector.get_columns("casos_mayor_a_casa")]

                # Migration: add sexo column
                if "sexo" not in cols:
                    _db.execute(text(
                        "ALTER TABLE casos_mayor_a_casa "
                        "ADD COLUMN IF NOT EXISTS sexo VARCHAR(10)"
                    ))
                    _db.commit()
                    print("\u2705 Columna 'sexo' añadida")

                # Migration: add rango_edad column
                if "rango_edad" not in cols:
                    _db.execute(text(
                        "ALTER TABLE casos_mayor_a_casa "
                        "ADD COLUMN IF NOT EXISTS rango_edad VARCHAR(15)"
                    ))
                    _db.commit()
                    print("\u2705 Columna 'rango_edad' añadida a casos_mayor_a_casa")

                # Migration: split dni_sip → dni + sip
                if "dni_sip" in cols and "dni" not in cols:
                    _db.execute(text(
                        "ALTER TABLE casos_mayor_a_casa "
                        "ADD COLUMN IF NOT EXISTS dni VARCHAR(9)"
                    ))
                    _db.execute(text(
                        "ALTER TABLE casos_mayor_a_casa "
                        "ADD COLUMN IF NOT EXISTS sip VARCHAR(8)"
                    ))
                    # Migrate existing data: DNI has letter at end, SIP is 8 digits
                    _db.execute(text("""
                        UPDATE casos_mayor_a_casa
                        SET dni = CASE WHEN dni_sip ~ '^[0-9]{8}[A-Za-z]$' THEN dni_sip ELSE NULL END,
                            sip = CASE WHEN dni_sip ~ '^[0-9]{8}$' THEN dni_sip ELSE NULL END
                        WHERE dni IS NULL AND sip IS NULL
                    """))
                    _db.execute(text(
                        "ALTER TABLE casos_mayor_a_casa DROP COLUMN IF EXISTS dni_sip"
                    ))
                    _db.commit()
                    print("\u2705 Migración dni_sip → dni + sip completada")
                elif "dni_sip" in cols and "dni" in cols:
                    # Column exists from model but old column still around
                    _db.execute(text(
                        "ALTER TABLE casos_mayor_a_casa DROP COLUMN IF EXISTS dni_sip"
                    ))
                    _db.commit()

                # Migration for Comisiones table: add mes_comision
                if "comisiones_mayor_a_casa" in inspector.get_table_names():
                    com_cols = [c["name"] for c in inspector.get_columns("comisiones_mayor_a_casa")]
                    if "mes_comision" not in com_cols:
                        _db.execute(text(
                            "ALTER TABLE comisiones_mayor_a_casa "
                            "ADD COLUMN IF NOT EXISTS mes_comision VARCHAR(7)"
                        ))
                        _db.commit()
                        print("\u2705 Columna 'mes_comision' añadida a comisiones_mayor_a_casa")

                print("\u2705 Migraciones verificadas")
        except Exception as e:
            _db.rollback()
            print(f"\u26a0\ufe0f  Migración omitida: {e}")
        finally:
            _db.close()

        # 3. Crea o actualiza el departamento de Promo
        from app.models.departamento import Departamento
        db = SessionLocal()
        try:
            dept = db.query(Departamento).filter_by(username="promocion").first()
            if not dept:
                db.add(Departamento(
                    nombre="Servicio de Promoción",
                    username="promocion",
                    hashed_password=hash_password(settings.DEPT_PROMOCION_PASSWORD),
                ))
                db.commit()
                print("\u2705 Departamento 'promocion' creado")
            else:
                dept.hashed_password = hash_password(settings.DEPT_PROMOCION_PASSWORD)
                db.commit()
                print("\u2705 Contraseña 'promocion' sincronizada")
        finally:
            db.close()

        # 4. Seed de datos de ejemplo (con campos dni/sip separados)
        from app.models.caso_mayor_a_casa import CasoMayorACasa
        from datetime import date as _date
        db2 = SessionLocal()
        try:
            count = db2.query(CasoMayorACasa).count()
            # Re-seed if table is empty or still has old schema data
            needs_seed = count == 0
            if not needs_seed:
                # Re-seed if rango_edad column exists but seed data has no values (old seed)
                has_seed_sip = db2.query(CasoMayorACasa).filter(CasoMayorACasa.sip == "10000001").count() > 0
                if has_seed_sip:
                    missing_edad = db2.query(CasoMayorACasa).filter(
                        CasoMayorACasa.sip == "10000001",
                        CasoMayorACasa.rango_edad == None  # noqa: E711
                    ).count() > 0
                    needs_seed = missing_edad

            if needs_seed:
                db2.query(CasoMayorACasa).delete()
                _m65 = 'mayor_65'
                _e65 = '60_65'
                _m60 = 'menor_60'
                _SEED = [
                    dict(apellidos="Abad Molina",       nombre="Josefa",       dni="12345678A", sip="10000001", zona=1, sexo="mujer",     rango_edad=_m65, telefono="966 801 234", direccion="C/ Tomàs Ortuño, 12, 2ºA",        mes_renovacion="2026-03", fecha_alta=_date(2024,1,10),  activo=True),
                    dict(apellidos="Álvarez Campos",    nombre="Manuel",       dni="23456789B", sip="10000002", zona=1, sexo="hombre",    rango_edad=_m65, telefono="966 802 345", direccion="Avda. del Mediterráneo, 34, 1ºB", mes_renovacion="2026-05", fecha_alta=_date(2023,6,15),  activo=True),
                    dict(apellidos="Blanco Navarro",    nombre="Amparo",       dni="34567890C", sip="10000003", zona=1, sexo="mujer",     rango_edad=_m65, telefono="966 803 456", direccion="C/ Gambo, 8, bajo",               mes_renovacion="2026-07", fecha_alta=_date(2024,3,20),  activo=True),
                    dict(apellidos="Cabrera Soler",     nombre="Francisco",    dni="45678901D", sip="10000004", zona=1, sexo="hombre",    rango_edad=_m65, telefono="966 804 567", direccion="C/ La Mar, 4, 3ºA",              mes_renovacion="2026-04", fecha_alta=_date(2022,11,5),  activo=True),
                    dict(apellidos="Domènech Ramos",    nombre="Pilar",        dni="56789012E", sip="10000005", zona=1, sexo="mujer",     rango_edad=_e65, telefono=None,          direccion="C/ Esperança, 7, 1ºC",            mes_renovacion="2026-06", fecha_alta=_date(2023,9,12),  activo=True),
                    dict(apellidos="Esteban Torres",    nombre="Enrique",      dni="67890123F", sip="10000006", zona=1, sexo="hombre",    rango_edad=_m65, telefono="966 805 678", direccion="Avda. de l'Aigüera, 3, 2ºD",     mes_renovacion="2026-08", fecha_alta=_date(2024,2,28),  activo=True),
                    dict(apellidos="Ferrer Llopis",     nombre="Carmen",       dni="78901234G", sip="10000007", zona=1, sexo="mujer",     rango_edad=_m65, telefono="966 806 789", direccion="C/ Ausiàs March, 11, 4ºB",       mes_renovacion="2026-03", fecha_alta=_date(2022,7,18),  activo=False),
                    dict(apellidos="Gómez Ibáñez",      nombre="Salvador",     dni="89012345H", sip="10000008", zona=1, sexo="hombre",    rango_edad=_m65, telefono="966 807 890", direccion="C/ Mayor, 18, bajo B",            mes_renovacion="2026-09", fecha_alta=_date(2023,4,1),   activo=True),
                    dict(apellidos="Herrero Prats",     nombre="Inmaculada",   dni="90123456J", sip="10000009", zona=1, sexo="mujer",     rango_edad=_m65, telefono="966 808 901", direccion="C/ Martínez Alejos, 5, 2ºA",     mes_renovacion="2026-05", fecha_alta=_date(2024,1,22),  activo=True),
                    dict(apellidos="Iglesias Vidal",    nombre="Rogelio",      dni="01234567K", sip="10000010", zona=1, sexo="hombre",    rango_edad=_e65, telefono=None,          direccion="C/ Sant Vicent, 22, 1ºB",         mes_renovacion="2026-07", fecha_alta=_date(2022,12,10), activo=True),
                    dict(apellidos="Jiménez Colomer",   nombre="Rosa",         dni="11223344L", sip="10000011", zona=1, sexo="mujer",     rango_edad=_m65, telefono="966 809 012", direccion="C/ Tomàs Ortuño, 31, 3ºC",       mes_renovacion="2026-04", fecha_alta=_date(2023,8,7),   activo=True),
                    dict(apellidos="León Asensio",      nombre="Valentina",    dni="22334455M", sip="10000012", zona=1, sexo="mujer",     rango_edad=_m65, telefono="966 810 123", direccion="Avda. del Mediterráneo, 67, 5ºA", mes_renovacion="2026-10", fecha_alta=_date(2021,5,14),  activo=True),
                    dict(apellidos="Marín Díaz",        nombre="Consuelo",     dni="33445566N", sip="10000013", zona=2, sexo="no_define", rango_edad=_m60, telefono="966 811 234", direccion="C/ Ibiza, 6, 2ºD",               mes_renovacion="2026-08", fecha_alta=_date(2022,5,30),  activo=False),
                    dict(apellidos="Martínez Blasco",   nombre="Rafael",       dni="44556677P", sip="10000014", zona=2, sexo="hombre",    rango_edad=_m65, telefono="966 812 345", direccion="Avda. de Mallorca, 23, 1ºA",     mes_renovacion="2026-03", fecha_alta=_date(2023,10,20), activo=True),
                    dict(apellidos="Navarro Ortega",    nombre="Asunción",     dni="55667788Q", sip="10000015", zona=2, sexo="mujer",     rango_edad=_m65, telefono="966 813 456", direccion="C/ Menorca, 14, bajo A",          mes_renovacion="2026-05", fecha_alta=_date(2024,6,1),   activo=True),
                    dict(apellidos="Oliva Herrera",     nombre="Agustín",      dni="66778899R", sip="10000016", zona=2, sexo="hombre",    rango_edad=_m65, telefono=None,          direccion="C/ Almeria, 9, 3ºB",              mes_renovacion="2026-07", fecha_alta=_date(2023,2,14),  activo=True),
                    dict(apellidos="Palomar Ruiz",      nombre="Encarnación",  dni="77889900S", sip="10000017", zona=2, sexo="mujer",     rango_edad=_m65, telefono="966 814 567", direccion="C/ Lepanto, 17, 2ºC",             mes_renovacion="2026-09", fecha_alta=_date(2022,9,25),  activo=True),
                    dict(apellidos="Ramos Sánchez",     nombre="Joaquín",      dni="88990011T", sip="10000018", zona=2, sexo="hombre",    rango_edad=_e65, telefono="966 815 678", direccion="C/ Formentera, 4, 1ºA",           mes_renovacion="2026-04", fecha_alta=_date(2024,1,8),   activo=False),
                    dict(apellidos="Reyes Gómez",       nombre="Teresa",       dni="99001122V", sip="10000019", zona=2, sexo="mujer",     rango_edad=_m65, telefono="966 816 789", direccion="C/ Canarias, 20, 4ºD",            mes_renovacion="2026-06", fecha_alta=_date(2023,7,17),  activo=True),
                    dict(apellidos="Rico Ferrer",       nombre="Bernardo",     dni="10112233W", sip="10000020", zona=2, sexo="hombre",    rango_edad=_m65, telefono="966 817 890", direccion="Avda. de Europa, 38, 3ºA",        mes_renovacion="2026-08", fecha_alta=_date(2022,3,11),  activo=True),
                    dict(apellidos="Romero Bernal",     nombre="Gloria",       dni="21223344X", sip="10000021", zona=2, sexo="mujer",     rango_edad=_m65, telefono="966 818 901", direccion="C/ del Rincón de Loix, 12, 2ºB",  mes_renovacion="2026-10", fecha_alta=_date(2021,8,22),  activo=True),
                    dict(apellidos="Ruiz Pons",         nombre="Pedro",        dni="32334455Y", sip="10000022", zona=2, sexo="hombre",    rango_edad=_m65, telefono=None,          direccion="C/ Martínez Alejos, 28, bajo",    mes_renovacion="2026-11", fecha_alta=_date(2020,11,3),  activo=True),
                    dict(apellidos="Sánchez Llobet",    nombre="Dolores",      dni="43445566Z", sip="10000023", zona=2, sexo="mujer",     rango_edad=_m65, telefono="966 819 012", direccion="C/ Ibiza, 15, 1ºC",              mes_renovacion="2026-03", fecha_alta=_date(2024,4,25),  activo=True),
                    dict(apellidos="Segura Colomer",    nombre="Eduardo",      dni="54556677A", sip="10000024", zona=2, sexo="no_define", rango_edad=_m60, telefono="966 820 123", direccion="Avda. de Mallorca, 40, 5ºB",     mes_renovacion="2026-05", fecha_alta=_date(2023,1,30),  activo=True),
                    dict(apellidos="Serra Campos",      nombre="Francisca",    dni="65667788B", sip="10000025", zona=3, sexo="mujer",     rango_edad=_m65, telefono="966 821 234", direccion="C/ Menorca, 3, 2ºA",             mes_renovacion="2026-07", fecha_alta=_date(2024,5,8),   activo=True),
                    dict(apellidos="Soler Castillo",    nombre="Ignacio",      dni="76778899C", sip="10000026", zona=3, sexo="hombre",    rango_edad=_m65, telefono="966 822 345", direccion="C/ Gambo, 21, 1ºD",              mes_renovacion="2026-09", fecha_alta=_date(2022,8,19),  activo=True),
                    dict(apellidos="Torres Morales",    nombre="Montserrat",   dni="87889900D", sip="10000027", zona=3, sexo="mujer",     rango_edad=_m65, telefono="966 823 456", direccion="C/ Almeria, 14, 3ºC",            mes_renovacion="2026-04", fecha_alta=_date(2023,3,5),   activo=True),
                    dict(apellidos="Úbeda Reyes",       nombre="Juan",         dni="98990011E", sip="10000028", zona=3, sexo="hombre",    rango_edad=_e65, telefono=None,          direccion="Avda. del Mediterráneo, 89, 2ºB", mes_renovacion="2026-06", fecha_alta=_date(2024,7,14),  activo=True),
                    dict(apellidos="Vidal González",    nombre="Natividad",    dni="09001122F", sip="10000029", zona=3, sexo="mujer",     rango_edad=_m65, telefono="966 824 567", direccion="C/ Lepanto, 6, bajo A",           mes_renovacion="2026-08", fecha_alta=_date(2022,6,27),  activo=False),
                    dict(apellidos="Villanueva Mora",   nombre="Carlos",       dni="10112233G", sip="10000030", zona=3, sexo="hombre",    rango_edad=_m65, telefono="966 825 678", direccion="C/ Esperança, 18, 4ºA",           mes_renovacion="2026-10", fecha_alta=_date(2021,2,8),   activo=True),
                    dict(apellidos="Zaragoza Gil",      nombre="Nieves",       dni="21223344H", sip="10000031", zona=3, sexo="mujer",     rango_edad=_m65, telefono="966 826 789", direccion="C/ Ausiàs March, 25, 1ºA",       mes_renovacion="2026-11", fecha_alta=_date(2020,9,15),  activo=True),
                    dict(apellidos="Aguilar López",     nombre="Miguel",       dni="32334455J", sip="10000032", zona=3, sexo="hombre",    rango_edad=_m65, telefono="966 827 890", direccion="C/ La Mar, 11, 3ºB",             mes_renovacion="2026-12", fecha_alta=_date(2020,4,20),  activo=True),
                    dict(apellidos="Alba Moreno",       nombre="Remedios",     dni="43445566K", sip="10000033", zona=3, sexo="mujer",     rango_edad=_m65, telefono=None,          direccion="C/ Sant Vicent, 34, 2ºC",         mes_renovacion="2026-03", fecha_alta=_date(2024,8,11),  activo=True),
                    dict(apellidos="Alonso Villena",    nombre="Luis",         dni="54556677L", sip="10000034", zona=3, sexo="hombre",    rango_edad=_m60, telefono="966 828 901", direccion="Avda. de l'Aigüera, 16, 5ºD",    mes_renovacion="2026-05", fecha_alta=_date(2023,5,23),  activo=True),
                    dict(apellidos="Ángel Gutiérrez",   nombre="Socorro",      dni="65667788M", sip="10000035", zona=3, sexo="mujer",     rango_edad=_m65, telefono="966 829 012", direccion="C/ Mayor, 7, 1ºA",               mes_renovacion="2026-07", fecha_alta=_date(2022,10,4),  activo=False),
                    dict(apellidos="Arcos Roca",        nombre="Santiago",     dni="76778899N", sip="10000036", zona=3, sexo="hombre",    rango_edad=_m65, telefono="966 830 123", direccion="C/ del Rincón de Loix, 27, bajo B", mes_renovacion="2026-09", fecha_alta=_date(2021,12,17), activo=True),
                    dict(apellidos="Arroyo Serrano",    nombre="Isabel",       dni="87889900P", sip="10000037", zona=4, sexo="mujer",     rango_edad=_e65, telefono="966 831 234", direccion="C/ Formentera, 9, 2ºA",           mes_renovacion="2026-04", fecha_alta=_date(2024,9,30),  activo=True),
                    dict(apellidos="Aznar Mínguez",     nombre="Ramón",        dni="98990011Q", sip="10000038", zona=4, sexo="hombre",    rango_edad=_m65, telefono="966 832 345", direccion="C/ Canarias, 8, 3ºB",             mes_renovacion="2026-06", fecha_alta=_date(2023,11,7),  activo=True),
                    dict(apellidos="Bravo Hidalgo",     nombre="Luisa",        dni="09001122R", sip="10000039", zona=4, sexo="mujer",     rango_edad=_m65, telefono=None,          direccion="Avda. de Europa, 55, 1ºC",        mes_renovacion="2026-08", fecha_alta=_date(2022,4,16),  activo=True),
                    dict(apellidos="Bueno Climent",     nombre="Pascual",      dni="10112233S", sip="10000040", zona=4, sexo="hombre",    rango_edad=_m65, telefono="966 833 456", direccion="Avda. de Mallorca, 12, 4ºA",     mes_renovacion="2026-10", fecha_alta=_date(2021,7,29),  activo=True),
                    dict(apellidos="Caballero Flores",  nombre="María",        dni="21223344T", sip="10000041", zona=4, sexo="mujer",     rango_edad=_m65, telefono="966 834 567", direccion="C/ Gambo, 16, bajo C",            mes_renovacion="2026-11", fecha_alta=_date(2020,6,3),   activo=False),
                    dict(apellidos="Calvo Pastor",      nombre="Marcelino",    dni="32334455V", sip="10000042", zona=4, sexo="hombre",    rango_edad=_m65, telefono="966 835 678", direccion="C/ Ibiza, 11, 2ºD",              mes_renovacion="2026-12", fecha_alta=_date(2020,1,18),  activo=True),
                    dict(apellidos="Campos Expósito",   nombre="Milagros",     dni="43445566W", sip="10000043", zona=4, sexo="mujer",     rango_edad=_e65, telefono="966 836 789", direccion="C/ Menorca, 20, 3ºA",            mes_renovacion="2026-03", fecha_alta=_date(2024,10,22), activo=True),
                    dict(apellidos="Cano Guerrero",     nombre="Alfonso",      dni="54556677X", sip="10000044", zona=4, sexo="hombre",    rango_edad=_m65, telefono=None,          direccion="C/ Lepanto, 3, 1ºB",              mes_renovacion="2026-05", fecha_alta=_date(2023,12,9),  activo=True),
                    dict(apellidos="Castellano Castro", nombre="Petra",        dni="65667788Y", sip="10000045", zona=4, sexo="no_define", rango_edad=_m65, telefono="966 837 890", direccion="C/ Ausiàs March, 38, 5ºC",       mes_renovacion="2026-07", fecha_alta=_date(2022,2,25),  activo=True),
                    dict(apellidos="Castro Díaz",       nombre="Emilio",       dni="76778899Z", sip="10000046", zona=4, sexo="hombre",    rango_edad=_m65, telefono="966 838 901", direccion="C/ Tomàs Ortuño, 47, 2ºB",       mes_renovacion="2026-09", fecha_alta=_date(2021,10,6),  activo=True),
                    dict(apellidos="Climent Font",      nombre="Serafina",     dni="87889900A", sip="10000047", zona=4, sexo="mujer",     rango_edad=_m65, telefono="966 839 012", direccion="Avda. del Mediterráneo, 22, 4ºD", mes_renovacion="2026-11", fecha_alta=_date(2020,8,13),  activo=False),
                    dict(apellidos="Coll Rivas",        nombre="Sergio",       dni="98990011B", sip="10000048", zona=4, sexo="hombre",    rango_edad=_e65, telefono="966 840 123", direccion="C/ La Mar, 18, 1ºA",             mes_renovacion="2026-12", fecha_alta=_date(2020,3,27),  activo=True),
                    dict(apellidos="Díaz Alvarado",     nombre="Trinidad",     dni="09001122C", sip="10000049", zona=4, sexo="no_define", rango_edad=_m65, telefono="966 841 234", direccion="Avda. de l'Aigüera, 9, 3ºC",     mes_renovacion="2026-02", fecha_alta=_date(2024,11,15), activo=True),
                    dict(apellidos="Expósito Arroyo",   nombre="Alberto",      dni="10112233D", sip="10000050", zona=4, sexo="hombre",    rango_edad=_m60, telefono=None,          direccion="C/ Sant Vicent, 5, 2ºA",          mes_renovacion="2026-04", fecha_alta=_date(2023,4,21),  activo=True),
                ]
                for row in _SEED:
                    db2.add(CasoMayorACasa(**row))
                db2.commit()
                print(f"\u2705 {len(_SEED)} casos de ejemplo insertados (dni/sip separados)")
            else:
                print("\u2139\ufe0f  Datos ya existen, seed omitido")
        finally:
            db2.close()

        # 5. Seed de Comisiones
        from app.models.comision_mayor_a_casa import ComisionMayorACasa
        db3 = SessionLocal()
        try:
            if db3.query(ComisionMayorACasa).count() == 0:
                _mes = _date.today().strftime("%Y-%m")
                _SEED_COM = [
                    dict(apellidos="Pérez Gómez",    nombre="Antonia",  dni="11111111A", sip="20000001", zona=1, sexo="mujer",  rango_edad="mayor_65", estado="en_tramite", mes_comision=_mes, fecha_alta=_date.today()),
                    dict(apellidos="García Ruiz",    nombre="Manuel",   dni="22222222B", sip="20000002", zona=2, sexo="hombre", rango_edad="60_65",    estado="en_tramite", mes_comision=_mes, fecha_alta=_date.today()),
                    dict(apellidos="López Sanz",     nombre="Carmen",   dni="33333333C", sip="20000003", zona=1, sexo="mujer",  rango_edad="mayor_65", estado="denegado",   mes_comision=_mes, fecha_alta=_date.today()),
                    dict(apellidos="Sánchez Mas",    nombre="Vicente",  dni="44444444D", sip="20000004", zona=3, sexo="hombre", rango_edad="menor_60", estado="en_tramite", mes_comision=_mes, fecha_alta=_date.today()),
                    dict(apellidos="Marti Bel",      nombre="Rosa",     dni="55555555E", sip="20000005", zona=4, sexo="mujer",  rango_edad="mayor_65", estado="en_tramite", mes_comision=_mes, fecha_alta=_date.today()),
                    dict(apellidos="Torres Vila",    nombre="Josep",    dni="66666666F", sip="20000006", zona=2, sexo="hombre", rango_edad="60_65",    estado="en_tramite", mes_comision=_mes, fecha_alta=_date.today()),
                    dict(apellidos="Molina Cap",     nombre="Anna",     dni="77777777G", sip="20000007", zona=1, sexo="mujer",  rango_edad="mayor_65", estado="aprobado",   mes_comision=_mes, fecha_alta=_date.today()),
                    dict(apellidos="Vila Seco",      nombre="Pere",     dni="88888888H", sip="20000008", zona=3, sexo="hombre", rango_edad="mayor_65", estado="en_tramite", mes_comision=_mes, fecha_alta=_date.today()),
                    dict(apellidos="Roca Font",      nombre="Teresa",   dni="99999999J", sip="20000009", zona=4, sexo="mujer",  rango_edad="60_65",    estado="en_tramite", mes_comision=_mes, fecha_alta=_date.today()),
                    dict(apellidos="Soler Pau",      nombre="Joan",     dni="00000000K", sip="20000010", zona=2, sexo="hombre", rango_edad="menor_60", estado="en_tramite", mes_comision=_mes, fecha_alta=_date.today()),
                    dict(apellidos="Beltran Rus",    nombre="Eva",      dni="12121212A", sip="20000011", zona=1, sexo="mujer",  rango_edad="mayor_65", estado="aprobado",  mes_comision="2026-03", fecha_alta=_date(2026,3,5)),
                    dict(apellidos="Castillo Mar",   nombre="Felipe",   dni="23232323B", sip="20000012", zona=2, sexo="hombre", rango_edad="60_65",    estado="denegado",  mes_comision="2026-03", fecha_alta=_date(2026,3,10)),
                    dict(apellidos="Duarte Sol",     nombre="Sonia",    dni="34343434C", sip="20000013", zona=3, sexo="mujer",  rango_edad="menor_60", estado="aprobado",  mes_comision="2026-03", fecha_alta=_date(2026,3,15)),
                    dict(apellidos="Esteve Pla",     nombre="Ramon",    dni="45454545D", sip="20000014", zona=4, sexo="hombre", rango_edad="mayor_65", estado="aprobado",  mes_comision="2026-03", fecha_alta=_date(2026,3,20)),
                    dict(apellidos="Fabra Pou",      nombre="Isabel",   dni="56565656E", sip="20000015", zona=1, sexo="mujer",  rango_edad="60_65",    estado="denegado",  mes_comision="2026-03", fecha_alta=_date(2026,3,25)),
                    dict(apellidos="Gallego Ros",    nombre="Luis",     dni="67676767F", sip="20000016", zona=2, sexo="hombre", rango_edad="mayor_65", estado="aprobado",  mes_comision="2026-02", fecha_alta=_date(2026,2,5)),
                    dict(apellidos="Hidalgo Luz",    nombre="Elena",    dni="78787878G", sip="20000017", zona=3, sexo="mujer",  rango_edad="menor_60", estado="denegado",  mes_comision="2026-02", fecha_alta=_date(2026,2,12)),
                    dict(apellidos="Iborra Marí",    nombre="Marc",     dni="89898989H", sip="20000018", zona=4, sexo="hombre", rango_edad="mayor_65", estado="aprobado",  mes_comision="2026-02", fecha_alta=_date(2026,2,18)),
                    dict(apellidos="Jover Soro",     nombre="Julia",    dni="90909090J", sip="20000019", zona=1, sexo="mujer",  rango_edad="60_65",    estado="aprobado",  mes_comision="2026-02", fecha_alta=_date(2026,2,22)),
                    dict(apellidos="Lacasa Mir",     nombre="Andreu",   dni="01010101K", sip="20000020", zona=2, sexo="hombre", rango_edad="mayor_65", estado="denegado",  mes_comision="2026-02", fecha_alta=_date(2026,2,26)),

                ]
                for row in _SEED_COM:
                    db3.add(ComisionMayorACasa(**row))
                db3.commit()
                print(f"\u2705 {len(_SEED_COM)} comisiones de ejemplo insertadas")
        finally:
            db3.close()

    except Exception as startup_err:
        import traceback
        print(f"\u274c ERROR EN ARRANQUE: {startup_err}")
        traceback.print_exc()

    yield
    print("\U0001f6d1 Apagando APBApp API...")


app = FastAPI(
    title="APBApp API",
    description="Backend de APBApp — gestión de servicios sociales",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,         prefix="/auth",        tags=["Autenticación"])
app.include_router(users.router,        prefix="/users",       tags=["Usuarios"])
app.include_router(mayor_a_casa.router, prefix="/mayor-a-casa", tags=["Major a Casa"])

app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")


@app.get("/health", tags=["Sistema"])
async def health_check():
    return {"status": "ok", "version": "0.1.0"}


@app.get("/", include_in_schema=False)
async def serve_frontend():
    return FileResponse(Path(__file__).parent / "static" / "index.html")
