# ⚡ Início Rápido Docker - 5 Minutos

## 📋 Pré-requisitos
- Servidor Linux com Ubuntu 20.04+ ou Debian 11+
- Acesso SSH como root ou com sudo
- IP fixo ou domínio configurado

---

## 🚀 Comandos para Copiar e Colar

### 1️⃣ No Servidor - Instalar Docker (apenas primeira vez)

```bash
# Instalar Docker
curl -fsSL https://get.docker.com | sudo sh

# Instalar Docker Compose
sudo apt update && sudo apt install -y docker-compose-plugin

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# IMPORTANTE: Fazer logout e login novamente
exit
```

Reconecte ao servidor após o exit:
```bash
ssh seu-usuario@seu-servidor.com
```

---

### 2️⃣ Na Sua Máquina Local (WSL) - Preparar e Enviar

```bash
# Ir para o diretório do projeto
cd /home/icolas_atsuda/ProjetosWeb/prova_modelagem_app

# Comprimir projeto
tar -czf prova_app.tar.gz \
    --exclude='.venv' \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='instance' \
    --exclude='uploads/*' \
    .

# Enviar para servidor (SUBSTITUA com seus dados)
scp prova_app.tar.gz SEU_USUARIO@SEU_SERVIDOR:/tmp/

# Exemplo real:
# scp prova_app.tar.gz root@192.168.1.100:/tmp/
# ou
# scp prova_app.tar.gz admin@meusite.com:/tmp/
```

---

### 3️⃣ No Servidor - Extrair e Configurar

```bash
# Criar diretório e extrair
sudo mkdir -p /opt/prova_app
cd /opt/prova_app
sudo tar -xzf /tmp/prova_app.tar.gz
rm /tmp/prova_app.tar.gz

# Ajustar permissões
sudo chown -R $USER:$USER /opt/prova_app
```

---

### 4️⃣ No Servidor - Configurar Ambiente

```bash
# Copiar arquivo de exemplo
cd /opt/prova_app
cp .env.example .env

# Gerar SECRET_KEY
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"

# Editar .env (COPIE a SECRET_KEY gerada acima)
nano .env
```

**Cole este conteúdo no .env (ajuste os valores):**

```bash
# Flask
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=COLE_AQUI_A_CHAVE_GERADA_ACIMA

# Database - IMPORTANTE: use 'db' como host
DATABASE_URL=postgresql://prova_user:SuaSenhaForte123@db:5432/prova_modelagem_db

# Admin
ADMIN_USERNAME=admin
ADMIN_PASSWORD=SuaSenhaAdminForte123
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
LOG_FILE=/app/logs/app.log
```

**Salvar:** Ctrl+O, Enter, Ctrl+X

---

### 5️⃣ No Servidor - Iniciar Docker

```bash
cd /opt/prova_app

# Build e iniciar containers
docker compose up -d --build

# Ver logs (aguarde aparecer "Application startup complete")
docker compose logs -f

# Pressione Ctrl+C para sair dos logs quando ver a mensagem acima
```

---

### 6️⃣ No Servidor - Criar Usuário Admin

```bash
cd /opt/prova_app

# Executar comando de criação do admin
docker compose exec web python3 -c "
from app import app, db
from models import User
from werkzeug.security import generate_password_hash
import os

with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username=os.getenv('ADMIN_USERNAME', 'admin'),
            email=os.getenv('ADMIN_EMAIL', 'admin@puket.com'),
            password_hash=generate_password_hash(os.getenv('ADMIN_PASSWORD')),
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

### 7️⃣ Verificar

```bash
# Ver status dos containers
docker compose ps

# Deve mostrar:
# NAME                STATUS              PORTS
# prova_app-web-1     Up                  0.0.0.0:8000->8000/tcp
# prova_app-db-1      Up                  5432/tcp

# Testar localmente
curl http://localhost:8000

# Pegar IP do servidor
ip addr show | grep "inet " | grep -v 127.0.0.1
```

**Acessar no navegador:**
```
http://SEU_IP:8000
```

**Login:**
- Usuário: admin (ou o que você configurou)
- Senha: a que você colocou no .env

---

## 🌐 OPCIONAL: Adicionar Nginx e SSL

### Instalar Nginx

```bash
# Instalar
sudo apt install -y nginx

# Criar configuração
sudo nano /etc/nginx/sites-available/prova_app
```

**Cole este conteúdo (SUBSTITUA seu-dominio.com):**

```nginx
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    client_max_body_size 50M;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Ativar e reiniciar:**

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/prova_app /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Testar e reiniciar
sudo nginx -t
sudo systemctl restart nginx
```

### Adicionar SSL (HTTPS)

```bash
# Instalar Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obter certificado (SUBSTITUA seu domínio)
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com

# Seguir instruções na tela
# Escolher opção para redirecionar HTTP para HTTPS
```

### Configurar Firewall

```bash
# Instalar UFW
sudo apt install -y ufw

# Configurar regras
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Ativar
sudo ufw enable

# Verificar
sudo ufw status
```

---

## 📦 Backup Automático

```bash
# Tornar script executável
chmod +x /opt/prova_app/scripts/docker-backup.sh

# Testar backup manual
/opt/prova_app/scripts/docker-backup.sh

# Configurar backup automático diário (2h da manhã)
sudo crontab -e

# Adicionar esta linha:
0 2 * * * /opt/prova_app/scripts/docker-backup.sh >> /opt/prova_app/logs/backup.log 2>&1
```

---

## 🔧 Comandos Úteis do Dia a Dia

```bash
# Ver logs em tempo real
docker compose logs -f

# Reiniciar aplicação
docker compose restart web

# Parar tudo
docker compose stop

# Iniciar tudo
docker compose start

# Ver status
docker compose ps

# Backup manual
/opt/prova_app/scripts/docker-backup.sh

# Atualizar aplicação (após enviar novos arquivos)
cd /opt/prova_app
docker compose restart web
# ou rebuild completo:
docker compose up -d --build --force-recreate
```

---

## 🆘 Troubleshooting Rápido

### Aplicação não abre
```bash
docker compose logs -f web
docker compose restart web
```

### Ver erros
```bash
docker compose logs --tail=100 web | grep -i error
```

### Reiniciar tudo do zero
```bash
cd /opt/prova_app
docker compose down
docker compose up -d --build --force-recreate
```

### Limpar espaço
```bash
docker system prune -a
```

---

## ✅ Checklist Final

- [ ] Docker instalado
- [ ] Código transferido para /opt/prova_app
- [ ] .env configurado (SECRET_KEY, senhas, etc)
- [ ] DATABASE_URL usando `db` como host
- [ ] `docker compose up -d` executado
- [ ] Usuário admin criado
- [ ] Acesso http://SEU_IP:8000 funcionando
- [ ] Nginx instalado (opcional)
- [ ] SSL configurado (opcional)
- [ ] Firewall ativo
- [ ] Backup automático configurado

---

## 🎯 URLs de Acesso

**Sem Nginx/SSL:**
- http://SEU_IP:8000

**Com Nginx sem SSL:**
- http://seu-dominio.com

**Com Nginx e SSL:**
- https://seu-dominio.com
- https://seu-dominio.com/admin (painel administrativo)

**Login padrão:**
- Usuário: admin
- Senha: a configurada no .env

---

## 📞 Suporte Emergencial

**Container não inicia:**
```bash
docker compose down
docker compose up -d --build
docker compose logs -f
```

**Erro no banco:**
```bash
docker compose restart db
docker compose logs db
```

**Resetar tudo (CUIDADO - apaga dados):**
```bash
docker compose down -v
docker compose up -d --build
# Criar admin novamente
```

---

**Sistema pronto para produção! 🚀**

Para mais detalhes, consulte:
- `DEPLOY_DOCKER.md` - Documentação completa Docker
- `DEPLOY_PRODUCAO.md` - Deploy tradicional sem Docker
