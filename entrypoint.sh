#!/bin/bash
# ==================================
# Entrypoint de Produção
# Sistema de Provas Puket
# ==================================

set -e

echo "=========================================="
echo "🚀 Sistema de Provas Puket"
echo "=========================================="

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p /app/uploads /app/logs /app/backups

# Verificar tipo de banco de dados
DB_URL="${DATABASE_URL:-}"

if [[ "$DB_URL" == *"postgresql"* ]]; then
    echo "⏳ Aguardando PostgreSQL..."
    MAX_TRIES=30
    COUNTER=0

    while ! python3 -c "
import psycopg2
import os
import sys
try:
    db_url = os.getenv('DATABASE_URL', '')
    parts = db_url.replace('postgresql://', '').split('@')
    user_pass = parts[0].split(':')
    host_db = parts[1].split('/')
    host_port = host_db[0].split(':')

    conn = psycopg2.connect(
        host=host_port[0],
        port=host_port[1] if len(host_port) > 1 else '5432',
        user=user_pass[0],
        password=user_pass[1],
        database=host_db[1]
    )
    conn.close()
    print('✅ PostgreSQL conectado!')
    sys.exit(0)
except Exception as e:
    print(f'❌ Erro: {e}')
    sys.exit(1)
" 2>/dev/null; do
        COUNTER=$((COUNTER+1))
        if [ $COUNTER -gt $MAX_TRIES ]; then
            echo "❌ Timeout aguardando PostgreSQL"
            exit 1
        fi
        echo "   Tentativa $COUNTER/$MAX_TRIES..."
        sleep 2
    done
else
    echo "📦 Usando SQLite - criando diretório de dados..."
    mkdir -p /app/data
fi

# Inicializar banco de dados
echo "🗄️  Verificando banco de dados..."
python3 << 'EOF'
from app import app, db
from models import User
from werkzeug.security import generate_password_hash
import os
import sys

try:
    with app.app_context():
        # Criar tabelas
        print("   Criando/atualizando tabelas...")
        db.create_all()

        # Migração: adicionar colunas de checklist se não existirem
        print("   Verificando colunas de checklist...")
        from sqlalchemy import text, inspect
        inspector = inspect(db.engine)
        colunas_existentes = [col['name'] for col in inspector.get_columns('provas')]

        with db.engine.connect() as conn:
            if 'checklist_qualidade' not in colunas_existentes:
                conn.execute(text("ALTER TABLE provas ADD COLUMN checklist_qualidade TEXT"))
                print("   + Adicionada coluna checklist_qualidade")

            if 'checklist_estilo' not in colunas_existentes:
                conn.execute(text("ALTER TABLE provas ADD COLUMN checklist_estilo TEXT"))
                print("   + Adicionada coluna checklist_estilo")

            if 'checklist_modelagem' not in colunas_existentes:
                conn.execute(text("ALTER TABLE provas ADD COLUMN checklist_modelagem TEXT"))
                print("   + Adicionada coluna checklist_modelagem")

            conn.commit()

        # Verificar se admin existe
        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin = User.query.filter_by(username=admin_username).first()

        if not admin:
            print(f"   Criando usuário admin: {admin_username}")
            admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
            admin_email = os.getenv('ADMIN_EMAIL', 'admin@puket.com')

            admin = User(
                username=admin_username,
                email=admin_email,
                password_hash=generate_password_hash(admin_password),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print(f"   ✅ Usuário admin criado!")
        else:
            print(f"   ℹ️  Usuário admin já existe")

        print("✅ Banco de dados pronto!")
        sys.exit(0)

except Exception as e:
    print(f"❌ Erro inicializando banco: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
EOF

if [ $? -ne 0 ]; then
    echo "❌ Falha ao inicializar banco de dados"
    exit 1
fi

# Informações do ambiente
echo ""
echo "📊 Configuração:"
echo "   Ambiente: ${FLASK_ENV:-production}"
echo "   Host: ${HOST:-0.0.0.0}"
echo "   Port: ${PORT:-8000}"
echo "   Debug: ${DEBUG:-False}"
echo "   Database: PostgreSQL"
echo "   Admin: ${ADMIN_USERNAME:-admin}"
echo ""
echo "=========================================="
echo "🚀 Iniciando aplicação..."
echo "=========================================="
echo ""

# Executar comando
exec "$@"
