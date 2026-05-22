# Documentação do Servidor de Produção
## Sistema de Provas de Modelagem Puket

**Última atualização:** 16/01/2026 (credenciais redacted em 22/05/2026)
**Versão do Sistema:** 2.0.0
**Responsável:** Nicolas Matsuda

> ⚠️ **CREDENCIAIS REMOVIDAS DESTE DOCUMENTO.** Todas as senhas, chaves
> secretas e tokens vivem no vault local em `secrets/*.env` (chmod 600,
> gitignored). Em produção, são injetadas via Docker secrets ou
> systemd `LoadCredential`. Para acesso ao servidor, use chave SSH
> autorizada (`ssh-copy-id`), não senha. Ver `secrets/README.md`.

---

## 1. Informações Gerais do Servidor

### 1.1 Dados de Acesso

```
Host: 192.168.168.124
Usuário: nicolas
Acesso: SSH key (ssh-copy-id já feito) — senha removida deste doc
Hostname: n8n
```

### 1.2 Especificações do Servidor

| Componente | Especificação |
|------------|---------------|
| **Sistema Operacional** | Ubuntu 24.04.3 LTS (Noble Numbat) |
| **Kernel** | Linux 6.8.0-90-generic |
| **Arquitetura** | x86_64 |
| **Virtualização** | Xen (Full virtualization) |
| **Processador** | Intel Xeon E5-2650 @ 2.00GHz |
| **Núcleos (vCPUs)** | 12 cores |
| **Memória RAM** | 9.7 GB (8.1 GB disponível) |
| **Swap** | 4.0 GB |
| **Disco** | 97 GB (35% usado, 61 GB disponível) |
| **Boot Partition** | 2.0 GB (11% usado) |

### 1.3 Configuração de Rede

```
Interface Principal: enX0
IP Interno: 192.168.168.124/23
Gateway: 192.168.168.1
Broadcast: 192.168.169.255
```

**Redes Docker:**
- `bridge` (padrão): 172.17.0.1/16
- `prova_modelagem_app_app_network`: 172.21.0.1/16
- `n8n_web`: 172.19.0.1/16
- `n8n_internal`: 172.18.0.1/16

---

## 2. Ambiente Docker

### 2.1 Versões Instaladas

```bash
Docker version: 28.5.0 (build 887030f)
Docker Compose version: v2.39.4
```

### 2.2 Containers em Execução

| Container | Imagem | Status | Portas | Função |
|-----------|--------|--------|--------|--------|
| `prova_modelagem_app` | prova_modelagem_app-app:latest | Running (healthy) | 5000:5000 | Aplicação principal |
| `n8n-n8n-1` | n8nio/n8n:latest | Running | 5678 | Automação (n8n) |
| `n8n-traefik-1` | traefik:v3.0 | Running | 80, 443 | Reverse Proxy |
| `n8n-postgres-1` | postgres:15 | Running | 5432 | Banco n8n |

### 2.3 Container da Aplicação

**Nome:** `prova_modelagem_app`
**ID:** `aa81a7b1cf25`
**Imagem:** `sha256:3b5d2acea45a` (331 MB)
**Status:** Running (healthy)
**Restart Policy:** unless-stopped
**Health Check:** Verificação HTTP a cada 30s

**Recursos Alocados:**
```yaml
Limites:
  - CPU: 1 core
  - Memória: 512 MB (limite) / 256 MB (reserva)
  - Swap: 1 GB

Uso Atual:
  - CPU: 0.02%
  - Memória: 94.04 MB (18.37% do limite)
  - Network I/O: 229 KB (in) / 2.67 MB (out)
```

---

## 3. Estrutura de Diretórios

### 3.1 Diretório da Aplicação (Host)

```
/home/nicolas/prova_modelagem_app/
├── app.py                          # Aplicação Flask principal
├── models.py                       # Modelos do banco de dados
├── auth.py                         # Autenticação
├── admin.py                        # Painel administrativo
├── config.py                       # Configurações
├── db.py                          # Database helper
├── error_handlers.py              # Tratamento de erros
├── excel_export.py                # Exportação Excel
├── utils.py                       # Funções utilitárias
├── security.py                    # Segurança
├── audit_bp.py                    # Blueprint de auditoria
├── audit_helpers.py               # Helpers de auditoria
├── api_pagination.py              # Paginação API
├── migrate_db.py                  # Scripts de migração
├── Dockerfile                     # Build da imagem Docker
├── docker-compose.sqlite.yml      # Compose SQLite (em uso)
├── docker-compose.yml             # Compose PostgreSQL
├── entrypoint.sh                  # Script de inicialização
├── gunicorn_config.py             # Configuração Gunicorn
├── requirements.txt               # Dependências Python
├── .env                          # Variáveis de ambiente
├── nginx.conf                    # Configuração Nginx (não usado)
├── static/                       # Arquivos estáticos
│   ├── css/
│   ├── js/
│   └── img/
├── templates/                    # Templates HTML
├── data/                        # Banco de dados (bind mount)
├── uploads/                     # Arquivos enviados (bind mount)
├── logs/                        # Logs da aplicação (bind mount)
├── backups/                     # Backups locais
├── scripts/                     # Scripts auxiliares
└── tests/                       # Testes
```

### 3.2 Estrutura de Dados Persistentes

**Localização:** `/opt/prova_modelagem_app/`

```
/opt/prova_modelagem_app/
├── data/                        # Volume Docker: app_data
│   ├── provas.db               # Banco SQLite (80 KB)
│   └── provas_backup_*.db      # Backups automáticos
├── uploads/                     # Volume Docker: app_uploads
│   ├── *.xlsx                  # Tabelas de medidas (14 MB total)
│   └── *.jpg, *.png           # Fotos das provas
└── logs/                        # Volume Docker: app_logs
    ├── access.log              # Logs de acesso (3.2 MB)
    ├── error.log               # Logs de erro (855 KB)
    └── gunicorn.pid           # PID do Gunicorn
```

---

## 4. Configurações da Aplicação

### 4.1 Variáveis de Ambiente (.env)

```bash
# Segurança
SECRET_KEY=<REDACTED — em .env do servidor; rotacionar e mover para vault>

# Flask
FLASK_ENV=production
FLASK_DEBUG=False

# Banco de Dados
DATABASE_URL=sqlite:////app/data/provas.db

# Upload
MAX_CONTENT_LENGTH=16777216
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,pdf,xlsx,xls,ppt,pptx

# Servidor
HOST=0.0.0.0
PORT=5000

# Admin
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<REDACTED — definir via env var no servidor; mudar primeira vez>
ADMIN_EMAIL=nicolas.matsuda@grupounico.com
```

### 4.2 Configuração do Gunicorn

**Arquivo:** `/home/nicolas/prova_modelagem_app/gunicorn_config.py`

```python
# Bind
bind = "0.0.0.0:5000"

# Workers (otimizado para SQLite)
workers = 2
worker_class = 'sync'
worker_connections = 100
timeout = 60
keepalive = 2

# Logging
accesslog = '/app/logs/access.log'
errorlog = '/app/logs/error.log'
loglevel = 'info'

# Process
proc_name = 'provas_app'
```

### 4.3 Docker Compose (SQLite)

**Arquivo:** `/home/nicolas/prova_modelagem_app/docker-compose.sqlite.yml`

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: prova_modelagem_app
    restart: unless-stopped
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=sqlite:////app/data/provas.db
      - PORT=5000
      - HOST=0.0.0.0
    volumes:
      - app_data:/app/data
      - app_uploads:/app/uploads
      - app_logs:/app/logs
    networks:
      - app_network
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M

volumes:
  app_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /opt/prova_modelagem_app/data
  app_uploads:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /opt/prova_modelagem_app/uploads
  app_logs:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /opt/prova_modelagem_app/logs

networks:
  app_network:
    driver: bridge
```

---

## 5. Dependências Python

**Arquivo:** `/home/nicolas/prova_modelagem_app/requirements.txt`

```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-Compress==1.14
Werkzeug==3.0.1
xhtml2pdf==0.2.11
python-dotenv==1.0.0
pyodbc==5.0.1
wfastcgi==3.0.0
openpyxl==3.1.2
Pillow==10.1.0
requests==2.31.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

---

## 6. Processo de Deploy

### 6.1 Deploy Atual (Manual)

O sistema é deployado manualmente via SSH. O processo envolve:

1. **Conexão ao servidor**
```bash
ssh nicolas@192.168.168.124
```

2. **Navegação até o diretório**
```bash
cd /home/nicolas/prova_modelagem_app
```

3. **Atualização do código** (se necessário)
```bash
git pull origin main
```

4. **Rebuild da imagem Docker**
```bash
docker compose -f docker-compose.sqlite.yml build
```

5. **Restart do container**
```bash
docker compose -f docker-compose.sqlite.yml down
docker compose -f docker-compose.sqlite.yml up -d
```

6. **Verificação**
```bash
docker ps
docker logs prova_modelagem_app
```

### 6.2 Script de Entrypoint

O container executa o script `/app/entrypoint.sh` que:

1. Cria diretórios necessários (`/app/uploads`, `/app/logs`, `/app/backups`)
2. Verifica o tipo de banco de dados (SQLite ou PostgreSQL)
3. Cria diretório `/app/data` para SQLite
4. Inicializa o banco de dados via Python
   - Cria/atualiza tabelas
   - Adiciona colunas de checklist (se não existirem)
   - Cria usuário admin (se não existir)
5. Inicia o Gunicorn

### 6.3 Health Check

O Docker executa health check a cada 30 segundos:

```bash
python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/').read()"
```

**Configuração:**
- Intervalo: 30s
- Timeout: 10s
- Start Period: 40s
- Retries: 3

---

## 7. Backup e Recuperação

### 7.1 Backups Automáticos do Banco

O sistema cria backups automáticos em `/opt/prova_modelagem_app/data/`:

```
provas.db (atual - 80 KB)
provas_backup_20260112_140815.db
provas_backup_20260112_151726.db
provas_backup_ANTES_UPDATE_20260116_202303.db
provas_backup_uppercase_20260116_205830.db
provas_backup_uppercase.db
```

### 7.2 Backup Manual

**Backup completo:**
```bash
# Via SSH
ssh nicolas@192.168.168.124

# Backup do banco de dados
cp /opt/prova_modelagem_app/data/provas.db \
   /opt/prova_modelagem_app/data/provas_backup_$(date +%Y%m%d_%H%M%S).db

# Backup dos uploads
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz \
   /opt/prova_modelagem_app/uploads/

# Backup dos logs
tar -czf logs_backup_$(date +%Y%m%d).tar.gz \
   /opt/prova_modelagem_app/logs/
```

**Backup via Docker:**
```bash
# Copiar banco do container para host
docker cp prova_modelagem_app:/app/data/provas.db \
   ./provas_backup_$(date +%Y%m%d).db
```

### 7.3 Recuperação

**Restaurar banco de dados:**
```bash
# Parar container
docker stop prova_modelagem_app

# Restaurar backup
cp /opt/prova_modelagem_app/data/provas_backup_YYYYMMDD.db \
   /opt/prova_modelagem_app/data/provas.db

# Iniciar container
docker start prova_modelagem_app
```

---

## 8. Logs e Monitoramento

### 8.1 Localização dos Logs

**No Host:**
- Access Log: `/opt/prova_modelagem_app/logs/access.log` (3.2 MB)
- Error Log: `/opt/prova_modelagem_app/logs/error.log` (855 KB)
- PID File: `/opt/prova_modelagem_app/logs/gunicorn.pid`

**Docker Logs:**
```bash
# Logs do container (stdout/stderr)
docker logs prova_modelagem_app

# Logs em tempo real
docker logs -f prova_modelagem_app

# Últimas 100 linhas
docker logs --tail 100 prova_modelagem_app
```

### 8.2 Formato dos Logs

**Access Log:**
```
%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s
```

Exemplo:
```
192.168.1.100 - - [16/Jan/2026:21:15:30] "GET / HTTP/1.1" 200 1234 "-" "Mozilla/5.0" 123456
```

**Error Log:**
```
[2026-01-16 21:15:30,855] INFO in app: Aplicação de Provas iniciada em modo produção
[2026-01-16 21:15:30,954] INFO in app: Compressão HTTP habilitada: GZIP
```

### 8.3 Monitoramento de Recursos

```bash
# Estatísticas do container
docker stats prova_modelagem_app

# Processos dentro do container
docker top prova_modelagem_app

# Informações detalhadas
docker inspect prova_modelagem_app
```

---

## 9. Comandos Úteis

### 9.1 Gerenciamento do Container

```bash
# Acessar servidor
ssh nicolas@192.168.168.124

# Ver status dos containers
docker ps -a

# Ver logs em tempo real
docker logs -f prova_modelagem_app

# Acessar shell do container
docker exec -it prova_modelagem_app /bin/bash

# Reiniciar container
docker restart prova_modelagem_app

# Parar container
docker stop prova_modelagem_app

# Iniciar container
docker start prova_modelagem_app

# Remover container (mantém volumes)
docker rm prova_modelagem_app
```

### 9.2 Build e Deploy

```bash
# Ir para diretório
cd /home/nicolas/prova_modelagem_app

# Rebuild da imagem
docker compose -f docker-compose.sqlite.yml build --no-cache

# Deploy completo
docker compose -f docker-compose.sqlite.yml up -d --build

# Ver logs do compose
docker compose -f docker-compose.sqlite.yml logs -f
```

### 9.3 Gerenciamento de Volumes

```bash
# Listar volumes
docker volume ls

# Inspecionar volume
docker volume inspect prova_modelagem_app_app_data

# Ver tamanho dos volumes
du -sh /opt/prova_modelagem_app/*

# Backup de volume
docker run --rm -v prova_modelagem_app_app_data:/data \
   -v $(pwd):/backup alpine tar czf /backup/data_backup.tar.gz /data
```

### 9.4 Banco de Dados

```bash
# Acessar SQLite dentro do container
docker exec -it prova_modelagem_app sqlite3 /app/data/provas.db

# Comandos SQLite úteis
.tables                    # Listar tabelas
.schema provas            # Ver schema de tabela
SELECT COUNT(*) FROM provas;  # Contar registros
.quit                     # Sair

# Backup do banco
docker exec prova_modelagem_app sqlite3 /app/data/provas.db .dump > backup.sql

# Verificar integridade
docker exec prova_modelagem_app sqlite3 /app/data/provas.db "PRAGMA integrity_check;"
```

### 9.5 Rede e Conectividade

```bash
# Ver IP do container
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' prova_modelagem_app

# Testar conectividade
curl -I http://192.168.168.124:5000

# Ver portas abertas
netstat -tulpn | grep 5000

# Inspecionar rede Docker
docker network inspect prova_modelagem_app_app_network
```

### 9.6 Limpeza e Manutenção

```bash
# Limpar imagens antigas (dangling)
docker image prune -a

# Limpar containers parados
docker container prune

# Limpar volumes não utilizados
docker volume prune

# Limpar tudo (CUIDADO!)
docker system prune -a --volumes

# Ver uso de disco do Docker
docker system df

# Rotação de logs
truncate -s 0 /opt/prova_modelagem_app/logs/access.log
truncate -s 0 /opt/prova_modelagem_app/logs/error.log
```

---

## 10. Troubleshooting

### 10.1 Container não Inicia

**Problema:** Container para logo após iniciar

**Diagnóstico:**
```bash
# Ver logs do container
docker logs prova_modelagem_app

# Ver últimos logs
docker logs --tail 50 prova_modelagem_app

# Inspecionar container
docker inspect prova_modelagem_app | grep -A 10 "Status"
```

**Soluções:**
1. Verificar se o banco de dados está acessível
2. Verificar variáveis de ambiente no `.env`
3. Verificar permissões nos volumes
4. Verificar se a porta 5000 está disponível

### 10.2 Aplicação Lenta

**Diagnóstico:**
```bash
# Ver uso de recursos
docker stats prova_modelagem_app

# Ver processos no container
docker top prova_modelagem_app

# Verificar logs de erro
docker logs prova_modelagem_app | grep ERROR
```

**Soluções:**
1. Aumentar workers do Gunicorn (cuidado com SQLite lock)
2. Verificar tamanho do banco de dados
3. Verificar se há queries lentas nos logs
4. Considerar migração para PostgreSQL

### 10.3 Banco de Dados Corrompido

**Sintomas:**
- Erros "database disk image is malformed"
- Aplicação não inicia
- Queries retornam erros

**Recuperação:**
```bash
# 1. Parar container
docker stop prova_modelagem_app

# 2. Backup do banco atual
cp /opt/prova_modelagem_app/data/provas.db \
   /opt/prova_modelagem_app/data/provas_corrupted.db

# 3. Tentar reparar
docker run --rm -v prova_modelagem_app_app_data:/data \
   alpine/sqlite3 /data/provas.db "PRAGMA integrity_check;"

# 4. Restaurar backup mais recente
cp /opt/prova_modelagem_app/data/provas_backup_*.db \
   /opt/prova_modelagem_app/data/provas.db

# 5. Reiniciar container
docker start prova_modelagem_app
```

### 10.4 Espaço em Disco Cheio

**Diagnóstico:**
```bash
# Ver uso de disco
df -h

# Ver tamanho dos diretórios
du -sh /opt/prova_modelagem_app/*
du -sh /var/lib/docker/*

# Ver tamanho das imagens Docker
docker system df
```

**Soluções:**
```bash
# Limpar logs antigos
find /opt/prova_modelagem_app/logs -name "*.log" -mtime +30 -delete

# Limpar backups antigos
find /opt/prova_modelagem_app/data -name "provas_backup_*.db" -mtime +7 -delete

# Limpar imagens Docker antigas
docker image prune -a

# Limpar containers parados
docker container prune
```

### 10.5 Porta 5000 já em Uso

**Diagnóstico:**
```bash
# Ver processo usando a porta
netstat -tulpn | grep 5000
lsof -i :5000
```

**Solução:**
```bash
# Parar processo que está usando a porta
kill -9 <PID>

# Ou mudar porta no docker-compose.yml
ports:
  - "5001:5000"  # Host:Container
```

### 10.6 Erro de Permissões

**Problema:** "Permission denied" nos volumes

**Solução:**
```bash
# Verificar proprietário
ls -la /opt/prova_modelagem_app/

# Ajustar permissões (se necessário)
sudo chown -R nicolas:nicolas /opt/prova_modelagem_app/
sudo chmod -R 755 /opt/prova_modelagem_app/
```

### 10.7 Container "Unhealthy"

**Diagnóstico:**
```bash
# Ver health check
docker inspect prova_modelagem_app | grep -A 20 "Health"
```

**Soluções:**
1. Verificar se a aplicação está respondendo na porta 5000
2. Aumentar timeout do health check
3. Verificar logs de erro

---

## 11. Segurança

### 11.1 Configurações de Segurança

**Container:**
- Usuário não-root: `appuser` (UID 1000)
- Restart policy: `unless-stopped`
- Memory limits: 512 MB
- Read-only paths protegidos
- AppArmor profile: `docker-default`

**Aplicação:**
- HTTPS: Não configurado (usar reverse proxy)
- Secret key: Definido em variável de ambiente
- CORS: Não habilitado
- Rate limiting: Não configurado
- SQL Injection: Protegido por SQLAlchemy ORM

### 11.2 Recomendações de Segurança

1. **Implementar HTTPS:**
```bash
# Adicionar Nginx como reverse proxy
# Configurar certificados SSL (Let's Encrypt)
```

2. **Firewall:**
```bash
# Permitir apenas porta 5000 de redes internas
sudo ufw allow from 192.168.0.0/16 to any port 5000
```

3. **Atualizar regularmente:**
```bash
# Sistema
sudo apt update && sudo apt upgrade

# Docker
sudo apt upgrade docker-ce

# Imagens
docker pull python:3.11-slim
docker compose build --no-cache
```

4. **Monitorar logs:**
```bash
# Configurar logrotate
sudo nano /etc/logrotate.d/prova_modelagem
```

5. **Backup automatizado:**
```bash
# Criar cron job para backups diários
0 2 * * * /home/nicolas/scripts/backup_prova_modelagem.sh
```

---

## 12. Performance

### 12.1 Otimizações Atuais

- **Gunicorn:** 2 workers síncronos (otimizado para SQLite)
- **Flask-Compress:** Compressão GZIP habilitada
- **Worker connections:** 100 (balanceado)
- **Timeout:** 60 segundos
- **Keep-alive:** 2 segundos

### 12.2 Métricas Atuais

```
CPU: 0.02% (12 cores disponíveis)
Memória: 94 MB / 512 MB (18.37%)
Disco: 32 GB / 97 GB (35%)
Network I/O: 229 KB in / 2.67 MB out
Uptime: 4h 33min
Load average: 1.29, 1.26, 2.29
```

### 12.3 Recomendações de Performance

1. **Aumentar workers Gunicorn (se migrar para PostgreSQL):**
```python
workers = (2 * num_cores) + 1  # ~25 workers para 12 cores
```

2. **Implementar cache Redis:**
```python
CACHE_TYPE = "redis"
CACHE_REDIS_URL = "redis://redis:6379/0"
```

3. **CDN para arquivos estáticos:**
- Servir CSS/JS via CDN
- Usar Nginx para arquivos estáticos

4. **Database tuning:**
```sql
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = 10000;
```

---

## 13. Acesso à Aplicação

### 13.1 URLs de Acesso

```
Aplicação: http://192.168.168.124:5000
Login: http://192.168.168.124:5000/login
Dashboard: http://192.168.168.124:5000/dashboard
Admin: http://192.168.168.124:5000/admin
```

### 13.2 Credenciais de Admin

```
Username: admin
Password: <REDACTED — ver .env / vault no servidor>
Email: nicolas.matsuda@grupounico.com
```

### 13.3 Endpoints Principais

- `GET /` - Redireciona para login
- `GET /login` - Página de login
- `GET /dashboard` - Dashboard principal
- `GET /nova_prova` - Criar nova prova
- `GET /relatorios` - Lista de relatórios
- `GET /admin/users` - Gerenciar usuários
- `GET /audit` - Logs de auditoria
- `GET /analytics` - Analytics

---

## 14. Migração para PostgreSQL

### 14.1 Quando Migrar

Considere migrar para PostgreSQL quando:
- Número de usuários simultâneos > 10
- Database size > 100 MB
- Erros de "database is locked"
- Necessidade de replicação

### 14.2 Passos para Migração

```bash
# 1. Backup do SQLite
docker exec prova_modelagem_app sqlite3 /app/data/provas.db .dump > backup.sql

# 2. Modificar docker-compose.yml
# Adicionar serviço PostgreSQL

# 3. Converter dump SQLite para PostgreSQL
# (usar ferramentas como pgloader)

# 4. Atualizar DATABASE_URL
DATABASE_URL=postgresql://user:pass@postgres:5432/provas

# 5. Deploy
docker compose up -d
```

---

## 15. Contatos e Suporte

### 15.1 Responsáveis

**Desenvolvedor/Admin:**
- Nome: Nicolas Matsuda
- Email: nicolas.matsuda@grupounico.com
- Empresa: Puket / Grupo Unico

### 15.2 Documentação Adicional

Documentos disponíveis em `/home/nicolas/prova_modelagem_app/`:
- `README.md` - Documentação geral
- `DEPLOY_DOCKER.md` - Deploy com Docker
- `DEPLOY_PRODUCAO.md` - Deploy em produção
- `MANUAL_USUARIO.md` - Manual do usuário

---

## 16. Checklist de Manutenção

### 16.1 Diária

- [ ] Verificar status do container: `docker ps`
- [ ] Verificar logs de erro: `docker logs prova_modelagem_app | grep ERROR`
- [ ] Verificar uso de recursos: `docker stats prova_modelagem_app`

### 16.2 Semanal

- [ ] Verificar tamanho do banco de dados
- [ ] Verificar tamanho dos logs
- [ ] Limpar backups antigos (> 7 dias)
- [ ] Verificar espaço em disco: `df -h`

### 16.3 Mensal

- [ ] Atualizar sistema operacional
- [ ] Atualizar imagens Docker
- [ ] Backup completo do sistema
- [ ] Revisar logs de auditoria
- [ ] Verificar certificados SSL (se aplicável)

### 16.4 Trimestral

- [ ] Revisar configurações de segurança
- [ ] Otimizar banco de dados
- [ ] Revisar acessos de usuários
- [ ] Atualizar documentação

---

## 17. Comandos Executados na Pesquisa

### 17.1 Comandos de Sistema

```bash
# Informações do SO
uname -a
cat /etc/os-release

# Recursos
free -h
df -h
nproc
lscpu

# Rede
ip addr show
hostname -I

# Sistema
uptime
who
```

### 17.2 Comandos Docker

```bash
# Versões
docker --version
docker compose version

# Containers
docker ps -a
docker images
docker inspect prova_modelagem_app
docker logs --tail 50 prova_modelagem_app
docker stats --no-stream prova_modelagem_app

# Volumes
docker volume ls
docker volume inspect prova_modelagem_app_app_data

# Rede
docker network ls
docker network inspect prova_modelagem_app_app_network
```

### 17.3 Comandos de Arquivos

```bash
# Estrutura
ls -la /home/nicolas/prova_modelagem_app/
ls -lh /opt/prova_modelagem_app/

# Configurações
cat docker-compose.sqlite.yml
cat .env
cat gunicorn_config.py
cat Dockerfile
cat entrypoint.sh
cat requirements.txt
```

---

## 18. Resumo Executivo

### 18.1 Configuração Atual

- **Servidor:** Ubuntu 24.04 LTS com 12 vCPUs e 9.7 GB RAM
- **Container:** Docker com Flask + SQLite + Gunicorn
- **Recursos:** CPU 0.02%, RAM 94 MB (18%), Disco 35%
- **Uptime:** 4h 33min (última reinicialização)
- **Status:** Running (healthy)

### 18.2 Pontos Fortes

✅ Containerização completa
✅ Volumes persistentes configurados
✅ Health checks implementados
✅ Backups automáticos do banco
✅ Logs estruturados
✅ Restart policy configurado

### 18.3 Pontos de Atenção

⚠️ HTTPS não configurado
⚠️ SQLite pode limitar escalabilidade
⚠️ Sem reverse proxy (Nginx inativo)
⚠️ Sem monitoramento automatizado
⚠️ Backups não automatizados
⚠️ Logs crescendo (3.2 MB access.log)

### 18.4 Próximos Passos Recomendados

1. Implementar HTTPS com Let's Encrypt
2. Configurar logrotate para logs
3. Automatizar backups com cron
4. Implementar monitoramento (Prometheus/Grafana)
5. Considerar migração para PostgreSQL
6. Configurar firewall (UFW)
7. Documentar processo de deploy automatizado

---

**Fim da Documentação**

*Este documento foi gerado em 16/01/2026 através de pesquisa automatizada no servidor de produção.*
