# ============================================================
# Dockerfile — Para Railway (se coloca en la RAÍZ del proyecto)
# ============================================================
# Railway construye desde la raíz, así que este Dockerfile
# copia los archivos desde la carpeta backend/.
#
# El Dockerfile que hay en backend/ se sigue usando para
# el desarrollo local con Docker Compose.
# ============================================================

# ─── Stage 1: Builder ────────────────────────────────────────
FROM python:3.12-slim-bookworm AS builder

WORKDIR /build

# Herramientas para compilar (psycopg2 y similares las necesitan)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements desde la subcarpeta backend/
COPY backend/requirements.txt .
RUN pip install --upgrade pip --no-cache-dir && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt


# ─── Stage 2: Production ─────────────────────────────────────
FROM python:3.12-slim-bookworm AS production

# libpq5: librería de cliente PostgreSQL (necesaria en runtime)
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && addgroup --system appgroup \
    && adduser  --system --ingroup appgroup appuser

WORKDIR /api

# Copia librerías del stage builder
COPY --from=builder /install /usr/local

# Copia el código de la app desde backend/app/
COPY backend/app ./app
# Ensure static files (HTML, CSS, JS) are explicitly included
COPY backend/app/static ./app/static

USER appuser

# Railway asigna el puerto dinámicamente en la variable de entorno $PORT
# ${PORT:-8000} significa: usa $PORT si existe, si no usa 8000 (desarrollo)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1
