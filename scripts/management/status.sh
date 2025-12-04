#!/bin/bash
# Script para verificar status da aplicação

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$APP_DIR"

echo "=== Status da Aplicação de Provas ==="

# Localizar PID file
if [ -w "/var/run/provas_app" ] && [ -d "/var/run/provas_app" ]; then
    PIDFILE="/var/run/provas_app/gunicorn.pid"
else
    PIDFILE="$APP_DIR/run/gunicorn.pid"
fi

if [ ! -f "$PIDFILE" ]; then
    echo "Status: ✗ Parada (PID file não encontrado)"
    exit 1
fi

PID=$(cat "$PIDFILE")

if ps -p $PID > /dev/null 2>&1; then
    echo "Status: ✓ Rodando"
    echo "PID: $PID"
    echo "Memória: $(ps -p $PID -o rss= | awk '{printf "%.2f MB", $1/1024}')"
    echo "CPU: $(ps -p $PID -o %cpu=)%"
    echo "Uptime: $(ps -p $PID -o etime=)"

    # Verificar porta
    source .env.production 2>/dev/null || true
    PORT=${PORT:-8000}
    if netstat -tlnp 2>/dev/null | grep -q ":$PORT "; then
        echo "Porta: $PORT (ATIVA)"
    else
        echo "Porta: $PORT (verificar configuração)"
    fi

    exit 0
else
    echo "Status: ✗ Parada (processo não encontrado)"
    rm "$PIDFILE"
    exit 1
fi
