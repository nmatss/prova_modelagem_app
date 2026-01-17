# 🛠️ Guia Completo de Desenvolvimento - Prova Modelagem App

## 📑 Índice

1. [Setup do Ambiente](#setup-do-ambiente)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Padrões de Código](#padrões-de-código)
4. [Workflow de Desenvolvimento](#workflow-de-desenvolvimento)
5. [Como Criar Novas Features](#como-criar-novas-features)
6. [Testes e Debugging](#testes-e-debugging)
7. [Boas Práticas](#boas-práticas)
8. [Code Review Checklist](#code-review-checklist)

---

## 🚀 Setup do Ambiente

### Requisitos do Sistema

**Software necessário**:
- **Python**: 3.9 ou superior
- **Node.js**: 16+ (opcional, para minificação de assets)
- **PostgreSQL**: 14+ (produção) ou SQLite (desenvolvimento)
- **Git**: 2.30+

**Sistema operacional**: Linux (WSL2), macOS, ou Windows 10/11

---

### Passo 1: Clonar o Repositório

```bash
# Clonar o projeto
git clone https://github.com/sua-org/prova_modelagem_app.git
cd prova_modelagem_app

# Criar branch de desenvolvimento
git checkout -b feature/sua-feature
```

---

### Passo 2: Criar Ambiente Virtual

```bash
# Criar virtual environment
python3 -m venv venv

# Ativar virtual environment
# Linux/Mac:
source venv/bin/activate

# Windows:
.\venv\Scripts\activate

# Verificar ativação
which python  # Deve mostrar caminho dentro de venv/
```

---

### Passo 3: Instalar Dependências

```bash
# Instalar dependências do requirements.txt
pip install -r requirements.txt

# Verificar instalação
pip list

# Dependências principais esperadas:
# Flask==3.0.0
# Flask-SQLAlchemy==3.1.1
# Flask-Login==0.6.3
# Flask-Compress==1.14
# Werkzeug==3.0.1
# psycopg2-binary==2.9.9
# gunicorn==21.2.0
```

---

### Passo 4: Configurar Variáveis de Ambiente

**Criar arquivo `.env`**:
```bash
# Copiar template
cp .env.example .env

# Editar com suas configurações
nano .env
```

**Conteúdo do `.env`**:
```bash
# Flask
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production

# Database (escolha um)
# SQLite (desenvolvimento)
DATABASE_URL=sqlite:///instance/provas.db

# PostgreSQL (produção)
# DATABASE_URL=postgresql://user:password@192.168.168.124:5432/prova_modelagem_db

# Upload
MAX_CONTENT_LENGTH=16777216  # 16MB em bytes
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,pdf,xlsx,xls,ppt,pptx

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Server
HOST=127.0.0.1
PORT=5000
```

---

### Passo 5: Inicializar Banco de Dados

**SQLite (desenvolvimento)**:
```bash
# Criar diretórios
mkdir -p instance logs uploads relatorios_pdf

# Criar banco e tabelas
python3 << EOF
from app import app, db
with app.app_context():
    db.create_all()
    print("✅ Banco criado!")
EOF
```

**PostgreSQL (produção)**:
```bash
# Conectar ao PostgreSQL
psql -h 192.168.168.124 -U postgres

# Criar banco
CREATE DATABASE prova_modelagem_db;
\q

# Criar tabelas
python3 << EOF
from app import app, db
with app.app_context():
    db.create_all()
    print("✅ Banco criado!")
EOF
```

---

### Passo 6: Criar Usuário Admin

```bash
# Usando comando Flask CLI
flask create-admin

# Ou manualmente:
python3 << EOF
from app import app, db
from models import Usuario
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = Usuario(
        username='admin',
        password_hash=generate_password_hash('Admin@123'),
        email='admin@sistema.local',
        nome_completo='Administrador',
        role='admin',
        is_admin=True,
        is_active=True,
        senha_temporaria=True
    )
    db.session.add(admin)
    db.session.commit()
    print("✅ Admin criado! User: admin | Senha: Admin@123")
EOF
```

---

### Passo 7: Executar o Servidor de Desenvolvimento

```bash
# Método 1: Flask development server (recomendado para dev)
flask run

# Método 2: Python direto
python app.py

# Método 3: Gunicorn (mais próximo de produção)
gunicorn -c gunicorn_config.py app:app

# Servidor estará rodando em:
# http://127.0.0.1:5000
```

**Testar acesso**:
```bash
# Em outro terminal
curl http://localhost:5000

# Ou abrir no navegador
open http://localhost:5000
```

---

### Passo 8: Verificar Instalação

**Checklist de verificação**:
```bash
# ✅ Python version
python --version  # >= 3.9

# ✅ Flask instalado
flask --version

# ✅ Banco acessível
python3 << EOF
from app import app, db
from models import Usuario
with app.app_context():
    print(f"Usuários cadastrados: {Usuario.query.count()}")
EOF

# ✅ Diretórios criados
ls -la uploads/ relatorios_pdf/ logs/ instance/

# ✅ Servidor respondendo
curl -I http://localhost:5000
```

---

## 📁 Estrutura do Projeto

```
prova_modelagem_app/
│
├── 📄 app.py                    # Aplicação Flask principal (1943 linhas)
├── 📄 models.py                 # Modelos SQLAlchemy (190 linhas)
├── 📄 auth.py                   # Autenticação (177 linhas)
├── 📄 admin.py                  # Painel administrativo (402 linhas)
├── 📄 config.py                 # Configurações (112 linhas)
├── 📄 db.py                     # Inicialização do banco
├── 📄 utils.py                  # Funções utilitárias
├── 📄 error_handlers.py         # Tratamento de erros HTTP
├── 📄 security.py               # Headers de segurança
├── 📄 audit_helpers.py          # Helpers de auditoria
├── 📄 excel_export.py           # Exportação para Excel
├── 📄 gunicorn_config.py        # Config Gunicorn (produção)
├── 📄 wsgi.py                   # Entry point WSGI
├── 📄 requirements.txt          # Dependências Python
├── 📄 .env                      # Variáveis de ambiente (não commitar!)
├── 📄 .gitignore                # Arquivos ignorados pelo Git
│
├── 📂 static/                   # Assets estáticos
│   ├── 📂 css/                  # Folhas de estilo
│   │   ├── design-system.css   # Design tokens (200+ variáveis)
│   │   ├── components.css      # Componentes reutilizáveis
│   │   ├── custom.css          # Estilos customizados
│   │   ├── mobile.css          # Responsividade mobile
│   │   ├── accessibility.css   # WCAG 2.1 AA
│   │   ├── navigation.css      # Sistema de navegação
│   │   ├── table.css           # Tabelas responsivas
│   │   ├── wizard.css          # Multi-step forms
│   │   ├── file-upload.css     # Upload de arquivos
│   │   └── *.min.css           # Versões minificadas
│   │
│   ├── 📂 js/                   # JavaScript
│   │   ├── app.js              # Aplicação principal (632 linhas)
│   │   ├── accessibility.js    # Melhorias de acessibilidade
│   │   ├── charts-config.js    # Configuração Chart.js
│   │   ├── datatable.js        # Tabelas interativas
│   │   ├── date-picker.js      # Seletor de data
│   │   ├── file-upload.js      # Upload drag-and-drop
│   │   ├── wizard.js           # Forms multi-step
│   │   ├── lazy-loading.js     # Lazy loading de imagens
│   │   └── *.min.js            # Versões minificadas
│   │
│   ├── 📂 img/                  # Imagens estáticas
│   └── 📂 vendor/               # Bibliotecas third-party
│       ├── bootstrap/           # Bootstrap 5.3
│       ├── chartjs/             # Chart.js 4.4
│       └── fontawesome/         # Font Awesome 6.4
│
├── 📂 templates/                # Templates Jinja2
│   ├── base.html               # Template base
│   ├── login.html              # Página de login
│   ├── dashboard.html          # Dashboard principal
│   ├── novo_relatorio.html     # Criar relatório
│   ├── editar_relatorio.html   # Editar relatório
│   ├── detalhes_relatorio.html # Visualizar detalhes
│   ├── nova_prova.html         # Adicionar prova
│   ├── analytics.html          # Página de analytics
│   │
│   ├── 📂 admin/                # Área administrativa
│   │   ├── dashboard.html
│   │   ├── users.html
│   │   ├── create_user.html
│   │   ├── edit_user.html
│   │   └── change_password.html
│   │
│   ├── 📂 audit/                # Sistema de auditoria
│   │   ├── index.html
│   │   ├── detalhes.html
│   │   └── timeline.html
│   │
│   └── 📂 errors/               # Páginas de erro
│       ├── 403.html            # Forbidden
│       ├── 404.html            # Not Found
│       ├── 413.html            # File Too Large
│       ├── 429.html            # Rate Limit
│       └── 500.html            # Server Error
│
├── 📂 instance/                 # Dados de instância (não commitar!)
│   └── provas.db               # SQLite database
│
├── 📂 uploads/                  # Arquivos enviados (não commitar!)
│   ├── 2025/01/                # Organizados por ano/mês
│   └── ...
│
├── 📂 relatorios_pdf/          # PDFs gerados (não commitar!)
├── 📂 logs/                    # Logs da aplicação (não commitar!)
│   └── app.log
│
├── 📂 DOCS/                    # Documentação (você está aqui!)
│   ├── 📂 architecture/
│   │   └── DATABASE.md
│   ├── 📂 guides/
│   │   ├── DEVELOPMENT.md
│   │   └── TROUBLESHOOTING.md
│   ├── 📂 api/
│   │   └── API_REFERENCE.md
│   └── 📂 design/
│       ├── COMPONENTS.md
│       └── UX_PATTERNS.md
│
└── 📂 tests/                   # Testes (a implementar)
    ├── test_models.py
    ├── test_auth.py
    └── test_api.py
```

---

## 📝 Padrões de Código

### 1. Python (Backend)

#### PEP 8 + Flask Best Practices

**Imports**:
```python
# ✅ Ordem correta
# 1. Standard library
import os
from datetime import datetime

# 2. Third-party
from flask import Flask, render_template, request
from sqlalchemy import desc

# 3. Local
from models import db, Usuario, Relatorio
from utils import save_file
```

**Naming Conventions**:
```python
# ✅ Classes: PascalCase
class Usuario(db.Model):
    pass

class ProvaModelagem(db.Model):
    pass

# ✅ Functions/Variables: snake_case
def criar_relatorio():
    total_usuarios = 10
    pass

# ✅ Constants: UPPER_SNAKE_CASE
MAX_UPLOAD_SIZE = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'pdf'}

# ✅ Private: _prefixo
def _internal_function():
    pass
```

**Docstrings** (Google Style):
```python
def buscar_relatorios_filtrados(status=None, colecao=None, page=1):
    """Busca relatórios com filtros opcionais.

    Args:
        status (str, optional): Filtro por status da prova.
        colecao (str, optional): Filtro por nome da coleção.
        page (int, optional): Número da página. Defaults to 1.

    Returns:
        Pagination: Objeto de paginação do SQLAlchemy com resultados.

    Raises:
        ValueError: Se page < 1.

    Example:
        >>> resultados = buscar_relatorios_filtrados(status='APROVADA', page=1)
        >>> print(resultados.items)
    """
    if page < 1:
        raise ValueError("Page deve ser >= 1")

    query = Relatorio.query

    if status:
        query = query.filter_by(status=status)

    if colecao:
        query = query.filter(Relatorio.colecao.ilike(f'%{colecao}%'))

    return query.paginate(page=page, per_page=20)
```

**Type Hints**:
```python
from typing import List, Optional, Dict, Any

def get_user_stats(user_id: int) -> Dict[str, Any]:
    """Retorna estatísticas do usuário."""
    return {
        'total_relatorios': 10,
        'ultima_atividade': datetime.utcnow()
    }

def process_files(files: List[str]) -> Optional[List[str]]:
    """Processa lista de arquivos."""
    if not files:
        return None
    return [f.upper() for f in files]
```

**Error Handling**:
```python
# ✅ Específico e com logging
def criar_usuario(username: str, email: str) -> Optional[Usuario]:
    try:
        usuario = Usuario(username=username, email=email)
        db.session.add(usuario)
        db.session.commit()
        return usuario

    except IntegrityError as e:
        db.session.rollback()
        app.logger.error(f"Usuário duplicado: {username} - {e}")
        raise ValueError(f"Username '{username}' já existe")

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Erro ao criar usuário: {e}")
        raise
```

---

### 2. JavaScript (Frontend)

#### ES6+ + Modern Practices

**Modules**:
```javascript
// ✅ Use strict mode
'use strict';

// ✅ Constantes no topo
const API_BASE_URL = '/api';
const DEBOUNCE_DELAY = 300;

// ✅ Arrow functions
const fetchData = async (url) => {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Erro ao buscar dados:', error);
        throw error;
    }
};

// ✅ Destructuring
const { data, status } = await fetchData('/api/relatorios');

// ✅ Template literals
const message = `Encontrados ${data.length} relatórios`;

// ✅ Spread operator
const newArray = [...oldArray, newItem];
```

**DOM Manipulation**:
```javascript
// ✅ Modern selectors
const form = document.querySelector('#form-relatorio');
const buttons = document.querySelectorAll('.btn-submit');

// ✅ Event delegation
document.addEventListener('click', (e) => {
    if (e.target.matches('.btn-delete')) {
        handleDelete(e.target.dataset.id);
    }
});

// ✅ Dataset API
element.dataset.userId = '123';
console.log(element.dataset.userId);  // '123'
```

**Async/Await**:
```javascript
// ✅ Async function
async function loadDashboard() {
    try {
        const [stats, relatorios] = await Promise.all([
            fetch('/api/stats').then(r => r.json()),
            fetch('/api/relatorios').then(r => r.json())
        ]);

        renderStats(stats);
        renderRelatorios(relatorios);
    } catch (error) {
        showError('Erro ao carregar dashboard');
        console.error(error);
    }
}
```

**Code Organization**:
```javascript
// ✅ IIFE para evitar poluir global scope
(function() {
    'use strict';

    // Private variables
    let cache = {};

    // Private functions
    function _validateInput(value) {
        return value && value.trim().length > 0;
    }

    // Public API
    window.MyApp = {
        init() {
            this.bindEvents();
            this.loadInitialData();
        },

        bindEvents() {
            document.querySelector('#btn-save')
                .addEventListener('click', this.handleSave.bind(this));
        },

        handleSave(e) {
            e.preventDefault();
            // ...
        }
    };

})();

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    window.MyApp.init();
});
```

---

### 3. CSS (Frontend)

#### BEM + Design System

**BEM Naming**:
```css
/* Block */
.card { }

/* Element */
.card__header { }
.card__body { }
.card__footer { }

/* Modifier */
.card--primary { }
.card--large { }
.card__header--fixed { }
```

**Design Tokens**:
```css
/* ✅ Usar variáveis CSS */
.button-primary {
    background-color: var(--primary);
    color: var(--white);
    border-radius: var(--radius-md);
    padding: var(--spacing-md) var(--spacing-lg);
    font-size: var(--font-size-base);
    font-weight: var(--font-weight-semibold);
    transition: var(--transition-base);
}

.button-primary:hover {
    background-color: var(--primary-hover);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}
```

**Responsive Design**:
```css
/* ✅ Mobile-first */
.container {
    width: 100%;
    padding: 0 1rem;
}

/* Tablet */
@media (min-width: 768px) {
    .container {
        max-width: 720px;
        padding: 0 2rem;
    }
}

/* Desktop */
@media (min-width: 1024px) {
    .container {
        max-width: 960px;
    }
}
```

**Accessibility**:
```css
/* ✅ Focus visible */
button:focus-visible {
    outline: 2px solid var(--primary);
    outline-offset: 2px;
}

/* ✅ Contraste WCAG AA */
.text-on-primary {
    color: var(--white);  /* Contraste 4.5:1 no mínimo */
}

/* ✅ Prefers reduced motion */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
```

---

### 4. Git (Versionamento)

#### Conventional Commits

**Formato**:
```
<tipo>(<escopo>): <descrição>

[corpo opcional]

[rodapé opcional]
```

**Tipos**:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação (não afeta código)
- `refactor`: Refatoração
- `perf`: Melhoria de performance
- `test`: Adicionar/corrigir testes
- `chore`: Tarefas de build, configs

**Exemplos**:
```bash
# ✅ Feature
git commit -m "feat(relatorios): adicionar filtro por fornecedor"

# ✅ Fix
git commit -m "fix(auth): corrigir validação de senha forte"

# ✅ Docs
git commit -m "docs(database): adicionar ERD diagram"

# ✅ Refactor
git commit -m "refactor(models): simplificar queries de auditoria"

# ✅ Com breaking change
git commit -m "feat(api)!: mudar formato de resposta para JSON:API

BREAKING CHANGE: O formato de resposta da API mudou de:
  { data: [...] }
para:
  { data: { items: [...], meta: {} } }
"
```

**Branching Model**:
```
main                 [produção - protegida]
  └─ develop         [desenvolvimento ativo]
      ├─ feature/user-roles
      ├─ feature/excel-export
      ├─ fix/upload-validation
      └─ hotfix/security-patch
```

**Workflow**:
```bash
# 1. Criar branch de feature
git checkout develop
git pull origin develop
git checkout -b feature/nome-da-feature

# 2. Desenvolver com commits frequentes
git add .
git commit -m "feat(escopo): descrição"

# 3. Atualizar com develop
git fetch origin
git rebase origin/develop

# 4. Push e Pull Request
git push -u origin feature/nome-da-feature

# 5. Após aprovação, merge em develop
# (Usar GitHub/GitLab UI)
```

---

## 🔄 Workflow de Desenvolvimento

### Ciclo de Desenvolvimento

```mermaid
graph LR
    A[Issue/Task] --> B[Create Branch]
    B --> C[Develop]
    C --> D[Test Locally]
    D --> E{Tests Pass?}
    E -->|No| C
    E -->|Yes| F[Commit]
    F --> G[Push]
    G --> H[Pull Request]
    H --> I[Code Review]
    I --> J{Approved?}
    J -->|No| C
    J -->|Yes| K[Merge]
    K --> L[Deploy]
```

### Fluxo Detalhado

**1. Receber Tarefa**
```bash
# Criar branch a partir de develop
git checkout develop
git pull origin develop
git checkout -b feature/TASK-123-filtro-fornecedor
```

**2. Desenvolver**
```python
# Implementar feature
# app.py ou arquivo relevante

@app.route('/api/fornecedores')
@login_required
def listar_fornecedores():
    """Lista fornecedores únicos"""
    fornecedores = db.session.query(
        Referencia.fornecedor
    ).distinct().order_by(Referencia.fornecedor).all()

    return jsonify({
        'success': True,
        'data': [f[0] for f in fornecedores if f[0]]
    })
```

**3. Testar Localmente**
```bash
# Rodar servidor
flask run

# Testar endpoint
curl http://localhost:5000/api/fornecedores

# Verificar no navegador
open http://localhost:5000
```

**4. Commit**
```bash
git add app.py
git commit -m "feat(api): adicionar endpoint de listagem de fornecedores

Retorna lista de fornecedores únicos ordenados alfabeticamente.

Closes #123"
```

**5. Push e PR**
```bash
git push -u origin feature/TASK-123-filtro-fornecedor

# Criar Pull Request no GitHub/GitLab
# Título: feat(api): adicionar endpoint de listagem de fornecedores
# Descrição: Link para issue, screenshots, testes realizados
```

**6. Code Review**
- Aguardar revisão de 1+ pessoa
- Corrigir feedback se necessário
- Atualizar PR com novos commits

**7. Merge**
```bash
# Após aprovação, merge via UI ou:
git checkout develop
git merge --no-ff feature/TASK-123-filtro-fornecedor
git push origin develop

# Deletar branch local e remota
git branch -d feature/TASK-123-filtro-fornecedor
git push origin --delete feature/TASK-123-filtro-fornecedor
```

---

## 🆕 Como Criar Novas Features

### Template de Feature Completa

Vamos criar uma feature exemplo: **"Sistema de Tags para Relatórios"**

#### 1. Planejamento

**Documentar antes de codificar**:
```markdown
# Feature: Sistema de Tags

## Objetivo
Permitir categorização de relatórios com tags (ex: "urgente", "revisão", "aprovado")

## Requisitos
- [ ] CRUD de tags
- [ ] Associação N:N entre relatórios e tags
- [ ] Filtro por tags na dashboard
- [ ] UI para adicionar/remover tags

## Banco de Dados
- Nova tabela: `tags` (id, nome, cor)
- Nova tabela: `relatorio_tags` (relatorio_id, tag_id)

## Endpoints API
- GET /api/tags - Listar todas
- POST /api/tags - Criar nova
- DELETE /api/tags/<id> - Deletar
- POST /relatorio/<id>/tags - Adicionar tag
- DELETE /relatorio/<id>/tags/<tag_id> - Remover tag

## UI
- Badge de tags no card de relatório
- Modal para gerenciar tags
- Filtro dropdown na sidebar
```

#### 2. Implementação Backend

**A. Criar Models**:
```python
# models.py

class Tag(db.Model):
    """Tags para categorização de relatórios"""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    cor = db.Column(db.String(7), default='#6c757d')  # Hex color
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Tag {self.nome}>'


# Tabela associativa N:N
relatorio_tags = db.Table('relatorio_tags',
    db.Column('relatorio_id', db.Integer, db.ForeignKey('relatorios.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


# Adicionar em Relatorio
class Relatorio(db.Model):
    # ... campos existentes ...

    # Relacionamento com tags
    tags = db.relationship('Tag', secondary=relatorio_tags, lazy='subquery',
                          backref=db.backref('relatorios', lazy=True))
```

**B. Criar Migration**:
```bash
# Criar tabelas
python3 << EOF
from app import app, db
from models import Tag, relatorio_tags
with app.app_context():
    db.create_all()
    print("✅ Tabelas de tags criadas!")
EOF
```

**C. Criar Endpoints API**:
```python
# app.py

@app.route('/api/tags', methods=['GET'])
@login_required
def api_list_tags():
    """Lista todas as tags"""
    tags = Tag.query.order_by(Tag.nome).all()
    return jsonify({
        'success': True,
        'data': [{
            'id': tag.id,
            'nome': tag.nome,
            'cor': tag.cor
        } for tag in tags]
    })


@app.route('/api/tags', methods=['POST'])
@login_required
@admin_required
def api_create_tag():
    """Cria nova tag (admin only)"""
    try:
        data = request.get_json()

        if not data.get('nome'):
            return jsonify({'success': False, 'error': 'Nome obrigatório'}), 400

        tag = Tag(
            nome=data['nome'].strip().upper(),
            cor=data.get('cor', '#6c757d')
        )

        db.session.add(tag)
        db.session.commit()

        return jsonify({
            'success': True,
            'data': {
                'id': tag.id,
                'nome': tag.nome,
                'cor': tag.cor
            }
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Tag já existe'}), 400

    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Erro ao criar tag: {e}')
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/relatorio/<int:id>/tags', methods=['POST'])
@login_required
def add_tag_to_relatorio(id):
    """Adiciona tag a um relatório"""
    try:
        relatorio = Relatorio.query.get_or_404(id)
        data = request.get_json()

        tag_id = data.get('tag_id')
        tag = Tag.query.get_or_404(tag_id)

        if tag not in relatorio.tags:
            relatorio.tags.append(tag)
            db.session.commit()

        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/relatorio/<int:id>/tags/<int:tag_id>', methods=['DELETE'])
@login_required
def remove_tag_from_relatorio(id, tag_id):
    """Remove tag de um relatório"""
    try:
        relatorio = Relatorio.query.get_or_404(id)
        tag = Tag.query.get_or_404(tag_id)

        if tag in relatorio.tags:
            relatorio.tags.remove(tag)
            db.session.commit()

        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
```

#### 3. Implementação Frontend

**A. UI Component (HTML)**:
```html
<!-- templates/dashboard.html -->

{% for relatorio in relatorios %}
<div class="card">
    <div class="card-body">
        <h5>{{ relatorio.descricao_geral }}</h5>

        <!-- Tags -->
        <div class="tags-container">
            {% for tag in relatorio.tags %}
                <span class="badge" style="background-color: {{ tag.cor }}">
                    {{ tag.nome }}
                    <button class="btn-remove-tag" data-relatorio-id="{{ relatorio.id }}" data-tag-id="{{ tag.id }}">
                        &times;
                    </button>
                </span>
            {% endfor %}

            <button class="btn-add-tag" data-relatorio-id="{{ relatorio.id }}">
                + Adicionar Tag
            </button>
        </div>
    </div>
</div>
{% endfor %}
```

**B. JavaScript Logic**:
```javascript
// static/js/tags.js

(function() {
    'use strict';

    const TagsManager = {
        init() {
            this.bindEvents();
        },

        bindEvents() {
            // Adicionar tag
            document.querySelectorAll('.btn-add-tag').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const relatorioId = e.target.dataset.relatorioId;
                    this.showTagSelector(relatorioId);
                });
            });

            // Remover tag
            document.querySelectorAll('.btn-remove-tag').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const relatorioId = e.target.dataset.relatorioId;
                    const tagId = e.target.dataset.tagId;
                    this.removeTag(relatorioId, tagId);
                });
            });
        },

        async showTagSelector(relatorioId) {
            try {
                // Buscar tags disponíveis
                const response = await fetch('/api/tags');
                const { data: tags } = await response.json();

                // Mostrar modal com opções
                const html = `
                    <div class="modal" id="tag-selector">
                        <div class="modal-content">
                            <h3>Selecione uma tag</h3>
                            <ul class="tag-list">
                                ${tags.map(tag => `
                                    <li>
                                        <button class="tag-option" data-tag-id="${tag.id}">
                                            <span class="badge" style="background: ${tag.cor}">
                                                ${tag.nome}
                                            </span>
                                        </button>
                                    </li>
                                `).join('')}
                            </ul>
                        </div>
                    </div>
                `;

                document.body.insertAdjacentHTML('beforeend', html);

                // Bind click events
                document.querySelectorAll('.tag-option').forEach(btn => {
                    btn.addEventListener('click', async (e) => {
                        const tagId = e.currentTarget.dataset.tagId;
                        await this.addTag(relatorioId, tagId);
                        document.getElementById('tag-selector').remove();
                    });
                });

            } catch (error) {
                console.error('Erro ao buscar tags:', error);
            }
        },

        async addTag(relatorioId, tagId) {
            try {
                const response = await fetch(`/relatorio/${relatorioId}/tags`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ tag_id: tagId })
                });

                if (response.ok) {
                    location.reload();  // Ou atualizar dinamicamente
                }
            } catch (error) {
                console.error('Erro ao adicionar tag:', error);
            }
        },

        async removeTag(relatorioId, tagId) {
            if (!confirm('Remover esta tag?')) return;

            try {
                const response = await fetch(`/relatorio/${relatorioId}/tags/${tagId}`, {
                    method: 'DELETE'
                });

                if (response.ok) {
                    location.reload();
                }
            } catch (error) {
                console.error('Erro ao remover tag:', error);
            }
        }
    };

    // Initialize
    document.addEventListener('DOMContentLoaded', () => {
        TagsManager.init();
    });

})();
```

#### 4. Testes

```python
# tests/test_tags.py

import pytest
from app import app, db
from models import Tag, Relatorio, Usuario

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    with app.app_context():
        db.drop_all()


def test_create_tag(client):
    """Testa criação de tag"""
    # Login como admin
    # ...

    response = client.post('/api/tags', json={
        'nome': 'URGENTE',
        'cor': '#ff0000'
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['nome'] == 'URGENTE'


def test_add_tag_to_relatorio(client):
    """Testa adicionar tag a relatório"""
    # Setup
    # ...

    response = client.post(f'/relatorio/{relatorio_id}/tags', json={
        'tag_id': tag_id
    })

    assert response.status_code == 200
    assert response.get_json()['success'] is True
```

#### 5. Documentação

```markdown
# Tags System

## Endpoints

### GET /api/tags
Lista todas as tags disponíveis.

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nome": "URGENTE",
      "cor": "#ff0000"
    }
  ]
}
```

### POST /api/tags
Cria nova tag (admin only).

**Request**:
```json
{
  "nome": "URGENTE",
  "cor": "#ff0000"
}
```

### POST /relatorio/{id}/tags
Adiciona tag a um relatório.

**Request**:
```json
{
  "tag_id": 1
}
```
```

---

## 🧪 Testes e Debugging

### Testes Manuais

**Checklist pré-deploy**:
- [ ] Login funciona com credenciais válidas
- [ ] Login falha com credenciais inválidas
- [ ] Criar novo relatório
- [ ] Editar relatório existente
- [ ] Adicionar prova a referência
- [ ] Upload de arquivos (imagens, PDF, Excel)
- [ ] Validação de arquivo muito grande (> 16MB)
- [ ] Exportar para Excel
- [ ] Gerar PDF
- [ ] Analytics carregam corretamente
- [ ] Filtros funcionam
- [ ] Painel admin (se for admin)
- [ ] Criar/editar/deletar usuários
- [ ] Logout

### Debugging no Flask

**Debug Mode**:
```python
# .env
FLASK_DEBUG=True

# app.py
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**Print Debugging**:
```python
# Adicionar prints estratégicos
@app.route('/relatorio/<int:id>')
def detalhes_relatorio(id):
    print(f"[DEBUG] Buscando relatório ID: {id}")

    relatorio = Relatorio.query.get_or_404(id)
    print(f"[DEBUG] Relatório encontrado: {relatorio.descricao_geral}")
    print(f"[DEBUG] Total de referências: {len(relatorio.referencias)}")

    return render_template('detalhes_relatorio.html', relatorio=relatorio)
```

**Logging**:
```python
# Usar logger ao invés de print
import logging

app.logger.info(f"Usuário {current_user.username} acessou relatório {id}")
app.logger.error(f"Erro ao salvar: {e}")
app.logger.warning(f"Upload grande: {file_size} bytes")
```

**Flask Toolbar** (recomendado):
```bash
pip install flask-debugtoolbar

# app.py
from flask_debugtoolbar import DebugToolbarExtension

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)
```

### Debugging JavaScript

**Console Methods**:
```javascript
console.log('Simple message');
console.info('Info message');
console.warn('Warning message');
console.error('Error message');

// Tabela
console.table([{name: 'João', age: 30}, {name: 'Maria', age: 25}]);

// Tempo de execução
console.time('loadData');
await loadData();
console.timeEnd('loadData');

// Stack trace
console.trace('Execution path');
```

**Debugger**:
```javascript
function problematicFunction(data) {
    debugger;  // Pausa execução aqui quando DevTools aberto

    const result = processData(data);
    return result;
}
```

**Network Monitoring**:
```javascript
// Ver requisições
fetch('/api/relatorios')
    .then(response => {
        console.log('Status:', response.status);
        console.log('Headers:', response.headers);
        return response.json();
    })
    .then(data => console.log('Data:', data))
    .catch(error => console.error('Error:', error));
```

---

## ✅ Boas Práticas

### 1. Segurança

```python
# ✅ Sempre validar inputs
username = request.form.get('username', '').strip()
if not username or len(username) < 3:
    flash('Username inválido', 'error')
    return redirect(url_for('login'))

# ✅ Usar prepared statements (SQLAlchemy já faz isso)
# ❌ NUNCA fazer:
query = f"SELECT * FROM usuarios WHERE username = '{username}'"  # SQL Injection!

# ✅ SQLAlchemy protege automaticamente:
usuario = Usuario.query.filter_by(username=username).first()

# ✅ Sanitizar HTML
from markupsafe import escape
comentario_seguro = escape(request.form.get('comentario'))

# ✅ Validar arquivos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if not allowed_file(file.filename):
    flash('Tipo de arquivo não permitido', 'error')
```

### 2. Performance

```python
# ✅ Usar paginação SEMPRE
pagination = Relatorio.query.paginate(page=page, per_page=20)

# ✅ Eager loading para relacionamentos
relatorios = Relatorio.query.options(
    db.joinedload(Relatorio.referencias)
).all()

# ✅ Índices em colunas de busca
username = db.Column(db.String(150), unique=True, index=True)

# ✅ Cache de queries caras
from functools import lru_cache

@lru_cache(maxsize=128)
def get_dashboard_stats():
    return {
        'total_relatorios': Relatorio.query.count(),
        'total_provas': Prova.query.count()
    }
```

### 3. Manutenibilidade

```python
# ✅ Funções pequenas e específicas
def calcular_taxa_aprovacao(provas):
    """Calcula taxa de aprovação de uma lista de provas"""
    if not provas:
        return 0

    total = len(provas)
    aprovadas = sum(1 for p in provas if p.status == 'APROVADA')

    return round(aprovadas / total * 100, 1)


# ✅ Constantes ao invés de magic numbers
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
PAGE_SIZE = 20
CACHE_TIMEOUT = 300  # 5 minutos


# ✅ Type hints
from typing import List, Optional

def buscar_usuarios(ativo: Optional[bool] = True) -> List[Usuario]:
    """Busca usuários ativos ou inativos"""
    if ativo is None:
        return Usuario.query.all()
    return Usuario.query.filter_by(is_active=ativo).all()
```

### 4. Error Handling

```python
# ✅ Try-except específico
try:
    db.session.commit()
except IntegrityError as e:
    db.session.rollback()
    app.logger.error(f'Constraint violation: {e}')
    flash('Dados duplicados', 'error')
except Exception as e:
    db.session.rollback()
    app.logger.error(f'Database error: {e}')
    flash('Erro ao salvar dados', 'error')
```

---

## 📋 Code Review Checklist

### Backend (Python)

- [ ] **Código segue PEP 8**
- [ ] **Imports organizados** (stdlib → 3rd party → local)
- [ ] **Docstrings em funções públicas**
- [ ] **Type hints quando apropriado**
- [ ] **Validação de inputs**
- [ ] **Error handling apropriado**
- [ ] **Logging em operações importantes**
- [ ] **Queries otimizadas** (evitar N+1)
- [ ] **Paginação em listagens**
- [ ] **Commits de banco com try-except**
- [ ] **Nomes descritivos de variáveis/funções**
- [ ] **Sem código comentado** (deletar ou explicar)
- [ ] **Sem secrets no código** (usar .env)
- [ ] **Testes passando** (se existirem)

### Frontend (JavaScript/CSS)

- [ ] **ES6+ syntax**
- [ ] **Código em strict mode**
- [ ] **Event delegation quando apropriado**
- [ ] **Async/await para chamadas assíncronas**
- [ ] **Error handling em fetches**
- [ ] **Loading states em operações async**
- [ ] **Acessibilidade** (ARIA labels, keyboard navigation)
- [ ] **CSS usando variáveis** (design tokens)
- [ ] **Responsividade mobile**
- [ ] **Compatibilidade de browsers** (ES6+ suportado?)
- [ ] **Sem console.log em produção**
- [ ] **Assets minificados** (se aplicável)

### Geral

- [ ] **Commits seguem Conventional Commits**
- [ ] **PR tem descrição clara**
- [ ] **Issue linkada no PR** (#123)
- [ ] **Sem conflitos com branch base**
- [ ] **Arquivos desnecessários não commitados** (.env, __pycache__, etc)
- [ ] **README atualizado** (se mudou setup)
- [ ] **Documentação atualizada** (se mudou API)
- [ ] **Testes manuais realizados**
- [ ] **Screenshots incluídos** (se mudou UI)

---

**📝 Última atualização**: 16/01/2025
**👤 Mantido por**: Equipe de Desenvolvimento
**🔗 Links relacionados**:
- [Documentação do Banco](../architecture/DATABASE.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [API Reference](../api/API_REFERENCE.md)
