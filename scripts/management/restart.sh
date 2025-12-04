#!/bin/bash
# Script para reiniciar a aplicação

set -e

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$APP_DIR"

echo "=== Reiniciando Aplicação de Provas ==="

# Parar aplicação
./stop.sh

# Aguardar um momento
sleep 2

# Iniciar aplicação
./start.sh
