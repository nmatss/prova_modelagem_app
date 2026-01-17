# 🚀 Documentação de Instalação e Configuração
# Sistema de Gestão de Provas de Modelagem

**Versão:** 1.0
**Data:** 03/12/2025
**Autor:** Equipe de Desenvolvimento

---

## 📋 Índice

1. [Requisitos do Sistema](#requisitos-do-sistema)
2. [Instalação em Desenvolvimento](#instalação-em-desenvolvimento)
3. [Instalação em Produção](#instalação-em-produção)
4. [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
5. [Variáveis de Ambiente](#variáveis-de-ambiente)
6. [Inicialização do Sistema](#inicialização-do-sistema)
7. [Criação de Usuário Administrador](#criação-de-usuário-administrador)
8. [Troubleshooting](#troubleshooting)
9. [Upgrade e Manutenção](#upgrade-e-manutenção)

---

## 💻 Requisitos do Sistema

### Requisitos Mínimos

| Componente | Desenvolvimento | Produção |
|------------|----------------|----------|
| **Sistema Operacional** | Linux, Windows, macOS | Linux (Ubuntu 20.04+ / CentOS 8+) |
| **Python** | 3.11+ | 3.11+ |
| **RAM** | 2 GB | 4 GB |
| **Disco** | 5 GB | 20 GB (+ espaço para uploads) |
| **CPU** | 2 cores | 4 cores |
| **Banco de Dados** | SQLite (incluído) | PostgreSQL 14+ |
| **Servidor Web** | Flask dev server | Nginx + Gunicorn |

### Dependências de Sistema

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    postgresql \
    postgresql-contrib \
    libpq-dev \
    nginx \
    git
```

#### CentOS/RHEL
```bash
sudo yum install -y \
    python311 \
    python311-devel \
    python311-pip \
    postgresql14-server \
    postgresql14-contrib \
    postgresql14-devel \
    nginx \
    git
```

#### Windows
```powershell
# Instalar Python 3.11+ do site oficial: https://www.python.org/downloads/
# Verificar instalação
python --version

# Instalar PostgreSQL do site oficial (produção): https://www.postgresql.org/download/windows/
```

#### macOS
```bash
# Instalar Homebrew se não tiver: https://brew.sh/
brew install python@3.11
brew install postgresql@14
brew install nginx
```

---

## 🛠️ Instalação em Desenvolvimento

### 1. Clonar o Repositório

```bash
# Clone o repositório (ou baixe o código)
git clone https://github.com/seu-usuario/prova_modelagem_app.git
cd prova_modelagem_app
```

### 2. Criar Ambiente Virtual

```bash
# Criar virtual environment
python3 -m venv .venv

# Ativar virtual environment
# Linux/macOS:
source .venv/bin/activate

# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# Windows (CMD):
.venv\Scripts\activate.bat
```

### 3. Instalar Dependências

```bash
# Atualizar pip
pip install --upgrade pip

# Instalar dependências do projeto
pip install -r requirements.txt
```

**Conteúdo do `requirements.txt`:**
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.0.1
xhtml2pdf==0.2.11
python-dotenv==1.0.0
openpyxl==3.1.2
Pillow==10.1.0
requests==2.31.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

### 4. Configurar Variáveis de Ambiente

```bash
# Criar arquivo .env na raiz do projeto
touch .env
```

**Conteúdo mínimo do `.env` (desenvolvimento):**
```env
# Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production

# Database (SQLite para dev)
DATABASE_URL=sqlite:///instance/provas.db

# Upload
MAX_CONTENT_LENGTH=16777216
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,pdf,xlsx,xls,ppt,pptx

# Logging
LOG_LEVEL=DEBUG
```

### 5. Inicializar Banco de Dados

```bash
# Criar banco de dados e tabelas
python init_db.py

# Saída esperada:
# ✅ Banco de dados criado com sucesso!
# ✅ Tabelas criadas: usuarios, relatorios, referencias, provas_modelagem, fotos_provas, historico_status, audit_logs, configuracoes_sistema
```

### 6. Criar Usuário Administrador

```bash
# Criar primeiro usuário admin
python create_test_user.py

# Ou criar manualmente:
python -c "
from app import app
from models import db, Usuario
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = Usuario(
        username='admin',
        password_hash=generate_password_hash('admin123'),
        email='admin@empresa.com',
        nome_completo='Administrador',
        role='admin',
        is_admin=True,
        is_active=True
    )
    db.session.add(admin)
    db.session.commit()
    print('✅ Usuário admin criado!')
"
```

**Credenciais padrão:**
- **Usuário:** `admin`
- **Senha:** `admin123`
- ⚠️ **IMPORTANTE:** Alterar senha após primeiro login!

### 7. Executar Aplicação

```bash
# Executar servidor de desenvolvimento
python app.py

# Saída esperada:
#  * Running on http://127.0.0.1:5000
#  * Debug mode: on
```

### 8. Acessar o Sistema

```
URL: http://127.0.0.1:5000
Usuário: admin
Senha: admin123
```

---

## 🏭 Instalação em Produção

### Arquitetura de Produção

```
Internet → Nginx (80/443) → Gunicorn (Socket) → Flask App → PostgreSQL
                                                          ↓
                                                    File System
                                                    (uploads/)
```

### 1. Preparar Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Criar usuário para aplicação
sudo useradd -m -s /bin/bash provaapp
sudo usermod -aG www-data provaapp

# Criar diretórios
sudo mkdir -p /var/www/prova_modelagem_app
sudo chown provaapp:www-data /var/www/prova_modelagem_app
```

### 2. Clonar Aplicação

```bash
# Mudar para usuário da aplicação
sudo su - provaapp

# Clonar código
cd /var/www/prova_modelagem_app
git clone https://github.com/seu-usuario/prova_modelagem_app.git .

# Criar virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configurar PostgreSQL

```bash
# Mudar para usuário postgres
sudo su - postgres

# Criar banco de dados e usuário
psql

-- No prompt do PostgreSQL:
CREATE DATABASE prova_modelagem;
CREATE USER provaapp WITH PASSWORD 'SenhaSegura123!@#';
GRANT ALL PRIVILEGES ON DATABASE prova_modelagem TO provaapp;
\q

# Voltar para usuário provaapp
exit
```

### 4. Configurar Variáveis de Ambiente (.env)

```bash
# Criar arquivo .env (produção)
sudo nano /var/www/prova_modelagem_app/.env
```

**Conteúdo do `.env` (produção):**
```env
# Flask
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=GERE_UMA_CHAVE_FORTE_AQUI_64_CARACTERES_MINIMO

# Database
DATABASE_URL=postgresql://provaapp:SenhaSegura123!@#@localhost:5432/prova_modelagem

# Upload
MAX_CONTENT_LENGTH=16777216
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,pdf,xlsx,xls,ppt,pptx

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/prova_modelagem/app.log

# Security
SESSION_COOKIE_SECURE=True
```

**Gerar SECRET_KEY forte:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Inicializar Banco de Dados

```bash
# Como usuário provaapp
cd /var/www/prova_modelagem_app
source .venv/bin/activate

# Inicializar banco
python init_db.py

# Criar usuário admin
python create_test_user.py
```

### 6. Criar Diretórios de Logs e Uploads

```bash
# Criar diretórios
sudo mkdir -p /var/log/prova_modelagem
sudo mkdir -p /var/www/prova_modelagem_app/uploads/fotos
sudo mkdir -p /var/www/prova_modelagem_app/uploads/tabelas
sudo mkdir -p /var/www/prova_modelagem_app/uploads/ppts
sudo mkdir -p /var/www/prova_modelagem_app/relatorios_pdf

# Ajustar permissões
sudo chown -R provaapp:www-data /var/log/prova_modelagem
sudo chown -R provaapp:www-data /var/www/prova_modelagem_app/uploads
sudo chown -R provaapp:www-data /var/www/prova_modelagem_app/relatorios_pdf

sudo chmod -R 755 /var/www/prova_modelagem_app/uploads
sudo chmod -R 755 /var/www/prova_modelagem_app/relatorios_pdf
```

### 7. Configurar Gunicorn

**Criar arquivo `gunicorn_config.py` (já existe no projeto):**
```python
# gunicorn_config.py
bind = "unix:/var/www/prova_modelagem_app/prova_modelagem.sock"
workers = 4  # 2 * CPU cores + 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = "/var/log/prova_modelagem/gunicorn_access.log"
errorlog = "/var/log/prova_modelagem/gunicorn_error.log"
loglevel = "info"

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Process naming
proc_name = "prova_modelagem"

# Server mechanics
daemon = False
pidfile = "/var/www/prova_modelagem_app/gunicorn.pid"
user = "provaapp"
group = "www-data"
```

### 8. Configurar Systemd Service

**Criar arquivo `/etc/systemd/system/prova_modelagem.service`:**
```ini
[Unit]
Description=Gunicorn instance to serve Prova Modelagem App
After=network.target

[Service]
Type=notify
User=provaapp
Group=www-data
WorkingDirectory=/var/www/prova_modelagem_app
Environment="PATH=/var/www/prova_modelagem_app/.venv/bin"
ExecStart=/var/www/prova_modelagem_app/.venv/bin/gunicorn \
          --config gunicorn_config.py \
          wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

# Restart
Restart=always
RestartSec=10

# Security
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/www/prova_modelagem_app/uploads /var/www/prova_modelagem_app/relatorios_pdf /var/log/prova_modelagem

[Install]
WantedBy=multi-user.target
```

**Habilitar e iniciar serviço:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable prova_modelagem
sudo systemctl start prova_modelagem

# Verificar status
sudo systemctl status prova_modelagem
```

### 9. Configurar Nginx

**Criar arquivo `/etc/nginx/sites-available/prova_modelagem`:**
```nginx
upstream prova_modelagem {
    server unix:/var/www/prova_modelagem_app/prova_modelagem.sock fail_timeout=0;
}

server {
    listen 80;
    server_name seu-dominio.com.br www.seu-dominio.com.br;

    # Redirect HTTP to HTTPS (depois de configurar SSL)
    # return 301 https://$server_name$request_uri;

    client_max_body_size 50M;

    # Logs
    access_log /var/log/nginx/prova_modelagem_access.log;
    error_log /var/log/nginx/prova_modelagem_error.log;

    # Static files
    location /static/ {
        alias /var/www/prova_modelagem_app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Uploads (servir com autenticação via X-Accel)
    location /uploads/ {
        internal;
        alias /var/www/prova_modelagem_app/uploads/;
    }

    # Application
    location / {
        proxy_pass http://prova_modelagem;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_buffering off;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

**Habilitar site:**
```bash
sudo ln -s /etc/nginx/sites-available/prova_modelagem /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 10. Configurar SSL com Let's Encrypt (Recomendado)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado SSL
sudo certbot --nginx -d seu-dominio.com.br -d www.seu-dominio.com.br

# Certificado será renovado automaticamente
sudo systemctl status certbot.timer
```

### 11. Configurar Firewall

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow from 192.168.0.0/16 to any port 5432  # PostgreSQL (rede interna)
sudo ufw enable
```

### 12. Verificar Instalação

```bash
# Verificar serviço
sudo systemctl status prova_modelagem

# Verificar logs
sudo tail -f /var/log/prova_modelagem/gunicorn_error.log

# Testar aplicação
curl http://localhost/
```

---

## 🗄️ Configuração do Banco de Dados

### SQLite (Desenvolvimento)

SQLite é usado automaticamente em desenvolvimento. Nenhuma configuração adicional necessária.

```python
# config.py
SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/provas.db'
```

**Localização do arquivo:**
```
prova_modelagem_app/instance/provas.db
```

### PostgreSQL (Produção)

#### Instalação PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt install postgresql postgresql-contrib
```

**CentOS/RHEL:**
```bash
sudo yum install postgresql14-server postgresql14-contrib
sudo /usr/pgsql-14/bin/postgresql-14-setup initdb
```

#### Configuração Inicial

```bash
# Iniciar serviço
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Acessar PostgreSQL
sudo su - postgres
psql
```

#### Criar Banco de Dados

```sql
-- Criar database
CREATE DATABASE prova_modelagem
    WITH
    OWNER = provaapp
    ENCODING = 'UTF8'
    LC_COLLATE = 'pt_BR.UTF-8'
    LC_CTYPE = 'pt_BR.UTF-8'
    TEMPLATE = template0;

-- Criar usuário
CREATE USER provaapp WITH PASSWORD 'SenhaForte123!@#';

-- Conceder privilégios
GRANT ALL PRIVILEGES ON DATABASE prova_modelagem TO provaapp;

-- Conectar ao banco
\c prova_modelagem

-- Conceder privilégios no schema public
GRANT ALL ON SCHEMA public TO provaapp;

-- Sair
\q
```

#### Configurar Autenticação (pg_hba.conf)

```bash
# Editar arquivo de configuração
sudo nano /etc/postgresql/14/main/pg_hba.conf
```

**Adicionar linha:**
```
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   prova_modelagem provaapp                                md5
host    prova_modelagem provaapp        127.0.0.1/32            md5
host    prova_modelagem provaapp        ::1/128                 md5
```

**Reiniciar PostgreSQL:**
```bash
sudo systemctl restart postgresql
```

#### Testar Conexão

```bash
# Testar conexão
psql -h localhost -U provaapp -d prova_modelagem

# Senha: SenhaForte123!@#
```

#### Connection String

```env
# .env
DATABASE_URL=postgresql://provaapp:SenhaForte123!@#@localhost:5432/prova_modelagem
```

### Migração SQLite → PostgreSQL

```bash
# 1. Fazer backup do SQLite
cp instance/provas.db instance/provas.db.backup

# 2. Exportar dados do SQLite
python -c "
from app import app
from models import db, Usuario, Relatorio, Referencia, ProvaModelagem
import json

with app.app_context():
    # Exportar usuários
    usuarios = Usuario.query.all()
    with open('backup_usuarios.json', 'w') as f:
        json.dump([{
            'username': u.username,
            'password_hash': u.password_hash,
            'email': u.email,
            'role': u.role
        } for u in usuarios], f)

    print('✅ Backup realizado!')
"

# 3. Alterar .env para PostgreSQL
nano .env
# DATABASE_URL=postgresql://...

# 4. Inicializar banco PostgreSQL
python init_db.py

# 5. Importar dados
python migrate_to_postgres.py
```

---

## 🔐 Variáveis de Ambiente

### Arquivo .env Completo

```env
# ====================================
# FLASK CONFIGURATION
# ====================================
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=gere_uma_chave_forte_aqui_com_pelo_menos_64_caracteres

# ====================================
# DATABASE
# ====================================
# Desenvolvimento (SQLite)
# DATABASE_URL=sqlite:///instance/provas.db

# Produção (PostgreSQL)
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_banco

# ====================================
# UPLOAD CONFIGURATION
# ====================================
MAX_CONTENT_LENGTH=16777216
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,pdf,xlsx,xls,ppt,pptx

# ====================================
# LOGGING
# ====================================
LOG_LEVEL=INFO
LOG_FILE=/var/log/prova_modelagem/app.log

# ====================================
# SECURITY
# ====================================
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
PERMANENT_SESSION_LIFETIME=43200

# ====================================
# EMAIL (Futuro)
# ====================================
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USE_TLS=True
# MAIL_USERNAME=seu_email@gmail.com
# MAIL_PASSWORD=sua_senha_app
```

### Descrição das Variáveis

| Variável | Tipo | Padrão | Descrição |
|----------|------|--------|-----------|
| `FLASK_ENV` | string | development | Ambiente (development/production) |
| `FLASK_DEBUG` | boolean | False | Modo debug (NUNCA True em produção) |
| `SECRET_KEY` | string | - | Chave secreta para sessões (OBRIGATÓRIO) |
| `DATABASE_URL` | string | sqlite:/// | Connection string do banco |
| `MAX_CONTENT_LENGTH` | int | 16777216 | Tamanho máximo upload (bytes) |
| `ALLOWED_EXTENSIONS` | string | png,jpg,... | Extensões permitidas (separadas por vírgula) |
| `LOG_LEVEL` | string | INFO | Nível de log (DEBUG/INFO/WARNING/ERROR) |
| `LOG_FILE` | string | None | Caminho do arquivo de log |
| `SESSION_COOKIE_SECURE` | boolean | False | HTTPS obrigatório para cookies |

### Validação de Variáveis

```bash
# Verificar se .env está configurado corretamente
python -c "
from dotenv import load_dotenv
import os

load_dotenv()

required_vars = ['SECRET_KEY', 'DATABASE_URL']
missing = [var for var in required_vars if not os.getenv(var)]

if missing:
    print(f'❌ Variáveis faltando: {missing}')
else:
    print('✅ Todas as variáveis obrigatórias estão configuradas!')
"
```

---

## 🎬 Inicialização do Sistema

### Primeiro Uso

```bash
# 1. Ativar ambiente virtual
source .venv/bin/activate

# 2. Criar banco de dados
python init_db.py

# 3. Criar usuário admin
python create_test_user.py

# 4. Executar aplicação
python app.py
```

### Desenvolvimento

```bash
# Modo desenvolvimento (auto-reload)
python app.py

# Ou com variável de ambiente
FLASK_DEBUG=True python app.py
```

### Produção

```bash
# Via systemd (recomendado)
sudo systemctl start prova_modelagem
sudo systemctl status prova_modelagem

# Manual (não recomendado)
gunicorn --config gunicorn_config.py wsgi:application
```

### Verificação de Saúde

```bash
# Verificar se aplicação está respondendo
curl http://localhost/

# Verificar logs
tail -f /var/log/prova_modelagem/gunicorn_error.log

# Verificar processos
ps aux | grep gunicorn
```

---

## 👤 Criação de Usuário Administrador

### Método 1: Script Automático

```bash
python create_test_user.py
```

**Usuário criado:**
- Username: `admin`
- Senha: `admin123`
- Role: `admin`
- Email: `admin@empresa.com`

### Método 2: Console Interativo

```bash
python -c "
from app import app
from models import db, Usuario
from werkzeug.security import generate_password_hash

with app.app_context():
    username = input('Username: ')
    password = input('Senha: ')
    email = input('Email: ')
    nome = input('Nome Completo: ')

    usuario = Usuario(
        username=username,
        password_hash=generate_password_hash(password),
        email=email,
        nome_completo=nome,
        role='admin',
        is_admin=True,
        is_active=True
    )

    db.session.add(usuario)
    db.session.commit()

    print(f'✅ Usuário {username} criado com sucesso!')
"
```

### Método 3: Via Interface Web (após primeiro admin criado)

1. Login com admin
2. Menu → Administração → Usuários
3. Botão "Criar Novo Usuário"
4. Preencher formulário
5. Selecionar role "admin"
6. Salvar

---

## 🔧 Troubleshooting

### Problemas Comuns

#### 1. Erro: "No module named 'flask'"

**Causa:** Virtual environment não ativado ou dependências não instaladas.

**Solução:**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

#### 2. Erro: "sqlite3.OperationalError: unable to open database file"

**Causa:** Diretório `instance/` não existe.

**Solução:**
```bash
mkdir -p instance
python init_db.py
```

#### 3. Erro: "Permission denied: '/var/log/prova_modelagem/app.log'"

**Causa:** Usuário não tem permissão para escrever no diretório de logs.

**Solução:**
```bash
sudo mkdir -p /var/log/prova_modelagem
sudo chown provaapp:www-data /var/log/prova_modelagem
sudo chmod 755 /var/log/prova_modelagem
```

#### 4. Erro: "502 Bad Gateway" (Nginx)

**Causa:** Gunicorn não está rodando ou socket não existe.

**Solução:**
```bash
# Verificar se Gunicorn está rodando
sudo systemctl status prova_modelagem

# Verificar se socket existe
ls -la /var/www/prova_modelagem_app/prova_modelagem.sock

# Reiniciar serviço
sudo systemctl restart prova_modelagem
```

#### 5. Erro: "CSRF token missing or invalid"

**Causa:** Cookie de sessão não está sendo enviado ou SECRET_KEY mudou.

**Solução:**
```bash
# Limpar cookies do navegador
# Ou fazer logout e login novamente

# Verificar SECRET_KEY no .env
grep SECRET_KEY .env
```

#### 6. Erro: "psycopg2.OperationalError: FATAL: password authentication failed"

**Causa:** Credenciais PostgreSQL incorretas.

**Solução:**
```bash
# Verificar connection string
grep DATABASE_URL .env

# Testar conexão manualmente
psql -h localhost -U provaapp -d prova_modelagem

# Resetar senha do usuário PostgreSQL
sudo su - postgres
psql
ALTER USER provaapp WITH PASSWORD 'nova_senha';
\q
```

#### 7. Upload de Arquivo Falha (413 Request Entity Too Large)

**Causa:** Arquivo excede limite configurado.

**Solução:**
```bash
# Aumentar limite no .env
echo "MAX_CONTENT_LENGTH=52428800" >> .env  # 50MB

# Aumentar limite no Nginx
sudo nano /etc/nginx/sites-available/prova_modelagem
# Adicionar: client_max_body_size 50M;

sudo systemctl restart nginx
sudo systemctl restart prova_modelagem
```

### Logs para Debug

```bash
# Logs da aplicação
tail -f /var/log/prova_modelagem/app.log

# Logs do Gunicorn
tail -f /var/log/prova_modelagem/gunicorn_error.log
tail -f /var/log/prova_modelagem/gunicorn_access.log

# Logs do Nginx
sudo tail -f /var/log/nginx/prova_modelagem_error.log
sudo tail -f /var/log/nginx/prova_modelagem_access.log

# Logs do sistema (systemd)
sudo journalctl -u prova_modelagem -f
```

---

## 🔄 Upgrade e Manutenção

### Atualização da Aplicação

```bash
# 1. Fazer backup do banco de dados
sudo su - provaapp
cd /var/www/prova_modelagem_app

# Backup SQLite
cp instance/provas.db instance/provas.db.backup

# Backup PostgreSQL
pg_dump -h localhost -U provaapp prova_modelagem > backup_$(date +%Y%m%d).sql

# 2. Parar aplicação
sudo systemctl stop prova_modelagem

# 3. Atualizar código
git pull origin main

# 4. Ativar virtual environment
source .venv/bin/activate

# 5. Atualizar dependências
pip install --upgrade -r requirements.txt

# 6. Executar migrações (se houver)
python migrate_db.py

# 7. Reiniciar aplicação
sudo systemctl start prova_modelagem

# 8. Verificar
sudo systemctl status prova_modelagem
```

### Backup Automático (Cron)

```bash
# Criar script de backup
sudo nano /usr/local/bin/backup_prova_modelagem.sh
```

**Conteúdo:**
```bash
#!/bin/bash

BACKUP_DIR="/var/backups/prova_modelagem"
DATE=$(date +%Y%m%d_%H%M%S)

# Criar diretório de backup
mkdir -p $BACKUP_DIR

# Backup PostgreSQL
pg_dump -h localhost -U provaapp prova_modelagem | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup uploads
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz /var/www/prova_modelagem_app/uploads/

# Remover backups antigos (manter últimos 30 dias)
find $BACKUP_DIR -type f -mtime +30 -delete

echo "✅ Backup concluído: $DATE"
```

**Tornar executável:**
```bash
sudo chmod +x /usr/local/bin/backup_prova_modelagem.sh
```

**Adicionar ao cron:**
```bash
sudo crontab -e

# Adicionar linha (backup diário às 2h da manhã):
0 2 * * * /usr/local/bin/backup_prova_modelagem.sh >> /var/log/prova_modelagem/backup.log 2>&1
```

### Monitoramento

```bash
# Instalar htop para monitoramento
sudo apt install htop

# Monitorar recursos
htop

# Monitorar espaço em disco
df -h

# Monitorar uso de memória
free -h

# Monitorar processos da aplicação
ps aux | grep gunicorn
```

### Limpeza de Arquivos Temporários

```bash
# Criar script de limpeza
sudo nano /usr/local/bin/cleanup_prova_modelagem.sh
```

**Conteúdo:**
```bash
#!/bin/bash

# Remover PDFs antigos (mais de 7 dias)
find /var/www/prova_modelagem_app/relatorios_pdf -type f -mtime +7 -delete

# Limpar logs antigos
find /var/log/prova_modelagem -type f -name "*.log.*" -mtime +30 -delete

# Rodar VACUUM no SQLite (se usar)
# sqlite3 /var/www/prova_modelagem_app/instance/provas.db "VACUUM;"

# PostgreSQL VACUUM
PGPASSWORD="senha" psql -h localhost -U provaapp -d prova_modelagem -c "VACUUM ANALYZE;"

echo "✅ Limpeza concluída: $(date)"
```

**Executável + Cron:**
```bash
sudo chmod +x /usr/local/bin/cleanup_prova_modelagem.sh

sudo crontab -e
# Adicionar: limpeza semanal (domingos às 3h)
0 3 * * 0 /usr/local/bin/cleanup_prova_modelagem.sh >> /var/log/prova_modelagem/cleanup.log 2>&1
```

---

## 📞 Suporte

**Documentação Relacionada:**
- `README.md` - Visão geral do projeto
- `DOCUMENTACAO_ARQUITETURA.md` - Arquitetura do sistema
- `RELATORIO_SEGURANCA.md` - Segurança
- `DEPLOY.md` - Deploy detalhado

**Comandos Úteis:**

```bash
# Verificar versão Python
python --version

# Verificar pacotes instalados
pip list

# Verificar status de todos os serviços
sudo systemctl status prova_modelagem nginx postgresql

# Reiniciar tudo
sudo systemctl restart prova_modelagem nginx postgresql

# Logs em tempo real
sudo tail -f /var/log/prova_modelagem/*.log /var/log/nginx/*.log
```

---

**Última Atualização:** 03/12/2025
**Versão:** 1.0
