#!/bin/bash
# Script para parar a aplicação

set -e

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$APP_DIR"

echo "=== Parando Aplicação de Provas ==="

# Localizar PID file
if [ -w "/var/run/provas_app" ]; then
    PIDFILE="/var/run/provas_app/gunicorn.pid"
else
    PIDFILE="$APP_DIR/run/gunicorn.pid"
fi

if [ ! -f "$PIDFILE" ]; then
    echo "Aplicação não está rodando (PID file não encontrado)"
    exit 0
fi

PID=$(cat "$PIDFILE")

if ! ps -p $PID > /dev/null 2>&1; then
    echo "Processo não encontrado, removendo PID file..."
    rm "$PIDFILE"
    exit 0
fi

echo "Parando processo $PID..."
kill -TERM $PID

# Aguardar processo encerrar
for i in {1..10}; do
    if ! ps -p $PID > /dev/null 2>&1; then
        rm "$PIDFILE"
        echo "✓ Aplicação parada com sucesso"
        exit 0
    fi
    sleep 1
done

# Forçar encerramento se necessário
if ps -p $PID > /dev/null 2>&1; then
    echo "Forçando encerramento..."
    kill -9 $PID
    rm "$PIDFILE"
    echo "✓ Aplicação parada (força)"
fi
