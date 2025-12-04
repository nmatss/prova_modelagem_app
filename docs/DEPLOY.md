# Guia de Deploy - Aplicação de Provas de Modelagem

Este guia descreve como fazer o deploy da aplicação em um servidor de produção interno.

## 📋 Pré-requisitos

### Software Necessário
- Python 3.8+
- PostgreSQL 12+ (recomendado) ou MySQL 8+ ou SQLite (não recomendado para produção)
- Nginx
- Git (opcional, mas recomendado)

### Sistema Operacional
Testado em:
- Ubuntu 20.04/22.04 LTS
- Debian 11+
- CentOS/RHEL 8+

---

## 🚀 Instalação Passo a Passo

### 1. Preparar o Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências do sistema
sudo apt install -y python3 python3-pip python3-venv \
    postgresql postgresql-contrib \
    nginx \
    git

# Criar usuário para a aplicação (opcional, mas recomendado)
sudo useradd -m -s /bin/bash provas
sudo usermod -aG www-data provas
```

### 2. Configurar PostgreSQL

```bash
# Acessar PostgreSQL
sudo -u postgres psql

# Executar os comandos do init_db.sql ou manualmente:
CREATE DATABASE provas_db
    WITH
    ENCODING = 'UTF8';

CREATE USER provas_user WITH PASSWORD 'sua_senha_segura_aqui';
GRANT ALL PRIVILEGES ON DATABASE provas_db TO provas_user;
\q
```

**Importante:** Guarde a senha do banco de dados, você precisará dela no `.env.production`

### 3. Clonar/Transferir Aplicação

#### Opção A: Via Git (recomendado)
```bash
sudo mkdir -p /var/www
cd /var/www
sudo git clone <url-do-repositorio> provas_app
sudo chown -R provas:www-data provas_app
cd provas_app
```

#### Opção B: Transferir arquivos manualmente
```bash
# No seu computador local, compactar a aplicação
tar -czf provas_app.tar.gz prova_modelagem_app/

# Transferir para o servidor (ajuste IP e caminho)
scp provas_app.tar.gz usuario@ip-servidor:/tmp/

# No servidor
sudo mkdir -p /var/www/provas_app
cd /var/www/provas_app
sudo tar -xzf /tmp/provas_app.tar.gz --strip-components=1
sudo chown -R provas:www-data /var/www/provas_app
```

### 4. Configurar Ambiente de Produção

```bash
cd /var/www/provas_app

# Criar virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# Configurar .env.production
cp .env.example .env.production
nano .env.production
```

**Edite `.env.production` com suas configurações:**

```env
# Flask Configuration
SECRET_KEY=<cole_a_secret_key_gerada>
FLASK_ENV=production
FLASK_DEBUG=False

# Database - PostgreSQL
DATABASE_URL=postgresql://provas_user:sua_senha_segura_aqui@localhost:5432/provas_db

# Upload Configuration
MAX_CONTENT_LENGTH=16777216
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,pdf,xlsx,xls,ppt,pptx

# Server Configuration
HOST=0.0.0.0
PORT=8000
WORKERS=4

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/provas_app/app.log
```

### 5. Inicializar Banco de Dados

```bash
# Carregar ambiente
export ENV_FILE=.env.production

# Criar estrutura do banco
python3 migrate_to_postgres.py

# Criar usuário administrador
python3 create_test_user.py
```

### 6. Configurar Diretórios e Permissões

```bash
# Criar diretórios necessários
sudo mkdir -p /var/log/provas_app
sudo mkdir -p /var/run/provas_app
sudo mkdir -p /var/www/provas_app/uploads
sudo mkdir -p /var/www/provas_app/relatorios_pdf
sudo mkdir -p /var/www/provas_app/instance

# Definir permissões
sudo chown -R provas:www-data /var/www/provas_app
sudo chown -R provas:www-data /var/log/provas_app
sudo chown -R provas:www-data /var/run/provas_app

# Permissões de escrita onde necessário
sudo chmod -R 775 /var/www/provas_app/uploads
sudo chmod -R 775 /var/www/provas_app/relatorios_pdf
sudo chmod -R 775 /var/www/provas_app/instance
sudo chmod -R 775 /var/log/provas_app
```

### 7. Configurar Nginx

```bash
# Copiar configuração
sudo cp nginx.conf /etc/nginx/sites-available/provas_app

# Editar configuração (ajustar caminhos e domínio)
sudo nano /etc/nginx/sites-available/provas_app
```

**Altere no arquivo:**
- `server_name` para seu domínio ou IP
- Todos os `/caminho/para/prova_modelagem_app/` para `/var/www/provas_app/`

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/provas_app /etc/nginx/sites-enabled/

# Testar configuração
sudo nginx -t

# Recarregar Nginx
sudo systemctl reload nginx
```

### 8. Configurar Serviço Systemd (Opcional, mas Recomendado)

```bash
# Copiar arquivo de serviço
sudo cp provas_app.service /etc/systemd/system/

# Editar configuração
sudo nano /etc/systemd/system/provas_app.service
```

**Altere no arquivo:**
- `User` e `Group` conforme seu usuário (ex: provas)
- `WorkingDirectory` para `/var/www/provas_app`
- `Environment="PATH=..."` para `/var/www/provas_app/.venv/bin`
- `ExecStart` para `/var/www/provas_app/.venv/bin/gunicorn -c gunicorn_config.py wsgi:app`

```bash
# Recarregar systemd
sudo systemctl daemon-reload

# Habilitar serviço
sudo systemctl enable provas_app

# Iniciar serviço
sudo systemctl start provas_app

# Verificar status
sudo systemctl status provas_app
```

### 9. Iniciar Aplicação

#### Opção A: Com Systemd (recomendado)
```bash
sudo systemctl start provas_app
sudo systemctl status provas_app
```

#### Opção B: Com Scripts Manualmente
```bash
cd /var/www/provas_app
sudo -u provas ./start.sh
./status.sh
```

---

## 🔧 Gerenciamento da Aplicação

### Iniciar
```bash
sudo systemctl start provas_app
# ou
./start.sh
```

### Parar
```bash
sudo systemctl stop provas_app
# ou
./stop.sh
```

### Reiniciar
```bash
sudo systemctl restart provas_app
# ou
./restart.sh
```

### Verificar Status
```bash
sudo systemctl status provas_app
# ou
./status.sh
```

### Ver Logs
```bash
# Logs da aplicação
tail -f /var/log/provas_app/app.log
tail -f /var/log/provas_app/error.log
tail -f /var/log/provas_app/access.log

# Logs do systemd
sudo journalctl -u provas_app -f

# Logs do Nginx
tail -f /var/log/nginx/provas_app_access.log
tail -f /var/log/nginx/provas_app_error.log
```

---

## 🔐 Segurança

### Firewall
```bash
# Permitir HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Bloquear acesso direto ao Gunicorn (porta 8000)
sudo ufw deny 8000/tcp

# Ativar firewall
sudo ufw enable
```

### SSL/HTTPS (Recomendado)

#### Com Let's Encrypt (gratuito)
```bash
# Instalar certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d seu-dominio.com.br

# Renovação automática já está configurada
sudo certbot renew --dry-run
```

#### Com Certificado Próprio
Descomente a seção HTTPS no `nginx.conf` e configure os caminhos dos certificados.

---

## 📊 Monitoramento

### Verificar Uso de Recursos
```bash
# CPU e Memória
top -p $(cat /var/run/provas_app/gunicorn.pid)

# Espaço em disco
df -h

# Tamanho dos uploads
du -sh /var/www/provas_app/uploads
du -sh /var/www/provas_app/relatorios_pdf
```

### Logs Importantes

| Arquivo | Descrição |
|---------|-----------|
| `/var/log/provas_app/app.log` | Logs da aplicação |
| `/var/log/provas_app/error.log` | Erros do Gunicorn |
| `/var/log/provas_app/access.log` | Acessos ao Gunicorn |
| `/var/log/nginx/provas_app_access.log` | Acessos via Nginx |
| `/var/log/nginx/provas_app_error.log` | Erros do Nginx |

---

## 🔄 Atualização da Aplicação

```bash
cd /var/www/provas_app

# Backup do banco (importante!)
sudo -u postgres pg_dump provas_db > backup_$(date +%Y%m%d).sql

# Parar aplicação
sudo systemctl stop provas_app

# Atualizar código (via git)
git pull origin main

# Ou atualizar arquivos manualmente
# scp novos_arquivos usuario@servidor:/var/www/provas_app/

# Ativar virtual environment
source .venv/bin/activate

# Atualizar dependências se necessário
pip install -r requirements.txt

# Executar migrações se houver
python3 migrate_to_postgres.py

# Iniciar aplicação
sudo systemctl start provas_app

# Verificar se está funcionando
./status.sh
```

---

## 🐛 Troubleshooting

### Aplicação não inicia

```bash
# Verificar logs
tail -100 /var/log/provas_app/error.log
sudo journalctl -u provas_app -n 50

# Verificar se porta está em uso
sudo netstat -tlnp | grep 8000

# Verificar permissões
ls -la /var/www/provas_app
```

### Erro de conexão com banco de dados

```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Testar conexão
psql -U provas_user -d provas_db -h localhost

# Verificar DATABASE_URL no .env.production
```

### Erro 502 Bad Gateway (Nginx)

```bash
# Verificar se Gunicorn está rodando
./status.sh
sudo systemctl status provas_app

# Verificar configuração Nginx
sudo nginx -t

# Verificar logs
tail -50 /var/log/nginx/provas_app_error.log
```

### Erro de permissão ao fazer upload

```bash
# Corrigir permissões
sudo chown -R provas:www-data /var/www/provas_app/uploads
sudo chmod -R 775 /var/www/provas_app/uploads
```

---

## 📱 Acesso à Aplicação

Após deploy completo, acesse:

- **HTTP:** `http://seu-servidor.com` ou `http://IP-DO-SERVIDOR`
- **HTTPS:** `https://seu-servidor.com` (se SSL configurado)

**Login padrão (criado no passo 5):**
- Usuário: (o que você configurou)
- Senha: (o que você configurou)

---

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique os logs em `/var/log/provas_app/`
2. Consulte a seção Troubleshooting acima
3. Verifique as configurações em `.env.production`

---

## 🔒 Checklist Pós-Deploy

- [ ] Aplicação está acessível via navegador
- [ ] Login funciona corretamente
- [ ] Upload de arquivos funciona
- [ ] Geração de PDF funciona
- [ ] Logs estão sendo gerados
- [ ] Firewall configurado
- [ ] SSL/HTTPS configurado (recomendado)
- [ ] Backup do banco de dados agendado
- [ ] SECRET_KEY única gerada e configurada
- [ ] DEBUG=False no `.env.production`
- [ ] Credenciais padrão alteradas

---

## 📝 Notas Importantes

1. **Nunca** exponha o arquivo `.env.production` publicamente
2. **Sempre** faça backup antes de atualizar
3. **Configure** rotação de logs para evitar disco cheio
4. **Monitore** o uso de disco dos uploads
5. **Use** PostgreSQL em vez de SQLite para produção
6. **Teste** a aplicação em ambiente de teste antes de produção

---

**Aplicação pronta para produção!** 🎉
