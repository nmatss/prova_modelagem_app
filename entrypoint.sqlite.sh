#!/bin/bash
# Entrypoint para aplicação Flask
# Inicializa banco de dados se necessário

set -e

echo "=========================================="
echo "🐳 Iniciando Aplicação de Provas"
echo "=========================================="

# Diretórios
DATA_DIR="${DATA_DIR:-/app/data}"
UPLOADS_DIR="${UPLOADS_DIR:-/app/uploads}"
LOGS_DIR="${LOGS_DIR:-/app/logs}"

# Criar diretórios se não existirem
echo "📁 Criando diretórios..."
mkdir -p "$DATA_DIR" "$UPLOADS_DIR" "$LOGS_DIR"

# Verificar se banco de dados existe
DB_PATH="${DATABASE_URL:-sqlite:///$DATA_DIR/provas.db}"
DB_FILE=$(echo "$DB_PATH" | sed 's/sqlite:\/\/\///')

if [ ! -f "$DB_FILE" ]; then
    echo "🗄️  Banco de dados não encontrado. Criando..."

    # Inicializar banco de dados
    python3 << EOF
from app import app
from models import db, Usuario
from werkzeug.security import generate_password_hash
from datetime import datetime

print("Criando tabelas...")
with app.app_context():
    db.create_all()

    # Criar usuário admin padrão
    admin = Usuario.query.filter_by(username='admin').first()
    if not admin:
        admin = Usuario(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            email='admin@provas.local',
            nome_completo='Administrador',
            is_admin=True,
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuário admin criado (senha: admin123)")

    print("✅ Banco de dados inicializado")
EOF
else
    echo "✅ Banco de dados já existe: $DB_FILE"
fi

# Verificar permissões
echo "🔒 Verificando permissões..."
chmod -R 755 "$UPLOADS_DIR" 2>/dev/null || true
chmod -R 755 "$LOGS_DIR" 2>/dev/null || true

# Informações do ambiente
echo ""
echo "📊 Configuração:"
echo "   FLASK_ENV: ${FLASK_ENV:-production}"
echo "   DATABASE: $DB_FILE"
echo "   HOST: ${HOST:-0.0.0.0}"
echo "   PORT: ${PORT:-5000}"
echo ""
echo "=========================================="
echo "🚀 Iniciando servidor..."
echo "=========================================="
echo ""

# Executar comando passado como argumento
exec "$@"
