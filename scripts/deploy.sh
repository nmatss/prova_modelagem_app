#!/bin/bash
# Script automatizado de deploy - Sistema de Provas Puket
# Uso: ./scripts/deploy.sh [opcao]
# Opções: setup, update, backup, restore

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variáveis
APP_DIR="/opt/prova_app"
BACKUP_DIR="$APP_DIR/backups"
VENV_DIR="$APP_DIR/venv"

# Funções auxiliares
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_error "Este script deve ser executado como root (sudo)"
        exit 1
    fi
}

# Função 1: Setup completo do servidor
setup_server() {
    log_info "Iniciando setup do servidor..."

    # Atualizar sistema
    log_info "Atualizando sistema operacional..."
    apt update && apt upgrade -y

    # Instalar dependências
    log_info "Instalando dependências..."
    apt install -y \
        python3.11 \
        python3.11-venv \
        python3-pip \
        postgresql \
        postgresql-contrib \
        nginx \
        git \
        supervisor \
        libpq-dev \
        build-essential \
        python3-dev \
        libcairo2 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libgdk-pixbuf2.0-0 \
        libffi-dev \
        shared-mime-info \
        ufw

    # Configurar PostgreSQL
    log_info "Configurando PostgreSQL..."
    read -p "Nome do banco de dados [prova_modelagem_db]: " DB_NAME
    DB_NAME=${DB_NAME:-prova_modelagem_db}

    read -p "Usuário do banco [prova_user]: " DB_USER
    DB_USER=${DB_USER:-prova_user}

    read -sp "Senha do banco: " DB_PASS
    echo

    sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;" || true
    sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';" || true
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
    sudo -u postgres psql -c "ALTER DATABASE $DB_NAME OWNER TO $DB_USER;"

    # Criar usuário da aplicação
    log_info "Criando usuário da aplicação..."
    id -u prova_app &>/dev/null || useradd --system --group --home $APP_DIR --shell /bin/bash prova_app

    # Criar diretórios
    log_info "Criando estrutura de diretórios..."
    mkdir -p $APP_DIR/{uploads,logs,backups,scripts}
    chown -R prova_app:prova_app $APP_DIR

    # Configurar firewall
    log_info "Configurando firewall..."
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow ssh
    ufw allow 'Nginx Full'
    echo "y" | ufw enable

    log_info "Setup inicial concluído!"
    log_warn "Próximos passos:"
    echo "1. Transferir código da aplicação para $APP_DIR"
    echo "2. Configurar arquivo .env"
    echo "3. Executar: sudo ./scripts/deploy.sh install"
}

# Função 2: Instalar aplicação
install_app() {
    log_info "Instalando aplicação..."

    cd $APP_DIR

    # Criar virtual environment
    if [ ! -d "$VENV_DIR" ]; then
        log_info "Criando virtual environment..."
        sudo -u prova_app python3.11 -m venv $VENV_DIR
    fi

    # Instalar dependências Python
    log_info "Instalando dependências Python..."
    sudo -u prova_app bash -c "
        source $VENV_DIR/bin/activate
        pip install --upgrade pip
        pip install -r $APP_DIR/requirements.txt
        pip install gunicorn weasyprint
    "

    # Verificar .env
    if [ ! -f "$APP_DIR/.env" ]; then
        log_error "Arquivo .env não encontrado!"
        log_info "Criando .env de exemplo..."
        cp $APP_DIR/.env.example $APP_DIR/.env
        log_warn "IMPORTANTE: Edite o arquivo $APP_DIR/.env com suas configurações!"
        exit 1
    fi

    # Inicializar banco de dados
    log_info "Inicializando banco de dados..."
    sudo -u prova_app bash -c "
        source $VENV_DIR/bin/activate
        cd $APP_DIR
        python3 -c '
from app import app, db
with app.app_context():
    db.create_all()
    print(\"Banco inicializado!\")
'
    "

    # Configurar Supervisor
    log_info "Configurando Supervisor..."
    cat > /etc/supervisor/conf.d/prova_app.conf <<EOF
[program:prova_app]
command=$VENV_DIR/bin/gunicorn -c $APP_DIR/gunicorn_config.py app:app
directory=$APP_DIR
user=prova_app
group=prova_app
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=$APP_DIR/logs/supervisor_error.log
stdout_logfile=$APP_DIR/logs/supervisor_output.log
environment=PATH="$VENV_DIR/bin",PYTHONPATH="$APP_DIR"
EOF

    supervisorctl reread
    supervisorctl update
    supervisorctl start prova_app

    # Configurar Nginx
    if [ ! -f "/etc/nginx/sites-available/prova_app" ]; then
        log_info "Configurando Nginx..."
        cp $APP_DIR/scripts/nginx.conf /etc/nginx/sites-available/prova_app
        ln -sf /etc/nginx/sites-available/prova_app /etc/nginx/sites-enabled/
        rm -f /etc/nginx/sites-enabled/default
        nginx -t && systemctl reload nginx
    fi

    log_info "Instalação concluída!"
    log_info "Status da aplicação:"
    supervisorctl status prova_app
}

# Função 3: Atualizar aplicação
update_app() {
    log_info "Atualizando aplicação..."

    # Backup antes de atualizar
    backup_app

    cd $APP_DIR

    # Atualizar código
    log_info "Atualizando código..."
    if [ -d ".git" ]; then
        sudo -u prova_app git pull
    else
        log_warn "Não é um repositório Git. Atualize manualmente."
    fi

    # Atualizar dependências
    log_info "Atualizando dependências..."
    sudo -u prova_app bash -c "
        source $VENV_DIR/bin/activate
        pip install --upgrade pip
        pip install -r $APP_DIR/requirements.txt --upgrade
    "

    # Reiniciar aplicação
    log_info "Reiniciando aplicação..."
    supervisorctl restart prova_app

    log_info "Atualização concluída!"
    supervisorctl status prova_app
}

# Função 4: Backup
backup_app() {
    log_info "Criando backup..."

    DATE=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/backup_$DATE"

    mkdir -p $BACKUP_DIR

    # Backup do banco
    log_info "Backup do banco de dados..."
    source $APP_DIR/.env
    DB_NAME=$(echo $DATABASE_URL | sed -n 's/.*\/\([^?]*\).*/\1/p')
    DB_USER=$(echo $DATABASE_URL | sed -n 's/.*:\/\/\([^:]*\):.*/\1/p')

    sudo -u postgres pg_dump $DB_NAME | gzip > "${BACKUP_FILE}_db.sql.gz"

    # Backup dos uploads
    log_info "Backup dos uploads..."
    tar -czf "${BACKUP_FILE}_uploads.tar.gz" -C $APP_DIR uploads/

    # Backup do .env
    log_info "Backup das configurações..."
    cp $APP_DIR/.env "${BACKUP_FILE}_env"

    # Remover backups antigos (manter últimos 7)
    log_info "Removendo backups antigos..."
    cd $BACKUP_DIR
    ls -t backup_*.sql.gz 2>/dev/null | tail -n +8 | xargs -r rm --
    ls -t backup_*.tar.gz 2>/dev/null | tail -n +8 | xargs -r rm --

    log_info "Backup concluído: $BACKUP_FILE"
}

# Função 5: Restaurar backup
restore_app() {
    log_info "Restaurando backup..."

    # Listar backups disponíveis
    echo "Backups disponíveis:"
    ls -lh $BACKUP_DIR/backup_*_db.sql.gz 2>/dev/null | awk '{print $9}' | while read file; do
        basename $file _db.sql.gz
    done

    read -p "Digite o nome do backup (sem extensão): " BACKUP_NAME

    if [ ! -f "$BACKUP_DIR/${BACKUP_NAME}_db.sql.gz" ]; then
        log_error "Backup não encontrado!"
        exit 1
    fi

    # Parar aplicação
    log_warn "Parando aplicação..."
    supervisorctl stop prova_app

    # Restaurar banco
    log_info "Restaurando banco de dados..."
    source $APP_DIR/.env
    DB_NAME=$(echo $DATABASE_URL | sed -n 's/.*\/\([^?]*\).*/\1/p')

    gunzip < "$BACKUP_DIR/${BACKUP_NAME}_db.sql.gz" | sudo -u postgres psql $DB_NAME

    # Restaurar uploads
    if [ -f "$BACKUP_DIR/${BACKUP_NAME}_uploads.tar.gz" ]; then
        log_info "Restaurando uploads..."
        rm -rf $APP_DIR/uploads.old
        mv $APP_DIR/uploads $APP_DIR/uploads.old
        tar -xzf "$BACKUP_DIR/${BACKUP_NAME}_uploads.tar.gz" -C $APP_DIR
        chown -R prova_app:prova_app $APP_DIR/uploads
    fi

    # Reiniciar aplicação
    log_info "Reiniciando aplicação..."
    supervisorctl start prova_app

    log_info "Restauração concluída!"
}

# Função 6: Ver logs
view_logs() {
    log_info "Logs da aplicação (Ctrl+C para sair):"
    tail -f $APP_DIR/logs/*.log
}

# Função 7: Status
show_status() {
    log_info "Status do sistema:"
    echo ""
    echo "=== Supervisor ==="
    supervisorctl status prova_app
    echo ""
    echo "=== Nginx ==="
    systemctl status nginx --no-pager -l
    echo ""
    echo "=== PostgreSQL ==="
    systemctl status postgresql --no-pager -l
    echo ""
    echo "=== Disco ==="
    df -h $APP_DIR
    echo ""
    echo "=== Memória ==="
    free -h
}

# Menu principal
case "${1:-}" in
    setup)
        check_root
        setup_server
        ;;
    install)
        check_root
        install_app
        ;;
    update)
        check_root
        update_app
        ;;
    backup)
        check_root
        backup_app
        ;;
    restore)
        check_root
        restore_app
        ;;
    logs)
        view_logs
        ;;
    status)
        show_status
        ;;
    *)
        echo "Sistema de Deploy - Provas Puket"
        echo ""
        echo "Uso: $0 [comando]"
        echo ""
        echo "Comandos disponíveis:"
        echo "  setup    - Setup inicial do servidor (primeira vez)"
        echo "  install  - Instalar/configurar aplicação"
        echo "  update   - Atualizar aplicação"
        echo "  backup   - Criar backup"
        echo "  restore  - Restaurar backup"
        echo "  logs     - Ver logs em tempo real"
        echo "  status   - Ver status do sistema"
        echo ""
        exit 1
        ;;
esac
