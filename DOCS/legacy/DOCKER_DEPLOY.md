# 🐳 Deploy Docker - Sistema de Provas de Modelagem

## 📋 Visão Geral

Aplicação Flask com SQLite containerizada, pronta para deploy em qualquer ambiente Docker.

### Características:

- ✅ **SQLite persistente** via volumes
- ✅ **Uploads persistentes** (fotos, documentos)
- ✅ **Multi-stage build** otimizado
- ✅ **Usuário não-root** para segurança
- ✅ **Health checks** integrados
- ✅ **Gunicorn** para produção
- ✅ **Auto-inicialização** do banco de dados

---

## 🚀 Opção 1: Deploy com Docker Compose (Standalone)

### Passo 1: Build da imagem

```bash
docker-compose build
```

### Passo 2: Iniciar aplicação

```bash
docker-compose up -d
```

### Passo 3: Acessar

```
http://localhost:5000
```

**Credenciais padrão:**
- Usuário: `admin`
- Senha: `admin123`

### Comandos úteis:

```bash
# Ver logs
docker-compose logs -f app

# Parar
docker-compose down

# Reiniciar
docker-compose restart

# Rebuild e restart
docker-compose up -d --build
```

---

## 🔧 Opção 2: Integrar em Docker Existente

### Método A: Usar docker-compose como serviço adicional

Adicione ao seu `docker-compose.yml` existente:

```yaml
services:
  prova_modelagem:
    build: ./prova_modelagem_app
    container_name: prova_modelagem
    restart: unless-stopped
    ports:
      - "5000:5000"
    volumes:
      - ./prova_modelagem_app/data:/app/data
      - ./prova_modelagem_app/uploads:/app/uploads
      - ./prova_modelagem_app/logs:/app/logs
    environment:
      - SECRET_KEY=sua-chave-secreta-aqui
      - FLASK_ENV=production
    networks:
      - sua_rede_existente
```

### Método B: Build e run manual

```bash
# Build da imagem
docker build -t prova_modelagem:latest .

# Run com volumes
docker run -d \
  --name prova_modelagem \
  --restart unless-stopped \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/logs:/app/logs \
  -e SECRET_KEY="sua-chave-secreta" \
  -e FLASK_ENV=production \
  prova_modelagem:latest
```

### Método C: Usar em rede Docker existente

```bash
# Conectar à rede existente
docker run -d \
  --name prova_modelagem \
  --network sua_rede_docker \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/uploads:/app/uploads \
  prova_modelagem:latest
```

---

## 📁 Estrutura de Volumes

### Volumes necessários:

| Volume | Path no Container | Descrição |
|--------|------------------|-----------|
| **data** | `/app/data` | Banco SQLite persistente |
| **uploads** | `/app/uploads` | Fotos, PPTs, tabelas |
| **logs** | `/app/logs` | Logs da aplicação |

### Backup dos dados:

```bash
# Backup do banco
docker cp prova_modelagem:/app/data/provas.db ./backup_$(date +%Y%m%d).db

# Backup dos uploads
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz ./uploads/
```

---

## ⚙️ Variáveis de Ambiente

### Obrigatórias:

```bash
SECRET_KEY=sua-chave-super-secreta-aqui-mude-em-producao
```

### Opcionais:

```bash
# Flask
FLASK_ENV=production
FLASK_DEBUG=False

# Banco de dados
DATABASE_URL=sqlite:////app/data/provas.db

# Servidor
HOST=0.0.0.0
PORT=5000

# Upload
MAX_CONTENT_LENGTH=16777216
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,pdf,xlsx,xls,ppt,pptx

# Logs
LOG_LEVEL=INFO
```

---

## 🔒 Segurança

### Checklist de Produção:

- [ ] Alterar `SECRET_KEY` no `.env`
- [ ] Definir `FLASK_ENV=production`
- [ ] Definir `FLASK_DEBUG=False`
- [ ] Trocar senha do usuário `admin`
- [ ] Configurar firewall (permitir apenas porta necessária)
- [ ] Usar HTTPS (via reverse proxy)
- [ ] Backups automáticos configurados

### Trocar senha do admin:

```bash
docker exec -it prova_modelagem python3 << EOF
from app import app
from models import db, Usuario
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = Usuario.query.filter_by(username='admin').first()
    admin.password_hash = generate_password_hash('nova_senha_forte')
    db.session.commit()
    print('✅ Senha alterada')
EOF
```

---

## 🔍 Troubleshooting

### Container não inicia

```bash
# Ver logs
docker logs prova_modelagem

# Ver logs em tempo real
docker logs -f prova_modelagem
```

### Erro de permissão no SQLite

```bash
# Ajustar permissões dos volumes
chmod -R 755 data/ uploads/ logs/

# Recriar container
docker-compose down
docker-compose up -d
```

### Banco de dados corrompido

```bash
# Restaurar backup
docker cp backup_20251203.db prova_modelagem:/app/data/provas.db

# Ou recriar (CUIDADO: apaga dados!)
docker exec prova_modelagem rm /app/data/provas.db
docker restart prova_modelagem
```

### Reset completo

```bash
# Para e remove container
docker-compose down

# Remove volumes (CUIDADO: apaga dados!)
rm -rf data/ logs/

# Recria tudo
docker-compose up -d
```

---

## 🌐 Reverse Proxy (Opcional)

### Nginx

```nginx
server {
    listen 80;
    server_name provas.exemplo.com;

    client_max_body_size 16M;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /uploads/ {
        alias /caminho/para/uploads/;
    }
}
```

### Traefik

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.provas.rule=Host(`provas.exemplo.com`)"
  - "traefik.http.services.provas.loadbalancer.server.port=5000"
```

---

## 📊 Monitoramento

### Health check manual

```bash
curl http://localhost:5000/
```

### Status do container

```bash
docker ps | grep prova_modelagem
docker stats prova_modelagem
```

### Logs de acesso

```bash
docker exec prova_modelagem tail -f /app/logs/app.log
```

---

## 🔄 Atualização da Aplicação

### Atualizar para nova versão:

```bash
# 1. Backup dos dados
docker cp prova_modelagem:/app/data/provas.db ./backup_antes_update.db

# 2. Para container
docker-compose down

# 3. Atualiza código
git pull  # ou copiar novos arquivos

# 4. Rebuild
docker-compose build --no-cache

# 5. Inicia
docker-compose up -d

# 6. Verifica logs
docker-compose logs -f
```

---

## 📦 Estrutura de Arquivos

```
prova_modelagem_app/
├── Dockerfile              # Imagem Docker
├── docker-compose.yml      # Orquestração
├── .dockerignore          # Arquivos ignorados
├── entrypoint.sh          # Inicialização
├── requirements.txt       # Dependências Python
├── app.py                 # Aplicação Flask
├── models.py              # Modelos do banco
├── gunicorn_config.py     # Config Gunicorn
├── data/                  # 📁 Volume: Banco SQLite
│   └── provas.db
├── uploads/               # 📁 Volume: Arquivos
│   ├── fotos/
│   ├── ppts/
│   └── tabelas/
└── logs/                  # 📁 Volume: Logs
    └── app.log
```

---

## 💡 Dicas de Produção

### 1. Use volumes nomeados

```yaml
volumes:
  prova_data:
  prova_uploads:
```

### 2. Limite recursos

```yaml
deploy:
  resources:
    limits:
      cpus: '1'
      memory: 512M
```

### 3. Restart policy

```yaml
restart: unless-stopped
```

### 4. Backup automático

```bash
# Cron job para backup diário
0 2 * * * docker exec prova_modelagem tar -czf /tmp/backup_$(date +\%Y\%m\%d).tar.gz /app/data /app/uploads
```

---

## 📞 Suporte

**Problemas?**
1. Verifique logs: `docker logs prova_modelagem`
2. Verifique volumes: `docker volume ls`
3. Verifique rede: `docker network inspect bridge`

**Versão:** 2.0.0
**Stack:** Python 3.12 + Flask + SQLite + Gunicorn
