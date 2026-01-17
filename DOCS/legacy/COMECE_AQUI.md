# 🚀 COMECE AQUI - Deploy Docker em 5 Minutos

## ✅ O que você precisa:
- Servidor Linux (Ubuntu/Debian)
- Acesso SSH
- 10 minutos

---

## 📦 Passo 1: No Seu Servidor

```bash
# Copie e cole TUDO de uma vez:
curl -fsSL https://get.docker.com | sudo sh && \
sudo apt update && sudo apt install -y docker-compose-plugin && \
sudo usermod -aG docker $USER && \
echo "✅ Docker instalado! Faça logout e login novamente."
```

**⚠️ IMPORTANTE:** Fazer logout e login após instalar!

---

## 📤 Passo 2: Na Sua Máquina Local (WSL)

```bash
# Ir para o projeto
cd /home/icolas_atsuda/ProjetosWeb/prova_modelagem_app

# Comprimir
tar -czf prova_app.tar.gz --exclude='.venv' --exclude='venv' --exclude='.git' --exclude='__pycache__' .

# Enviar (SUBSTITUA com seus dados!)
scp prova_app.tar.gz SEU_USUARIO@SEU_SERVIDOR_IP:/tmp/

# Exemplo: scp prova_app.tar.gz root@192.168.1.100:/tmp/
```

---

## 🔧 Passo 3: No Servidor - Extrair

```bash
sudo mkdir -p /opt/prova_app && cd /opt/prova_app
sudo tar -xzf /tmp/prova_app.tar.gz
sudo chown -R $USER:$USER /opt/prova_app
```

---

## ⚙️ Passo 4: No Servidor - Configurar

```bash
cd /opt/prova_app
cp .env.example .env

# Gerar SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"

# Editar .env
nano .env
```

**Cole isso no .env (AJUSTE OS VALORES!):**

```bash
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=COLE_A_CHAVE_GERADA_ACIMA

# IMPORTANTE: use 'db' como host
DATABASE_URL=postgresql://prova_user:SuaSenhaForte@db:5432/prova_modelagem_db
POSTGRES_USER=prova_user
POSTGRES_PASSWORD=SuaSenhaForte
POSTGRES_DB=prova_modelagem_db

ADMIN_USERNAME=admin
ADMIN_PASSWORD=SuaSenhaAdmin
ADMIN_EMAIL=seu@email.com

HOST=0.0.0.0
PORT=8000
DEBUG=False
```

Salvar: **Ctrl+O**, **Enter**, **Ctrl+X**

---

## 🚀 Passo 5: No Servidor - Iniciar

```bash
cd /opt/prova_app

# Iniciar containers
docker compose up -d --build

# Ver logs (aguarde "Application startup complete")
docker compose logs -f

# Pressione Ctrl+C para sair dos logs
```

---

## ✅ Pronto! Testar

```bash
# Ver status
docker compose ps

# Testar
curl http://localhost:8000

# Acessar no navegador:
# http://SEU_IP:8000
```

**Login:**
- Usuário: admin
- Senha: a que você configurou

---

## 🌐 OPCIONAL: Adicionar Domínio + SSL

### 1. Instalar Nginx

```bash
sudo apt install -y nginx

sudo tee /etc/nginx/sites-available/prova_app > /dev/null << 'NGINXCONF'
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
NGINXCONF

sudo ln -s /etc/nginx/sites-available/prova_app /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx
```

### 2. Instalar SSL

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com
```

### 3. Firewall

```bash
sudo apt install -y ufw
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 📋 Comandos Úteis

```bash
# Ver logs
docker compose logs -f

# Reiniciar
docker compose restart web

# Parar tudo
docker compose stop

# Iniciar tudo
docker compose start

# Status
docker compose ps

# Backup
chmod +x scripts/docker-backup.sh
./scripts/docker-backup.sh
```

---

## 🆘 Problemas?

### Aplicação não abre
```bash
docker compose logs -f web
docker compose restart web
```

### Resetar tudo
```bash
docker compose down
docker compose up -d --build
```

---

## 📚 Documentação Completa

- **[README_DEPLOY.md](README_DEPLOY.md)** - Índice principal
- **[INICIO_RAPIDO_DOCKER.md](INICIO_RAPIDO_DOCKER.md)** - Guia detalhado
- **[DEPLOY_DOCKER.md](DEPLOY_DOCKER.md)** - Documentação completa
- **[DEPLOY_PRODUCAO.md](DEPLOY_PRODUCAO.md)** - Deploy manual

---

## ✅ Checklist

- [ ] Docker instalado
- [ ] Código no servidor (/opt/prova_app)
- [ ] .env configurado
- [ ] `docker compose up -d` executado
- [ ] Acesso http://SEU_IP:8000 funcionando
- [ ] Login funcionando
- [ ] Nginx instalado (opcional)
- [ ] SSL configurado (opcional)
- [ ] Firewall ativo

---

**🎉 Sistema no ar!**

Acesse: https://seu-dominio.com (ou http://SEU_IP:8000)
Login: admin / sua senha

