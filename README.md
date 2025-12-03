# Aplicação de Provas de Modelagem

Sistema web para gerenciamento de provas de peças piloto, controle de qualidade e acompanhamento de modelagem.

## 🎯 Funcionalidades

- Gestão de relatórios de provas por coleção
- Upload e organização de fotos (desenho, qualidade, estilo, amostras)
- Controle de múltiplas provas por referência
- Geração automática de PDF para cada relatório
- Sistema de status e acompanhamento
- Gestão de usuários e permissões
- Painel administrativo

## 🛠️ Tecnologias

- **Backend:** Flask 3.0
- **Banco de Dados:** SQLite (dev) / PostgreSQL (prod)
- **Servidor WSGI:** Gunicorn
- **Proxy Reverso:** Nginx
- **PDF:** xhtml2pdf
- **Excel:** openpyxl
- **Autenticação:** Flask-Login

## 📦 Estrutura do Projeto

```
prova_modelagem_app/
├── app.py                    # Aplicação principal
├── wsgi.py                   # Entry point WSGI
├── config.py                 # Configurações
├── models.py                 # Modelos do banco
├── auth.py                   # Autenticação
├── admin.py                  # Painel admin
├── utils.py                  # Utilitários
├── requirements.txt          # Dependências
├── .env.production          # Variáveis de ambiente (produção)
├── gunicorn_config.py       # Config Gunicorn
├── nginx.conf               # Config Nginx
├── start.sh                 # Script de inicialização
├── stop.sh                  # Script para parar
├── restart.sh               # Script de reinício
├── status.sh                # Verificar status
├── templates/               # Templates HTML
├── static/                  # CSS, JS, imagens
├── uploads/                 # Arquivos enviados
├── relatorios_pdf/         # PDFs gerados
└── instance/               # Banco SQLite (dev)
```

## 🚀 Quick Start - Desenvolvimento

```bash
# Clonar repositório
git clone <url-repositorio>
cd prova_modelagem_app

# Criar virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou .venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Criar banco e usuário admin
python3 create_test_user.py

# Executar em modo desenvolvimento
python3 app.py
```

Acesse: http://localhost:5000

## 🏭 Deploy em Produção

Para deploy em servidor de produção, consulte o guia completo: **[DEPLOY.md](DEPLOY.md)**

### Quick Deploy

```bash
# 1. Configurar .env.production
cp .env.example .env.production
nano .env.production

# 2. Instalar dependências
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Configurar banco de dados
python3 migrate_to_postgres.py
python3 create_test_user.py

# 4. Iniciar aplicação
./start.sh
```

## 📝 Configuração

### Variáveis de Ambiente (.env.production)

```env
SECRET_KEY=<chave-secreta-gerada>
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=postgresql://usuario:senha@localhost:5432/provas_db
HOST=0.0.0.0
PORT=8000
WORKERS=4
LOG_LEVEL=INFO
```

### Banco de Dados Suportados

- **PostgreSQL** (recomendado para produção)
- **MySQL/MariaDB** (suportado)
- **SQLite** (apenas desenvolvimento)

## 🔒 Segurança

- Senhas hasheadas com Werkzeug
- Autenticação via Flask-Login
- SECRET_KEY única por instalação
- HTTPS recomendado
- Validação de tipos de arquivo
- Proteção contra CSRF

## 📊 Gerenciamento

### Comandos Úteis

```bash
./start.sh      # Iniciar aplicação
./stop.sh       # Parar aplicação
./restart.sh    # Reiniciar aplicação
./status.sh     # Ver status
```

### Logs

```bash
tail -f /var/log/provas_app/app.log
tail -f /var/log/provas_app/error.log
```

## 🧪 Testes

```bash
# Executar testes
python3 -m pytest tests/

# Com cobertura
python3 -m pytest --cov=. tests/
```

## 📄 Licença

Uso interno - Todos os direitos reservados

## 👥 Autores

Imaginarium - Equipe de Desenvolvimento

## 📞 Suporte

Para problemas ou dúvidas, consulte:
1. [DEPLOY.md](DEPLOY.md) - Guia completo de deploy
2. Logs da aplicação
3. Equipe de TI

---

**Versão:** 1.0.0
**Última Atualização:** 2024
