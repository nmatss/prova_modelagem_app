# Quick Reference - Sistema de Provas de Modelagem

**Guia de Referência Rápida | Comandos Essenciais**

---

## 🚀 Deploy em 5 Comandos (SQLite)

```bash
# 1. Clonar/navegar
cd /opt/prova_app

# 2. Configurar .env
cp .env.example .env && nano .env

# 3. Criar estrutura
mkdir -p data uploads logs backups && chown -R 1000:1000 data uploads logs backups

# 4. Deploy
docker compose -f docker-compose.sqlite.yml up -d

# 5. Verificar
docker compose -f docker-compose.sqlite.yml ps && curl http://localhost:5000/health
```

**Tempo:** 10 minutos | **Acesso:** http://localhost:5000

---

## 🐳 Comandos Docker Essenciais

### Status e Logs
```bash
docker compose ps                    # Ver status
docker compose logs -f              # Logs ao vivo
docker compose logs -f web          # Logs apenas da app
docker compose logs --tail=100 web  # Últimas 100 linhas
docker stats --no-stream            # Uso de recursos
```

### Controle
```bash
docker compose up -d                # Iniciar
docker compose down                 # Parar
docker compose restart web          # Reiniciar app
docker compose restart              # Reiniciar tudo
docker compose up -d --build        # Rebuild e reiniciar
```

### Debug
```bash
docker compose exec web bash        # Shell no container
docker compose exec web env         # Ver variáveis
docker compose config               # Ver configuração
docker compose exec web python3 -c "from app import app; print('OK')"
```

---

## 💾 Backup e Restore - One-Liners

### Backup Rápido
```bash
# Banco
docker compose exec -T db pg_dump -U prova_user prova_modelagem_db | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Uploads
tar -czf backup_uploads_$(date +%Y%m%d_%H%M%S).tar.gz uploads/

# Tudo (usando script)
./scripts/docker-backup.sh
```

### Restore Rápido
```bash
# Parar app
docker compose stop web

# Restore banco
gunzip < backup_20250116.sql.gz | docker compose exec -T db psql -U prova_user -d prova_modelagem_db

# Restore uploads
tar -xzf backup_uploads_20250116.tar.gz

# Reiniciar
docker compose start web
```

---

## 🔍 Troubleshooting em 30 Segundos

### Container não inicia
```bash
docker compose logs web | tail -50
docker compose config
docker compose up web  # Sem -d para ver erros
```

### Banco não conecta
```bash
docker compose ps db
docker compose logs db
docker compose exec web python3 -c "import psycopg2; psycopg2.connect('postgresql://prova_user:senha@db:5432/prova_modelagem_db')"
```

### Erro de permissão
```bash
sudo chown -R 1000:1000 uploads logs data
chmod -R 755 uploads logs data
```

### App lenta
```bash
docker stats
ps aux | grep gunicorn
# Aumentar WORKERS no .env
```

---

## 📊 Monitoramento Rápido

### Health Check
```bash
curl http://localhost:8000/health
curl -I http://localhost:8000/
```

### Recursos
```bash
docker stats --no-stream              # CPU/RAM dos containers
df -h /opt/prova_app                 # Espaço em disco
free -h                              # Memória do host
```

### Logs de Erro
```bash
docker compose logs web | grep -i error | tail -20
find /opt/prova_app/logs -name "*.log" -mtime -1 -exec grep -i error {} \;
```

---

## 🔧 Manutenção Diária

```bash
# Checklist diário (1 minuto)
docker compose ps                                    # Status OK?
docker stats --no-stream                            # Recursos OK?
curl -s http://localhost:8000/health | grep "OK"   # Health OK?
df -h | grep "/opt/prova_app"                      # Disco OK?
docker compose logs web | grep -i error | wc -l    # Erros < 10?
```

---

## 🆘 Comandos de Emergência

### App Travada
```bash
docker compose restart web
# ou
docker compose up -d --force-recreate web
```

### Disco Cheio
```bash
find /opt/prova_app/logs -name "*.log" -mtime +7 -delete
find /opt/prova_app/backups -name "*.gz" -mtime +7 -delete
docker system prune -a -f
```

### Rollback Completo
```bash
docker compose down
git checkout <commit-anterior>
gunzip < backup_pre_deploy.sql.gz | docker compose exec -T db psql -U prova_user -d prova_modelagem_db
tar -xzf backup_uploads_pre_deploy.tar.gz
docker compose up -d --build
```

---

## 📝 Variáveis de Ambiente Essenciais (.env)

```bash
# Obrigatórias
SECRET_KEY=sua-chave-64-caracteres                    # python3 -c "import secrets; print(secrets.token_hex(32))"
DATABASE_URL=sqlite:////app/data/provas.db            # ou postgresql://...
ADMIN_USERNAME=admin
ADMIN_PASSWORD=senha_forte

# Importantes
PORT=8000                                             # 5000 (SQLite) ou 8000 (PostgreSQL)
WORKERS=2                                             # 2 (SQLite) ou 4 (PostgreSQL)
LOG_LEVEL=INFO
MAX_CONTENT_LENGTH=16777216                           # 16MB

# PostgreSQL
POSTGRES_DB=prova_modelagem_db
POSTGRES_USER=prova_user
POSTGRES_PASSWORD=senha_forte
```

---

## 🎯 Workflows Comuns

### Atualizar Aplicação
```bash
cd /opt/prova_app
./scripts/docker-backup.sh                # Backup
git pull origin main                      # Código novo
docker compose up -d --build              # Deploy
docker compose logs -f web                # Verificar
curl http://localhost:8000/health         # Testar
```

### Trocar de SQLite para PostgreSQL
```bash
# 1. Backup SQLite
docker compose -f docker-compose.sqlite.yml exec -T app cat /app/data/provas.db > backup_sqlite.db

# 2. Parar SQLite
docker compose -f docker-compose.sqlite.yml down

# 3. Configurar .env para PostgreSQL
nano .env  # Mudar DATABASE_URL e adicionar POSTGRES_*

# 4. Iniciar PostgreSQL
docker compose up -d

# 5. Migrar dados (script Python customizado)
# Ver: scripts/database/migrate_to_postgres.py
```

### Ver Tamanho dos Dados
```bash
# Banco PostgreSQL
docker compose exec db psql -U prova_user -d prova_modelagem_db -c "SELECT pg_size_pretty(pg_database_size('prova_modelagem_db'));"

# Banco SQLite
du -h data/provas.db

# Uploads
du -sh uploads/

# Logs
du -sh logs/

# Tudo
du -sh /opt/prova_app/*
```

---

## 🔐 Segurança Quick Check

```bash
# Verificar SECRET_KEY não é padrão
grep SECRET_KEY .env | grep -v "change-me"

# PostgreSQL não exposto
sudo netstat -tulpn | grep 5432 | grep -v "127.0.0.1"

# Firewall ativo
sudo ufw status | grep active

# HTTPS funcionando (produção)
curl -I https://seu-dominio.com | grep "HTTP/2"

# Senha de admin alterada (verificar no primeiro acesso)
```

---

## 📈 Performance Quick Wins

### Aumentar Workers
```bash
# .env
WORKERS=4  # De 2 para 4 (se CPU disponível)

# Reiniciar
docker compose up -d --build
```

### Habilitar Nginx Cache
```nginx
# /etc/nginx/sites-available/prova_app
location /static/ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

### Vacuum PostgreSQL
```bash
docker compose exec db psql -U prova_user -d prova_modelagem_db -c "VACUUM ANALYZE;"
```

---

## 🗂️ Estrutura de Diretórios

```
/opt/prova_app/
├── app.py                    # App principal
├── models.py                 # Modelos de dados
├── .env                      # Configurações (NUNCA commitar)
├── Dockerfile                # Imagem Docker
├── docker-compose.yml        # PostgreSQL
├── docker-compose.sqlite.yml # SQLite
├── requirements.txt          # Dependências Python
│
├── data/                     # Banco SQLite
├── uploads/                  # Arquivos enviados
│   ├── fotos/
│   ├── ppts/
│   └── tabelas/
├── logs/                     # Logs
│   ├── app.log
│   ├── error.log
│   └── access.log
├── backups/                  # Backups
│   ├── db_*.sql.gz
│   └── uploads_*.tar.gz
│
├── static/                   # Arquivos estáticos
│   ├── css/
│   ├── js/
│   └── img/
├── templates/                # Templates HTML
└── scripts/                  # Scripts de automação
    ├── docker-backup.sh
    ├── deploy.sh
    └── database/
```

---

## 📞 Onde Buscar Ajuda

| Problema | Documento | Seção |
|----------|-----------|-------|
| Deploy inicial | [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md) | Deploy Rápido ou Completo |
| Erro no Docker | [DOCKER_GUIDE.md](DOCKER_GUIDE.md) | Troubleshooting |
| App não funciona | [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md) | Troubleshooting Comum |
| Comandos | [DEPLOY_CHECKLIST_COMPLETE.md](DEPLOY_CHECKLIST_COMPLETE.md) | Comandos de Administração |
| Backup/Restore | [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md) | Backup e Restore |
| Performance | [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md) | Performance e Otimização |
| Visão geral | [README_DOCKER_DEPLOY.md](README_DOCKER_DEPLOY.md) | Todo o documento |

---

## 🎓 Cheat Sheet de Comandos

### Docker Compose
| Ação | Comando |
|------|---------|
| Iniciar | `docker compose up -d` |
| Parar | `docker compose down` |
| Restart | `docker compose restart` |
| Logs | `docker compose logs -f` |
| Status | `docker compose ps` |
| Rebuild | `docker compose up -d --build` |
| Shell | `docker compose exec web bash` |

### Git
| Ação | Comando |
|------|---------|
| Atualizar | `git pull origin main` |
| Ver log | `git log --oneline -10` |
| Rollback | `git checkout <commit>` |
| Status | `git status` |

### Sistema
| Ação | Comando |
|------|---------|
| Disco | `df -h` |
| Memória | `free -h` |
| CPU | `top` |
| Rede | `netstat -tulpn` |
| Processos | `ps aux | grep gunicorn` |

### Nginx
| Ação | Comando |
|------|---------|
| Testar config | `sudo nginx -t` |
| Reload | `sudo systemctl reload nginx` |
| Restart | `sudo systemctl restart nginx` |
| Logs | `sudo tail -f /var/log/nginx/error.log` |

---

## 🏁 Deploy Checklist (1 Página)

### Pré-Deploy
- [ ] Docker instalado
- [ ] .env configurado
- [ ] SECRET_KEY gerada
- [ ] Diretórios criados
- [ ] Backup (se atualizando)

### Deploy
- [ ] `docker compose up -d`
- [ ] `docker compose ps` (todos rodando)
- [ ] `curl http://localhost:8000/health` (OK)
- [ ] Login funciona
- [ ] Upload funciona

### Pós-Deploy
- [ ] Senha de admin alterada
- [ ] Backup automático configurado
- [ ] Firewall configurado
- [ ] SSL configurado (produção)
- [ ] Equipe notificada

---

## 🔢 Portas e URLs

| Serviço | Porta | URL |
|---------|-------|-----|
| Flask (SQLite) | 5000 | http://localhost:5000 |
| Gunicorn (PostgreSQL) | 8000 | http://localhost:8000 |
| PostgreSQL | 5432 | Interno (não expor) |
| Nginx | 80/443 | http(s)://seu-dominio.com |

---

## 💡 Dicas Pro

### Desenvolvimento Local
```bash
# Usar SQLite para desenvolvimento
docker compose -f docker-compose.sqlite.yml up -d

# Hot reload automático (Flask dev server)
FLASK_DEBUG=True FLASK_ENV=development python app.py
```

### Logs Coloridos
```bash
# Instalar ccze
sudo apt install ccze

# Ver logs coloridos
docker compose logs -f | ccze -A
```

### Alias Úteis
```bash
# Adicionar ao ~/.bashrc
alias dcp='docker compose'
alias dcl='docker compose logs -f'
alias dcs='docker compose ps'
alias dcr='docker compose restart'

# Recarregar
source ~/.bashrc

# Usar
dcs      # docker compose ps
dcl web  # docker compose logs -f web
```

### Watch Logs
```bash
# Ver logs que mudam em tempo real
watch -n 2 'docker compose logs --tail=20 web'
```

---

## 📚 Documentação Completa

**6 Documentos Principais (~200 páginas):**

1. **[README_DOCKER_DEPLOY.md](README_DOCKER_DEPLOY.md)** - Comece aqui
2. **[DOCKER_GUIDE.md](DOCKER_GUIDE.md)** - Docker completo
3. **[DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)** - Deploy passo a passo
4. **[MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md)** - Manutenção diária
5. **[DEPLOY_CHECKLIST_COMPLETE.md](DEPLOY_CHECKLIST_COMPLETE.md)** - Checklists
6. **[DOCS_INDEX.md](DOCS_INDEX.md)** - Índice completo

**Este arquivo:** Quick Reference para consultas rápidas

---

## 🆘 Contatos de Emergência

| Situação | Ação |
|----------|------|
| App não responde | Verificar logs: `docker compose logs web` |
| Banco corrompido | Restore backup: Ver [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md) |
| Disco cheio | Limpar: `find /opt/prova_app/logs -mtime +7 -delete` |
| Invasão suspeita | Parar: `docker compose down` + Verificar logs |
| Dúvidas | Consultar documentação ou equipe de dev |

---

**Última atualização:** 2025-01-16
**Versão:** 1.0
**Sistema:** Prova de Modelagem App 2.0.0

**💾 Salve este arquivo para referência rápida!**
