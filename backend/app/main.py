# ============================================================
# main.py — El corazón de tu aplicación FastAPI
# ============================================================

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles   # Sirve archivos HTML/CSS/JS
from fastapi.responses import FileResponse    # Devuelve el index.html al navegador

# Conexión a la BD y modelos (importamos el módulo completo para que SQLAlchemy conozca todas las tablas)
from app.database import engine
from app import models as _models  # noqa: F401

# Routers
from app.routers import users
from app.routers import mayor_a_casa

# ============================================================
# LIFESPAN — Código que se ejecuta al arrancar y al apagar
# ============================================================
# "lifespan" es como un interruptor:
#   - Lo que está ANTES del "yield" se ejecuta al arrancar el servidor
#   - Lo que está DESPUÉS del "yield" se ejecuta al apagarlo

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── AL ARRANCAR ──────────────────────────────────────────
    # Crea TODAS las tablas en PostgreSQL si no existen todavía.
    # Es seguro: si la tabla ya existe, no la toca ni borra datos.
    print("🚀 Arrancando SocialApp API...")
    # create_all crea todas las tablas registradas en models/__init__.py
    # si ya existen, no las modifica (es seguro correrlo siempre)
    _models.Base.metadata.create_all(bind=engine)
    print("✅ Tablas verificadas/creadas en PostgreSQL")

    yield   # ← Aquí el servidor empieza a atender peticiones

    # ── AL APAGAR ────────────────────────────────────────────
    print("🛑 Apagando SocialApp API...")


# ============================================================
# CREAR LA APP
# ============================================================

app = FastAPI(
    title="SocialApp API",
    description="Backend de SocialApp — gestión de usuarios, posts y más",
    version="0.1.0",
    lifespan=lifespan,   # Le decimos a FastAPI que use nuestro ciclo de vida
)

# ============================================================
# CORS (Cross-Origin Resource Sharing)
# ============================================================

# 5. Lista de orígenes permitidos para hablar con este servidor
#    Añade aquí la URL de tu app de escritorio o web frontend
origins = [
    "http://localhost",           # Servidor local genérico
    "http://localhost:3000",      # Frontend React/Next.js típico
    "http://localhost:8080",      # Otro puerto común de frontends
    # "https://tu-app.com",       # ← Añade tu dominio en producción
]

# 6. Añadimos el middleware de CORS a la app
#    Esto se ejecuta en cada petición antes de que llegue a tus endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Quién puede llamar a la API
    allow_credentials=True,       # Permite enviar cookies/tokens
    allow_methods=["*"],          # GET, POST, PUT, DELETE… todos permitidos
    allow_headers=["*"],          # Cualquier cabecera HTTP permitida
)

# ============================================================
# INCLUIR ROUTERS
# ============================================================
# Cada include_router conecta un "sub-menú" de URLs a la app principal.
# prefix="/users" significa que todas las rutas del router empezarán por /users
# tags=["Usuarios"] agrupa los endpoints en la documentación /docs

app.include_router(users.router,       prefix="/users",       tags=["Usuarios"])
app.include_router(mayor_a_casa.router, prefix="/mayor-a-casa", tags=["Mayor a Casa"])
# app.include_router(posts.router, prefix="/posts", tags=["Posts"])  ← futuro

# ============================================================
# ARCHIVOS ESTÁTICOS (HTML, CSS, JS del frontend)
# ============================================================
# Monta la carpeta app/static/ en la URL /static
# El navegador pedirá /static/css/app.css → FastAPI devuelve el archivo real
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ============================================================
# ENDPOINTS BASE
# ============================================================

@app.get("/health", tags=["Sistema"])
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

# Raíz: devuelve el frontend HTML para que se abra en el navegador
@app.get("/", include_in_schema=False)
async def serve_frontend():
    """Sirve la interfaz gráfica."""
    return FileResponse("app/static/index.html")
