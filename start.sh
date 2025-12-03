#!/bin/bash
# Script para iniciar a aplicação em produção

set -e

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$APP_DIR"

echo "=== Iniciando Aplicação de Provas em Produção ==="

# Verificar se .env.production existe
if [ ! -f ".env.production" ]; then
    echo "ERRO: Arquivo .env.production não encontrado!"
    echo "Copie .env.example para .env.production e configure as variáveis"
    exit 1
fi

# Carregar variáveis de ambiente
export ENV_FILE=.env.production
source .env.production

# Verificar se virtual environment existe
if [ ! -d ".venv" ]; then
    echo "Criando virtual environment..."
    python3 -m venv .venv
fi

# Ativar virtual environment
source .venv/bin/activate

# Instalar/atualizar dependências
echo "Instalando dependências..."
pip install -r requirements.txt --quiet

# Criar diretórios necessários
echo "Criando diretórios..."
mkdir -p uploads relatorios_pdf instance
mkdir -p /var/log/provas_app 2>/dev/null || mkdir -p logs
mkdir -p /var/run/provas_app 2>/dev/null || mkdir -p run

# Ajustar caminhos de log se não tiver permissão em /var
if [ ! -w "/var/log/provas_app" ]; then
    export LOG_FILE="$APP_DIR/logs/app.log"
    mkdir -p "$APP_DIR/logs"
fi

if [ ! -w "/var/run/provas_app" ]; then
    PIDFILE="$APP_DIR/run/gunicorn.pid"
else
    PIDFILE="/var/run/provas_app/gunicorn.pid"
fi

# Verificar se já está rodando
if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo "Aplicação já está rodando (PID: $PID)"
        exit 1
    else
        echo "Removendo PID file antigo..."
        rm "$PIDFILE"
    fi
fi

# Iniciar com Gunicorn
echo "Iniciando Gunicorn..."
gunicorn -c gunicorn_config.py \
    --daemon \
    --pid "$PIDFILE" \
    wsgi:app

sleep 2

# Verificar se iniciou corretamente
if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo "✓ Aplicação iniciada com sucesso!"
        echo "  PID: $PID"
        echo "  Porta: ${PORT:-8000}"
        echo "  Logs: ${LOG_FILE:-/var/log/provas_app/app.log}"
    else
        echo "✗ Falha ao iniciar aplicação"
        exit 1
    fi
else
    echo "✗ Falha ao criar PID file"
    exit 1
fi
