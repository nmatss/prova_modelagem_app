# Guia de Deploy - Sistema de Provas de Modelagem

## Índice
1. [Visão Geral](#visão-geral)
2. [Ambientes de Deploy](#ambientes-de-deploy)
3. [Deploy com Docker (Recomendado)](#deploy-com-docker-recomendado)
4. [Deploy Manual (Servidor Linux)](#deploy-manual-servidor-linux)
5. [Deploy de Atualizações](#deploy-de-atualizações)
6. [Rollback](#rollback)
7. [Configuração de SSL/HTTPS](#configuração-de-sslhttps)
8. [Monitoramento](#monitoramento)
9. [Checklist de Deploy](#checklist-de-deploy)

---

## Visão Geral

Este guia cobre todos os cenários de deploy do sistema:

| Método | Complexidade | Tempo Setup | Recomendado Para |
|--------|--------------|-------------|------------------|
| Docker SQLite | Baixa | 10 min | Testes, demos, single-user |
| Docker PostgreSQL | Média | 20 min | Produção, multi-user |
| Manual + Nginx | Alta | 60 min | Servidores dedicados |

---

## Ambientes de Deploy

### 1. Desenvolvimento Local
- **Banco:** SQLite
- **Server:** Flask dev server
- **Porta:** 5000

### 2. Testes/Staging
- **Banco:** SQLite ou PostgreSQL
- **Server:** Gunicorn
- **Porta:** 8000
- **Proxy:** Nginx (opcional)

### 3. Produção
- **Banco:** PostgreSQL
- **Server:** Gunicorn
- **Porta:** 8000
- **Proxy:** Nginx + SSL
- **Process Manager:** Supervisor ou Systemd

---

## Deploy com Docker (Recomendado)

### Opção 1: Deploy Rápido (SQLite)

**Ideal para:** Testes, demonstrações, ambientes de baixo volume

#### Passo 1: Preparar o Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Instalar Docker Compose
sudo apt install docker-compose-plugin

# Verificar instalação
docker --version
docker compose version
```

#### Passo 2: Clonar o Projeto

```bash
# Criar diretório
sudo mkdir -p /opt/prova_app
cd /opt/prova_app

# Clonar repositório (ou fazer upload dos arquivos)
git clone <seu-repo> .
# OU
# scp -r prova_modelagem_app/* user@servidor:/opt/prova_app/
```

#### Passo 3: Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Gerar SECRET_KEY
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" >> .env

# Editar .env
nano .env
```

Configuração mínima para SQLite:
```bash
SECRET_KEY=sua-chave-gerada-aqui-64-caracteres
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=sqlite:////app/data/provas.db
ADMIN_USERNAME=admin
ADMIN_PASSWORD=senha_forte_admin
ADMIN_EMAIL=admin@suaempresa.com
HOST=0.0.0.0
PORT=5000
```

#### Passo 4: Criar Estrutura de Diretórios

```bash
# Criar diretórios
mkdir -p data uploads logs backups

# Ajustar permissões (appuser = UID 1000)
sudo chown -R 1000:1000 data uploads logs backups
chmod -R 755 data uploads logs backups
```

#### Passo 5: Iniciar Aplicação

```bash
# Build e start
docker compose -f docker-compose.sqlite.yml up -d

# Verificar logs
docker compose -f docker-compose.sqlite.yml logs -f

# Verificar status
docker compose -f docker-compose.sqlite.yml ps
```

#### Passo 6: Testar Aplicação

```bash
# Verificar se está respondendo
curl http://localhost:5000

# Verificar health check
curl http://localhost:5000/health

# Acessar via navegador
# http://SEU_IP:5000
```

#### Passo 7: Configurar Firewall

```bash
# Instalar UFW
sudo apt install ufw

# Permitir SSH (importante!)
sudo ufw allow ssh

# Permitir porta da aplicação
sudo ufw allow 5000/tcp

# Habilitar firewall
sudo ufw enable

# Verificar status
sudo ufw status
```

**Tempo total:** ~10 minutos

---

### Opção 2: Deploy Completo (PostgreSQL)

**Ideal para:** Produção, múltiplos usuários, dados críticos

#### Passo 1-2: Igual ao Deploy Rápido

#### Passo 3: Configurar Variáveis de Ambiente

```bash
cp .env.example .env
nano .env
```

Configuração completa para PostgreSQL:
```bash
# Flask
SECRET_KEY=sua-chave-gerada-aqui-64-caracteres
FLASK_ENV=production
FLASK_DEBUG=False

# PostgreSQL
POSTGRES_DB=prova_modelagem_db
POSTGRES_USER=prova_user
POSTGRES_PASSWORD=senha_forte_do_banco
DATABASE_URL=postgresql://prova_user:senha_forte_do_banco@db:5432/prova_modelagem_db

# Admin
ADMIN_USERNAME=admin
ADMIN_PASSWORD=senha_forte_admin
ADMIN_EMAIL=admin@suaempresa.com

# Server
HOST=0.0.0.0
PORT=8000

# Upload
MAX_CONTENT_LENGTH=16777216
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,pdf,xlsx,xls,ppt,pptx

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/app.log

# Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
PERMANENT_SESSION_LIFETIME=3600
RATELIMIT_ENABLED=True

# Workers
WORKERS=2
```

#### Passo 4: Criar Estrutura de Diretórios

```bash
mkdir -p uploads logs backups
sudo chown -R 1000:1000 uploads logs backups
chmod -R 755 uploads logs backups
```

#### Passo 5: Iniciar Aplicação

```bash
# Build das imagens
docker compose build

# Iniciar serviços
docker compose up -d

# Aguardar PostgreSQL ficar pronto (health check)
sleep 10

# Verificar status
docker compose ps

# Ver logs
docker compose logs -f
```

#### Passo 6: Verificar Banco de Dados

```bash
# Conectar ao PostgreSQL
docker compose exec db psql -U prova_user -d prova_modelagem_db

# Dentro do psql:
\dt  # Listar tabelas
\q   # Sair

# Verificar se admin foi criado
docker compose exec web python3 << 'EOF'
from app import app, db
from models import Usuario
with app.app_context():
    admin = Usuario.query.filter_by(username='admin').first()
    print(f"Admin existe: {admin is not None}")
EOF
```

#### Passo 7: Configurar Backups Automáticos

```bash
# Criar script de backup
cp scripts/docker-backup.sh /opt/prova_app/backup.sh
chmod +x /opt/prova_app/backup.sh

# Adicionar ao crontab (backup diário às 2h da manhã)
sudo crontab -e
# Adicionar linha:
0 2 * * * /opt/prova_app/backup.sh >> /var/log/prova_backup.log 2>&1
```

#### Passo 8: Configurar Nginx (Opcional mas Recomendado)

```bash
# Copiar configuração
sudo cp scripts/nginx.conf /etc/nginx/sites-available/prova_app

# Editar configuração
sudo nano /etc/nginx/sites-available/prova_app
# Alterar:
# - server_name (seu domínio)
# - upstream (porta do Gunicorn)

# Criar link simbólico
sudo ln -s /etc/nginx/sites-available/prova_app /etc/nginx/sites-enabled/

# Remover site padrão
sudo rm /etc/nginx/sites-enabled/default

# Testar configuração
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx

# Habilitar no boot
sudo systemctl enable nginx
```

#### Passo 9: Configurar SSL/HTTPS com Let's Encrypt

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d seu-dominio.com.br -d www.seu-dominio.com.br

# Renovação automática (já configurada pelo Certbot)
sudo certbot renew --dry-run
```

**Tempo total:** ~30 minutos

---

## Deploy Manual (Servidor Linux)

### Para Ubuntu/Debian 20.04+

#### Passo 1: Instalar Dependências do Sistema

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python 3.11
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev

# Instalar PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Instalar Nginx
sudo apt install -y nginx

# Instalar bibliotecas para WeasyPrint (geração de PDF)
sudo apt install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info

# Instalar build tools
sudo apt install -y build-essential libpq-dev

# Instalar Supervisor
sudo apt install -y supervisor

# Instalar ferramentas
sudo apt install -y git curl htop
```

#### Passo 2: Configurar PostgreSQL

```bash
# Mudar para usuário postgres
sudo -u postgres psql

# Dentro do psql:
CREATE DATABASE prova_modelagem_db;
CREATE USER prova_user WITH PASSWORD 'senha_forte_aqui';
GRANT ALL PRIVILEGES ON DATABASE prova_modelagem_db TO prova_user;
ALTER DATABASE prova_modelagem_db OWNER TO prova_user;
\q

# Testar conexão
psql -U prova_user -d prova_modelagem_db -h localhost -W
```

#### Passo 3: Criar Usuário da Aplicação

```bash
# Criar usuário sistema
sudo useradd --system --group --home /opt/prova_app --shell /bin/bash prova_app

# Criar diretório
sudo mkdir -p /opt/prova_app
sudo chown prova_app:prova_app /opt/prova_app
```

#### Passo 4: Transferir Código

```bash
# Clonar repositório
sudo -u prova_app git clone <seu-repo> /opt/prova_app
cd /opt/prova_app

# OU fazer upload via SCP
# scp -r prova_modelagem_app/* user@servidor:/tmp/app/
# sudo mv /tmp/app/* /opt/prova_app/
# sudo chown -R prova_app:prova_app /opt/prova_app
```

#### Passo 5: Configurar Virtual Environment

```bash
# Mudar para usuário da app
sudo -u prova_app -s
cd /opt/prova_app

# Criar venv
python3.11 -m venv .venv

# Ativar venv
source .venv/bin/activate

# Atualizar pip
pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt
pip install gunicorn psycopg2-binary weasyprint

# Sair do usuário prova_app
exit
```

#### Passo 6: Configurar Ambiente

```bash
# Criar .env
sudo -u prova_app nano /opt/prova_app/.env
```

Conteúdo:
```bash
SECRET_KEY=sua-chave-64-caracteres
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=postgresql://prova_user:senha_forte_aqui@localhost:5432/prova_modelagem_db
ADMIN_USERNAME=admin
ADMIN_PASSWORD=senha_admin
ADMIN_EMAIL=admin@empresa.com
HOST=0.0.0.0
PORT=8000
LOG_FILE=/opt/prova_app/logs/app.log
```

```bash
# Criar diretórios
sudo -u prova_app mkdir -p /opt/prova_app/{uploads,logs,backups}

# Ajustar permissões
sudo chmod 755 /opt/prova_app/{uploads,logs,backups}
```

#### Passo 7: Inicializar Banco de Dados

```bash
# Executar como usuário prova_app
sudo -u prova_app -s
cd /opt/prova_app
source .venv/bin/activate

# Inicializar banco
python3 << 'EOF'
from app import app, db
from models import Usuario
from werkzeug.security import generate_password_hash
import os

with app.app_context():
    # Criar tabelas
    db.create_all()
    print("Tabelas criadas!")

    # Criar admin
    admin_user = os.getenv('ADMIN_USERNAME', 'admin')
    admin_pass = os.environ['ADMIN_PASSWORD']  # obrigatório — sem fallback hardcoded
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')

    admin = Usuario.query.filter_by(username=admin_user).first()
    if not admin:
        admin = Usuario(
            username=admin_user,
            email=admin_email,
            password_hash=generate_password_hash(admin_pass),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print(f"Admin criado: {admin_user}")
    else:
        print("Admin já existe")
EOF

exit
```

#### Passo 8: Configurar Supervisor

```bash
# Criar arquivo de configuração
sudo nano /etc/supervisor/conf.d/prova_app.conf
```

Conteúdo:
```ini
[program:prova_app]
command=/opt/prova_app/.venv/bin/gunicorn -c /opt/prova_app/gunicorn_config.py app:app
directory=/opt/prova_app
user=prova_app
group=prova_app
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/opt/prova_app/logs/supervisor_error.log
stdout_logfile=/opt/prova_app/logs/supervisor_output.log
environment=PATH="/opt/prova_app/.venv/bin",PYTHONPATH="/opt/prova_app"
```

```bash
# Recarregar Supervisor
sudo supervisorctl reread
sudo supervisorctl update

# Iniciar aplicação
sudo supervisorctl start prova_app

# Verificar status
sudo supervisorctl status prova_app
```

#### Passo 9: Configurar Nginx

```bash
# Criar configuração
sudo nano /etc/nginx/sites-available/prova_app
```

Conteúdo:
```nginx
upstream prova_app {
    server 127.0.0.1:8000 fail_timeout=0;
}

server {
    listen 80;
    server_name seu-dominio.com.br www.seu-dominio.com.br;

    client_max_body_size 20M;
    client_body_timeout 120s;

    access_log /var/log/nginx/provas_app_access.log;
    error_log /var/log/nginx/provas_app_error.log;

    location /static/ {
        alias /opt/prova_app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /uploads/ {
        alias /opt/prova_app/uploads/;
        expires 30d;
        add_header Cache-Control "private";
    }

    location / {
        proxy_pass http://prova_app;
        proxy_redirect off;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }
}
```

```bash
# Criar link simbólico
sudo ln -s /etc/nginx/sites-available/prova_app /etc/nginx/sites-enabled/

# Remover site padrão
sudo rm /etc/nginx/sites-enabled/default

# Testar configuração
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

#### Passo 10: Configurar Firewall

```bash
# Instalar UFW
sudo apt install ufw

# Configurar regras
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'

# Habilitar firewall
sudo ufw enable

# Verificar status
sudo ufw status
```

**Tempo total:** ~60 minutos

---

## Deploy de Atualizações

### Atualização com Docker

#### Método 1: Zero Downtime (Blue-Green)

```bash
cd /opt/prova_app

# Backup antes de atualizar
./scripts/docker-backup.sh

# Pull das mudanças
git pull origin main

# Build nova imagem
docker compose build

# Testar nova imagem localmente
docker compose -f docker-compose.test.yml up -d

# Se OK, fazer deploy
docker compose up -d

# Verificar logs
docker compose logs -f web
```

#### Método 2: Atualização Simples

```bash
cd /opt/prova_app

# Backup
docker compose exec db pg_dump -U prova_user prova_modelagem_db | gzip > backups/db_$(date +%Y%m%d_%H%M%S).sql.gz

# Pull das mudanças
git pull

# Rebuild e restart
docker compose up -d --build

# Verificar
docker compose ps
docker compose logs -f
```

### Atualização Manual

```bash
cd /opt/prova_app

# Backup do banco
sudo -u postgres pg_dump prova_modelagem_db | gzip > backups/db_$(date +%Y%m%d_%H%M%S).sql.gz

# Backup dos uploads
tar -czf backups/uploads_$(date +%Y%m%d_%H%M%S).tar.gz uploads/

# Parar aplicação
sudo supervisorctl stop prova_app

# Atualizar código
sudo -u prova_app git pull

# Atualizar dependências
sudo -u prova_app -s
cd /opt/prova_app
source .venv/bin/activate
pip install -r requirements.txt --upgrade
exit

# Executar migrações (se houver)
sudo -u prova_app -s
cd /opt/prova_app
source .venv/bin/activate
python3 migrate_db.py
exit

# Reiniciar aplicação
sudo supervisorctl start prova_app

# Verificar logs
sudo supervisorctl tail -f prova_app stdout
```

### Atualização via Script Automatizado

```bash
# Usar script de deploy
sudo /opt/prova_app/scripts/deploy.sh update

# Ver logs
sudo /opt/prova_app/scripts/deploy.sh logs
```

---

## Rollback

### Rollback com Docker

```bash
cd /opt/prova_app

# Parar serviços
docker compose down

# Restaurar backup do banco
docker compose up -d db
sleep 5

# Listar backups
ls -lh backups/db_*.sql.gz

# Restaurar backup específico
gunzip < backups/db_20250116_140000.sql.gz | \
docker compose exec -T db psql -U prova_user -d prova_modelagem_db

# Restaurar uploads
tar -xzf backups/uploads_20250116_140000.tar.gz

# Voltar para versão anterior do código
git log --oneline -10
git checkout <commit-hash-anterior>

# Rebuild e restart
docker compose up -d --build

# Verificar
docker compose ps
docker compose logs -f
```

### Rollback Manual

```bash
cd /opt/prova_app

# Parar aplicação
sudo supervisorctl stop prova_app

# Restaurar código
sudo -u prova_app git reset --hard <commit-anterior>

# Restaurar banco
sudo -u postgres psql prova_modelagem_db < backups/db_backup.sql

# Restaurar uploads
sudo -u prova_app tar -xzf backups/uploads_backup.tar.gz -C /opt/prova_app

# Reiniciar
sudo supervisorctl start prova_app
```

---

## Configuração de SSL/HTTPS

### Let's Encrypt (Gratuito)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com

# Testar renovação automática
sudo certbot renew --dry-run

# Renovação é automática via cron
sudo cat /etc/cron.d/certbot
```

### Certificado Próprio

```bash
# Gerar chave e CSR
sudo openssl req -new -newkey rsa:2048 -nodes \
  -keyout /etc/ssl/private/prova_app.key \
  -out /etc/ssl/certs/prova_app.csr

# Enviar CSR para autoridade certificadora
# Receber certificado assinado

# Configurar Nginx
sudo nano /etc/nginx/sites-available/prova_app
```

Adicionar:
```nginx
server {
    listen 443 ssl http2;
    server_name seu-dominio.com;

    ssl_certificate /etc/ssl/certs/prova_app.crt;
    ssl_certificate_key /etc/ssl/private/prova_app.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # ... resto da configuração
}

# Redirecionar HTTP para HTTPS
server {
    listen 80;
    server_name seu-dominio.com;
    return 301 https://$server_name$request_uri;
}
```

---

## Monitoramento

### Logs

```bash
# Docker
docker compose logs -f web
docker compose logs --tail=100 web

# Manual
sudo tail -f /opt/prova_app/logs/app.log
sudo tail -f /opt/prova_app/logs/error.log
sudo supervisorctl tail -f prova_app stdout

# Nginx
sudo tail -f /var/log/nginx/provas_app_access.log
sudo tail -f /var/log/nginx/provas_app_error.log
```

### Status dos Serviços

```bash
# Docker
docker compose ps
docker stats

# Manual
sudo supervisorctl status prova_app
sudo systemctl status nginx
sudo systemctl status postgresql

# Sistema
htop
df -h
free -m
```

### Health Checks

```bash
# Endpoint de health
curl http://localhost:8000/health

# Verificar resposta completa
curl -I http://localhost:8000/

# Testar login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"sua_senha"}'
```

---

## Checklist de Deploy

### Pré-Deploy

- [ ] Backup do banco de dados realizado
- [ ] Backup dos uploads realizado
- [ ] Backup do .env realizado
- [ ] Código testado em ambiente de staging
- [ ] Dependências atualizadas no requirements.txt
- [ ] Migrações de banco testadas
- [ ] Documentação atualizada

### Durante Deploy

- [ ] Serviços parados corretamente
- [ ] Código atualizado (git pull ou upload)
- [ ] Dependências instaladas
- [ ] Migrações executadas
- [ ] Permissões de arquivos verificadas
- [ ] Serviços reiniciados
- [ ] Logs verificados (sem erros críticos)

### Pós-Deploy

- [ ] Aplicação acessível via navegador
- [ ] Login funcionando
- [ ] Upload de arquivos testado
- [ ] Geração de PDF testada
- [ ] Relatórios funcionando
- [ ] Health check respondendo
- [ ] Monitoramento ativo
- [ ] Backup automático configurado
- [ ] Equipe notificada

### Segurança

- [ ] SECRET_KEY forte configurada
- [ ] Senhas de admin alteradas
- [ ] Firewall configurado
- [ ] SSL/HTTPS ativo (produção)
- [ ] PostgreSQL não exposto
- [ ] Logs protegidos (permissions)
- [ ] Backups criptografados (se necessário)

---

## Comandos Úteis de Administração

```bash
# Ver todos os processos Python
ps aux | grep python

# Ver todas as conexões na porta 8000
sudo netstat -tulpn | grep 8000

# Ver tamanho dos diretórios
du -sh /opt/prova_app/*

# Limpar logs antigos (mais de 30 dias)
find /opt/prova_app/logs -name "*.log" -mtime +30 -delete

# Backup rápido manual
tar -czf /tmp/prova_app_backup_$(date +%Y%m%d).tar.gz \
  --exclude='.venv' \
  --exclude='*.pyc' \
  /opt/prova_app

# Verificar uso de memória da aplicação
ps aux | grep gunicorn | awk '{sum+=$6} END {print sum/1024 " MB"}'

# Reiniciar todos os serviços (Docker)
docker compose restart

# Reiniciar todos os serviços (Manual)
sudo supervisorctl restart prova_app
sudo systemctl restart nginx
```

---

## Suporte e Troubleshooting

Para problemas específicos, consulte:
- [DOCKER_GUIDE.md](DOCKER_GUIDE.md) - Troubleshooting de Docker
- [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md) - Operações de manutenção
- Logs da aplicação em `/opt/prova_app/logs/`
