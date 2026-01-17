# Sistema de Provas de Modelagem - Puket

Sistema completo de gerenciamento de provas de modelagem para indústria têxtil, desenvolvido em Flask com suporte a Docker e deploy em produção.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-Proprietary-red)

---

## Índice

1. [Visão Geral](#visão-geral)
2. [Funcionalidades](#funcionalidades)
3. [Tecnologias](#tecnologias)
4. [Arquitetura](#arquitetura)
5. [Início Rápido](#início-rápido)
6. [Instalação](#instalação)
7. [Configuração](#configuração)
8. [Deploy](#deploy)
9. [Documentação](#documentação)
10. [Suporte](#suporte)

---

## Visão Geral

O Sistema de Provas de Modelagem é uma solução completa para gerenciar todo o ciclo de vida das provas de modelagem na indústria têxtil, desde o cadastro de referências até a aprovação final das peças.

### Principais Características

- **Gestão Completa**: Relatórios, referências, provas e avaliações
- **Multi-usuário**: Controle de acesso e permissões
- **Upload de Arquivos**: Fotos, PPTs, fichas técnicas e tabelas Excel
- **Geração de PDFs**: Relatórios profissionais para impressão
- **Checklists de Avaliação**: Qualidade, estilo e modelagem
- **Analytics**: Dashboard com métricas e gráficos
- **Auditoria**: Log de todas as operações
- **Responsivo**: Interface adaptada para mobile e desktop

---

## Funcionalidades

### Módulo de Relatórios
- Criação de relatórios por coleção/temporada
- Upload de PPT, imagem do produto e ficha técnica
- Gestão de múltiplas referências por relatório
- Status geral (Em Andamento, Aprovado, Reprovado)
- Exportação para Excel e PDF

### Módulo de Referências
- Cadastro completo de referências de produtos
- Categorias: Baby, Kids, Teen, Adulto
- Informações técnicas: composição, gramatura, aviamentos
- Dados de fornecedor e contato
- Upload de tabela de medidas (Excel)

### Módulo de Provas
- Múltiplas provas por referência (Prova 1, 2, 3...)
- Upload de fotos por contexto (desenho, qualidade, estilo, etc)
- Checklist de avaliação com checkboxes:
  - Qualidade (estrutura, acabamento, defeitos)
  - Estilo (cor, estampa, caimento)
  - Modelagem (medidas, proporções, conforto)
- Comentários e observações detalhadas
- Status individual por prova

### Módulo Administrativo
- Gestão de usuários e permissões
- Logs de auditoria
- Configurações do sistema
- Estatísticas de uso

### Analytics
- Dashboard com métricas em tempo real
- Gráficos de status de provas
- Análise por categoria de produto
- Histórico de aprovações e reprovações

---

## Tecnologias

### Backend
- **Python 3.11**: Linguagem principal
- **Flask 3.0.0**: Framework web
- **SQLAlchemy**: ORM para banco de dados
- **Flask-Login**: Autenticação de usuários
- **Gunicorn**: Servidor WSGI para produção
- **WeasyPrint**: Geração de PDFs

### Banco de Dados
- **PostgreSQL 15**: Produção (recomendado)
- **SQLite**: Desenvolvimento e testes

### Frontend
- **Bootstrap 5**: Framework CSS
- **JavaScript ES6+**: Interatividade
- **Chart.js**: Gráficos e visualizações
- **Font Awesome**: Ícones

### Infraestrutura
- **Docker**: Containerização
- **Docker Compose**: Orquestração
- **Nginx**: Reverse proxy e servir arquivos estáticos
- **Supervisor**: Gerenciamento de processos (deploy manual)

### Segurança
- **CSRF Protection**: Proteção contra ataques CSRF
- **Password Hashing**: Senhas criptografadas (bcrypt)
- **Rate Limiting**: Proteção contra força bruta
- **Security Headers**: Headers HTTP de segurança

---

## Arquitetura

### Estrutura de Diretórios

```
prova_modelagem_app/
├── app.py                      # Aplicação Flask principal
├── models.py                   # Modelos de dados (SQLAlchemy)
├── auth.py                     # Autenticação e autorização
├── admin.py                    # Módulo administrativo
├── config.py                   # Configurações da aplicação
├── utils.py                    # Funções auxiliares
├── security.py                 # Segurança e validações
├── excel_export.py             # Exportação para Excel
├── error_handlers.py           # Tratamento de erros
│
├── templates/                  # Templates HTML (Jinja2)
│   ├── base.html              # Template base
│   ├── login.html             # Login
│   ├── dashboard.html         # Dashboard principal
│   ├── novo_relatorio.html    # Criar relatório
│   ├── editar_relatorio.html  # Editar relatório
│   ├── detalhes_relatorio.html# Ver relatório
│   ├── nova_prova.html        # Criar prova
│   ├── analytics.html         # Analytics e gráficos
│   └── admin/                 # Templates administrativos
│
├── static/                     # Arquivos estáticos
│   ├── css/                   # Estilos
│   │   ├── custom.css         # Estilos customizados
│   │   ├── mobile.css         # Responsividade
│   │   └── components.css     # Componentes
│   ├── js/                    # JavaScript
│   │   ├── app.js             # Aplicação principal
│   │   ├── charts-config.js   # Configuração de gráficos
│   │   └── file-upload.js     # Upload de arquivos
│   └── img/                   # Imagens
│
├── uploads/                    # Arquivos enviados (runtime)
├── logs/                       # Logs da aplicação
├── backups/                    # Backups automáticos
├── data/                       # Banco SQLite (se usado)
│
├── Dockerfile                  # Imagem Docker
├── docker-compose.yml         # PostgreSQL
├── docker-compose.sqlite.yml  # SQLite
├── entrypoint.sh              # Script de inicialização
├── gunicorn_config.py         # Configuração Gunicorn
├── requirements.txt           # Dependências Python
├── nginx.conf                 # Configuração Nginx
│
├── scripts/                    # Scripts auxiliares
│   ├── deploy.sh              # Deploy automatizado
│   ├── docker-backup.sh       # Backup Docker
│   └── database/              # Scripts de banco
│
└── docs/                       # Documentação
    ├── DOCKER_GUIDE.md        # Guia de Docker
    ├── DEPLOY_GUIDE.md        # Guia de Deploy
    ├── MAINTENANCE_GUIDE.md   # Guia de Manutenção
    └── ...
```

### Fluxo de Dados

```
Usuário
   ↓
Nginx (Reverse Proxy)
   ↓
Gunicorn (WSGI Server)
   ↓
Flask Application
   ↓
SQLAlchemy ORM
   ↓
PostgreSQL / SQLite
```

### Modelo de Dados

```
Usuario (usuários do sistema)
   ↓
Relatorio (coleções/temporadas)
   ↓
Referencia (produtos)
   ↓
ProvaModelagem (provas de cada produto)
   ↓
FotoProva (fotos das provas)
```

---

## Início Rápido

### Pré-requisitos

- Docker 20.10+
- Docker Compose 2.0+
- Git

### Deploy em 5 Minutos (SQLite)

```bash
# 1. Clonar repositório
git clone <seu-repo>
cd prova_modelagem_app

# 2. Criar arquivo .env
cp .env.example .env
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" >> .env
nano .env  # Configurar ADMIN_PASSWORD

# 3. Criar diretórios
mkdir -p data uploads logs backups
sudo chown -R 1000:1000 data uploads logs backups

# 4. Iniciar aplicação
docker compose -f docker-compose.sqlite.yml up -d

# 5. Verificar
docker compose -f docker-compose.sqlite.yml ps
curl http://localhost:5000

# 6. Acessar no navegador
# http://localhost:5000
# User: admin
# Pass: (definida no .env)
```

---

## Instalação

### Opção 1: Docker (Recomendado)

#### SQLite (Desenvolvimento/Testes)

```bash
# Configurar
cp .env.example .env
nano .env  # Editar configurações

# Criar diretórios
mkdir -p data uploads logs backups
chown -R 1000:1000 data uploads logs backups

# Iniciar
docker compose -f docker-compose.sqlite.yml up -d
```

#### PostgreSQL (Produção)

```bash
# Configurar .env com PostgreSQL
cp .env.example .env
nano .env
# Configurar:
# - SECRET_KEY
# - POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
# - ADMIN_USERNAME, ADMIN_PASSWORD

# Criar diretórios
mkdir -p uploads logs backups
chown -R 1000:1000 uploads logs backups

# Iniciar
docker compose up -d

# Verificar
docker compose ps
docker compose logs -f
```

### Opção 2: Instalação Manual

```bash
# Instalar Python 3.11
sudo apt install python3.11 python3.11-venv

# Criar virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
pip install gunicorn psycopg2-binary weasyprint

# Configurar .env
cp .env.example .env
nano .env

# Criar diretórios
mkdir -p uploads logs backups instance

# Inicializar banco
python3 << 'EOF'
from app import app, db
with app.app_context():
    db.create_all()
    print("Banco criado!")
EOF

# Iniciar aplicação
gunicorn -c gunicorn_config.py app:app
```

---

## Configuração

### Variáveis de Ambiente (.env)

```bash
# Flask
SECRET_KEY=gere-uma-chave-secreta-forte-de-64-caracteres
FLASK_ENV=production
FLASK_DEBUG=False

# Database - Escolher uma opção

# Opção 1: SQLite (desenvolvimento)
DATABASE_URL=sqlite:////app/data/provas.db

# Opção 2: PostgreSQL (produção)
DATABASE_URL=postgresql://usuario:senha@db:5432/nome_banco
POSTGRES_DB=prova_modelagem_db
POSTGRES_USER=prova_user
POSTGRES_PASSWORD=senha_forte_aqui

# Admin inicial
ADMIN_USERNAME=admin
ADMIN_PASSWORD=senha_admin_forte
ADMIN_EMAIL=admin@empresa.com

# Server
HOST=0.0.0.0
PORT=8000

# Upload
MAX_CONTENT_LENGTH=16777216  # 16MB
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,pdf,xlsx,xls,ppt,pptx

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/app.log

# Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
PERMANENT_SESSION_LIFETIME=3600

# Workers (Gunicorn)
WORKERS=2
```

### Gerar SECRET_KEY

```bash
# Python
python3 -c "import secrets; print(secrets.token_hex(32))"

# OpenSSL
openssl rand -hex 32

# /dev/urandom
cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1
```

---

## Deploy

### Deploy Rápido (SQLite)

```bash
# 1. Preparar servidor
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 2. Clonar projeto
git clone <repo>
cd prova_modelagem_app

# 3. Configurar
cp .env.example .env
nano .env  # Editar configurações

# 4. Criar estrutura
mkdir -p data uploads logs backups
chown -R 1000:1000 data uploads logs backups

# 5. Deploy
docker compose -f docker-compose.sqlite.yml up -d

# 6. Verificar
docker compose -f docker-compose.sqlite.yml ps
curl http://localhost:5000/health
```

**Tempo:** ~10 minutos

### Deploy Completo (PostgreSQL + Nginx + SSL)

```bash
# 1. Preparar servidor
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt install nginx certbot python3-certbot-nginx

# 2. Configurar aplicação
cp .env.example .env
nano .env  # Configurar todas as variáveis

# 3. Deploy Docker
docker compose up -d

# 4. Configurar Nginx
sudo cp scripts/nginx.conf /etc/nginx/sites-available/prova_app
sudo ln -s /etc/nginx/sites-available/prova_app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 5. Configurar SSL
sudo certbot --nginx -d seu-dominio.com

# 6. Configurar backups automáticos
sudo crontab -e
# Adicionar:
0 2 * * * /opt/prova_app/scripts/docker-backup.sh
```

**Tempo:** ~30 minutos

---

## Documentação

### Guias Completos

| Documento | Descrição |
|-----------|-----------|
| [DOCKER_GUIDE.md](DOCKER_GUIDE.md) | Guia completo de Docker, build, volumes e troubleshooting |
| [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md) | Deploy passo a passo (Docker e manual), atualizações e rollback |
| [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md) | Manutenção, monitoramento, backup/restore e operação diária |

### Documentação Técnica

- [DESIGN_SYSTEM_GUIDE.md](DESIGN_SYSTEM_GUIDE.md) - Sistema de design e componentes
- [MOBILE_IMPLEMENTATION_SUMMARY.md](MOBILE_IMPLEMENTATION_SUMMARY.md) - Responsividade mobile
- [ANALYTICS_REDESIGN_SUMMARY.md](ANALYTICS_REDESIGN_SUMMARY.md) - Dashboard analytics
- [PERFORMANCE_README.md](PERFORMANCE_README.md) - Otimização e performance

### Manuais de Usuário

- [MANUAL_USUARIO.md](MANUAL_USUARIO.md) - Guia do usuário final
- [ACESSO_ADMIN.md](ACESSO_ADMIN.md) - Funcionalidades administrativas

---

## Uso

### Acessar o Sistema

```
URL: http://seu-servidor:5000 (SQLite)
     http://seu-servidor:8000 (PostgreSQL)
     https://seu-dominio.com (Produção com Nginx)

Credenciais iniciais:
- Usuário: admin (configurável via ADMIN_USERNAME)
- Senha: (definida em ADMIN_PASSWORD no .env)
```

### Primeiro Acesso

1. Faça login com as credenciais de admin
2. Vá em "Administração" → "Usuários"
3. **IMPORTANTE**: Altere a senha do admin
4. Crie usuários adicionais conforme necessário
5. Comece cadastrando um relatório em "Novo Relatório"

### Fluxo de Trabalho Típico

1. **Criar Relatório**: Coleção/temporada com PPT e informações gerais
2. **Adicionar Referências**: Produtos com dados técnicos e fornecedor
3. **Criar Provas**: Múltiplas provas para cada referência
4. **Upload de Fotos**: Fotos por contexto (desenho, qualidade, estilo)
5. **Preencher Checklists**: Avaliar qualidade, estilo e modelagem
6. **Aprovar/Reprovar**: Definir status final de cada prova
7. **Gerar PDF**: Relatório completo para impressão/envio

---

## Backup e Restore

### Backup Automático (Docker)

```bash
# Script já configurado
./scripts/docker-backup.sh

# Agendar no cron (diário às 2h)
0 2 * * * /opt/prova_app/scripts/docker-backup.sh >> /var/log/prova_backup.log 2>&1
```

### Backup Manual

```bash
# Banco de dados
docker compose exec -T db pg_dump -U prova_user prova_modelagem_db | \
    gzip > backup_db_$(date +%Y%m%d_%H%M%S).sql.gz

# Uploads
tar -czf backup_uploads_$(date +%Y%m%d_%H%M%S).tar.gz uploads/

# Configurações
cp .env backup_env_$(date +%Y%m%d_%H%M%S)
```

### Restore

```bash
# Parar aplicação
docker compose stop web

# Restaurar banco
gunzip < backup_db_20250116.sql.gz | \
    docker compose exec -T db psql -U prova_user -d prova_modelagem_db

# Restaurar uploads
tar -xzf backup_uploads_20250116.tar.gz

# Reiniciar
docker compose start web
```

---

## Monitoramento

### Health Check

```bash
# Verificar saúde da aplicação
curl http://localhost:8000/health

# Ver status dos containers
docker compose ps

# Ver logs em tempo real
docker compose logs -f web
```

### Métricas

```bash
# Uso de recursos
docker stats

# Espaço em disco
df -h /opt/prova_app

# Tamanho do banco
docker compose exec db psql -U prova_user -d prova_modelagem_db -c "\
    SELECT pg_size_pretty(pg_database_size('prova_modelagem_db'));"
```

---

## Troubleshooting

### Problema: Container não inicia

```bash
# Ver logs
docker compose logs web

# Verificar variáveis de ambiente
docker compose config

# Testar manualmente
docker compose run --rm web python3 -c "from app import app; print(app.config)"
```

### Problema: Erro de permissão

```bash
# Ajustar permissões (appuser = UID 1000)
sudo chown -R 1000:1000 uploads logs data
chmod -R 755 uploads logs data
```

### Problema: Banco não conecta

```bash
# Verificar se PostgreSQL está rodando
docker compose ps db

# Testar conexão
docker compose exec web python3 -c "
from app import app, db
with app.app_context():
    try:
        db.engine.connect()
        print('Conexão OK')
    except Exception as e:
        print(f'Erro: {e}')
"
```

### Mais Troubleshooting

Consulte [DOCKER_GUIDE.md](DOCKER_GUIDE.md) e [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md) para troubleshooting detalhado.

---

## Segurança

### Boas Práticas

- ✅ Usar SECRET_KEY forte (64+ caracteres aleatórios)
- ✅ Alterar senha do admin após primeiro acesso
- ✅ Usar HTTPS em produção (SSL/TLS)
- ✅ Nunca expor PostgreSQL diretamente
- ✅ Manter sistema e dependências atualizados
- ✅ Configurar firewall (UFW, iptables)
- ✅ Habilitar backups automáticos
- ✅ Executar aplicação como usuário não-root

### Atualizações de Segurança

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Atualizar imagem Docker
docker compose pull
docker compose up -d --build

# Verificar vulnerabilidades (Python)
pip install safety
safety check
```

---

## Performance

### Otimizações Implementadas

- **Multi-stage Docker build**: Imagem 60% menor
- **Gunicorn**: Múltiplos workers para concorrência
- **Nginx cache**: Arquivos estáticos com cache de 30 dias
- **Gzip compression**: Redução de ~70% no tráfego
- **Database indexing**: Queries otimizadas
- **Lazy loading**: Carregamento sob demanda de imagens

### Ajuste de Workers

```python
# gunicorn_config.py
workers = 2  # Para SQLite
workers = 4  # Para PostgreSQL (recomendado: CPU * 2 + 1)
```

---

## Roadmap

### Versão 2.1 (Planejado)

- [ ] API REST completa
- [ ] Integração com sistemas externos
- [ ] Relatórios customizáveis
- [ ] Notificações por email
- [ ] Mobile app (PWA)

### Versão 2.2 (Futuro)

- [ ] Machine Learning para análise de qualidade
- [ ] OCR para leitura de fichas técnicas
- [ ] Integração com ERP
- [ ] Multi-idioma

---

## Contribuindo

Este é um projeto proprietário da Puket. Para contribuições internas:

1. Criar branch a partir de `main`
2. Fazer alterações
3. Testar localmente
4. Criar Pull Request
5. Aguardar review

---

## Suporte

### Contatos

- **Desenvolvedor**: Nicolas Matsuda
- **Empresa**: Puket
- **Email**: [contato]
- **Documentação**: Consultar arquivos na pasta `/docs`

### Obter Ajuda

1. Consultar documentação em `/docs`
2. Verificar logs em `/opt/prova_app/logs`
3. Abrir issue no repositório interno
4. Contatar equipe de desenvolvimento

---

## Licença

Copyright © 2025 Puket - Todos os direitos reservados.

Este software é proprietário e confidencial. Uso não autorizado é estritamente proibido.

---

## Changelog

### v2.0.0 (2025-01-16)

- ✨ Novo sistema de checklists de avaliação
- ✨ Dashboard analytics redesenhado
- ✨ Sistema de design components completo
- ✨ Responsividade mobile aprimorada
- 🐛 Correções de bugs diversos
- 📝 Documentação completa de Docker e Deploy

### v1.5.0 (2024-12-08)

- ✨ Suporte a Docker
- ✨ Migração para PostgreSQL
- ✨ Sistema de auditoria
- 🔒 Melhorias de segurança

### v1.0.0 (2024-11-01)

- 🎉 Lançamento inicial
- 📝 Módulos de relatórios, referências e provas
- 📊 Dashboard básico
- 🔐 Sistema de autenticação

---

## Agradecimentos

Desenvolvido com ❤️ pela equipe Puket.

Tecnologias open-source utilizadas:
- Flask
- SQLAlchemy
- Bootstrap
- Chart.js
- Font Awesome
- Docker
- PostgreSQL
