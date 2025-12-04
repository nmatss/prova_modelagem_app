# 🚀 Deploy Rápido - Resumo Executivo

## ⚡ Deploy em 5 Passos (15 minutos)

### 1️⃣ Preparar Servidor (2 min)
```bash
# Conectar ao servidor
ssh root@seu-servidor.com

# Atualizar sistema
apt update && apt upgrade -y
```

### 2️⃣ Transferir Aplicação (3 min)
```bash
# Na sua máquina local
cd /home/icolas_atsuda/ProjetosWeb/prova_modelagem_app
tar -czf prova_app.tar.gz --exclude='.venv' --exclude='venv' --exclude='.git' .
scp prova_app.tar.gz root@seu-servidor.com:/tmp/

# No servidor
mkdir -p /opt/prova_app
cd /opt/prova_app
tar -xzf /tmp/prova_app.tar.gz
rm /tmp/prova_app.tar.gz
```

### 3️⃣ Executar Setup Automático (5 min)
```bash
cd /opt/prova_app
chmod +x scripts/deploy.sh

# Setup completo (instala tudo automaticamente)
./scripts/deploy.sh setup

# Quando solicitado, forneça:
# - Nome do banco: prova_modelagem_db
# - Usuário: prova_user
# - Senha: [sua senha segura]
```

### 4️⃣ Configurar Ambiente (3 min)
```bash
# Editar .env com suas configurações
nano /opt/prova_app/.env

# Edite estas variáveis:
# SECRET_KEY=...     (gerar com: python3 -c "import secrets; print(secrets.token_hex(32))")
# DATABASE_URL=postgresql://prova_user:SUA_SENHA@localhost:5432/prova_modelagem_db
# ADMIN_USERNAME=admin
# ADMIN_PASSWORD=sua_senha_admin
# ADMIN_EMAIL=seu@email.com
```

### 5️⃣ Instalar e Iniciar (2 min)
```bash
# Instalar aplicação
./scripts/deploy.sh install

# Verificar status
./scripts/deploy.sh status
```

---

## 🌐 Configurar Domínio e SSL (Opcional - 10 min)

### Passo 1: Apontar DNS
No painel do seu provedor de domínio:
```
Tipo: A
Nome: @
Valor: SEU_IP
TTL: 3600
```

### Passo 2: Atualizar Nginx
```bash
# Editar arquivo de configuração
nano /etc/nginx/sites-available/prova_app

# Substituir "server_name _;" por:
# server_name seu-dominio.com www.seu-dominio.com;

# Recarregar Nginx
nginx -t && systemctl reload nginx
```

### Passo 3: Instalar SSL (Let's Encrypt)
```bash
# Instalar Certbot
apt install certbot python3-certbot-nginx -y

# Obter certificado
certbot --nginx -d seu-dominio.com -d www.seu-dominio.com

# Renovação é automática!
```

---

## 📋 Comandos Úteis

### Gerenciar Aplicação
```bash
# Ver status
./scripts/deploy.sh status

# Ver logs em tempo real
./scripts/deploy.sh logs

# Reiniciar aplicação
supervisorctl restart prova_app

# Atualizar aplicação
./scripts/deploy.sh update

# Criar backup
./scripts/deploy.sh backup

# Restaurar backup
./scripts/deploy.sh restore
```

### Verificar Serviços
```bash
# Status Supervisor
supervisorctl status

# Status Nginx
systemctl status nginx

# Status PostgreSQL
systemctl status postgresql

# Ver logs de erro
tail -f /opt/prova_app/logs/supervisor_error.log
tail -f /var/log/nginx/prova_app_error.log
```

---

## 🐳 Alternativa: Deploy com Docker (Mais Fácil!)

### Setup Único
```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Instalar Docker Compose
apt install docker-compose-plugin -y
```

### Deploy
```bash
# Transferir aplicação (igual ao Passo 2 acima)
# Depois:
cd /opt/prova_app

# Editar .env (ajustar DATABASE_URL):
# DATABASE_URL=postgresql://prova_user:senha@db:5432/prova_modelagem_db

# Iniciar tudo
docker compose up -d --build

# Ver logs
docker compose logs -f

# Gerenciar
docker compose restart    # Reiniciar
docker compose stop       # Parar
docker compose start      # Iniciar
docker compose ps         # Status
```

---

## ✅ Verificação Final

Acesse no navegador:
- **HTTP**: http://SEU_IP ou http://seu-dominio.com
- **HTTPS**: https://seu-dominio.com (após SSL)

Login padrão:
- **Usuário**: admin (ou o que você configurou)
- **Senha**: (a que você configurou no .env)

---

## 🆘 Problemas Comuns

### 1. Erro 502 Bad Gateway
```bash
# Verificar se aplicação está rodando
supervisorctl status prova_app
# ou
docker compose ps

# Reiniciar
supervisorctl restart prova_app
# ou
docker compose restart
```

### 2. Não consigo acessar externamente
```bash
# Verificar firewall
ufw status

# Abrir portas se necessário
ufw allow 'Nginx Full'
```

### 3. Erro de banco de dados
```bash
# Verificar PostgreSQL
systemctl status postgresql

# Testar conexão
psql -U prova_user -d prova_modelagem_db -h localhost
```

---

## 📞 URLs Importantes

- **Painel Admin**: https://seu-dominio.com/admin
- **Login**: https://seu-dominio.com/login
- **Dashboard**: https://seu-dominio.com/

---

## 🎯 Próximos Passos (Recomendado)

1. ✅ **Configurar backup automático**
   ```bash
   # Já configurado! Backup diário às 2h da manhã
   crontab -l
   ```

2. ✅ **Monitorar recursos**
   ```bash
   # Instalar htop
   apt install htop -y
   htop
   ```

3. ✅ **Configurar alertas**
   ```bash
   # Instalar fail2ban (proteção contra ataques)
   apt install fail2ban -y
   systemctl enable fail2ban
   ```

---

**Deploy simplificado para Puket**
Para documentação completa, veja: `DEPLOY_PRODUCAO.md`
