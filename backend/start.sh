#!/bin/sh
# start.sh — Script de arranque para Railway
# Imprime información de diagnóstico y arranca uvicorn
set -e

echo "=========================================="
echo "  APBApp — Arranque"
echo "=========================================="
echo "PORT asignado: ${PORT:-NO DEFINIDO}"
echo "DATABASE_URL presente: $(if [ -n \"$DATABASE_URL\" ]; then echo SI; else echo NO; fi)"
echo "Python: $(python --version)"
echo "=========================================="

# Usa el PORT de Railway, o 8000 si no está definido
exec uvicorn app.main:app \
  --host 0.0.0.0 \
  --port "${PORT:-8000}" \
  --workers 1 \
  --log-level info
