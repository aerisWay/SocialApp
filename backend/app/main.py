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
    print("\U0001f680 Arrancando SocialApp API...")

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
                    nombre="Servicio de Promoci\u00f3n",
                    username="promocion",
                    hashed_password=hash_password(settings.DEPT_PROMOCION_PASSWORD),
                ))
                db.commit()
                print("\u2705 Departamento 'promocion' creado")
            else:
                dept.hashed_password = hash_password(settings.DEPT_PROMOCION_PASSWORD)
                db.commit()
                print("\u2705 Contrase\u00f1a 'promocion' sincronizada")
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
                # Check if any record has both dni and sip as None (bad migration)
                has_new_data = db2.query(CasoMayorACasa).filter(
                    (CasoMayorACasa.dni != None) | (CasoMayorACasa.sip != None)
                ).count() > 0
                needs_seed = not has_new_data

            if needs_seed:
                db2.query(CasoMayorACasa).delete()
                _SEED = [
                    dict(apellidos="Abad Molina",       nombre="Josefa",       dni=None,        sip="47823641", zona=1, sexo="mujer",    telefono="966 801 234", direccion="C/ Tom\u00e0s Ortu\u00f1o, 12, 2\u00baA",       mes_renovacion="2026-03", fecha_alta=_date(2024,1,10),  activo=True),
                    dict(apellidos="\u00c1lvarez Campos",nombre="Manuel",      dni="12847365X",  sip=None,      zona=1, sexo="hombre",   telefono="966 802 345", direccion="Avda. del Mediterr\u00e1neo, 34, 1\u00baB",    mes_renovacion="2026-05", fecha_alta=_date(2023,6,15),  activo=True),
                    dict(apellidos="Blanco Navarro",    nombre="Amparo",       dni=None,         sip="93521847", zona=1, sexo="mujer",    telefono="966 803 456", direccion="C/ Gambo, 8, bajo",                            mes_renovacion="2026-07", fecha_alta=_date(2024,3,20),  activo=True),
                    dict(apellidos="Cabrera Soler",     nombre="Francisco",    dni="35621890M",  sip="11223344", zona=1, sexo="hombre",   telefono="966 804 567", direccion="C/ La Mar, 4, 3\u00baA",                       mes_renovacion="2026-04", fecha_alta=_date(2022,11,5),  activo=True),
                    dict(apellidos="Dom\u00e8nech Ramos",nombre="Pilar",       dni=None,         sip="71934205", zona=1, sexo="mujer",    telefono=None,          direccion="C/ Esperan\u00e7a, 7, 1\u00baC",               mes_renovacion="2026-06", fecha_alta=_date(2023,9,12),  activo=True),
                    dict(apellidos="Esteban Torres",    nombre="Enrique",      dni="48203967Y",  sip=None,      zona=1, sexo="hombre",   telefono="966 805 678", direccion="Avda. de l'Aig\u00fcera, 3, 2\u00baD",          mes_renovacion="2026-08", fecha_alta=_date(2024,2,28),  activo=True),
                    dict(apellidos="Ferrer Llopis",     nombre="Carmen",       dni=None,         sip="62891034", zona=1, sexo="mujer",    telefono="966 806 789", direccion="C/ Ausi\u00e0s March, 11, 4\u00baB",            mes_renovacion="2026-03", fecha_alta=_date(2022,7,18),  activo=False),
                    dict(apellidos="G\u00f3mez Ib\u00e1\u00f1ez",nombre="Salvador",dni="29047183R",sip="22334455",zona=1,sexo="hombre", telefono="966 807 890", direccion="C/ Mayor, 18, bajo B",                          mes_renovacion="2026-09", fecha_alta=_date(2023,4,1),   activo=True),
                    dict(apellidos="Herrero Prats",     nombre="Inmaculada",   dni=None,         sip="84615029", zona=1, sexo="mujer",    telefono="966 808 901", direccion="C/ Mart\u00ednez Alejos, 5, 2\u00baA",          mes_renovacion="2026-05", fecha_alta=_date(2024,1,22),  activo=True),
                    dict(apellidos="Iglesias Vidal",    nombre="Rogelio",      dni="53702948J",  sip=None,      zona=1, sexo="hombre",   telefono=None,          direccion="C/ Sant Vicent, 22, 1\u00baB",                  mes_renovacion="2026-07", fecha_alta=_date(2022,12,10), activo=True),
                    dict(apellidos="Jim\u00e9nez Colomer",nombre="Rosa",       dni=None,         sip="67840315", zona=1, sexo="mujer",    telefono="966 809 012", direccion="C/ Tom\u00e0s Ortu\u00f1o, 31, 3\u00baC",       mes_renovacion="2026-04", fecha_alta=_date(2023,8,7),   activo=True),
                    dict(apellidos="Le\u00f3n Asensio", nombre="Valentina",    dni=None,         sip="19563047", zona=1, sexo="mujer",    telefono="966 810 123", direccion="Avda. del Mediterr\u00e1neo, 67, 5\u00baA",    mes_renovacion="2026-10", fecha_alta=_date(2021,5,14),  activo=True),
                    dict(apellidos="Mar\u00edn D\u00edaz",nombre="Consuelo",   dni=None,         sip="80427631", zona=2, sexo="no_define",telefono="966 811 234", direccion="C/ Ibiza, 6, 2\u00baD",                         mes_renovacion="2026-08", fecha_alta=_date(2022,5,30),  activo=False),
                    dict(apellidos="Mart\u00ednez Blasco",nombre="Rafael",     dni="46083925T",  sip="33445566", zona=2, sexo="hombre",   telefono="966 812 345", direccion="Avda. de Mallorca, 23, 1\u00baA",               mes_renovacion="2026-03", fecha_alta=_date(2023,10,20), activo=True),
                    dict(apellidos="Navarro Ortega",    nombre="Asunci\u00f3n",dni=None,         sip="73195460", zona=2, sexo="mujer",    telefono="966 813 456", direccion="C/ Menorca, 14, bajo A",                        mes_renovacion="2026-05", fecha_alta=_date(2024,6,1),   activo=True),
                    dict(apellidos="Oliva Herrera",     nombre="Agust\u00edn", dni="31507284W",  sip=None,      zona=2, sexo="hombre",   telefono=None,          direccion="C/ Almeria, 9, 3\u00baB",                       mes_renovacion="2026-07", fecha_alta=_date(2023,2,14),  activo=True),
                    dict(apellidos="Palomar Ruiz",      nombre="Encarnaci\u00f3n",dni=None,      sip="94618352", zona=2, sexo="mujer",    telefono="966 814 567", direccion="C/ Lepanto, 17, 2\u00baC",                      mes_renovacion="2026-09", fecha_alta=_date(2022,9,25),  activo=True),
                    dict(apellidos="Ramos S\u00e1nchez",nombre="Joaqu\u00edn", dni="57829043Z",  sip="44556677", zona=2, sexo="hombre",   telefono="966 815 678", direccion="C/ Formentera, 4, 1\u00baA",                    mes_renovacion="2026-04", fecha_alta=_date(2024,1,8),   activo=False),
                    dict(apellidos="Reyes G\u00f3mez",  nombre="Teresa",       dni=None,         sip="20734891", zona=2, sexo="mujer",    telefono="966 816 789", direccion="C/ Canarias, 20, 4\u00baD",                     mes_renovacion="2026-06", fecha_alta=_date(2023,7,17),  activo=True),
                    dict(apellidos="Rico Ferrer",       nombre="Bernardo",     dni=None,         sip="68305274", zona=2, sexo="hombre",   telefono="966 817 890", direccion="Avda. de Europa, 38, 3\u00baA",                 mes_renovacion="2026-08", fecha_alta=_date(2022,3,11),  activo=True),
                    dict(apellidos="Romero Bernal",     nombre="Gloria",       dni="42907163H",  sip=None,      zona=2, sexo="mujer",    telefono="966 818 901", direccion="C/ del Rinc\u00f3n de Loix, 12, 2\u00baB",     mes_renovacion="2026-10", fecha_alta=_date(2021,8,22),  activo=True),
                    dict(apellidos="Ruiz Pons",         nombre="Pedro",        dni=None,         sip="85023746", zona=2, sexo="hombre",   telefono=None,          direccion="C/ Mart\u00ednez Alejos, 28, bajo",             mes_renovacion="2026-11", fecha_alta=_date(2020,11,3),  activo=True),
                    dict(apellidos="S\u00e1nchez Llobet",nombre="Dolores",     dni=None,         sip="13678059", zona=2, sexo="mujer",    telefono="966 819 012", direccion="C/ Ibiza, 15, 1\u00baC",                        mes_renovacion="2026-03", fecha_alta=_date(2024,4,25),  activo=True),
                    dict(apellidos="Segura Colomer",    nombre="Eduardo",      dni="76041382A",  sip="55667788", zona=2, sexo="no_define",telefono="966 820 123", direccion="Avda. de Mallorca, 40, 5\u00baB",               mes_renovacion="2026-05", fecha_alta=_date(2023,1,30),  activo=True),
                    dict(apellidos="Serra Campos",      nombre="Francisca",    dni=None,         sip="39182607", zona=3, sexo="mujer",    telefono="966 821 234", direccion="C/ Menorca, 3, 2\u00baA",                       mes_renovacion="2026-07", fecha_alta=_date(2024,5,8),   activo=True),
                    dict(apellidos="Soler Castillo",    nombre="Ignacio",      dni="60497325B",  sip=None,      zona=3, sexo="hombre",   telefono="966 822 345", direccion="C/ Gambo, 21, 1\u00baD",                        mes_renovacion="2026-09", fecha_alta=_date(2022,8,19),  activo=True),
                    dict(apellidos="Torres Morales",    nombre="Montserrat",   dni=None,         sip="82614093", zona=3, sexo="mujer",    telefono="966 823 456", direccion="C/ Almeria, 14, 3\u00baC",                      mes_renovacion="2026-04", fecha_alta=_date(2023,3,5),   activo=True),
                    dict(apellidos="\u00dabeda Reyes",  nombre="Juan",         dni="25803741N",  sip="66778899", zona=3, sexo="hombre",   telefono=None,          direccion="Avda. del Mediterr\u00e1neo, 89, 2\u00baB",    mes_renovacion="2026-06", fecha_alta=_date(2024,7,14),  activo=True),
                    dict(apellidos="Vidal Gonz\u00e1lez",nombre="Natividad",  dni=None,         sip="47916230", zona=3, sexo="mujer",    telefono="966 824 567", direccion="C/ Lepanto, 6, bajo A",                         mes_renovacion="2026-08", fecha_alta=_date(2022,6,27),  activo=False),
                    dict(apellidos="Villanueva Mora",   nombre="Carlos",       dni="93047185P",  sip=None,      zona=3, sexo="hombre",   telefono="966 825 678", direccion="C/ Esperan\u00e7a, 18, 4\u00baA",              mes_renovacion="2026-10", fecha_alta=_date(2021,2,8),   activo=True),
                    dict(apellidos="Zaragoza Gil",      nombre="Nieves",       dni=None,         sip="61308429", zona=3, sexo="mujer",    telefono="966 826 789", direccion="C/ Ausi\u00e0s March, 25, 1\u00baA",            mes_renovacion="2026-11", fecha_alta=_date(2020,9,15),  activo=True),
                    dict(apellidos="Aguilar L\u00f3pez",nombre="Miguel",       dni="54872013C",  sip="77889900", zona=3, sexo="hombre",   telefono="966 827 890", direccion="C/ La Mar, 11, 3\u00baB",                       mes_renovacion="2026-12", fecha_alta=_date(2020,4,20),  activo=True),
                    dict(apellidos="Alba Moreno",       nombre="Remedios",     dni=None,         sip="28165094", zona=3, sexo="mujer",    telefono=None,          direccion="C/ Sant Vicent, 34, 2\u00baC",                  mes_renovacion="2026-03", fecha_alta=_date(2024,8,11),  activo=True),
                    dict(apellidos="Alonso Villena",    nombre="Luis",         dni="70429638D",  sip=None,      zona=3, sexo="hombre",   telefono="966 828 901", direccion="Avda. de l'Aig\u00fcera, 16, 5\u00baD",         mes_renovacion="2026-05", fecha_alta=_date(2023,5,23),  activo=True),
                    dict(apellidos="\u00c1ngel Guti\u00e9rrez",nombre="Socorro",dni=None,        sip="38950271", zona=3, sexo="mujer",    telefono="966 829 012", direccion="C/ Mayor, 7, 1\u00baA",                          mes_renovacion="2026-07", fecha_alta=_date(2022,10,4),  activo=False),
                    dict(apellidos="Arcos Roca",        nombre="Santiago",     dni="81643705E",  sip="88990011", zona=3, sexo="hombre",   telefono="966 830 123", direccion="C/ del Rinc\u00f3n de Loix, 27, bajo B",       mes_renovacion="2026-09", fecha_alta=_date(2021,12,17), activo=True),
                    dict(apellidos="Arroyo Serrano",    nombre="Isabel",       dni=None,         sip="16074392", zona=4, sexo="mujer",    telefono="966 831 234", direccion="C/ Formentera, 9, 2\u00baA",                    mes_renovacion="2026-04", fecha_alta=_date(2024,9,30),  activo=True),
                    dict(apellidos="Aznar M\u00ednguez",nombre="Ram\u00f3n",  dni="49237806F",  sip=None,      zona=4, sexo="hombre",   telefono="966 832 345", direccion="C/ Canarias, 8, 3\u00baB",                      mes_renovacion="2026-06", fecha_alta=_date(2023,11,7),  activo=True),
                    dict(apellidos="Bravo Hidalgo",     nombre="Luisa",        dni=None,         sip="72890134", zona=4, sexo="mujer",    telefono=None,          direccion="Avda. de Europa, 55, 1\u00baC",                 mes_renovacion="2026-08", fecha_alta=_date(2022,4,16),  activo=True),
                    dict(apellidos="Bueno Climent",     nombre="Pascual",      dni="35614920G",  sip="99001122", zona=4, sexo="hombre",   telefono="966 833 456", direccion="Avda. de Mallorca, 12, 4\u00baA",               mes_renovacion="2026-10", fecha_alta=_date(2021,7,29),  activo=True),
                    dict(apellidos="Caballero Flores",  nombre="Mar\u00eda",   dni=None,         sip="98403257", zona=4, sexo="mujer",    telefono="966 834 567", direccion="C/ Gambo, 16, bajo C",                          mes_renovacion="2026-11", fecha_alta=_date(2020,6,3),   activo=False),
                    dict(apellidos="Calvo Pastor",      nombre="Marcelino",    dni="51728069L",  sip=None,      zona=4, sexo="hombre",   telefono="966 835 678", direccion="C/ Ibiza, 11, 2\u00baD",                        mes_renovacion="2026-12", fecha_alta=_date(2020,1,18),  activo=True),
                    dict(apellidos="Campos Exp\u00f3sito",nombre="Milagros",  dni=None,         sip="24396815", zona=4, sexo="mujer",    telefono="966 836 789", direccion="C/ Menorca, 20, 3\u00baA",                       mes_renovacion="2026-03", fecha_alta=_date(2024,10,22), activo=True),
                    dict(apellidos="Cano Guerrero",     nombre="Alfonso",      dni="67012438K",  sip="10112233", zona=4, sexo="hombre",   telefono=None,          direccion="C/ Lepanto, 3, 1\u00baB",                       mes_renovacion="2026-05", fecha_alta=_date(2023,12,9),  activo=True),
                    dict(apellidos="Castellano Castro", nombre="Petra",        dni=None,         sip="89547103", zona=4, sexo="no_define",telefono="966 837 890", direccion="C/ Ausi\u00e0s March, 38, 5\u00baC",            mes_renovacion="2026-07", fecha_alta=_date(2022,2,25),  activo=True),
                    dict(apellidos="Castro D\u00edaz",  nombre="Emilio",       dni="43861259S",  sip=None,      zona=4, sexo="hombre",   telefono="966 838 901", direccion="C/ Tom\u00e0s Ortu\u00f1o, 47, 2\u00baB",       mes_renovacion="2026-09", fecha_alta=_date(2021,10,6),  activo=True),
                    dict(apellidos="Climent Font",      nombre="Serafina",     dni=None,         sip="17024896", zona=4, sexo="mujer",    telefono="966 839 012", direccion="Avda. del Mediterr\u00e1neo, 22, 4\u00baD",    mes_renovacion="2026-11", fecha_alta=_date(2020,8,13),  activo=False),
                    dict(apellidos="Coll Rivas",        nombre="Sergio",       dni="80273641V",  sip="21233445", zona=4, sexo="hombre",   telefono="966 840 123", direccion="C/ La Mar, 18, 1\u00baA",                       mes_renovacion="2026-12", fecha_alta=_date(2020,3,27),  activo=True),
                    dict(apellidos="D\u00edaz Alvarado",nombre="Trinidad",     dni=None,         sip="52938407", zona=4, sexo="no_define",telefono="966 841 234", direccion="Avda. de l'Aig\u00fcera, 9, 3\u00baC",          mes_renovacion="2026-02", fecha_alta=_date(2024,11,15), activo=True),
                    dict(apellidos="Exp\u00f3sito Arroyo",nombre="Alberto",    dni="39605182Q",  sip=None,      zona=4, sexo="hombre",   telefono=None,          direccion="C/ Sant Vicent, 5, 2\u00baA",                   mes_renovacion="2026-04", fecha_alta=_date(2023,4,21),  activo=True),
                ]
                for row in _SEED:
                    db2.add(CasoMayorACasa(**row))
                db2.commit()
                print(f"\u2705 {len(_SEED)} casos de ejemplo insertados (dni/sip separados)")
            else:
                print("\u2139\ufe0f  Datos ya existen, seed omitido")
        finally:
            db2.close()

    except Exception as startup_err:
        import traceback
        print(f"\u274c ERROR EN ARRANQUE: {startup_err}")
        traceback.print_exc()

    yield
    print("\U0001f6d1 Apagando SocialApp API...")


app = FastAPI(
    title="SocialApp API",
    description="Backend de SocialApp — gestión de usuarios, posts y más",
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
