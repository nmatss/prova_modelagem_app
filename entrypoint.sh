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

# Pré-migrações SQL diretas (executadas ANTES do import do app)
# Necessário porque db.py:init_app() faz User.query no startup, que falha
# se a coluna idioma/pais não existir ainda (DB de prod antes desta atualização).
echo "🔧 Pré-migrações SQL low-level..."
python3 << 'PREMIG'
import os
import sqlite3

db_url = os.getenv('DATABASE_URL', '')
if 'sqlite' in db_url:
    # sqlite:////absolute → /absolute ; sqlite:///relative → relative
    if db_url.startswith('sqlite:////'):
        path = '/' + db_url[len('sqlite:////'):]
    elif db_url.startswith('sqlite:///'):
        path = db_url[len('sqlite:///'):]
    else:
        path = None

    if path and os.path.exists(path):
        conn = sqlite3.connect(path)
        cur = conn.cursor()

        def add_col(table, column, ddl):
            try:
                cur.execute(f"PRAGMA table_info({table})")
                cols = [r[1] for r in cur.fetchall()]
                if not cols:
                    print(f"   ⊘ table {table} ausente — db.create_all() criará")
                    return
                if column not in cols:
                    cur.execute(f"ALTER TABLE {table} ADD COLUMN {ddl}")
                    print(f"   + {table}.{column} adicionada (pré-migração)")
                else:
                    print(f"   = {table}.{column} já existe")
            except sqlite3.OperationalError as e:
                print(f"   ⚠ skip {table}.{column}: {e}")

        add_col('usuarios', 'idioma', "idioma VARCHAR(5) DEFAULT 'pt'")
        add_col('fornecedores', 'pais', "pais VARCHAR(100)")
        conn.commit()
        conn.close()
    else:
        print(f"   ℹ DB ainda não existe ({path}) — db.create_all() vai construir")
else:
    print("   ℹ Não-SQLite — pré-migração pulada (entrypoint Postgres faz ALTER abaixo)")
PREMIG

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

            # Migração: pais em fornecedores (Onda 1.2)
            try:
                colunas_fornec = [col['name'] for col in inspector.get_columns('fornecedores')]
                if 'pais' not in colunas_fornec:
                    conn.execute(text("ALTER TABLE fornecedores ADD COLUMN pais VARCHAR(100)"))
                    print("   + Adicionada coluna pais em fornecedores")
            except Exception as _e:
                print(f"   ⚠ skip pais migration: {_e}")

            # Migração: idioma em usuarios (Onda 3.2)
            try:
                colunas_user = [col['name'] for col in inspector.get_columns('usuarios')]
                if 'idioma' not in colunas_user:
                    conn.execute(text("ALTER TABLE usuarios ADD COLUMN idioma VARCHAR(5) DEFAULT 'pt'"))
                    print("   + Adicionada coluna idioma em usuarios")
            except Exception as _e:
                print(f"   ⚠ skip idioma migration: {_e}")

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
