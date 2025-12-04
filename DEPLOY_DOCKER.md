# 🐳 Deploy com Docker - Guia Definitivo

## 🎯 Por que Docker?
✅ Setup em minutos
✅ Isolamento completo
✅ Fácil atualização e rollback
✅ Funciona em qualquer servidor
✅ Backup simplificado

---

## 🚀 Deploy em 3 Passos (10 minutos)

### Passo 1: Preparar Servidor (2 min)

```bash
# Conectar ao servidor
ssh usuario@seu-servidor.com

# Instalar Docker (se não tiver)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo apt update
sudo apt install docker-compose-plugin -y

# Verificar instalação
docker --version
docker compose version

# IMPORTANTE: Fazer logout e login novamente para aplicar permissões
exit
```

### Passo 2: Transferir Aplicação (3 min)

**Opção A: Via SCP (da sua máquina local)**

```bash
# Na sua máquina (WSL)
cd /home/icolas_atsuda/ProjetosWeb/prova_modelagem_app

# Comprimir (sem arquivos desnecessários)
tar -czf prova_app.tar.gz \
    --exclude='.venv' \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    --exclude='instance' \
    --exclude='uploads/*' \
    .

# Transferir para servidor
scp prova_app.tar.gz usuario@seu-servidor.com:/tmp/

# No servidor, extrair
ssh usuario@seu-servidor.com
sudo mkdir -p /opt/prova_app
cd /opt/prova_app
sudo tar -xzf /tmp/prova_app.tar.gz
rm /tmp/prova_app.tar.gz
sudo chown -R $USER:$USER /opt/prova_app
```

**Opção B: Via Git (recomendado para updates)**

```bash
# No servidor
cd /opt
sudo git clone https://github.com/seu-usuario/seu-repo.git prova_app
cd prova_app
```

### Passo 3: Configurar e Iniciar (5 min)

```bash
cd /opt/prova_app

# 1. Configurar variáveis de ambiente
cp .env.example .env
nano .env
```

**Edite o .env com suas configurações:**

```bash
# Flask
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=cole_a_chave_gerada_abaixo

# Database (IMPORTANTE: use 'db' como host quando usar Docker Compose)
DATABASE_URL=postgresql://prova_user:SUA_SENHA_FORTE@db:5432/prova_modelagem_db

# Admin
ADMIN_USERNAME=admin
ADMIN_PASSWORD=sua_senha_admin_forte
ADMIN_EMAIL=seu@email.com

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
PERMANENT_SESSION_LIFETIME=3600

# Logging
LOG_LEVEL=INFO
```

**Gerar SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
# Cole o resultado no .env
```

**2. Iniciar containers:**

```bash
# Build e start (primeira vez)
docker compose up -d --build

# Ver logs em tempo real
docker compose logs -f

# Aguardar até ver: "Application startup complete"
# Pressione Ctrl+C para sair dos logs
```

**3. Criar usuário admin:**

```bash
# Executar dentro do container
docker compose exec web python3 -c "
from app import app, db
from models import User
from werkzeug.security import generate_password_hash
import os

with app.app_context():
    # Verificar se admin já existe
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username=os.getenv('ADMIN_USERNAME', 'admin'),
            email=os.getenv('ADMIN_EMAIL', 'admin@puket.com'),
            password_hash=generate_password_hash(os.getenv('ADMIN_PASSWORD', 'admin123')),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print('✅ Usuário admin criado!')
    else:
        print('ℹ️  Usuário admin já existe')
"
```

---

## ✅ Verificação

```bash
# Verificar containers rodando
docker compose ps

# Deve mostrar:
# NAME                STATUS              PORTS
# prova_app-web-1     Up About a minute   0.0.0.0:8000->8000/tcp
# prova_app-db-1      Up About a minute   5432/tcp

# Testar acesso
curl http://localhost:8000

# Acessar no navegador (substitua pelo IP do seu servidor):
# http://SEU_IP:8000
```

---

## 🌐 Expor para Internet (Nginx + SSL)

### Opção 1: Nginx no Host (Recomendado)

```bash
# Instalar Nginx
sudo apt install nginx -y

# Criar configuração
sudo nano /etc/nginx/sites-available/prova_app
```

Cole:

```nginx
upstream prova_app {
    server localhost:8000;
}

server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    client_max_body_size 50M;

    location / {
        proxy_pass http://prova_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/prova_app /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Testar e recarregar
sudo nginx -t
sudo systemctl restart nginx
```

**Instalar SSL (Let's Encrypt):**

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obter certificado
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com

# Renovação é automática!
```

### Opção 2: Usando Traefik (Avançado)

Já configurado no `docker-compose.yml`. Basta descomentar a seção do Traefik.

---

## 📋 Comandos Úteis

### Gerenciar Containers

```bash
# Ver status
docker compose ps

# Ver logs
docker compose logs -f          # Todos os serviços
docker compose logs -f web      # Apenas app
docker compose logs -f db       # Apenas banco

# Parar containers
docker compose stop

# Iniciar containers
docker compose start

# Reiniciar containers
docker compose restart

# Reiniciar apenas a aplicação
docker compose restart web

# Parar e remover containers
docker compose down

# Parar e remover TUDO (incluindo volumes - CUIDADO!)
docker compose down -v
```

### Acessar Container

```bash
# Entrar no container da aplicação
docker compose exec web bash

# Entrar no PostgreSQL
docker compose exec db psql -U prova_user -d prova_modelagem_db

# Executar comando Python
docker compose exec web python3 -c "print('Hello')"
```

### Atualizar Aplicação

```bash
cd /opt/prova_app

# Método 1: Via Git
git pull origin main
docker compose restart web

# Método 2: Rebuild completo
docker compose up -d --build --force-recreate

# Método 3: Atualizar apenas código (sem rebuild)
docker compose restart web
```

### Backup

```bash
# Backup do banco
docker compose exec db pg_dump -U prova_user prova_modelagem_db | gzip > backup_$(date +%Y%m%d).sql.gz

# Backup dos uploads
tar -czf backup_uploads_$(date +%Y%m%d).tar.gz /opt/prova_app/uploads/

# Backup completo (automático)
./scripts/docker-backup.sh
```

### Restaurar Backup

```bash
# Restaurar banco
gunzip < backup_20241204.sql.gz | docker compose exec -T db psql -U prova_user -d prova_modelagem_db

# Restaurar uploads
tar -xzf backup_uploads_20241204.tar.gz -C /opt/prova_app/
```

---

## 🔒 Segurança

### Firewall

```bash
# Instalar UFW
sudo apt install ufw -y

# Configurar regras
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Ativar
sudo ufw enable

# Ver status
sudo ufw status
```

### Atualizar Sistema

```bash
# Atualizar servidor
sudo apt update && sudo apt upgrade -y

# Atualizar Docker
sudo apt update && sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

---

## 📊 Monitoramento

### Ver Recursos

```bash
# Uso de recursos dos containers
docker stats

# Espaço em disco
docker system df

# Logs de erro
docker compose logs --tail=100 web | grep ERROR
```

### Health Check

```bash
# Verificar se aplicação responde
curl http://localhost:8000/health || echo "❌ App não está respondendo"

# Verificar banco
docker compose exec db pg_isready -U prova_user
```

---

## 🆘 Troubleshooting

### Problema 1: Container não inicia

```bash
# Ver logs completos
docker compose logs web

# Verificar se porta está em uso
sudo netstat -tlnp | grep 8000

# Remover e recriar
docker compose down
docker compose up -d --force-recreate
```

### Problema 2: Erro de conexão com banco

```bash
# Verificar se banco está rodando
docker compose ps db

# Ver logs do banco
docker compose logs db

# Testar conexão
docker compose exec web python3 -c "
from app import app, db
with app.app_context():
    try:
        db.engine.connect()
        print('✅ Conexão OK')
    except Exception as e:
        print(f'❌ Erro: {e}')
"
```

### Problema 3: Permissões de arquivo

```bash
# Ajustar permissões dos uploads
sudo chown -R 1000:1000 /opt/prova_app/uploads
docker compose restart web
```

### Problema 4: Out of Memory

```bash
# Ver uso de memória
docker stats

# Limpar cache do Docker
docker system prune -a --volumes

# Aumentar memória no docker-compose.yml:
# services:
#   web:
#     deploy:
#       resources:
#         limits:
#           memory: 1G
```

---

## 🔄 Migração de Dados

### Importar dados de outro servidor

```bash
# No servidor antigo
docker compose exec db pg_dump -U prova_user prova_modelagem_db | gzip > export.sql.gz
tar -czf uploads.tar.gz /opt/prova_app/uploads/

# Transferir para novo servidor
scp export.sql.gz uploads.tar.gz usuario@novo-servidor.com:/tmp/

# No novo servidor
cd /opt/prova_app
gunzip < /tmp/export.sql.gz | docker compose exec -T db psql -U prova_user -d prova_modelagem_db
tar -xzf /tmp/uploads.tar.gz -C /opt/prova_app/
docker compose restart web
```

---

## 📈 Otimizações de Performance

### 1. Usar volumes nomeados (já configurado)
### 2. Aumentar workers do Gunicorn

Editar `gunicorn_config.py`:
```python
workers = 4  # Ajuste conforme CPU disponível
```

### 3. Adicionar Redis para cache

Editar `docker-compose.yml`, adicionar:
```yaml
  redis:
    image: redis:7-alpine
    restart: always
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

---

## ✅ Checklist de Deploy

- [ ] Docker e Docker Compose instalados
- [ ] Aplicação transferida para /opt/prova_app
- [ ] Arquivo .env configurado corretamente
- [ ] SECRET_KEY gerada e configurada
- [ ] DATABASE_URL usando `db` como host
- [ ] Containers iniciados (`docker compose up -d`)
- [ ] Usuário admin criado
- [ ] Firewall configurado (portas 80, 443, SSH)
- [ ] Nginx instalado e configurado (se usar)
- [ ] SSL configurado com Let's Encrypt
- [ ] Backup automatizado configurado
- [ ] Acesso via navegador funcionando

---

## 🎯 Próximos Passos

1. **Configurar domínio** e apontar para o servidor
2. **Instalar SSL** para HTTPS seguro
3. **Configurar backup automático** (cron job)
4. **Monitorar logs** periodicamente
5. **Atualizar** sistema e aplicação regularmente

---

## 📞 Suporte Rápido

**Aplicação não abre:**
```bash
docker compose logs -f web
```

**Erro 502:**
```bash
docker compose restart web
```

**Banco não conecta:**
```bash
docker compose restart db
docker compose logs db
```

**Ver tudo:**
```bash
docker compose ps
docker compose logs --tail=50
```

---

**Deploy Docker otimizado para Puket**
Documentação completa em `DEPLOY_PRODUCAO.md`
