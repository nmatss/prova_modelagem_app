# 📚 Índice de Documentação - Deploy

Bem-vindo ao sistema de deploy do **Sistema de Provas Puket**!

## 🎯 Escolha seu Método de Deploy

### 🐳 Docker (Recomendado - Mais Fácil)
**✅ Use se você quer:**
- Deploy rápido (10-15 minutos)
- Isolamento total da aplicação
- Fácil atualização e rollback
- Funcionar em qualquer servidor Linux

**📖 Documentação:**
1. **[INICIO_RAPIDO_DOCKER.md](INICIO_RAPIDO_DOCKER.md)** ⭐
   - Guia copy-paste de 5 minutos
   - Comandos prontos para usar
   - Perfeito para começar rápido

2. **[DEPLOY_DOCKER.md](DEPLOY_DOCKER.md)**
   - Documentação completa Docker
   - Troubleshooting avançado
   - Otimizações de performance

---

### 🖥️ Deploy Manual (Tradicional)
**✅ Use se você:**
- Já tem servidor configurado
- Quer controle total do ambiente
- Prefere configuração tradicional
- Não pode usar Docker

**📖 Documentação:**
1. **[DEPLOY_RAPIDO_RESUMO.md](DEPLOY_RAPIDO_RESUMO.md)** ⭐
   - Resumo executivo de 15 minutos
   - Dois métodos (manual + Docker)
   - Comandos essenciais

2. **[DEPLOY_PRODUCAO.md](DEPLOY_PRODUCAO.md)**
   - Guia completo passo a passo
   - Deploy manual tradicional
   - Nginx, SSL, Supervisor
   - Backup e monitoramento

---

## 📁 Arquivos Importantes

### Configuração
- `.env.example` - Template de variáveis de ambiente
- `docker-compose.yml` - Configuração Docker com PostgreSQL
- `Dockerfile` - Imagem Docker otimizada para produção
- `gunicorn_config.py` - Configuração do servidor Gunicorn

### Scripts Auxiliares
- `scripts/deploy.sh` - Script automatizado de deploy
- `scripts/docker-backup.sh` - Backup automático para Docker
- `scripts/nginx.conf` - Configuração Nginx pronta

---

## ⚡ Quick Start - Escolha Seu Caminho

### Caminho 1: Docker (10 min)
```bash
# 1. No servidor
curl -fsSL https://get.docker.com | sudo sh
sudo apt install docker-compose-plugin -y

# 2. Transferir aplicação
scp prova_app.tar.gz usuario@servidor:/tmp/
ssh usuario@servidor
sudo mkdir -p /opt/prova_app && cd /opt/prova_app
sudo tar -xzf /tmp/prova_app.tar.gz

# 3. Configurar e iniciar
cp .env.example .env
nano .env  # Editar configurações
docker compose up -d --build

# 4. Criar admin
docker compose exec web python3 -c "..."
```

**👉 Veja detalhes em:** [INICIO_RAPIDO_DOCKER.md](INICIO_RAPIDO_DOCKER.md)

---

### Caminho 2: Manual (30 min)
```bash
# 1. Setup servidor
cd /opt/prova_app
chmod +x scripts/deploy.sh
sudo ./scripts/deploy.sh setup

# 2. Configurar
nano .env

# 3. Instalar
sudo ./scripts/deploy.sh install

# 4. Verificar
./scripts/deploy.sh status
```

**👉 Veja detalhes em:** [DEPLOY_PRODUCAO.md](DEPLOY_PRODUCAO.md)

---

## 🌐 Pós-Deploy: Configurar Domínio e SSL

### 1. Apontar Domínio
No seu provedor de domínio:
```
Tipo: A
Nome: @
Valor: SEU_IP_DO_SERVIDOR
TTL: 3600
```

### 2. Instalar SSL (Let's Encrypt)
```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obter certificado
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com
```

**Renovação é automática!**

---

## 📊 Monitoramento e Manutenção

### Docker
```bash
docker compose logs -f          # Ver logs
docker compose ps               # Status
docker compose restart web      # Reiniciar
./scripts/docker-backup.sh      # Backup
```

### Manual
```bash
./scripts/deploy.sh logs        # Ver logs
./scripts/deploy.sh status      # Status
./scripts/deploy.sh update      # Atualizar
./scripts/deploy.sh backup      # Backup
```

---

## 🆘 Troubleshooting Rápido

### Problema: Aplicação não abre
```bash
# Docker
docker compose logs -f web

# Manual
sudo supervisorctl status prova_app
sudo tail -f /opt/prova_app/logs/gunicorn_error.log
```

### Problema: Erro 502
```bash
# Docker
docker compose restart web

# Manual
sudo supervisorctl restart prova_app
```

### Problema: Banco não conecta
```bash
# Docker
docker compose logs db
docker compose restart db

# Manual
sudo systemctl status postgresql
sudo -u postgres psql -l
```

---

## ✅ Checklist de Deploy

Após o deploy, verifique:

- [ ] Aplicação acessível via HTTP/HTTPS
- [ ] Login funcionando
- [ ] Upload de fotos funcionando
- [ ] Geração de PDF funcionando
- [ ] Backup configurado
- [ ] Firewall ativo (portas 80, 443, SSH)
- [ ] SSL configurado (HTTPS)
- [ ] Logs sendo gerados
- [ ] Monitoramento ativo

---

## 📞 Suporte

### Documentação
- [DEPLOY_DOCKER.md](DEPLOY_DOCKER.md) - Docker completo
- [DEPLOY_PRODUCAO.md](DEPLOY_PRODUCAO.md) - Deploy manual
- [INICIO_RAPIDO_DOCKER.md](INICIO_RAPIDO_DOCKER.md) - Quick start

### Logs Importantes
```bash
# Aplicação
/opt/prova_app/logs/app.log
/opt/prova_app/logs/gunicorn_error.log

# Sistema
/var/log/nginx/prova_app_error.log
/var/log/supervisor/
```

### Comandos Úteis
```bash
# Ver uso de recursos
docker stats        # Docker
htop               # Sistema

# Espaço em disco
df -h
docker system df

# Limpar espaço
docker system prune -a
```

---

## 🎯 Próximos Passos Após Deploy

1. ✅ **Testar funcionalidades**
   - Criar relatório
   - Upload de fotos
   - Gerar PDF
   - Criar nova prova

2. ✅ **Configurar usuários**
   - Acessar `/admin`
   - Criar usuários do time
   - Definir permissões

3. ✅ **Backup regular**
   - Testar restauração
   - Verificar cron job
   - Copiar backups para outro local

4. ✅ **Monitorar performance**
   - Ver logs diariamente
   - Checar uso de disco
   - Monitorar uptime

---

## 🎉 Pronto!

Seu sistema está no ar! Acesse:
- **Aplicação**: https://seu-dominio.com
- **Admin**: https://seu-dominio.com/admin
- **Login**: admin / (senha configurada)

---

**Documentação criada para Puket**
Sistema de Gestão de Provas de Modelagem
Dezembro 2024
