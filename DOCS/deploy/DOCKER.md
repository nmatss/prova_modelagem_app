# Guia Completo de Docker - Sistema de Provas de Modelagem

## Índice
1. [Visão Geral](#visão-geral)
2. [Arquitetura Docker](#arquitetura-docker)
3. [Pré-requisitos](#pré-requisitos)
4. [Dockerfile Multi-Stage](#dockerfile-multi-stage)
5. [Docker Compose](#docker-compose)
6. [Variáveis de Ambiente](#variáveis-de-ambiente)
7. [Volumes e Persistência](#volumes-e-persistência)
8. [Rede e Segurança](#rede-e-segurança)
9. [Build e Execução](#build-e-execução)
10. [Troubleshooting](#troubleshooting)

---

## Visão Geral

O Sistema de Provas de Modelagem utiliza Docker para garantir portabilidade, isolamento e facilidade de deploy. A arquitetura suporta dois modos:

- **Modo SQLite** (desenvolvimento/teste): Banco de dados em arquivo local
- **Modo PostgreSQL** (produção): Banco de dados em container separado

### Características

- **Multi-stage build**: Otimização de tamanho da imagem
- **Non-root user**: Segurança aprimorada
- **Health checks**: Monitoramento automático
- **Hot reload**: Suporte a desenvolvimento local
- **Resource limits**: Controle de recursos de CPU e memória

---

## Arquitetura Docker

```
┌─────────────────────────────────────────┐
│  Docker Compose                         │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────┐    ┌───────────────┐  │
│  │   Nginx     │───▶│  Flask App    │  │
│  │  (Opcional) │    │  (Gunicorn)   │  │
│  └─────────────┘    └───────┬───────┘  │
│                             │          │
│                     ┌───────▼───────┐  │
│                     │   PostgreSQL  │  │
│                     │   (Opcional)  │  │
│                     └───────────────┘  │
│                                         │
│  Volumes:                               │
│  - uploads/  (arquivos enviados)        │
│  - logs/     (logs da aplicação)        │
│  - data/     (banco SQLite)             │
│  - backups/  (backups automáticos)      │
└─────────────────────────────────────────┘
```

---

## Pré-requisitos

### Software Necessário

```bash
# Docker Engine
docker --version  # >= 20.10.0

# Docker Compose
docker compose version  # >= 2.0.0

# Git (para clonar o repositório)
git --version
```

### Instalação do Docker

**Ubuntu/Debian:**
```bash
# Remover versões antigas
sudo apt remove docker docker-engine docker.io containerd runc

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
newgrp docker

# Instalar Docker Compose
sudo apt install docker-compose-plugin

# Verificar instalação
docker --version
docker compose version
```

**CentOS/RHEL:**
```bash
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo systemctl start docker
sudo systemctl enable docker
```

---

## Dockerfile Multi-Stage

O sistema utiliza um Dockerfile multi-stage para otimizar o tamanho da imagem:

### Stage 1: Builder (Compilação)

```dockerfile
FROM python:3.11-slim AS builder

# Instala dependências de build (gcc, libpq-dev, etc)
# Compila pacotes Python com extensões nativas
# Instala tudo em /root/.local
```

**Propósito:** Compilar dependências Python que requerem bibliotecas de desenvolvimento (psycopg2, weasyprint, etc).

### Stage 2: Runtime (Execução)

```dockerfile
FROM python:3.11-slim

# Copia apenas os pacotes compilados do builder
# Instala apenas bibliotecas de runtime
# Cria usuário não-root (appuser)
# Configura workdir, volumes e health checks
```

**Propósito:** Imagem final leve, contendo apenas o necessário para execução.

### Benefícios do Multi-Stage

- **Tamanho reduzido**: ~400MB vs ~1.2GB (sem multi-stage)
- **Segurança**: Sem ferramentas de compilação na imagem final
- **Performance**: Cache otimizado para builds incrementais

### Estrutura do Dockerfile

```dockerfile
# ==================================
# Stage 1: Builder
# ==================================
FROM python:3.11-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Dependências de build
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libpq-dev libcairo2-dev libpango1.0-dev \
    libgdk-pixbuf-2.0-dev libffi-dev shared-mime-info

WORKDIR /app
COPY requirements.txt .

# Instalar em /root/.local
RUN pip install --user --no-warn-script-location \
    -r requirements.txt gunicorn psycopg2-binary weasyprint

# ==================================
# Stage 2: Runtime
# ==================================
FROM python:3.11-slim

# Labels para metadados
LABEL maintainer="Puket - Nicolas Matsuda"
LABEL description="Sistema de Provas de Modelagem - Produção"
LABEL version="2.0.0"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production \
    DEBUG=False \
    PORT=8000

# Dependências de runtime (sem build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 libcairo2 libpango-1.0-0 libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 libffi8 shared-mime-info curl \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/uploads /app/logs /app/backups && \
    chown -R appuser:appuser /app

WORKDIR /app

# Copiar dependências compiladas do builder
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copiar código da aplicação
COPY --chown=appuser:appuser . .

# Ajustar permissões
RUN chown -R appuser:appuser /app && chmod +x /app/entrypoint.sh

# Mudar para usuário não-root
USER appuser

# PATH para pacotes Python
ENV PATH=/home/appuser/.local/bin:$PATH

# Expor porta
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Entrypoint e comando
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]
```

---

## Docker Compose

O sistema oferece dois arquivos Docker Compose:

### 1. docker-compose.sqlite.yml (Desenvolvimento)

**Uso:** Testes, desenvolvimento local, demos
**Banco:** SQLite em arquivo local

```yaml
services:
  app:
    build: .
    container_name: prova_modelagem_app
    restart: unless-stopped
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=sqlite:////app/data/provas.db
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - app_data:/app/data       # Banco SQLite
      - app_uploads:/app/uploads # Uploads
      - app_logs:/app/logs       # Logs
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
```

**Comandos:**
```bash
# Iniciar
docker compose -f docker-compose.sqlite.yml up -d

# Ver logs
docker compose -f docker-compose.sqlite.yml logs -f

# Parar
docker compose -f docker-compose.sqlite.yml down
```

### 2. docker-compose.yml (Produção)

**Uso:** Ambiente de produção
**Banco:** PostgreSQL 15 Alpine

```yaml
services:
  db:
    image: postgres:15-alpine
    container_name: prova_app_db
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build: .
    container_name: prova_app_web
    depends_on:
      db:
        condition: service_healthy
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
      - ./backups:/app/backups
```

---

## Variáveis de Ambiente

### Arquivo .env

Crie um arquivo `.env` na raiz do projeto:

```bash
# ====================================
# CONFIGURAÇÕES DE PRODUÇÃO
# ====================================

# Flask
SECRET_KEY=sua-chave-secreta-super-aleatoria-aqui-64-caracteres-minimo
FLASK_ENV=production
FLASK_DEBUG=False

# Database - SQLite (desenvolvimento)
DATABASE_URL=sqlite:////app/data/provas.db

# Database - PostgreSQL (produção)
# DATABASE_URL=postgresql://prova_user:senha_forte@db:5432/prova_modelagem_db
POSTGRES_DB=prova_modelagem_db
POSTGRES_USER=prova_user
POSTGRES_PASSWORD=senha_forte_aqui

# Admin User
ADMIN_USERNAME=admin
ADMIN_PASSWORD=senha_admin_forte
ADMIN_EMAIL=admin@suaempresa.com

# Server
HOST=0.0.0.0
PORT=8000

# Upload
MAX_CONTENT_LENGTH=16777216  # 16MB
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,pdf,xlsx,xls,ppt,pptx

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/app.log

# Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
PERMANENT_SESSION_LIFETIME=3600
RATELIMIT_ENABLED=True

# Workers (Gunicorn)
WORKERS=2
```

### Gerando SECRET_KEY Segura

```bash
# Python
python3 -c "import secrets; print(secrets.token_hex(32))"

# OpenSSL
openssl rand -hex 32

# /dev/urandom
cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1
```

---

## Volumes e Persistência

### Estrutura de Volumes

```
/app/
├── data/           # Banco SQLite (modo SQLite)
├── uploads/        # Arquivos enviados (fotos, PPT, Excel)
├── logs/           # Logs da aplicação e Gunicorn
└── backups/        # Backups automáticos
```

### Tipos de Volume

**1. Named Volumes (Docker-managed)**
```yaml
volumes:
  postgres_data:
    driver: local
```

**2. Bind Mounts (Host directory)**
```yaml
volumes:
  - ./uploads:/app/uploads
  - ./logs:/app/logs
```

### Vantagens e Desvantagens

| Tipo          | Vantagens                       | Desvantagens           | Uso Recomendado |
|---------------|---------------------------------|------------------------|-----------------|
| Named Volume  | Gerenciado pelo Docker          | Difícil localizar      | Banco de dados  |
|               | Melhor performance              | Sem acesso direto      |                 |
| Bind Mount    | Acesso direto do host           | Menos portável         | Logs, uploads   |
|               | Fácil backup manual             | Dependente do SO       |                 |

### Criar Diretórios no Host

```bash
# Criar estrutura de diretórios
mkdir -p data uploads logs backups

# Ajustar permissões (usuário appuser = UID 1000)
sudo chown -R 1000:1000 data uploads logs backups
chmod -R 755 data uploads logs backups
```

### Backup de Volumes

```bash
# Backup de volume nomeado (PostgreSQL)
docker run --rm \
  -v prova_app_postgres_data:/source \
  -v $(pwd)/backups:/backup \
  alpine \
  tar -czf /backup/postgres_$(date +%Y%m%d_%H%M%S).tar.gz -C /source .

# Backup de bind mount (uploads)
tar -czf backups/uploads_$(date +%Y%m%d_%H%M%S).tar.gz uploads/
```

---

## Rede e Segurança

### Rede Docker

```yaml
networks:
  app_network:
    driver: bridge
```

**Isolamento:** Todos os serviços (app, db, nginx) se comunicam pela rede `app_network`, isolada do host.

### Portas Expostas

| Serviço   | Container Port | Host Port | Descrição                  |
|-----------|----------------|-----------|----------------------------|
| Flask App | 8000           | 8000      | Gunicorn (produção)        |
| Flask App | 5000           | 5000      | Flask dev server (SQLite)  |
| PostgreSQL| 5432           | -         | Não exposta (segurança)    |
| Nginx     | 80/443         | 80/443    | Reverse proxy (opcional)   |

### Boas Práticas de Segurança

1. **Nunca expor PostgreSQL ao host** (exceto para debug)
2. **Usar SECRET_KEY forte** (mínimo 64 caracteres aleatórios)
3. **Executar como usuário não-root** (appuser, UID 1000)
4. **Limitar recursos** (CPU, memória)
5. **Usar HTTPS em produção** (via Nginx)
6. **Firewall no host** (UFW, iptables)

### Resource Limits

```yaml
deploy:
  resources:
    limits:
      cpus: '2'       # Máximo 2 cores
      memory: 1G      # Máximo 1GB RAM
    reservations:
      cpus: '0.5'     # Garantir 0.5 core
      memory: 512M    # Garantir 512MB
```

---

## Build e Execução

### Build da Imagem

```bash
# Build simples
docker build -t prova-modelagem-app:latest .

# Build com cache otimizado
docker build --build-arg BUILDKIT_INLINE_CACHE=1 \
  -t prova-modelagem-app:latest .

# Build sem cache (troubleshooting)
docker build --no-cache -t prova-modelagem-app:latest .

# Build com tag de versão
docker build -t prova-modelagem-app:2.0.0 \
  -t prova-modelagem-app:latest .
```

### Iniciar Aplicação (SQLite)

```bash
# Criar diretórios
mkdir -p data uploads logs

# Criar arquivo .env
cp .env.example .env
# Editar .env com suas configurações

# Iniciar em modo detached
docker compose -f docker-compose.sqlite.yml up -d

# Ver logs
docker compose -f docker-compose.sqlite.yml logs -f app

# Verificar status
docker compose -f docker-compose.sqlite.yml ps

# Acessar shell do container
docker compose -f docker-compose.sqlite.yml exec app bash
```

### Iniciar Aplicação (PostgreSQL)

```bash
# Criar arquivo .env com PostgreSQL configurado
cp .env.example .env
# Configurar:
# - POSTGRES_DB
# - POSTGRES_USER
# - POSTGRES_PASSWORD
# - DATABASE_URL

# Iniciar todos os serviços
docker compose up -d

# Verificar health checks
docker compose ps

# Ver logs do banco
docker compose logs -f db

# Ver logs da aplicação
docker compose logs -f web

# Executar comando no container
docker compose exec web python3 -c "from app import app, db; print(app.config['SQLALCHEMY_DATABASE_URI'])"
```

### Parar e Remover

```bash
# Parar containers (preserva volumes)
docker compose down

# Parar e remover volumes (CUIDADO: apaga dados)
docker compose down -v

# Parar, remover volumes e imagens
docker compose down -v --rmi all
```

---

## Troubleshooting

### Problema 1: Container não inicia

**Sintomas:**
```bash
docker compose ps
# STATUS: Restarting
```

**Diagnóstico:**
```bash
# Ver logs
docker compose logs web

# Ver último erro
docker compose logs --tail=50 web

# Verificar saúde
docker inspect prova_app_web | grep -A 10 Health
```

**Soluções:**
- Verificar variáveis de ambiente no `.env`
- Verificar permissões dos volumes
- Verificar se PostgreSQL está rodando (se usando)

### Problema 2: Banco de dados não conecta

**Sintomas:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Diagnóstico:**
```bash
# Verificar se PostgreSQL está rodando
docker compose ps db

# Ver logs do PostgreSQL
docker compose logs db

# Testar conexão manual
docker compose exec web bash
python3 -c "import psycopg2; psycopg2.connect('postgresql://...')"
```

**Soluções:**
```bash
# Aguardar PostgreSQL ficar pronto
docker compose up -d db
sleep 10
docker compose up -d web

# Verificar DATABASE_URL no .env
# Verificar credenciais do PostgreSQL
```

### Problema 3: Health check falhando

**Sintomas:**
```bash
docker compose ps
# Health: unhealthy
```

**Diagnóstico:**
```bash
# Testar endpoint manualmente
docker compose exec web curl -f http://localhost:8000/health

# Ver logs do Gunicorn
docker compose logs web | grep gunicorn
```

**Soluções:**
- Verificar se Gunicorn iniciou na porta correta
- Verificar se route `/health` existe
- Aumentar `start_period` no healthcheck

### Problema 4: Permissões de volume

**Sintomas:**
```
PermissionError: [Errno 13] Permission denied: '/app/uploads'
```

**Diagnóstico:**
```bash
# Verificar permissões no host
ls -la uploads/ logs/ data/

# Verificar UID/GID do container
docker compose exec web id
```

**Soluções:**
```bash
# Ajustar permissões (appuser = UID 1000)
sudo chown -R 1000:1000 uploads logs data
chmod -R 755 uploads logs data

# Ou criar diretórios com permissões corretas
mkdir -p uploads logs data
sudo chown 1000:1000 uploads logs data
```

### Problema 5: Build lento

**Sintomas:**
```
Building takes 10+ minutes
```

**Soluções:**
```bash
# Usar BuildKit (mais rápido)
export DOCKER_BUILDKIT=1
docker build .

# Limpar cache do Docker
docker builder prune

# Usar cache do registry
docker build --cache-from prova-modelagem-app:latest .
```

### Problema 6: Container usa muita memória

**Diagnóstico:**
```bash
# Verificar uso de recursos
docker stats prova_app_web

# Ver processos dentro do container
docker compose exec web ps aux
```

**Soluções:**
```yaml
# Reduzir workers do Gunicorn
environment:
  - WORKERS=2  # Reduzir de 4 para 2

# Limitar memória no docker-compose.yml
deploy:
  resources:
    limits:
      memory: 512M  # Reduzir de 1G para 512M
```

### Comandos Úteis para Debug

```bash
# Entrar no container
docker compose exec web bash

# Ver variáveis de ambiente
docker compose exec web env

# Ver arquivos
docker compose exec web ls -la /app

# Executar comando Python
docker compose exec web python3 -c "from app import app; print(app.config)"

# Ver processos
docker compose exec web ps aux

# Ver uso de disco
docker compose exec web df -h

# Ver logs do sistema
docker compose exec web tail -f /app/logs/app.log

# Reiniciar apenas um serviço
docker compose restart web

# Rebuild sem cache
docker compose build --no-cache web
```

---

## Performance e Otimização

### Cache de Build

```dockerfile
# Copiar requirements.txt primeiro (cache layer)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar código depois (muda com frequência)
COPY . .
```

### Otimização de Imagem

```bash
# Antes da otimização
docker images prova-modelagem-app
# REPOSITORY              SIZE
# prova-modelagem-app     1.2GB

# Depois do multi-stage
# REPOSITORY              SIZE
# prova-modelagem-app     400MB
```

### Gunicorn Workers

```python
# gunicorn_config.py
workers = 2  # Para SQLite (evitar lock contention)
workers = 4  # Para PostgreSQL (CPU cores * 2)
```

---

## Checklist de Deploy

- [ ] Arquivo `.env` criado e configurado
- [ ] SECRET_KEY gerada (64+ caracteres)
- [ ] Credenciais do admin definidas
- [ ] Diretórios criados (uploads, logs, data)
- [ ] Permissões ajustadas (UID 1000)
- [ ] PostgreSQL configurado (se usando)
- [ ] Build da imagem concluído
- [ ] Containers iniciados com sucesso
- [ ] Health checks passando
- [ ] Logs sem erros críticos
- [ ] Aplicação acessível via navegador
- [ ] Login de admin funcionando
- [ ] Upload de arquivos testado
- [ ] Backup configurado

---

## Referências

- [Documentação oficial do Docker](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Best Practices para Dockerfile](https://docs.docker.com/develop/dev-best-practices/)
- [Flask em Produção](https://flask.palletsprojects.com/en/3.0.x/deploying/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
