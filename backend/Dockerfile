# ============================================================
# Dockerfile — Backend FastAPI (multi-stage)
# ============================================================
# Usamos Python 3.12-slim (Estable y ligera)
# ============================================================

# ─────────────────────────────────────────────
# STAGE 1: builder
# ─────────────────────────────────────────────
FROM python:3.12-slim-bookworm AS builder

WORKDIR /build

# Instalamos dependencias temporales para compilar (por si acaso)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Actualiza pip e instala las dependencias
COPY requirements.txt .
RUN pip install --upgrade pip --no-cache-dir && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt


# ─────────────────────────────────────────────
# STAGE 2: production
# ─────────────────────────────────────────────
FROM python:3.12-slim-bookworm AS production

# Necesitamos libpq para que funcione el driver de Postgres
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/* && \
    addgroup --system appgroup && \
    adduser  --system --ingroup appgroup appuser

WORKDIR /api
COPY --from=builder /install /usr/local
COPY ./app ./app

USER appuser
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]


# ─────────────────────────────────────────────
# STAGE 3: development
# ─────────────────────────────────────────────
FROM production AS development
USER root
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
