# Guia de Manutenção e Operação - Sistema de Provas de Modelagem

## Índice
1. [Operações Diárias](#operações-diárias)
2. [Backup e Restore](#backup-e-restore)
3. [Monitoramento](#monitoramento)
4. [Logs e Diagnóstico](#logs-e-diagnóstico)
5. [Performance e Otimização](#performance-e-otimização)
6. [Segurança](#segurança)
7. [Troubleshooting Comum](#troubleshooting-comum)
8. [Manutenção Preventiva](#manutenção-preventiva)
9. [Scaling](#scaling)

---

## Operações Diárias

### Verificação de Saúde do Sistema

#### Docker

```bash
# Status dos containers
docker compose ps

# Verificar saúde
docker compose ps | grep -i healthy

# Ver uso de recursos
docker stats --no-stream

# Logs recentes
docker compose logs --tail=50 web
```

#### Manual

```bash
# Status dos serviços
sudo supervisorctl status prova_app
sudo systemctl status nginx
sudo systemctl status postgresql

# Ver processos
ps aux | grep -E 'gunicorn|nginx|postgres'

# Uso de recursos
htop
df -h
free -m
```

### Checklist Diário

```bash
#!/bin/bash
# daily-check.sh

echo "=== Verificação Diária do Sistema ==="
echo ""

# 1. Status dos serviços
echo "1. Status dos Serviços:"
docker compose ps 2>/dev/null || sudo supervisorctl status prova_app
echo ""

# 2. Espaço em disco
echo "2. Espaço em Disco:"
df -h /opt/prova_app | tail -1
echo ""

# 3. Uso de memória
echo "3. Memória:"
free -h | grep Mem
echo ""

# 4. Últimos erros nos logs
echo "4. Erros Recentes (últimas 24h):"
if [ -d "/opt/prova_app/logs" ]; then
    find /opt/prova_app/logs -name "*.log" -mtime -1 -exec grep -i "error\|critical" {} \; | tail -10
fi
echo ""

# 5. Health check
echo "5. Health Check:"
curl -s http://localhost:8000/health || echo "FALHOU"
echo ""

# 6. Backups
echo "6. Último Backup:"
ls -lht /opt/prova_app/backups/*.gz 2>/dev/null | head -1
echo ""

echo "=== Fim da Verificação ==="
```

---

## Backup e Restore

### Backup Completo (Docker)

#### Script Automatizado

```bash
#!/bin/bash
# /opt/prova_app/scripts/full-backup.sh

set -e

BACKUP_DIR="/opt/prova_app/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="full_backup_$DATE"
KEEP_DAYS=7

echo "🔄 Iniciando backup completo..."

# Criar diretório de backup
mkdir -p "$BACKUP_DIR"

# 1. Backup do banco de dados
echo "📦 Backup do banco de dados..."
docker compose exec -T db pg_dump -U prova_user prova_modelagem_db | \
    gzip > "$BACKUP_DIR/${BACKUP_NAME}_db.sql.gz"

# 2. Backup dos uploads
echo "📷 Backup dos uploads..."
tar -czf "$BACKUP_DIR/${BACKUP_NAME}_uploads.tar.gz" \
    -C /opt/prova_app uploads/

# 3. Backup do .env
echo "⚙️  Backup das configurações..."
cp /opt/prova_app/.env "$BACKUP_DIR/${BACKUP_NAME}_env"

# 4. Backup do código (opcional)
echo "📝 Backup do código..."
tar -czf "$BACKUP_DIR/${BACKUP_NAME}_code.tar.gz" \
    --exclude='venv' \
    --exclude='.venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='uploads' \
    --exclude='logs' \
    --exclude='backups' \
    -C /opt/prova_app .

# 5. Calcular tamanhos
DB_SIZE=$(du -h "$BACKUP_DIR/${BACKUP_NAME}_db.sql.gz" | cut -f1)
UPLOADS_SIZE=$(du -h "$BACKUP_DIR/${BACKUP_NAME}_uploads.tar.gz" | cut -f1)
CODE_SIZE=$(du -h "$BACKUP_DIR/${BACKUP_NAME}_code.tar.gz" | cut -f1)

echo ""
echo "✅ Backup concluído!"
echo "   📊 Banco: $DB_SIZE"
echo "   📷 Uploads: $UPLOADS_SIZE"
echo "   📝 Código: $CODE_SIZE"
echo "   📁 Local: $BACKUP_DIR"
echo ""

# 6. Limpar backups antigos
echo "🗑️  Removendo backups com mais de $KEEP_DAYS dias..."
find "$BACKUP_DIR" -name "full_backup_*" -mtime +$KEEP_DAYS -delete
echo "✅ Limpeza concluída!"

# 7. Listar backups disponíveis
echo ""
echo "Backups disponíveis:"
ls -lh "$BACKUP_DIR" | grep "full_backup_" | tail -5
```

#### Executar Backup

```bash
# Tornar executável
chmod +x /opt/prova_app/scripts/full-backup.sh

# Executar manualmente
/opt/prova_app/scripts/full-backup.sh

# Agendar no crontab (diário às 2h)
sudo crontab -e
# Adicionar:
0 2 * * * /opt/prova_app/scripts/full-backup.sh >> /var/log/prova_backup.log 2>&1
```

### Backup Manual (Componentes Separados)

#### Banco de Dados

```bash
# Docker + PostgreSQL
docker compose exec -T db pg_dump -U prova_user prova_modelagem_db | \
    gzip > backup_db_$(date +%Y%m%d_%H%M%S).sql.gz

# Docker + SQLite
docker compose exec -T app cat /app/data/provas.db > \
    backup_sqlite_$(date +%Y%m%d_%H%M%S).db

# Manual + PostgreSQL
sudo -u postgres pg_dump prova_modelagem_db | \
    gzip > backup_db_$(date +%Y%m%d_%H%M%S).sql.gz

# Manual + SQLite
cp /opt/prova_app/instance/provas.db \
    backup_sqlite_$(date +%Y%m%d_%H%M%S).db
```

#### Uploads

```bash
# Backup de uploads
tar -czf backup_uploads_$(date +%Y%m%d_%H%M%S).tar.gz \
    -C /opt/prova_app uploads/

# Backup incremental (rsync)
rsync -av --delete /opt/prova_app/uploads/ /backup/uploads/
```

#### Configurações

```bash
# Backup do .env
cp /opt/prova_app/.env backup_env_$(date +%Y%m%d_%H%M%S)

# Backup de configurações do Nginx
sudo cp /etc/nginx/sites-available/prova_app \
    backup_nginx_$(date +%Y%m%d_%H%M%S).conf

# Backup de configurações do Supervisor
sudo cp /etc/supervisor/conf.d/prova_app.conf \
    backup_supervisor_$(date +%Y%m%d_%H%M%S).conf
```

### Restore Completo

#### Docker + PostgreSQL

```bash
#!/bin/bash
# restore.sh

set -e

echo "🔄 Restauração de Backup"
echo ""

# Listar backups disponíveis
echo "Backups disponíveis:"
ls -1 /opt/prova_app/backups/full_backup_*_db.sql.gz | \
    sed 's/_db.sql.gz//' | \
    xargs -n1 basename | \
    nl

echo ""
read -p "Digite o número do backup: " BACKUP_NUM

# Obter nome do backup
BACKUP_NAME=$(ls -1 /opt/prova_app/backups/full_backup_*_db.sql.gz | \
    sed 's/_db.sql.gz//' | \
    xargs -n1 basename | \
    sed -n "${BACKUP_NUM}p")

if [ -z "$BACKUP_NAME" ]; then
    echo "❌ Backup não encontrado!"
    exit 1
fi

echo ""
echo "⚠️  ATENÇÃO: Isso irá SUBSTITUIR todos os dados atuais!"
read -p "Confirma a restauração? (digite 'CONFIRMO'): " CONFIRM

if [ "$CONFIRM" != "CONFIRMO" ]; then
    echo "❌ Operação cancelada"
    exit 0
fi

BACKUP_DIR="/opt/prova_app/backups"

# 1. Parar aplicação
echo "🛑 Parando aplicação..."
docker compose stop web

# 2. Restaurar banco de dados
echo "📦 Restaurando banco de dados..."
gunzip < "$BACKUP_DIR/${BACKUP_NAME}_db.sql.gz" | \
    docker compose exec -T db psql -U prova_user -d prova_modelagem_db

# 3. Restaurar uploads
if [ -f "$BACKUP_DIR/${BACKUP_NAME}_uploads.tar.gz" ]; then
    echo "📷 Restaurando uploads..."
    rm -rf /opt/prova_app/uploads.old
    mv /opt/prova_app/uploads /opt/prova_app/uploads.old
    tar -xzf "$BACKUP_DIR/${BACKUP_NAME}_uploads.tar.gz" \
        -C /opt/prova_app
    chown -R 1000:1000 /opt/prova_app/uploads
fi

# 4. Restaurar .env (opcional)
if [ -f "$BACKUP_DIR/${BACKUP_NAME}_env" ]; then
    echo "⚙️  .env de backup disponível em:"
    echo "   $BACKUP_DIR/${BACKUP_NAME}_env"
    read -p "Restaurar .env? (s/N): " RESTORE_ENV
    if [ "$RESTORE_ENV" = "s" ]; then
        cp /opt/prova_app/.env /opt/prova_app/.env.old
        cp "$BACKUP_DIR/${BACKUP_NAME}_env" /opt/prova_app/.env
    fi
fi

# 5. Reiniciar aplicação
echo "🚀 Reiniciando aplicação..."
docker compose start web

sleep 5

# 6. Verificar
echo "✅ Verificando aplicação..."
docker compose ps
curl -s http://localhost:8000/health

echo ""
echo "✅ Restauração concluída!"
```

---

## Monitoramento

### Métricas de Sistema

#### CPU e Memória

```bash
# Uso de CPU por processo
ps aux --sort=-%cpu | head -10

# Uso de memória por processo
ps aux --sort=-%mem | head -10

# Uso de recursos em tempo real
htop

# Docker stats
docker stats --no-stream
```

#### Disco

```bash
# Espaço total
df -h

# Tamanho dos diretórios
du -sh /opt/prova_app/*

# Arquivos grandes
find /opt/prova_app -type f -size +100M -exec ls -lh {} \;

# Uso por tipo de arquivo
find /opt/prova_app/uploads -type f -name "*.jpg" -exec du -ch {} + | grep total
find /opt/prova_app/uploads -type f -name "*.pdf" -exec du -ch {} + | grep total
```

#### Rede

```bash
# Conexões ativas
sudo netstat -tulpn | grep -E '8000|5432|80|443'

# Tráfego de rede
sudo iftop -i eth0

# Conexões por IP
sudo netstat -ntu | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -n
```

### Monitoramento de Logs

#### Logs em Tempo Real

```bash
# Docker
docker compose logs -f web
docker compose logs -f --tail=100 web

# Manual
sudo tail -f /opt/prova_app/logs/app.log

# Nginx
sudo tail -f /var/log/nginx/provas_app_access.log
sudo tail -f /var/log/nginx/provas_app_error.log

# Todos os logs
sudo tail -f /opt/prova_app/logs/*.log
```

#### Análise de Logs

```bash
# Contar erros por tipo
grep -i error /opt/prova_app/logs/app.log | \
    awk '{print $4}' | sort | uniq -c | sort -rn

# Top 10 IPs com mais requisições
awk '{print $1}' /var/log/nginx/provas_app_access.log | \
    sort | uniq -c | sort -rn | head -10

# Requisições mais lentas
awk '{print $NF, $7}' /var/log/nginx/provas_app_access.log | \
    sort -rn | head -10

# Códigos de status HTTP
awk '{print $9}' /var/log/nginx/provas_app_access.log | \
    sort | uniq -c | sort -rn

# Erros nas últimas 24h
find /opt/prova_app/logs -name "*.log" -mtime -1 \
    -exec grep -i "error\|critical\|exception" {} \;
```

### Alertas

#### Script de Monitoramento com Alertas

```bash
#!/bin/bash
# /opt/prova_app/scripts/monitor.sh

# Configurações
ALERT_EMAIL="admin@empresa.com"
DISK_THRESHOLD=80
MEM_THRESHOLD=80
CPU_THRESHOLD=80

# Funções
send_alert() {
    SUBJECT="$1"
    MESSAGE="$2"
    echo "$MESSAGE" | mail -s "$SUBJECT" "$ALERT_EMAIL"
}

# 1. Verificar espaço em disco
DISK_USAGE=$(df -h /opt/prova_app | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt "$DISK_THRESHOLD" ]; then
    send_alert "ALERTA: Disco Cheio" \
        "Uso de disco: ${DISK_USAGE}% (limite: ${DISK_THRESHOLD}%)"
fi

# 2. Verificar memória
MEM_USAGE=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
if [ "$MEM_USAGE" -gt "$MEM_THRESHOLD" ]; then
    send_alert "ALERTA: Memória Alta" \
        "Uso de memória: ${MEM_USAGE}% (limite: ${MEM_THRESHOLD}%)"
fi

# 3. Verificar se aplicação está respondendo
if ! curl -f -s http://localhost:8000/health > /dev/null; then
    send_alert "ALERTA: Aplicação Não Responde" \
        "A aplicação não está respondendo ao health check"
fi

# 4. Verificar erros recentes nos logs
ERROR_COUNT=$(grep -i "error\|critical" /opt/prova_app/logs/app.log | \
    grep "$(date +%Y-%m-%d)" | wc -l)
if [ "$ERROR_COUNT" -gt 10 ]; then
    send_alert "ALERTA: Muitos Erros" \
        "Foram detectados $ERROR_COUNT erros hoje"
fi
```

#### Configurar Monitoramento Contínuo

```bash
# Adicionar ao crontab (verificar a cada 5 minutos)
crontab -e
# Adicionar:
*/5 * * * * /opt/prova_app/scripts/monitor.sh
```

---

## Logs e Diagnóstico

### Estrutura de Logs

```
/opt/prova_app/logs/
├── app.log              # Log principal da aplicação
├── error.log            # Erros da aplicação
├── access.log           # Logs de acesso (Gunicorn)
├── supervisor_*.log     # Logs do Supervisor
└── audit.log            # Log de auditoria (se habilitado)
```

### Configuração de Rotação de Logs

```bash
# /etc/logrotate.d/prova_app

/opt/prova_app/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 appuser appuser
    sharedscripts
    postrotate
        # Recarregar Gunicorn
        kill -USR1 $(cat /var/run/prova_app/gunicorn.pid)
    endscript
}
```

### Análise de Performance nos Logs

```bash
# Tempo médio de resposta
awk '{sum+=$NF; count++} END {print sum/count " ms"}' \
    /var/log/nginx/provas_app_access.log

# Requisições por segundo (último minuto)
tail -n 100 /var/log/nginx/provas_app_access.log | \
    awk '{print $4}' | cut -d: -f2 | sort | uniq -c

# Endpoints mais acessados
awk '{print $7}' /var/log/nginx/provas_app_access.log | \
    sort | uniq -c | sort -rn | head -20
```

---

## Performance e Otimização

### Ajuste de Workers (Gunicorn)

```python
# gunicorn_config.py

import os
import multiprocessing

# Calcular workers baseado em CPUs
cpu_count = multiprocessing.cpu_count()

# Fórmula: (2 * CPU) + 1
workers = int(os.getenv('WORKERS', (2 * cpu_count) + 1))

# Para SQLite: máximo 2 workers (evitar lock contention)
if 'sqlite' in os.getenv('DATABASE_URL', ''):
    workers = min(workers, 2)

# Timeout (segundos)
timeout = 60

# Worker class
worker_class = 'sync'  # ou 'gevent' para async

# Connections per worker
worker_connections = 100
```

### Otimização de Banco de Dados

#### PostgreSQL

```sql
-- Conectar ao banco
psql -U prova_user -d prova_modelagem_db

-- Ver queries lentas
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Vacuum (limpar dados antigos)
VACUUM ANALYZE;

-- Verificar índices
SELECT * FROM pg_indexes WHERE schemaname = 'public';

-- Adicionar índices se necessário
CREATE INDEX idx_provas_referencia_id ON provas(referencia_id);
CREATE INDEX idx_referencias_relatorio_id ON referencias(relatorio_id);
```

#### SQLite

```bash
# Conectar ao banco
sqlite3 /opt/prova_app/data/provas.db

-- Vacuum (compactar)
VACUUM;

-- Analisar queries
EXPLAIN QUERY PLAN SELECT * FROM provas WHERE referencia_id = 1;

-- Ver índices
.indices

-- Sair
.quit
```

### Cache

#### Nginx Cache (Arquivos Estáticos)

```nginx
# /etc/nginx/sites-available/prova_app

location /static/ {
    alias /opt/prova_app/static/;
    expires 30d;
    add_header Cache-Control "public, immutable";
    access_log off;
}

location /uploads/ {
    alias /opt/prova_app/uploads/;
    expires 7d;
    add_header Cache-Control "private";
}
```

#### Flask Cache

```python
# app.py

from flask_caching import Cache

cache = Cache(config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})

cache.init_app(app)

# Usar em views
@app.route('/analytics')
@cache.cached(timeout=600)  # 10 minutos
def analytics():
    # código que consulta muitos dados
    return render_template('analytics.html', data=data)
```

### Compressão

```nginx
# /etc/nginx/nginx.conf

gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types
    text/plain
    text/css
    text/xml
    text/javascript
    application/json
    application/javascript
    application/xml+rss
    application/rss+xml
    font/truetype
    font/opentype
    application/vnd.ms-fontobject
    image/svg+xml;
```

---

## Segurança

### Auditoria de Segurança

```bash
# Verificar permissões de arquivos
find /opt/prova_app -type f -perm /o+w

# Verificar usuários com acesso ao banco
sudo -u postgres psql -c "\du"

# Verificar portas abertas
sudo netstat -tulpn

# Verificar últimos acessos SSH
sudo lastlog

# Verificar tentativas de login falhadas
sudo grep "Failed password" /var/log/auth.log | tail -20
```

### Atualização de Segurança

```bash
# Atualizar sistema
sudo apt update
sudo apt upgrade -y

# Atualizar dependências Python
cd /opt/prova_app
source .venv/bin/activate
pip list --outdated
pip install --upgrade <package>

# Verificar vulnerabilidades conhecidas
pip install safety
safety check
```

### Hardening

```bash
# Desabilitar login root via SSH
sudo sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart sshd

# Configurar fail2ban
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Limitar rate no Nginx
# /etc/nginx/sites-available/prova_app
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

location /auth/login {
    limit_req zone=login burst=2;
    # ... resto da config
}
```

---

## Troubleshooting Comum

### Problema: Aplicação Lenta

**Diagnóstico:**
```bash
# Verificar CPU
top -bn1 | grep "Cpu(s)"

# Verificar memória
free -m

# Verificar workers
ps aux | grep gunicorn | wc -l

# Verificar queries lentas no banco
# PostgreSQL:
SELECT * FROM pg_stat_activity WHERE state = 'active';

# SQLite:
# Não há pg_stat, verificar locks:
fuser /opt/prova_app/data/provas.db
```

**Soluções:**
- Aumentar workers do Gunicorn
- Adicionar índices no banco
- Habilitar cache
- Otimizar queries
- Aumentar recursos (CPU/RAM)

### Problema: Erros 500

**Diagnóstico:**
```bash
# Ver últimos erros
tail -50 /opt/prova_app/logs/error.log

# Ver traceback completo
grep -A 20 "Traceback" /opt/prova_app/logs/error.log | tail -30
```

**Soluções comuns:**
- Verificar .env (variáveis faltando)
- Verificar conexão com banco
- Verificar permissões de arquivos
- Verificar dependências instaladas

### Problema: Uploads Falhando

**Diagnóstico:**
```bash
# Verificar permissões
ls -la /opt/prova_app/uploads/

# Verificar espaço em disco
df -h /opt/prova_app

# Ver logs de erro
grep -i "upload" /opt/prova_app/logs/error.log
```

**Soluções:**
- Ajustar permissões: `chown -R 1000:1000 uploads/`
- Aumentar MAX_CONTENT_LENGTH no .env
- Aumentar client_max_body_size no Nginx
- Liberar espaço em disco

### Problema: Banco de Dados Bloqueado (SQLite)

**Sintomas:**
```
sqlite3.OperationalError: database is locked
```

**Soluções:**
```bash
# Verificar processos usando o banco
fuser /opt/prova_app/data/provas.db

# Reduzir workers para 1 ou 2
# Em gunicorn_config.py:
workers = 1

# Ou migrar para PostgreSQL
```

---

## Manutenção Preventiva

### Checklist Semanal

- [ ] Verificar espaço em disco
- [ ] Analisar logs de erro
- [ ] Verificar backups automáticos
- [ ] Revisar uso de recursos
- [ ] Verificar atualizações de segurança
- [ ] Testar restore de backup

### Checklist Mensal

- [ ] Rotacionar logs manualmente (se necessário)
- [ ] Limpar uploads antigos/não utilizados
- [ ] Vacuum no banco de dados
- [ ] Atualizar dependências Python
- [ ] Revisar configurações de segurança
- [ ] Documentar mudanças realizadas

### Checklist Trimestral

- [ ] Atualização completa do sistema operacional
- [ ] Revisar e otimizar queries do banco
- [ ] Auditoria de segurança completa
- [ ] Teste de disaster recovery
- [ ] Revisar e atualizar documentação
- [ ] Capacitação da equipe

---

## Scaling

### Escalonamento Vertical (Scale Up)

```bash
# Aumentar recursos do Docker container
# docker-compose.yml
deploy:
  resources:
    limits:
      cpus: '4'      # 2 -> 4 CPUs
      memory: 2G     # 1G -> 2G RAM
```

### Escalonamento Horizontal (Scale Out)

```yaml
# docker-compose.yml

services:
  web:
    # ... config
    deploy:
      replicas: 3  # 3 instâncias da aplicação

  nginx:
    # Load balancer
    # Configurar upstream com múltiplos backends
```

### Load Balancer (Nginx)

```nginx
upstream prova_app {
    least_conn;  # Algoritmo de balanceamento
    server web1:8000 weight=1 max_fails=3 fail_timeout=30s;
    server web2:8000 weight=1 max_fails=3 fail_timeout=30s;
    server web3:8000 weight=1 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;

    location / {
        proxy_pass http://prova_app;
        # ... headers
    }
}
```

---

## Scripts Úteis de Administração

### Limpeza de Arquivos Temporários

```bash
#!/bin/bash
# cleanup.sh

echo "🧹 Limpeza de arquivos temporários"

# Remover logs antigos (>30 dias)
find /opt/prova_app/logs -name "*.log.*" -mtime +30 -delete
echo "✓ Logs antigos removidos"

# Remover backups antigos (>30 dias)
find /opt/prova_app/backups -name "*.gz" -mtime +30 -delete
echo "✓ Backups antigos removidos"

# Limpar cache do Python
find /opt/prova_app -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find /opt/prova_app -type f -name "*.pyc" -delete
echo "✓ Cache Python limpo"

# Limpar arquivos temporários
rm -rf /tmp/flask_*
rm -rf /tmp/werkzeug_*
echo "✓ Arquivos temporários removidos"

# Docker: Limpar imagens antigas
docker image prune -a -f --filter "until=720h"  # 30 dias
echo "✓ Imagens Docker antigas removidas"

echo "✅ Limpeza concluída!"
```

### Relatório de Status

```bash
#!/bin/bash
# status-report.sh

echo "================================"
echo "RELATÓRIO DE STATUS DO SISTEMA"
echo "$(date)"
echo "================================"
echo ""

echo "1. SERVIÇOS"
echo "----------"
docker compose ps 2>/dev/null || sudo supervisorctl status
echo ""

echo "2. RECURSOS"
echo "----------"
echo "CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}')%"
echo "Memória: $(free | awk 'NR==2{printf "%.1f%%", $3*100/$2}')"
echo "Disco: $(df -h /opt/prova_app | awk 'NR==2{print $5}')"
echo ""

echo "3. BANCO DE DADOS"
echo "----------------"
docker compose exec -T db psql -U prova_user -d prova_modelagem_db -c "\
    SELECT schemaname, tablename, \
           pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size \
    FROM pg_tables WHERE schemaname = 'public' ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;" \
    2>/dev/null || echo "SQLite em uso"
echo ""

echo "4. UPLOADS"
echo "----------"
du -sh /opt/prova_app/uploads
echo "Total de arquivos: $(find /opt/prova_app/uploads -type f | wc -l)"
echo ""

echo "5. BACKUPS"
echo "----------"
echo "Último backup:"
ls -lht /opt/prova_app/backups/*.gz 2>/dev/null | head -1 || echo "Nenhum backup encontrado"
echo ""

echo "6. LOGS (Erros nas últimas 24h)"
echo "-------------------------------"
find /opt/prova_app/logs -name "*.log" -mtime -1 \
    -exec grep -i "error\|critical" {} \; | wc -l
echo ""

echo "================================"
```

---

## Referências Rápidas

### Comandos Docker

```bash
# Status
docker compose ps
docker compose logs -f web
docker stats

# Restart
docker compose restart web
docker compose restart

# Rebuild
docker compose up -d --build

# Shell
docker compose exec web bash

# Backup DB
docker compose exec -T db pg_dump -U prova_user prova_modelagem_db > backup.sql
```

### Comandos Manual

```bash
# Status
sudo supervisorctl status prova_app
sudo systemctl status nginx

# Restart
sudo supervisorctl restart prova_app
sudo systemctl restart nginx

# Logs
tail -f /opt/prova_app/logs/app.log
sudo tail -f /var/log/nginx/error.log

# Shell Python
cd /opt/prova_app
source .venv/bin/activate
python3
```

---

**Para mais informações, consulte:**
- [DOCKER_GUIDE.md](DOCKER_GUIDE.md)
- [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)
- [README.md](README.md)
