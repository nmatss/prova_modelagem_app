# 🎨 Sistema de Gestão de Provas de Modelagem - Puket

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Sistema profissional para gestão de provas de modelagem, criado especificamente para a **Puket**.

[🚀 Começar](#-quick-start) •
[📖 Documentação](#-documentação) •
[🐳 Deploy](#-deploy) •
[🤝 Suporte](#-suporte)

</div>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Quick Start](#-quick-start)
- [Deploy](#-deploy)
- [Documentação](#-documentação)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Contribuindo](#-contribuindo)
- [Suporte](#-suporte)
- [Licença](#-licença)

---

## 🎯 Sobre o Projeto

Sistema web completo para gerenciar todo o ciclo de vida das provas de modelagem, desde o recebimento das amostras até a aprovação final, incluindo:

- **Gestão de Referências** (Baby, Kids, Teen, Adulto)
- **Múltiplas Provas** por referência
- **Feedbacks** de 3 equipes (Qualidade, Estilo, Modelagem)
- **Upload de Fotos** organizadas por contexto
- **Relatórios PDF** profissionais com fotos
- **Painel Administrativo** completo
- **Dashboard** com estatísticas e insights

---

## ✨ Funcionalidades

### 📝 Gestão de Relatórios
- Criar relatórios de provas com múltiplas referências
- Organização por coleção e categoria
- Upload de apresentação (PPT)
- Histórico completo de alterações

### 🎨 Referências e Provas
- 4 categorias: Baby, Kids, Teen, Adulto
- Múltiplas provas por referência
- Controle de status (Em Andamento, Aprovada, Reprovada, Comitê)
- Rastreamento de motivos de alteração

### 📷 Gestão de Fotos
- Upload organizado por contexto:
  - Desenho do produto
  - Fotos da amostra
  - Fotos na modelo
  - Fotos de qualidade
  - Fotos de estilo
  - Fotos de modelagem
- Associação por tamanho
- Visualização em galeria

### 👥 Feedbacks Multi-Equipe
- **Time de Qualidade**: Comentários e observações
- **Time de Estilo**: Feedbacks visuais
- **Time de Modelagem**: Análise técnica
- Histórico completo de todos os feedbacks

### 📊 Dashboard e Relatórios
- Estatísticas em tempo real
- Taxa de aprovação
- Taxa de retrabalho
- Insights automáticos
- Exportação de PDF profissional

### 🔐 Segurança e Admin
- Sistema de autenticação robusto
- Painel administrativo completo
- Gerenciamento de usuários
- Rate limiting
- Logs de auditoria
- Sessões seguras

---

## 🛠 Tecnologias

### Backend
- **Python 3.11+**
- **Flask 3.0+** - Framework web
- **PostgreSQL 15** - Banco de dados
- **SQLAlchemy** - ORM
- **Flask-Login** - Autenticação
- **Flask-Limiter** - Rate limiting

### Frontend
- **Bootstrap 5.3** - UI framework
- **Bootstrap Icons** - Ícones
- **JavaScript** - Interatividade

### PDF Generation
- **WeasyPrint** - Geração de PDF com CSS

### Deploy
- **Docker & Docker Compose** - Containerização
- **Gunicorn** - WSGI server
- **Nginx** - Reverse proxy (opcional)

---

## 🚀 Quick Start

### Pré-requisitos

- Python 3.11+
- PostgreSQL 15+ (ou Docker)
- Git

### Instalação Local (Desenvolvimento)

```bash
# 1. Clonar repositório
git clone https://github.com/TIUnicoWeb/prova-modelagem-puket.git
cd prova-modelagem-puket

# 2. Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar ambiente
cp .env.example .env
nano .env  # Editar configurações

# 5. Inicializar banco
python3 -c "from app import app, db; app.app_context().push(); db.create_all()"

# 6. Iniciar aplicação
python3 app.py
```

Acesse: http://localhost:5000

**Login padrão:**
- Usuário: `admin`
- Senha: (configurada no .env)

---

## 🐳 Deploy

### Deploy com Docker (Recomendado)

```bash
# 1. Clonar repositório
git clone https://github.com/TIUnicoWeb/prova-modelagem-puket.git
cd prova-modelagem-puket

# 2. Configurar ambiente
cp .env.example .env
nano .env  # Configurar SECRET_KEY, senhas, etc

# 3. Iniciar containers
docker compose up -d --build

# 4. Ver logs
docker compose logs -f

# 5. Criar usuário admin (se necessário)
docker compose exec web python3 -c "
from app import app, db
from models import User
from werkzeug.security import generate_password_hash
import os

with app.app_context():
    admin = User(
        username=os.getenv('ADMIN_USERNAME', 'admin'),
        email=os.getenv('ADMIN_EMAIL', 'admin@puket.com'),
        password_hash=generate_password_hash(os.getenv('ADMIN_PASSWORD')),
        is_admin=True
    )
    db.session.add(admin)
    db.session.commit()
"
```

**Acesse:** http://seu-servidor:8000

Para deploy completo com Nginx e SSL, veja: **[COMECE_AQUI.md](COMECE_AQUI.md)**

---

## 📖 Documentação

### Guias de Deploy

| Guia | Descrição | Tempo |
|------|-----------|-------|
| **[COMECE_AQUI.md](COMECE_AQUI.md)** | Quick start - 5 minutos ⭐ | 5 min |
| **[INICIO_RAPIDO_DOCKER.md](INICIO_RAPIDO_DOCKER.md)** | Deploy Docker detalhado | 10 min |
| **[DEPLOY_DOCKER.md](DEPLOY_DOCKER.md)** | Documentação Docker completa | - |
| **[DEPLOY_PRODUCAO.md](DEPLOY_PRODUCAO.md)** | Deploy manual tradicional | 30 min |
| **[README_DEPLOY.md](README_DEPLOY.md)** | Índice de documentação | - |

### Manuais

| Manual | Descrição |
|--------|-----------|
| **[MANUAL_USUARIO.md](MANUAL_USUARIO.md)** | Como usar o sistema |
| **[ACESSO_ADMIN.md](ACESSO_ADMIN.md)** | Painel administrativo |
| **[DOCUMENTACAO_INSTALACAO.md](DOCUMENTACAO_INSTALACAO.md)** | Instalação detalhada |

### Técnica

| Documento | Descrição |
|-----------|-----------|
| **[IMPLEMENTACAO_COMPLETA.md](IMPLEMENTACAO_COMPLETA.md)** | Arquitetura e implementação |
| **[NOMENCLATURA_PADRAO.md](NOMENCLATURA_PADRAO.md)** | Padrões de código |

---

## 📁 Estrutura do Projeto

```
prova-modelagem-puket/
├── app.py                      # Aplicação principal
├── models.py                   # Modelos do banco
├── auth.py                     # Autenticação
├── admin.py                    # Painel admin
├── security.py                 # Segurança
├── config.py                   # Configurações
├── utils.py                    # Utilitários
├── error_handlers.py           # Tratamento de erros
│
├── templates/                  # Templates HTML
│   ├── base.html
│   ├── dashboard.html
│   ├── novo_relatorio.html
│   ├── detalhes_relatorio.html
│   ├── relatorio_pdf.html     # Template do PDF
│   └── admin/                 # Painel admin
│
├── static/                     # Arquivos estáticos
│   ├── css/
│   ├── js/
│   └── img/
│
├── scripts/                    # Scripts de deploy
│   ├── deploy.sh
│   ├── docker-backup.sh
│   └── nginx.conf
│
├── docker-compose.yml          # Docker Compose
├── Dockerfile                  # Imagem Docker
├── gunicorn_config.py         # Servidor Gunicorn
├── requirements.txt           # Dependências Python
│
└── docs/                      # Documentação
    ├── COMECE_AQUI.md        ⭐
    ├── DEPLOY_DOCKER.md
    ├── DEPLOY_PRODUCAO.md
    └── ...
```

---

## 🔧 Comandos Úteis

### Desenvolvimento

```bash
# Iniciar aplicação
python3 app.py

# Criar usuário admin
python3 -c "from app import app, db; from models import User; ..."

# Backup do banco
pg_dump prova_modelagem_db > backup.sql
```

### Docker

```bash
# Iniciar
docker compose up -d

# Logs
docker compose logs -f

# Reiniciar
docker compose restart web

# Parar
docker compose stop

# Backup
./scripts/docker-backup.sh

# Limpar
docker compose down -v
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

---

## 🆘 Suporte

### Problemas Comuns

**Erro ao gerar PDF:**
- Verifique se WeasyPrint está instalado
- Verifique permissões da pasta uploads

**Erro de conexão com banco:**
- Verifique se PostgreSQL está rodando
- Confirme DATABASE_URL no .env

**Erro 502:**
- Reinicie o Gunicorn/Docker
- Verifique logs em /logs

### Logs

```bash
# Docker
docker compose logs -f web

# Manual
tail -f /opt/prova_app/logs/app.log
```

### Contato

- **Issues**: [GitHub Issues](https://github.com/TIUnicoWeb/prova-modelagem-puket/issues)
- **Email**: suporte@unicoweb.com.br

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👥 Equipe

Desenvolvido com ❤️ pela equipe **TI Unico Web** para **Puket**.

- **Desenvolvedor**: Nicolas Matsuda
- **Cliente**: Puket

---

## 🙏 Agradecimentos

- Equipe Puket pelo feedback constante
- Comunidade Flask pela documentação excelente
- WeasyPrint pelo motor de PDF

---

<div align="center">

**[⬆ Voltar ao topo](#-sistema-de-gestão-de-provas-de-modelagem---puket)**

---

**Sistema de Gestão de Provas de Modelagem - Puket**
© 2024 TI Unico Web. Todos os direitos reservados.

</div>
