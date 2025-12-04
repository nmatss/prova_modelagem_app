# 🚀 Guia Completo de Deploy em Produção - Sistema de Provas Puket

## 📋 Índice
1. [Requisitos do Servidor](#requisitos-do-servidor)
2. [Método 1: Deploy Manual (Tradicional)](#método-1-deploy-manual)
3. [Método 2: Deploy com Docker (Recomendado)](#método-2-deploy-com-docker)
4. [Configuração de Domínio e SSL](#configuração-de-domínio-e-ssl)
5. [Backup e Monitoramento](#backup-e-monitoramento)
6. [Manutenção e Troubleshooting](#manutenção-e-troubleshooting)

---

## 📦 Requisitos do Servidor

### Hardware Mínimo Recomendado
- **CPU**: 2 cores
- **RAM**: 2GB (4GB recomendado)
- **Disco**: 20GB SSD
- **Largura de banda**: 100Mbps

### Software
- **Sistema Operacional**: Ubuntu 20.04/22.04 LTS ou Debian 11/12
- **Acesso**: SSH com sudo
- **IP**: Endereço IP fixo ou domínio configurado

---

## 🔧 Método 1: Deploy Manual (Tradicional)

### Passo 1: Conectar ao Servidor

```bash
# Conectar via SSH
ssh usuario@seu-servidor.com

# Atualizar sistema
sudo apt update && sudo apt upgrade -y
```

### Passo 2: Instalar Dependências do Sistema

```bash
# Instalar Python, PostgreSQL, Nginx e outras dependências
sudo apt install -y \
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
    shared-mime-info

# Verificar instalação do Python
python3.11 --version
```

### Passo 3: Configurar PostgreSQL

```bash
# Acessar PostgreSQL
sudo -u postgres psql

# No prompt do PostgreSQL, executar:
CREATE DATABASE prova_modelagem_db;
CREATE USER prova_user WITH PASSWORD 'SUA_SENHA_SEGURA_AQUI';
GRANT ALL PRIVILEGES ON DATABASE prova_modelagem_db TO prova_user;
ALTER DATABASE prova_modelagem_db OWNER TO prova_user;
\q

# Verificar conexão
psql -U prova_user -d prova_modelagem_db -h localhost -W
```

### Passo 4: Criar Usuário da Aplicação

```bash
# Criar usuário sem privilégios de sudo
sudo adduser --system --group --home /opt/prova_app prova_app

# Criar diretórios
sudo mkdir -p /opt/prova_app
sudo chown -R prova_app:prova_app /opt/prova_app
```

### Passo 5: Transferir Aplicação para o Servidor

**Opção A: Via Git (Recomendado)**

```bash
# No servidor
sudo -u prova_app bash
cd /opt/prova_app

# Clonar repositório (se usar Git)
git clone https://github.com/seu-usuario/seu-repo.git .

# Ou criar repositório
git init
```

**Opção B: Via SCP (da sua máquina local)**

```bash
# Na sua máquina local, comprimir o projeto
cd /home/icolas_atsuda/ProjetosWeb/prova_modelagem_app
tar -czf prova_app.tar.gz \
    --exclude='.venv' \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    --exclude='instance' \
    .

# Transferir para o servidor
scp prova_app.tar.gz usuario@seu-servidor.com:/tmp/

# No servidor, extrair
sudo -u prova_app bash
cd /opt/prova_app
tar -xzf /tmp/prova_app.tar.gz
rm /tmp/prova_app.tar.gz
```

### Passo 6: Configurar Ambiente Python

```bash
# Como usuário prova_app
cd /opt/prova_app

# Criar virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Instalar WeasyPrint (para PDFs)
pip install weasyprint
```

### Passo 7: Configurar Variáveis de Ambiente

```bash
# Criar arquivo .env
nano /opt/prova_app/.env
```

Cole o seguinte conteúdo (ajuste os valores):

```bash
# Flask
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=gere-uma-chave-secreta-muito-longa-e-aleatoria-aqui

# Database
DATABASE_URL=postgresql://prova_user:SUA_SENHA_SEGURA_AQUI@localhost:5432/prova_modelagem_db

# Admin
ADMIN_USERNAME=admin
ADMIN_PASSWORD=sua_senha_admin_forte_aqui
ADMIN_EMAIL=seu@email.com

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
PERMANENT_SESSION_LIFETIME=3600

# Logging
LOG_LEVEL=INFO
LOG_FILE=/opt/prova_app/logs/app.log

# Rate Limiting
RATELIMIT_ENABLED=True
RATELIMIT_STORAGE_URL=memory://
```

**Gerar SECRET_KEY segura:**

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### Passo 8: Inicializar Banco de Dados

```bash
# Ativar venv
source /opt/prova_app/venv/bin/activate

# Criar diretórios necessários
mkdir -p /opt/prova_app/{uploads,logs,backups}

# Inicializar banco
cd /opt/prova_app
python3 -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Banco de dados inicializado!')
"

# Criar usuário admin
python3 -c "
from app import app, db
from models import User
from werkzeug.security import generate_password_hash
import os

with app.app_context():
    admin = User(
        username=os.getenv('ADMIN_USERNAME', 'admin'),
        email=os.getenv('ADMIN_EMAIL', 'admin@puket.com'),
        password_hash=generate_password_hash(os.getenv('ADMIN_PASSWORD', 'admin123')),
        is_admin=True
    )
    db.session.add(admin)
    db.session.commit()
    print('Usuário admin criado!')
"
```

### Passo 9: Configurar Gunicorn (Servidor WSGI)

```bash
# Criar arquivo de configuração do Gunicorn
sudo nano /opt/prova_app/gunicorn_config.py
```

Cole o seguinte conteúdo:

```python
import os
import multiprocessing

# Binding
bind = "127.0.0.1:8000"
backlog = 2048

# Workers
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = "/opt/prova_app/logs/gunicorn_access.log"
errorlog = "/opt/prova_app/logs/gunicorn_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "prova_modelagem_gunicorn"

# Server mechanics
daemon = False
pidfile = "/opt/prova_app/gunicorn.pid"
user = "prova_app"
group = "prova_app"
umask = 0o007

# SSL (se necessário, descomente)
# keyfile = "/etc/letsencrypt/live/seu-dominio.com/privkey.pem"
# certfile = "/etc/letsencrypt/live/seu-dominio.com/fullchain.pem"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
```

### Passo 10: Configurar Supervisor (Gerenciador de Processos)

```bash
# Criar arquivo de configuração do Supervisor
sudo nano /etc/supervisor/conf.d/prova_app.conf
```

Cole o seguinte conteúdo:

```ini
[program:prova_app]
command=/opt/prova_app/venv/bin/gunicorn -c /opt/prova_app/gunicorn_config.py app:app
directory=/opt/prova_app
user=prova_app
group=prova_app
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/opt/prova_app/logs/supervisor_error.log
stdout_logfile=/opt/prova_app/logs/supervisor_output.log
environment=
    PATH="/opt/prova_app/venv/bin",
    PYTHONPATH="/opt/prova_app"
```

```bash
# Recarregar Supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start prova_app

# Verificar status
sudo supervisorctl status prova_app
```

### Passo 11: Configurar Nginx (Proxy Reverso)

```bash
# Criar configuração do Nginx
sudo nano /etc/nginx/sites-available/prova_app
```

Cole o seguinte conteúdo:

```nginx
# Upstream Gunicorn
upstream prova_app_server {
    server 127.0.0.1:8000 fail_timeout=0;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name seu-dominio.com www.seu-dominio.com;

    # Certbot challenge
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS Server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name seu-dominio.com www.seu-dominio.com;

    # SSL Configuration (será configurado pelo Certbot)
    # ssl_certificate /etc/letsencrypt/live/seu-dominio.com/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com/privkey.pem;
    # include /etc/letsencrypt/options-ssl-nginx.conf;
    # ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self' https: data: 'unsafe-inline' 'unsafe-eval';" always;

    # Logs
    access_log /var/log/nginx/prova_app_access.log;
    error_log /var/log/nginx/prova_app_error.log;

    # Max upload size (para fotos)
    client_max_body_size 50M;

    # Timeouts
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;

    # Root location
    location / {
        proxy_pass http://prova_app_server;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    # Static files
    location /static/ {
        alias /opt/prova_app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Uploads (protegido por login)
    location /uploads/ {
        internal;
        alias /opt/prova_app/uploads/;
    }

    # Favicon
    location = /favicon.ico {
        alias /opt/prova_app/static/favicon.ico;
        log_not_found off;
        access_log off;
    }

    # Robots
    location = /robots.txt {
        alias /opt/prova_app/static/robots.txt;
        log_not_found off;
        access_log off;
    }
}
```

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/prova_app /etc/nginx/sites-enabled/

# Remover site padrão
sudo rm /etc/nginx/sites-enabled/default

# Testar configuração
sudo nginx -t

# Recarregar Nginx
sudo systemctl reload nginx

# Habilitar no boot
sudo systemctl enable nginx
```

### Passo 12: Configurar Firewall

```bash
# Instalar UFW (se não instalado)
sudo apt install ufw -y

# Configurar regras
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'

# Ativar firewall
sudo ufw enable

# Verificar status
sudo ufw status
```

---

## 🐳 Método 2: Deploy com Docker (Recomendado)

### Vantagens do Docker
✅ Isolamento total da aplicação
✅ Deploy consistente em qualquer servidor
✅ Fácil rollback e updates
✅ Escalabilidade simplificada

### Passo 1: Instalar Docker no Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo apt install docker-compose-plugin -y

# Verificar instalação
docker --version
docker compose version
```

### Passo 2: Transferir Projeto

```bash
# Na sua máquina local
cd /home/icolas_atsuda/ProjetosWeb/prova_modelagem_app
tar -czf prova_app.tar.gz --exclude='.venv' --exclude='venv' .

# Transferir
scp prova_app.tar.gz usuario@seu-servidor.com:/opt/

# No servidor
sudo mkdir -p /opt/prova_app
cd /opt/prova_app
sudo tar -xzf /opt/prova_app.tar.gz
```

### Passo 3: Configurar Arquivo .env

```bash
# Criar .env no servidor
sudo nano /opt/prova_app/.env
```

Use o mesmo conteúdo do **Passo 7** do método manual, ajustando:

```bash
DATABASE_URL=postgresql://prova_user:senha@db:5432/prova_modelagem_db
```

### Passo 4: Iniciar Aplicação

```bash
cd /opt/prova_app

# Build e start
sudo docker compose up -d --build

# Ver logs
sudo docker compose logs -f

# Verificar status
sudo docker compose ps
```

### Passo 5: Configurar Nginx (Host)

Use a mesma configuração do **Passo 11** do método manual, mas mude o upstream:

```nginx
upstream prova_app_server {
    server localhost:8000 fail_timeout=0;
}
```

---

## 🔒 Configuração de Domínio e SSL

### Passo 1: Apontar Domínio para o Servidor

No painel do seu provedor de domínio (Registro.br, GoDaddy, etc.):

```
Tipo: A
Nome: @
Valor: SEU_IP_DO_SERVIDOR
TTL: 3600

Tipo: A
Nome: www
Valor: SEU_IP_DO_SERVIDOR
TTL: 3600
```

### Passo 2: Instalar Certbot (Let's Encrypt)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obter certificado SSL
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com

# Renovação automática (já configurada, mas pode testar)
sudo certbot renew --dry-run
```

---

## 💾 Backup e Monitoramento

### Script de Backup Automatizado

```bash
# Criar script de backup
sudo nano /opt/prova_app/scripts/backup.sh
```

```bash
#!/bin/bash
# Backup completo do sistema

BACKUP_DIR="/opt/prova_app/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="prova_modelagem_db"
DB_USER="prova_user"

# Criar diretório se não existir
mkdir -p "$BACKUP_DIR"

# Backup do banco de dados
pg_dump -U $DB_USER -h localhost $DB_NAME | gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

# Backup dos uploads
tar -czf "$BACKUP_DIR/uploads_$DATE.tar.gz" /opt/prova_app/uploads/

# Remover backups antigos (manter últimos 7 dias)
find "$BACKUP_DIR" -name "*.gz" -mtime +7 -delete

echo "Backup concluído: $DATE"
```

```bash
# Tornar executável
sudo chmod +x /opt/prova_app/scripts/backup.sh

# Agendar backup diário (2h da manhã)
sudo crontab -e
```

Adicione:

```cron
0 2 * * * /opt/prova_app/scripts/backup.sh >> /opt/prova_app/logs/backup.log 2>&1
```

### Monitoramento com Systemd

```bash
# Ver logs em tempo real
sudo journalctl -u supervisor -f

# Ver logs do Nginx
sudo tail -f /var/log/nginx/prova_app_access.log
sudo tail -f /var/log/nginx/prova_app_error.log

# Ver logs da aplicação
sudo tail -f /opt/prova_app/logs/app.log
```

---

## 🔧 Manutenção e Troubleshooting

### Comandos Úteis

```bash
# Reiniciar aplicação (Supervisor)
sudo supervisorctl restart prova_app

# Reiniciar aplicação (Docker)
sudo docker compose restart

# Ver status
sudo supervisorctl status
sudo docker compose ps

# Atualizar código
cd /opt/prova_app
git pull origin main
sudo supervisorctl restart prova_app

# Verificar erros
sudo tail -50 /opt/prova_app/logs/gunicorn_error.log
```

### Problemas Comuns

**1. Erro 502 Bad Gateway**
```bash
# Verificar se Gunicorn está rodando
sudo supervisorctl status prova_app
sudo netstat -tlnp | grep 8000
```

**2. Erro de Permissões**
```bash
# Ajustar permissões
sudo chown -R prova_app:prova_app /opt/prova_app
sudo chmod -R 755 /opt/prova_app
```

**3. Erro de Banco de Dados**
```bash
# Verificar PostgreSQL
sudo systemctl status postgresql
sudo -u postgres psql -l
```

---

## ✅ Checklist Final

- [ ] Servidor atualizado
- [ ] PostgreSQL configurado
- [ ] Aplicação transferida
- [ ] Variáveis de ambiente configuradas
- [ ] Banco de dados inicializado
- [ ] Usuário admin criado
- [ ] Gunicorn/Docker rodando
- [ ] Nginx configurado
- [ ] Firewall ativo
- [ ] SSL instalado
- [ ] Backup automatizado
- [ ] Domínio apontando corretamente
- [ ] Acesso HTTPS funcionando

---

## 📞 Suporte

Em caso de problemas:
1. Verifique os logs: `/opt/prova_app/logs/`
2. Teste a conexão: `curl http://localhost:8000`
3. Verifique o firewall: `sudo ufw status`
4. Reinicie os serviços

---

**Deploy criado por Claude Code para Puket**
Última atualização: Dezembro 2024
