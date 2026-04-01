# ============================================================
# Dockerfile — Para Railway (raíz del proyecto)
# ============================================================

FROM python:3.12-slim-bookworm AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --upgrade pip --no-cache-dir && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt


FROM python:3.12-slim-bookworm

# libpq5 necesaria para PostgreSQL en runtime
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /api

# Copia librerías instaladas
COPY --from=builder /install /usr/local

# Copia el código de la aplicación
COPY backend/app ./app

# Copia el script de arranque
COPY backend/start.sh ./start.sh
RUN chmod +x ./start.sh

# NO usamos USER appuser para evitar problemas de permisos en Railway

# Usa el script de arranque (loguea PORT y diagnostica)
CMD ["./start.sh"]
