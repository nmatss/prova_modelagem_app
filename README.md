# 🎨 Sistema de Gestão de Provas de Modelagem - Puket

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0+-green?logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap&logoColor=white)
![License](https://img.shields.io/badge/License-Proprietário-yellow)

**Sistema profissional para gestão completa de provas de modelagem de vestuário**

[🚀 Quick Start](#-quick-start) •
[📖 Documentação](#-documentação-completa) •
[🐳 Deploy](#-deploy) •
[💻 Desenvolvimento](#-desenvolvimento) •
[🤝 Suporte](#-suporte)

</div>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades-principais)
- [Tecnologias](#-stack-tecnológica)
- [Quick Start](#-quick-start)
- [Deploy](#-deploy)
- [Documentação Completa](#-documentação-completa)
- [Desenvolvimento](#-desenvolvimento)
- [Servidor de Produção](#-servidor-de-produção)
- [Suporte](#-suporte)

---

## 🎯 Sobre o Projeto

Sistema web completo desenvolvido especificamente para a **Puket** para gerenciar todo o ciclo de vida das provas de modelagem de vestuário, desde o recebimento das amostras até a aprovação final.

### Contexto de Negócio

Gerencia provas de modelagem organizadas por:
- **Categorias**: Baby, Kids, Teen, Adulto
- **Múltiplas Provas** por referência com controle de versão
- **Feedbacks Especializados**: Times de Qualidade, Estilo e Modelagem
- **Documentação Visual**: Upload organizado de fotos por contexto e tamanho
- **Rastreabilidade Completa**: Sistema de lacres e histórico de alterações

---

## ✨ Funcionalidades Principais

### 📝 Gestão de Relatórios
- ✅ Criação de relatórios por coleção/temporada
- ✅ Organização por categorias (Baby/Kids/Teen/Adulto)
- ✅ Upload de apresentações (PPT), fichas técnicas e imagens
- ✅ Histórico completo de alterações com auditoria

### 🎨 Referências e Provas
- ✅ Múltiplas referências por relatório
- ✅ Controle de provas numeradas (1ª, 2ª, 3ª prova...)
- ✅ Status: Em Andamento, Aprovada, Reprovada, Comitê
- ✅ Motivos de alteração rastreados
- ✅ Informações de fornecedor, composição e gramatura

### 📷 Gestão de Fotos Organizada
- ✅ **Por Contexto**: Desenho, Amostra, Prova na Modelo, Qualidade, Estilo, Modelagem
- ✅ **Por Tamanho**: Fotos separadas para cada tamanho (P, M, G, etc.)
- ✅ **Galeria Visual**: Visualização em grid responsivo
- ✅ **Upload em Lote**: Múltiplos arquivos simultaneamente

### 👥 Feedbacks Especializados
- ✅ **Time de Qualidade**: Checklists, comentários e observações
- ✅ **Time de Estilo**: Avaliação visual e sugestões
- ✅ **Time de Modelagem**: Análise técnica e medidas
- ✅ Histórico de todos os feedbacks por prova

### 📊 Dashboard e Analytics
- ✅ Estatísticas em tempo real (taxas de aprovação, retrabalho)
- ✅ Gráficos interativos (Chart.js)
- ✅ Filtros avançados (status, categoria, fornecedor, data)
- ✅ Insights automáticos de performance
- ✅ Exportação para Excel e PDF

### 🔐 Administração e Segurança
- ✅ Sistema de autenticação robusto (Flask-Login)
- ✅ Painel administrativo completo
- ✅ Gerenciamento de usuários com roles (Admin, Gestor, Usuário)
- ✅ Rate limiting e proteção contra ataques
- ✅ Logs de auditoria completos (quem, quando, o quê)
- ✅ Validação de senhas fortes

---

## 🛠 Stack Tecnológica

### Backend
```
Python 3.11+
├── Flask 3.0 - Framework web
├── SQLAlchemy 3.1 - ORM
├── Flask-Login 0.6 - Autenticação
├── PostgreSQL 15 - Banco de dados (Produção)
├── SQLite - Banco de dados (Desenvolvimento)
├── Gunicorn 21.2 - WSGI server
└── WeasyPrint - Geração de PDF
```

### Frontend
```
Bootstrap 5.3.0
├── Bootstrap Icons 1.11
├── Chart.js 4.4 - Gráficos interativos
├── JavaScript ES6+ Modular
└── Google Fonts (Inter)
```

### DevOps
```
Docker & Docker Compose
├── Multi-stage builds
├── Health checks
├── Resource limits
├── Volume persistence
└── Nginx (opcional como reverse proxy)
```

### Design System
```
Design Tokens CSS
├── 200+ variáveis CSS
├── 50+ componentes reutilizáveis
├── Mobile First & Responsive
├── WCAG 2.1 AA Compliant
└── Dark mode ready
```

---

## 🚀 Quick Start

### Opção 1: Docker (Recomendado) ⚡

```bash
# 1. Clonar repositório
git clone https://github.com/TIUnicoWeb/prova-modelagem-puket.git
cd prova-modelagem-puket

# 2. Configurar ambiente
cp .env.example .env
nano .env  # Configurar SECRET_KEY, senhas, etc

# 3. Gerar SECRET_KEY
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" >> .env

# 4. Iniciar com Docker
docker compose up -d --build

# 5. Verificar
docker compose ps
docker compose logs -f
```

**Acesse:** http://localhost:5000

**Login padrão:**
- Usuário: `admin`
- Senha: (definida no .env como ADMIN_PASSWORD)

### Opção 2: Desenvolvimento Local

```bash
# 1. Clonar repositório
git clone https://github.com/TIUnicoWeb/prova-modelagem-puket.git
cd prova-modelagem-puket

# 2. Criar ambiente virtual
python3.11 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar ambiente
cp .env.example .env
nano .env

# 5. Inicializar banco de dados
python3 -c "from app import app, db; app.app_context().push(); db.create_all()"

# 6. Iniciar aplicação
python3 app.py
```

**Acesse:** http://localhost:5000

---

## 🐳 Deploy

### Deploy Rápido (SQLite) - Testes e Demos

```bash
# Para ambientes de teste e demonstração
docker compose -f docker-compose.sqlite.yml up -d --build
```

**Tempo:** ~5 minutos
**Ideal para:** Testes, demos, ambiente single-user

### Deploy Produção (PostgreSQL) - Recomendado

```bash
# Para ambientes de produção
docker compose up -d --build

# Configurar backups automáticos
crontab -e
# Adicionar: 0 2 * * * /opt/prova_app/scripts/backup.sh
```

**Tempo:** ~15 minutos
**Ideal para:** Produção, múltiplos usuários simultâneos

### Deploy Manual (Ubuntu/Debian)

Para deploy tradicional sem Docker, consulte: **[Guia de Deploy em Produção](DOCS/deploy/PRODUCAO.md)**

---

## 📖 Documentação Completa

A documentação está organizada por área e público-alvo:

### 📚 Índice Geral
**[DOCS/INDEX.md](DOCS/INDEX.md)** - Índice mestre navegável de toda a documentação

### 🚀 Deploy e Infraestrutura
- **[Deploy com Docker](DOCS/deploy/DOCKER.md)** - Guia completo de containerização
- **[Deploy em Produção](DOCS/deploy/PRODUCAO.md)** - Deploy manual tradicional
- **[Servidor Atual](DOCS/deploy/SERVIDOR_ATUAL.md)** - Documentação do servidor 192.168.168.124

### 🏗️ Arquitetura
- **[Backend](DOCS/architecture/BACKEND.md)** - Flask, modelos, rotas, segurança
- **[Frontend](DOCS/architecture/FRONTEND.md)** - Templates, CSS, JavaScript, componentes
- **[Database](DOCS/architecture/DATABASE.md)** - Schema, relacionamentos, queries

### 📘 Guias de Uso
- **[Manutenção](DOCS/guides/MAINTENANCE.md)** - Operações diárias, backup, monitoramento
- **[Desenvolvimento](DOCS/guides/DEVELOPMENT.md)** - Padrões de código, workflows
- **[Troubleshooting](DOCS/guides/TROUBLESHOOTING.md)** - Resolução de problemas comuns

### 🎨 Design e UX
- **[Design System](DOCS/design/DESIGN_SYSTEM.md)** - Tokens, cores, tipografia
- **[Componentes](DOCS/design/COMPONENTS.md)** - Biblioteca de componentes CSS
- **[Padrões UX](DOCS/design/UX_PATTERNS.md)** - Interações e estados

### 🔌 API
- **[API Reference](DOCS/api/API_REFERENCE.md)** - Documentação completa de endpoints

---

## 💻 Desenvolvimento

### Pré-requisitos

- **Python:** 3.11+
- **PostgreSQL:** 15+ (ou Docker)
- **Node.js:** 18+ (apenas para build de assets)
- **Git:** 2.0+

### Setup do Ambiente

```bash
# Clonar e entrar no projeto
git clone https://github.com/TIUnicoWeb/prova-modelagem-puket.git
cd prova-modelagem-puket

# Criar ambiente virtual
python3.11 -m venv .venv
source .venv/bin/activate

# Instalar dependências de desenvolvimento
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Se existir

# Configurar ambiente
cp .env.example .env

# Inicializar banco
flask shell
>>> from db import init_app
>>> init_app(app)
>>> exit()

# Rodar em modo desenvolvimento
export FLASK_ENV=development
export FLASK_DEBUG=True
python app.py
```

### Estrutura do Projeto

```
prova_modelagem_app/
├── app.py                      # Aplicação Flask principal
├── models.py                   # Modelos SQLAlchemy
├── auth.py                     # Blueprint de autenticação
├── admin.py                    # Blueprint administrativo
├── config.py                   # Configurações
├── security.py                 # Camada de segurança
├── utils.py                    # Funções utilitárias
│
├── templates/                  # Templates Jinja2 (29 arquivos)
│   ├── base.html
│   ├── dashboard.html
│   ├── novo_relatorio.html
│   ├── detalhes_relatorio.html
│   ├── admin/                  # Painel admin
│   ├── audit/                  # Auditoria
│   └── errors/                 # Páginas de erro
│
├── static/                     # Assets estáticos
│   ├── css/                    # 10 arquivos CSS modulares
│   ├── js/                     # 11 módulos JavaScript
│   └── img/                    # Imagens e logos
│
├── DOCS/                       # 📚 Documentação organizada
│   ├── INDEX.md                # Índice mestre
│   ├── deploy/                 # Guias de deploy
│   ├── architecture/           # Arquitetura do sistema
│   ├── guides/                 # Guias de uso
│   ├── design/                 # Design system
│   └── api/                    # Referência de API
│
├── docker-compose.yml          # Compose PostgreSQL
├── docker-compose.sqlite.yml   # Compose SQLite
├── Dockerfile                  # Imagem Docker
├── requirements.txt            # Dependências Python
├── gunicorn_config.py         # Configuração Gunicorn
└── .env.example               # Exemplo de variáveis de ambiente
```

### Comandos Úteis

```bash
# Desenvolvimento
python app.py                   # Rodar aplicação
flask shell                     # Shell interativo
flask create-admin              # Criar usuário admin

# Docker
docker compose up -d            # Iniciar containers
docker compose logs -f web      # Ver logs
docker compose exec web bash   # Acessar container

# Testes
pytest                          # Rodar testes
pytest --cov                    # Com coverage

# Banco de dados
flask db init                   # Inicializar migrations
flask db migrate                # Criar migration
flask db upgrade                # Aplicar migration
```

### Padrões de Código

- **Python:** PEP 8 (Black formatter)
- **JavaScript:** ES6+ (Prettier)
- **CSS:** BEM naming convention
- **Git:** Conventional Commits

Consulte: **[Guia de Desenvolvimento](DOCS/guides/DEVELOPMENT.md)**

---

## 🖥️ Servidor de Produção

### Informações Gerais

```
Host: 192.168.168.124
Sistema: Ubuntu 24.04.3 LTS (Noble Numbat)
CPU: Intel Xeon E5-2650 @ 2.00GHz (12 vCPUs)
RAM: 9.7 GB
Disco: 97 GB (35% usado)
Container: prova_modelagem_app (Docker)
Status: ✅ Rodando (healthy)
```

### Acesso

```bash
# SSH
ssh nicolas@192.168.168.124

# Aplicação Web
http://192.168.168.124:5000
```

### Operações Comuns

```bash
# Ver logs
docker logs prova_modelagem_app -f

# Reiniciar aplicação
docker restart prova_modelagem_app

# Backup
./scripts/backup.sh

# Ver status
docker ps
docker stats prova_modelagem_app
```

**Documentação completa:** **[Servidor Atual](DOCS/deploy/SERVIDOR_ATUAL.md)**

---

## 📊 Estatísticas do Projeto

### Código
- **Linhas de Código:** ~25.000 total
  - Python: ~15.000 linhas
  - Templates (Jinja2): ~5.000 linhas
  - JavaScript: ~3.000 linhas
  - CSS: ~5.000 linhas
- **Arquivos:** ~150 arquivos
- **Módulos Python:** 15 principais
- **Templates:** 29 arquivos Jinja2
- **Endpoints:** 32 rotas HTTP

### Frontend
- **Componentes CSS:** 50+ reutilizáveis
- **Design Tokens:** 200+ variáveis
- **Breakpoints:** 5 níveis de responsividade
- **Acessibilidade:** WCAG 2.1 AA compliant

### Banco de Dados
- **Tabelas:** 6 principais
- **Relacionamentos:** Cascade completo
- **Índices:** Otimizados para performance
- **Auditoria:** 100% das ações logadas

### Documentação
- **Páginas:** 15+ documentos
- **Linhas:** ~34.000 linhas de markdown
- **Diagramas:** ERD, Fluxos, Sequências
- **Exemplos de Código:** 200+

---

## 🔐 Segurança

### Camadas de Proteção

✅ **Autenticação:**
- Flask-Login com sessões seguras
- Hashing de senhas (pbkdf2:sha256)
- Validação de senhas fortes
- Sistema de reset de senha com tokens

✅ **Autorização:**
- Role-Based Access Control (RBAC)
- Decorators de permissão
- Verificação de propriedade de recursos

✅ **Proteção de Dados:**
- CSRF Protection
- SQL Injection (SQLAlchemy ORM)
- XSS Prevention (sanitização de inputs)
- Path Traversal Protection

✅ **Headers de Segurança:**
- X-Frame-Options: SAMEORIGIN
- X-Content-Type-Options: nosniff
- Content-Security-Policy configurado
- Referrer-Policy restritivo

✅ **Rate Limiting:**
- Baseado em IP e endpoint
- Proteção contra brute force
- Configurável por rota

✅ **Auditoria:**
- Log completo de todas as ações
- Rastreamento de IP e User-Agent
- Retenção permanente de logs

---

## 📈 Performance

### Otimizações Implementadas

✅ **Backend:**
- Compressão GZIP (Flask-Compress)
- Connection pooling (SQLAlchemy)
- Lazy loading de relacionamentos
- Queries otimizadas com índices

✅ **Frontend:**
- Lazy loading de imagens
- Minificação de CSS/JS
- Cache headers otimizados
- Lazy loading de Chart.js

✅ **Infraestrutura:**
- Gunicorn com múltiplos workers
- Health checks automáticos
- Resource limits no Docker
- Nginx para arquivos estáticos

### Métricas Atuais (Produção)

```
CPU Usage: 0.02%
Memory: 94 MB / 512 MB (18%)
Response Time: < 200ms (média)
Uptime: 99.9%
```

---

## 🤝 Suporte

### Documentação

- **Índice Geral:** [DOCS/INDEX.md](DOCS/INDEX.md)
- **Troubleshooting:** [DOCS/guides/TROUBLESHOOTING.md](DOCS/guides/TROUBLESHOOTING.md)
- **Manutenção:** [DOCS/guides/MAINTENANCE.md](DOCS/guides/MAINTENANCE.md)

### Problemas Comuns

**Erro ao iniciar aplicação:**
→ Verifique [Troubleshooting](DOCS/guides/TROUBLESHOOTING.md#aplicação-não-inicia)

**Erro de conexão com banco:**
→ Verifique [Troubleshooting](DOCS/guides/TROUBLESHOOTING.md#banco-de-dados)

**Erro em uploads:**
→ Verifique [Troubleshooting](DOCS/guides/TROUBLESHOOTING.md#uploads-falhando)

### Contato

- **Desenvolvedor:** Nicolas Matsuda
- **Empresa:** Puket / Grupo Único
- **Email:** nicolas.matsuda@grupounico.com

---

## 📄 Licença

Este projeto é proprietário e foi desenvolvido exclusivamente para a **Puket**.

© 2024-2026 TI Unico Web. Todos os direitos reservados.

---

## 🙏 Agradecimentos

- **Equipe Puket** pelo feedback constante e requisitos claros
- **Comunidade Flask** pela documentação excelente
- **Bootstrap Team** pelo framework responsivo
- **Chart.js** pela biblioteca de gráficos
- **WeasyPrint** pelo motor de geração de PDF

---

## 🎯 Roadmap

### v2.1 (Q1 2026)
- [ ] Implementar notificações por email
- [ ] Adicionar comparação de provas lado a lado
- [ ] Timeline visual de histórico
- [ ] Filtros avançados em todas as tabs

### v2.2 (Q2 2026)
- [ ] API RESTful completa
- [ ] Integração com ERP
- [ ] App mobile (React Native)
- [ ] Dark mode

### v3.0 (Q3 2026)
- [ ] Multi-tenancy (múltiplas empresas)
- [ ] IA para sugestões automáticas
- [ ] Workflow de aprovações customizável
- [ ] Dashboard executivo avançado

---

<div align="center">

**[⬆ Voltar ao Topo](#-sistema-de-gestão-de-provas-de-modelagem---puket)**

---

**Sistema de Gestão de Provas de Modelagem - Puket**

Desenvolvido com ❤️ pela **TI Unico Web**

🚀 **[Começar Agora](#-quick-start)** | 📖 **[Documentação](DOCS/INDEX.md)** | 🐳 **[Deploy](#-deploy)**

</div>
