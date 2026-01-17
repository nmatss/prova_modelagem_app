# Checklist Completo de Deploy - Sistema de Provas de Modelagem

## Índice
1. [Checklist Pré-Deploy](#checklist-pré-deploy)
2. [Checklist de Deploy](#checklist-de-deploy)
3. [Checklist Pós-Deploy](#checklist-pós-deploy)
4. [Comandos de Administração Mais Usados](#comandos-de-administração-mais-usados)
5. [Troubleshooting Rápido](#troubleshooting-rápido)
6. [Comandos de Emergência](#comandos-de-emergência)

---

## Checklist Pré-Deploy

### 1. Preparação do Servidor

- [ ] Sistema operacional atualizado
  ```bash
  sudo apt update && sudo apt upgrade -y
  ```

- [ ] Docker instalado e funcionando
  ```bash
  docker --version
  docker compose version
  ```

- [ ] Git instalado
  ```bash
  git --version
  ```

- [ ] Espaço em disco suficiente (mínimo 10GB livre)
  ```bash
  df -h
  ```

- [ ] Memória RAM adequada (mínimo 2GB, recomendado 4GB)
  ```bash
  free -h
  ```

### 2. Código e Dependências

- [ ] Código atualizado no repositório
  ```bash
  git status
  git log -1
  ```

- [ ] requirements.txt atualizado
  ```bash
  cat requirements.txt
  ```

- [ ] Dockerfile testado localmente
  ```bash
  docker build -t prova-app-test .
  ```

- [ ] docker-compose.yml validado
  ```bash
  docker compose config
  ```

### 3. Configurações

- [ ] Arquivo .env criado
  ```bash
  cp .env.example .env
  ```

- [ ] SECRET_KEY gerada (64+ caracteres)
  ```bash
  python3 -c "import secrets; print(secrets.token_hex(32))"
  ```

- [ ] Credenciais do admin definidas
  ```bash
  grep ADMIN_ .env
  ```

- [ ] DATABASE_URL configurada corretamente
  ```bash
  grep DATABASE_URL .env
  ```

- [ ] Variáveis de ambiente validadas
  ```bash
  # Verificar todas as variáveis necessárias
  grep -E "^[A-Z]" .env
  ```

### 4. Backup

- [ ] Backup do banco de dados atual (se atualizando)
  ```bash
  # PostgreSQL
  docker compose exec -T db pg_dump -U prova_user prova_modelagem_db | gzip > backup_pre_deploy_$(date +%Y%m%d_%H%M%S).sql.gz

  # SQLite
  cp data/provas.db backup_pre_deploy_$(date +%Y%m%d_%H%M%S).db
  ```

- [ ] Backup dos uploads
  ```bash
  tar -czf backup_uploads_$(date +%Y%m%d_%H%M%S).tar.gz uploads/
  ```

- [ ] Backup do .env atual
  ```bash
  cp .env .env.backup_$(date +%Y%m%d_%H%M%S)
  ```

### 5. Segurança

- [ ] Firewall configurado
  ```bash
  sudo ufw status
  sudo ufw allow ssh
  sudo ufw allow 80/tcp
  sudo ufw allow 443/tcp
  ```

- [ ] Portas desnecessárias fechadas
  ```bash
  sudo netstat -tulpn | grep LISTEN
  ```

- [ ] Certificado SSL disponível (produção)
  ```bash
  ls -la /etc/letsencrypt/live/seu-dominio.com/
  ```

### 6. Rede e DNS

- [ ] Domínio apontando para o servidor (se aplicável)
  ```bash
  nslookup seu-dominio.com
  dig seu-dominio.com
  ```

- [ ] Portas abertas no firewall do provedor de cloud
  - HTTP (80)
  - HTTPS (443)
  - SSH (22)

---

## Checklist de Deploy

### Deploy com Docker - SQLite

#### 1. Preparar Ambiente

- [ ] Clonar/atualizar repositório
  ```bash
  git clone <repo> /opt/prova_app
  cd /opt/prova_app
  # OU
  git pull origin main
  ```

- [ ] Criar estrutura de diretórios
  ```bash
  mkdir -p data uploads logs backups
  ```

- [ ] Ajustar permissões
  ```bash
  sudo chown -R 1000:1000 data uploads logs backups
  chmod -R 755 data uploads logs backups
  ```

#### 2. Configurar

- [ ] Configurar .env
  ```bash
  nano .env
  # Verificar:
  # - SECRET_KEY
  # - DATABASE_URL=sqlite:////app/data/provas.db
  # - ADMIN_USERNAME
  # - ADMIN_PASSWORD
  ```

- [ ] Validar configuração
  ```bash
  docker compose -f docker-compose.sqlite.yml config
  ```

#### 3. Build e Deploy

- [ ] Build da imagem
  ```bash
  docker compose -f docker-compose.sqlite.yml build
  ```

- [ ] Iniciar serviços
  ```bash
  docker compose -f docker-compose.sqlite.yml up -d
  ```

- [ ] Verificar status
  ```bash
  docker compose -f docker-compose.sqlite.yml ps
  ```

- [ ] Verificar logs
  ```bash
  docker compose -f docker-compose.sqlite.yml logs -f
  # Aguardar mensagem: "Servidor pronto! Escutando em..."
  ```

### Deploy com Docker - PostgreSQL

#### 1. Preparar Ambiente

- [ ] Clonar/atualizar repositório
  ```bash
  git clone <repo> /opt/prova_app
  cd /opt/prova_app
  ```

- [ ] Criar estrutura de diretórios
  ```bash
  mkdir -p uploads logs backups
  ```

- [ ] Ajustar permissões
  ```bash
  sudo chown -R 1000:1000 uploads logs backups
  chmod -R 755 uploads logs backups
  ```

#### 2. Configurar

- [ ] Configurar .env com PostgreSQL
  ```bash
  nano .env
  # Configurar:
  # - SECRET_KEY
  # - POSTGRES_DB
  # - POSTGRES_USER
  # - POSTGRES_PASSWORD
  # - DATABASE_URL
  # - ADMIN_USERNAME
  # - ADMIN_PASSWORD
  # - ADMIN_EMAIL
  ```

- [ ] Validar configuração
  ```bash
  docker compose config
  ```

#### 3. Build e Deploy

- [ ] Build das imagens
  ```bash
  docker compose build
  ```

- [ ] Iniciar PostgreSQL primeiro
  ```bash
  docker compose up -d db
  ```

- [ ] Aguardar PostgreSQL ficar pronto
  ```bash
  docker compose logs db | grep "ready to accept connections"
  sleep 10
  ```

- [ ] Iniciar aplicação
  ```bash
  docker compose up -d web
  ```

- [ ] Verificar status
  ```bash
  docker compose ps
  # Todos devem estar "healthy" ou "running"
  ```

- [ ] Verificar logs
  ```bash
  docker compose logs -f web
  ```

#### 4. Configurar Nginx (Opcional)

- [ ] Instalar Nginx
  ```bash
  sudo apt install nginx
  ```

- [ ] Copiar configuração
  ```bash
  sudo cp scripts/nginx.conf /etc/nginx/sites-available/prova_app
  ```

- [ ] Editar configuração
  ```bash
  sudo nano /etc/nginx/sites-available/prova_app
  # Alterar: server_name para seu domínio
  ```

- [ ] Criar link simbólico
  ```bash
  sudo ln -s /etc/nginx/sites-available/prova_app /etc/nginx/sites-enabled/
  ```

- [ ] Remover site padrão
  ```bash
  sudo rm /etc/nginx/sites-enabled/default
  ```

- [ ] Testar configuração
  ```bash
  sudo nginx -t
  ```

- [ ] Reiniciar Nginx
  ```bash
  sudo systemctl restart nginx
  sudo systemctl enable nginx
  ```

#### 5. Configurar SSL (Produção)

- [ ] Instalar Certbot
  ```bash
  sudo apt install certbot python3-certbot-nginx
  ```

- [ ] Obter certificado
  ```bash
  sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com
  ```

- [ ] Testar renovação automática
  ```bash
  sudo certbot renew --dry-run
  ```

---

## Checklist Pós-Deploy

### 1. Verificação Básica

- [ ] Aplicação acessível via navegador
  ```bash
  curl -I http://localhost:8000
  # OU
  curl -I https://seu-dominio.com
  ```

- [ ] Health check respondendo
  ```bash
  curl http://localhost:8000/health
  ```

- [ ] Login funcionando
  - Acessar http://seu-servidor/auth/login
  - Fazer login com credenciais de admin
  - Verificar redirecionamento para dashboard

### 2. Testes Funcionais

- [ ] Dashboard carrega sem erros
- [ ] Menu de navegação funciona
- [ ] Criar novo relatório
- [ ] Upload de arquivo (PPT, imagem)
- [ ] Adicionar referência
- [ ] Criar prova
- [ ] Upload de fotos
- [ ] Preencher checklist
- [ ] Aprovar/reprovar prova
- [ ] Gerar PDF do relatório
- [ ] Exportar para Excel
- [ ] Analytics carrega gráficos

### 3. Verificação de Logs

- [ ] Logs da aplicação sem erros críticos
  ```bash
  docker compose logs web | grep -i "error\|critical"
  ```

- [ ] Logs do Nginx sem erros (se usando)
  ```bash
  sudo tail -50 /var/log/nginx/provas_app_error.log
  ```

### 4. Performance

- [ ] Tempo de resposta aceitável (< 2s)
  ```bash
  time curl -I http://localhost:8000
  ```

- [ ] Uso de recursos dentro do esperado
  ```bash
  docker stats --no-stream
  ```

### 5. Segurança

- [ ] HTTPS funcionando (produção)
  ```bash
  curl -I https://seu-dominio.com
  # Verificar: HTTP/2 200
  ```

- [ ] Senha de admin alterada
  - Login → Perfil → Alterar Senha

- [ ] PostgreSQL não exposto publicamente
  ```bash
  sudo netstat -tulpn | grep 5432
  # Não deve aparecer 0.0.0.0:5432
  ```

- [ ] Security headers configurados
  ```bash
  curl -I https://seu-dominio.com | grep -E "X-Frame-Options|X-Content-Type-Options|Strict-Transport-Security"
  ```

### 6. Backup

- [ ] Backup automático configurado
  ```bash
  sudo crontab -l | grep backup
  ```

- [ ] Script de backup testado
  ```bash
  /opt/prova_app/scripts/docker-backup.sh
  ls -lh /opt/prova_app/backups/
  ```

### 7. Monitoramento

- [ ] Logs acessíveis
  ```bash
  ls -la /opt/prova_app/logs/
  ```

- [ ] Health check endpoint funcionando
  ```bash
  curl http://localhost:8000/health
  ```

- [ ] Alertas configurados (se aplicável)

### 8. Documentação

- [ ] Credenciais documentadas (em local seguro)
- [ ] URL de acesso documentada
- [ ] Comandos de administração documentados
- [ ] Contatos de suporte definidos
- [ ] Procedimento de escalação definido

### 9. Comunicação

- [ ] Equipe notificada sobre novo deploy
- [ ] Usuários informados sobre nova versão
- [ ] Changelog disponibilizado
- [ ] Treinamento agendado (se necessário)

---

## Comandos de Administração Mais Usados

### Gerenciamento de Containers (Docker)

```bash
# ============================================
# STATUS E MONITORAMENTO
# ============================================

# Ver status de todos os containers
docker compose ps

# Ver logs em tempo real
docker compose logs -f

# Ver logs apenas da aplicação
docker compose logs -f web

# Ver últimas 100 linhas de log
docker compose logs --tail=100 web

# Ver uso de recursos
docker stats

# Ver uso de recursos (snapshot)
docker stats --no-stream


# ============================================
# INICIAR / PARAR / REINICIAR
# ============================================

# Iniciar todos os serviços
docker compose up -d

# Parar todos os serviços
docker compose down

# Reiniciar todos os serviços
docker compose restart

# Reiniciar apenas a aplicação
docker compose restart web

# Parar preservando volumes
docker compose stop

# Iniciar após stop
docker compose start


# ============================================
# BUILD E ATUALIZAÇÃO
# ============================================

# Rebuild e restart
docker compose up -d --build

# Rebuild sem cache
docker compose build --no-cache

# Pull de novas imagens
docker compose pull

# Atualizar código e rebuild
git pull && docker compose up -d --build


# ============================================
# ACESSO E DEBUG
# ============================================

# Entrar no container da aplicação
docker compose exec web bash

# Executar comando Python
docker compose exec web python3 -c "from app import app; print(app.config)"

# Ver variáveis de ambiente
docker compose exec web env

# Ver arquivos no container
docker compose exec web ls -la /app

# Ver processos no container
docker compose exec web ps aux


# ============================================
# BANCO DE DADOS
# ============================================

# Conectar ao PostgreSQL
docker compose exec db psql -U prova_user -d prova_modelagem_db

# Backup do banco
docker compose exec -T db pg_dump -U prova_user prova_modelagem_db | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Restore do banco
gunzip < backup.sql.gz | docker compose exec -T db psql -U prova_user -d prova_modelagem_db

# Ver tamanho do banco
docker compose exec db psql -U prova_user -d prova_modelagem_db -c "SELECT pg_size_pretty(pg_database_size('prova_modelagem_db'));"

# Listar tabelas
docker compose exec db psql -U prova_user -d prova_modelagem_db -c "\dt"


# ============================================
# LIMPEZA
# ============================================

# Remover containers parados
docker container prune -f

# Remover imagens não usadas
docker image prune -a -f

# Remover volumes não usados (CUIDADO!)
docker volume prune -f

# Limpeza completa do sistema Docker
docker system prune -a --volumes -f
```

### Backup e Restore

```bash
# ============================================
# BACKUP COMPLETO
# ============================================

# Backup usando script automatizado
/opt/prova_app/scripts/docker-backup.sh

# Backup manual completo
DATE=$(date +%Y%m%d_%H%M%S)
docker compose exec -T db pg_dump -U prova_user prova_modelagem_db | gzip > backup_db_$DATE.sql.gz
tar -czf backup_uploads_$DATE.tar.gz uploads/
cp .env backup_env_$DATE


# ============================================
# RESTORE
# ============================================

# Parar aplicação
docker compose stop web

# Restore do banco
gunzip < backup_db_20250116.sql.gz | docker compose exec -T db psql -U prova_user -d prova_modelagem_db

# Restore dos uploads
tar -xzf backup_uploads_20250116.tar.gz

# Restart
docker compose start web


# ============================================
# BACKUP INCREMENTAL (rsync)
# ============================================

# Sincronizar uploads para backup externo
rsync -av --delete /opt/prova_app/uploads/ /backup/prova_app/uploads/
```

### Monitoramento e Diagnóstico

```bash
# ============================================
# LOGS
# ============================================

# Ver todos os logs
docker compose logs

# Logs de erro apenas
docker compose logs web | grep -i error

# Logs com timestamp
docker compose logs -t

# Seguir logs em tempo real
docker compose logs -f --tail=50

# Logs do Nginx (se instalado)
sudo tail -f /var/log/nginx/provas_app_access.log
sudo tail -f /var/log/nginx/provas_app_error.log


# ============================================
# HEALTH CHECK
# ============================================

# Verificar saúde da aplicação
curl http://localhost:8000/health

# Verificar com detalhes
curl -v http://localhost:8000/health

# Verificar resposta completa
curl -I http://localhost:8000/


# ============================================
# RECURSOS DO SISTEMA
# ============================================

# Ver uso de CPU e memória (live)
htop

# Ver uso de disco
df -h

# Ver tamanho dos diretórios
du -sh /opt/prova_app/*

# Ver processos Python
ps aux | grep python

# Ver conexões de rede
sudo netstat -tulpn | grep -E '8000|5432'


# ============================================
# ANÁLISE DE LOGS
# ============================================

# Contar erros por tipo
grep -i error /opt/prova_app/logs/app.log | awk '{print $4}' | sort | uniq -c

# Ver erros nas últimas 24h
find /opt/prova_app/logs -name "*.log" -mtime -1 -exec grep -i error {} \;

# Top 10 IPs com mais requisições (Nginx)
awk '{print $1}' /var/log/nginx/provas_app_access.log | sort | uniq -c | sort -rn | head -10

# Requisições mais lentas (Nginx)
awk '{print $NF, $7}' /var/log/nginx/provas_app_access.log | sort -rn | head -10
```

### Manutenção

```bash
# ============================================
# ATUALIZAÇÃO
# ============================================

# Atualizar código
cd /opt/prova_app
git pull origin main

# Rebuild e restart
docker compose up -d --build

# Verificar
docker compose ps
docker compose logs -f


# ============================================
# LIMPEZA
# ============================================

# Limpar logs antigos (>30 dias)
find /opt/prova_app/logs -name "*.log" -mtime +30 -delete

# Limpar backups antigos (>30 dias)
find /opt/prova_app/backups -name "*.gz" -mtime +30 -delete

# Limpar cache Python
find /opt/prova_app -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null


# ============================================
# ROTAÇÃO DE LOGS
# ============================================

# Recarregar Gunicorn (rotação de logs)
docker compose exec web kill -USR1 1

# Limpar logs do Docker
docker compose logs --no-log-prefix > /dev/null
```

### Segurança

```bash
# ============================================
# VERIFICAÇÕES DE SEGURANÇA
# ============================================

# Verificar permissões de arquivos
ls -la /opt/prova_app

# Verificar portas abertas
sudo netstat -tulpn

# Verificar usuários do sistema
cat /etc/passwd | grep -E "prova|appuser"

# Verificar firewall
sudo ufw status verbose


# ============================================
# ATUALIZAÇÕES DE SEGURANÇA
# ============================================

# Atualizar sistema operacional
sudo apt update && sudo apt upgrade -y

# Atualizar Docker
sudo apt install docker-ce docker-ce-cli containerd.io


# ============================================
# SSL/HTTPS
# ============================================

# Renovar certificado SSL
sudo certbot renew

# Testar renovação
sudo certbot renew --dry-run

# Ver certificados instalados
sudo certbot certificates
```

---

## Troubleshooting Rápido

### Container não inicia

```bash
# 1. Ver logs
docker compose logs web

# 2. Verificar configuração
docker compose config

# 3. Verificar variáveis de ambiente
docker compose exec web env | grep -E "DATABASE|SECRET|ADMIN"

# 4. Testar manualmente
docker compose run --rm web python3 -c "from app import app; print('OK')"
```

### Erro de conexão com banco

```bash
# 1. Verificar se PostgreSQL está rodando
docker compose ps db

# 2. Verificar logs do PostgreSQL
docker compose logs db

# 3. Testar conexão
docker compose exec web python3 << 'EOF'
import psycopg2
try:
    conn = psycopg2.connect("postgresql://prova_user:senha@db:5432/prova_modelagem_db")
    print("Conexão OK")
    conn.close()
except Exception as e:
    print(f"Erro: {e}")
EOF
```

### Erro de permissão

```bash
# Ajustar permissões (UID 1000 = appuser)
sudo chown -R 1000:1000 /opt/prova_app/uploads
sudo chown -R 1000:1000 /opt/prova_app/logs
sudo chown -R 1000:1000 /opt/prova_app/data
chmod -R 755 /opt/prova_app/uploads
chmod -R 755 /opt/prova_app/logs
chmod -R 755 /opt/prova_app/data
```

### Aplicação lenta

```bash
# 1. Ver uso de recursos
docker stats

# 2. Ver workers do Gunicorn
docker compose exec web ps aux | grep gunicorn

# 3. Ver queries lentas (PostgreSQL)
docker compose exec db psql -U prova_user -d prova_modelagem_db -c "SELECT * FROM pg_stat_activity WHERE state = 'active';"

# 4. Aumentar workers (se CPU disponível)
# Editar .env:
WORKERS=4

# Rebuild
docker compose up -d --build
```

---

## Comandos de Emergência

### Aplicação travada

```bash
# Restart forçado
docker compose restart web

# Se não funcionar, parar e iniciar
docker compose stop web
docker compose start web

# Último recurso: recrear container
docker compose up -d --force-recreate web
```

### Banco de dados corrompido

```bash
# 1. Parar aplicação
docker compose stop web

# 2. Backup do banco atual
docker compose exec -T db pg_dump -U prova_user prova_modelagem_db | gzip > emergency_backup_$(date +%Y%m%d_%H%M%S).sql.gz

# 3. Verificar integridade
docker compose exec db psql -U prova_user -d prova_modelagem_db -c "VACUUM ANALYZE;"

# 4. Se corrompido, restaurar último backup bom
gunzip < backup_ultimo_bom.sql.gz | docker compose exec -T db psql -U prova_user -d prova_modelagem_db

# 5. Reiniciar
docker compose start web
```

### Disco cheio

```bash
# 1. Verificar uso
df -h

# 2. Ver maiores diretórios
du -sh /opt/prova_app/* | sort -h

# 3. Limpar logs
find /opt/prova_app/logs -name "*.log" -mtime +7 -delete

# 4. Limpar backups antigos
find /opt/prova_app/backups -name "*.gz" -mtime +7 -delete

# 5. Limpar Docker
docker system prune -a -f

# 6. Verificar uploads grandes
find /opt/prova_app/uploads -type f -size +50M -exec ls -lh {} \;
```

### Rollback completo

```bash
# 1. Parar aplicação
docker compose down

# 2. Restaurar código anterior
git log --oneline -10
git checkout <commit-anterior>

# 3. Restaurar banco
gunzip < backup_pre_deploy.sql.gz | docker compose exec -T db psql -U prova_user -d prova_modelagem_db

# 4. Restaurar uploads
tar -xzf backup_uploads_pre_deploy.tar.gz

# 5. Rebuild e restart
docker compose up -d --build

# 6. Verificar
docker compose ps
docker compose logs -f
curl http://localhost:8000/health
```

---

## Referências Rápidas

| Ação | Comando |
|------|---------|
| Ver status | `docker compose ps` |
| Ver logs | `docker compose logs -f web` |
| Restart | `docker compose restart web` |
| Rebuild | `docker compose up -d --build` |
| Shell | `docker compose exec web bash` |
| Backup DB | `docker compose exec -T db pg_dump -U prova_user prova_modelagem_db \| gzip > backup.sql.gz` |
| Health check | `curl http://localhost:8000/health` |
| Ver recursos | `docker stats --no-stream` |

---

**Última atualização:** 2025-01-16
**Versão do sistema:** 2.0.0
