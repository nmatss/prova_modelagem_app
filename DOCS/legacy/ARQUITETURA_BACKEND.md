# Arquitetura Backend - Sistema de Provas de Modelagem

## Visão Geral

O **Prova de Modelagem App** é um sistema web desenvolvido em Flask para gerenciar o ciclo completo de provas de modelagem de vestuário, desde o recebimento de amostras até a aprovação final, incluindo avaliações de qualidade, estilo e modelagem.

### Stack Tecnológica

- **Framework:** Flask 3.0.0
- **ORM:** SQLAlchemy 3.1.1
- **Autenticação:** Flask-Login 0.6.3
- **Banco de Dados:** PostgreSQL (produção) / SQLite (desenvolvimento)
- **Servidor:** Gunicorn 21.2.0
- **Compressão:** Flask-Compress 1.14
- **Geração de PDFs:** WeasyPrint / xhtml2pdf
- **Exportação Excel:** openpyxl 3.1.2
- **Processamento de Imagens:** Pillow 10.1.0

---

## Arquitetura Geral

```mermaid
graph TB
    subgraph "Camada de Apresentação"
        A[Templates Jinja2]
        B[Static Assets]
    end

    subgraph "Camada de Aplicação"
        C[app.py - Rotas Principais]
        D[auth.py - Autenticação]
        E[admin.py - Administração]
    end

    subgraph "Camada de Negócio"
        F[models.py - Modelos ORM]
        G[utils.py - Utilitários]
        H[excel_export.py - Exportação]
        I[audit_helpers.py - Auditoria]
    end

    subgraph "Camada de Infraestrutura"
        J[(PostgreSQL/SQLite)]
        K[uploads/]
        L[relatorios_pdf/]
    end

    subgraph "Segurança"
        M[security.py - Headers/Rate Limit]
        N[error_handlers.py - Tratamento]
    end

    A --> C
    B --> C
    C --> D
    C --> E
    D --> F
    E --> F
    C --> G
    C --> H
    C --> I
    F --> J
    G --> K
    H --> L
    M --> C
    N --> C
```

---

## Módulos do Sistema

### 1. app.py - Aplicação Principal

**Responsabilidades:**
- Configuração da aplicação Flask
- Registro de blueprints
- Rotas principais do sistema
- Sistema de auditoria
- Otimizações de performance
- Comandos CLI

**Principais Funcionalidades:**

#### 1.1 Configuração e Inicialização

```python
# Configuração de logging rotativo (10MB por arquivo, 10 backups)
# Compressão HTTP (GZIP) para responses
# Flask-Login configurado com mensagens personalizadas
# Criação automática de diretórios (uploads/, relatorios_pdf/)
```

#### 1.2 Sistema de Auditoria

```python
def registrar_log(acao, entidade_tipo, entidade_id, entidade_descricao, detalhes)
```

Registra todas as ações no sistema:
- **acao:** criar, editar, excluir, login, logout
- **entidade_tipo:** relatorio, prova, referencia, usuario
- **entidade_id:** ID da entidade afetada
- **detalhes:** JSON com informações adicionais
- **Captura:** IP, User-Agent, timestamp

#### 1.3 Otimizações de Performance

**Cache Headers:**
- `/static/`: Cache de 1 ano (immutable)
- `/uploads/`: Cache de 30 dias
- HTML: No-cache
- JSON API: Cache de 5 minutos

**Compressão:**
- GZIP nível 6
- Mínimo 500 bytes
- MIME types: HTML, CSS, JS, JSON, XML, SVG

---

### 2. auth.py - Sistema de Autenticação

**Blueprint:** `auth_bp`

**Rotas Implementadas:**

| Rota | Método | Descrição |
|------|--------|-----------|
| `/login` | GET, POST | Login de usuários |
| `/logout` | GET | Logout (requer login) |
| `/alterar-senha` | GET, POST | Alteração de senha própria |
| `/esqueci-senha` | GET, POST | Solicitação de reset de senha |
| `/reset-senha/<token>` | GET, POST | Reset de senha via token |

**Validação de Senha:**

Requisitos obrigatórios:
- Mínimo 8 caracteres
- 1 letra maiúscula
- 1 letra minúscula
- 1 número
- 1 caractere especial (@$!%*?&)

**Fluxo de Autenticação:**

```mermaid
sequenceDiagram
    participant U as Usuário
    participant A as auth.py
    participant DB as Banco de Dados
    participant L as Flask-Login

    U->>A: POST /login (username, password)
    A->>DB: Query User by username
    DB-->>A: User object
    A->>A: check_password_hash()
    alt Senha correta
        A->>L: login_user(user, remember)
        A->>DB: log_login(sucesso=True)
        A-->>U: Redirect /dashboard
    else Senha incorreta
        A->>DB: log_login(sucesso=False)
        A-->>U: Flash error + /login
    end
```

**Sistema de Reset de Senha:**

1. Usuário fornece username e email
2. Sistema gera token seguro (32 bytes)
3. Token expira em 24 horas
4. Token é armazenado em `User.reset_token`
5. Link enviado para admin (em produção, enviar email)

---

### 3. admin.py - Painel Administrativo

**Blueprint:** `admin_bp` (prefixo: `/admin`)

**Decorator de Segurança:**

```python
@admin_required
# Verifica current_user.is_admin OU current_user.role == 'admin'
# Redireciona para login se não autenticado
# Retorna 403 se não for administrador
```

**Rotas Implementadas:**

| Rota | Método | Descrição | Permissão |
|------|--------|-----------|-----------|
| `/admin/` | GET | Dashboard administrativo | Admin |
| `/admin/users` | GET | Lista todos os usuários | Admin |
| `/admin/users/create` | GET, POST | Cria novo usuário | Admin |
| `/admin/users/edit/<id>` | GET, POST | Edita usuário existente | Admin |
| `/admin/users/set_password/<id>` | POST | Define senha manualmente | Admin |
| `/admin/users/reset_password/<id>` | POST | Gera senha aleatória | Admin |
| `/admin/users/toggle_active/<id>` | POST | Ativa/desativa usuário | Admin |
| `/admin/users/delete/<id>` | POST | Soft delete (desativa) | Admin |
| `/admin/change-my-password` | GET, POST | Admin altera própria senha | Admin |

**Geração de Senha Segura:**

```python
gerar_senha_aleatoria(tamanho=12)
# Garante: 1 maiúscula, 1 minúscula, 1 número, 1 especial
# Caracteres especiais: @$!%*?&
# Embaralhamento criptográfico com secrets.SystemRandom()
```

**Roles do Sistema:**

- **admin:** Acesso total ao sistema
- **gestor:** Gerencia relatórios e provas
- **usuario:** Visualiza e cria relatórios

**Auditoria de Ações:**

Todas as ações administrativas são logadas:
- Criação de usuário
- Atualização de dados
- Mudança de role
- Reset de senha
- Ativação/desativação

---

### 4. models.py - Modelos de Dados

**ORM:** SQLAlchemy

#### 4.1 Diagrama de Relacionamento Entre Entidades

```mermaid
erDiagram
    USUARIOS ||--o{ RELATORIOS : cria
    USUARIOS ||--o{ AUDIT_LOGS : gera
    RELATORIOS ||--|{ REFERENCIAS : contem
    REFERENCIAS ||--|{ PROVAS : possui
    PROVAS ||--o{ FOTOS : anexa

    USUARIOS {
        int id PK
        string username UK
        string password_hash
        string email UK
        string nome_completo
        string role
        boolean is_admin
        boolean is_active
        datetime ultimo_acesso
        boolean senha_temporaria
        string reset_token
        datetime reset_token_expires
        datetime created_at
        datetime updated_at
    }

    RELATORIOS {
        int id PK
        string codigo UK
        string descricao_geral
        string colecao
        string temporada
        int ano
        string ppt_path
        string imagem_produto
        string ficha_tecnica
        string status_geral
        boolean is_active
        int created_by FK
        datetime created_at
        datetime updated_at
    }

    REFERENCIAS {
        int id PK
        int relatorio_id FK
        string codigo_referencia
        string tipo_categoria
        string numero_ref
        string origem
        string fornecedor
        string fornecedor_contato
        string materia_prima
        string composicao
        string gramatura
        string aviamentos
        text observacoes
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    PROVAS {
        int id PK
        int referencia_id FK
        int numero_prova
        string status
        text motivo_ultima_alteracao
        string tabela_medidas_path
        string data_recebimento
        string tamanhos_recebidos
        text info_medidas
        string data_prova
        string time_qualidade
        text checklist_qualidade
        text comentarios_qualidade
        text obs_qualidade
        string time_estilo
        text checklist_estilo
        text comentarios_estilo
        text obs_estilo
        string time_modelagem
        text checklist_modelagem
        text comentarios_modelagem
        text obs_modelagem
        string data_lacre
        string numero_lacre
        text info_adicionais
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    FOTOS {
        int id PK
        int prova_id FK
        string contexto
        string tamanho
        string file_path
    }

    AUDIT_LOGS {
        int id PK
        int usuario_id FK
        string usuario_nome
        string acao
        string entidade_tipo
        int entidade_id
        string entidade_descricao
        text detalhes
        string ip_address
        string user_agent
        datetime created_at
    }
```

#### 4.2 Descrição das Entidades

**Usuario (usuarios):**
- Tabela de usuários do sistema
- Autenticação via Flask-Login (UserMixin)
- Suporte a senhas temporárias
- Sistema de reset de senha com token
- Auditoria de último acesso

**Relatorio (relatorios):**
- Agrupa referências por coleção/temporada
- Código único gerado (REL-2025-001)
- Suporta anexos: PPT, imagem do produto, ficha técnica
- Status geral calculado pela última prova

**Referencia (referencias):**
- Referência de produto dentro de um relatório
- Categorias: baby, kids, teen, adulto
- Informações de fornecedor e composição
- Relacionamento 1:N com provas

**ProvaModelagem (provas):**
- Prova de modelagem de uma referência
- Número sequencial (1ª prova, 2ª prova, etc.)
- Status: EM ANDAMENTO, APROVADA, REPROVADA, COMITÊ
- Avaliações separadas: Qualidade, Estilo, Modelagem
- Checklists dinâmicos (vírgula-separados)
- Sistema de lacre

**FotoProva (fotos):**
- Fotos anexadas às provas
- Contextos: desenho, qualidade, estilo, modelagem, amostra, prova_modelo
- Suporte a fotos por tamanho (para amostra/prova_modelo)

**AuditLog (audit_logs):**
- Log completo de ações do sistema
- Rastreamento de IP e User-Agent
- Detalhes em JSON
- Relacionamento com usuário

#### 4.3 Relacionamentos

- **CASCADE DELETE:** Ao excluir um relatório, todas as referências, provas e fotos são excluídas automaticamente
- **LAZY LOADING:** Relacionamentos carregados sob demanda
- **INDEXES:** username, email, relatorio_id, referencia_id, prova_id, usuario_id, acao, created_at

---

### 5. Rotas Principais (app.py)

#### 5.1 Dashboard e Navegação

| Rota | Método | Auth | Descrição |
|------|--------|------|-----------|
| `/` | GET | Sim | Dashboard com estatísticas e lista de relatórios |
| `/favicon.ico` | GET | Não | Ícone do site |
| `/uploads/<filename>` | GET | Sim | Serve arquivos de upload |

**Dashboard - Estatísticas Exibidas:**

```python
# Totais
- total_relatorios
- total_referencias
- total_provas

# Por Status
- provas_aprovadas
- provas_reprovadas
- provas_em_andamento
- provas_comite

# Métricas
- taxa_aprovacao (%)
- taxa_retrabalho (%)
- media_provas_por_referencia
- relatorios_recentes (últimos 30 dias)

# Insights Inteligentes
- Performance (taxa > 80% = success)
- Retrabalho (taxa > 30% = warning)
- Produtividade (relatórios recentes)
- Provas pendentes
```

**Paginação:**
- 20 relatórios por página
- Ordenação: mais recentes primeiro

#### 5.2 Gerenciamento de Relatórios

| Rota | Método | Auth | Descrição |
|------|--------|------|-----------|
| `/novo` | GET, POST | Sim | Cria novo relatório |
| `/relatorio/<id>` | GET | Sim | Detalhes do relatório |
| `/relatorio/<id>/editar` | GET, POST | Sim | Edita relatório existente |
| `/relatorio/<id>/excluir` | POST | Sim | Exclui relatório (cascade) |
| `/relatorio/<id>/pdf` | GET | Sim | Gera PDF do relatório |

**Fluxo de Criação de Relatório:**

```mermaid
sequenceDiagram
    participant U as Usuário
    participant A as app.py
    participant DB as Database
    participant FS as File System

    U->>A: POST /novo (form-data)
    A->>FS: save_file(ppt, imagem, ficha)
    FS-->>A: filenames
    A->>DB: INSERT Relatorio
    DB-->>A: relatorio.id

    loop Para cada categoria (baby/kids/teen/adulto)
        alt Categoria preenchida
            A->>DB: INSERT Referencia
            DB-->>A: referencia.id
            A->>FS: save_file(tabela_medidas)
            A->>DB: INSERT Prova (numero=1)
            DB-->>A: prova.id
            loop Para cada contexto de foto
                A->>FS: save_file(foto)
                A->>DB: INSERT Foto
            end
        end
    end

    A->>DB: COMMIT
    A->>A: registrar_log(criar, relatorio)
    A-->>U: Redirect /dashboard
```

**Campos do Formulário:**

Relatório:
- descricao_geral (required)
- colecao
- ppt (file)
- imagem_produto (file)
- ficha_tecnica (file)

Por Referência:
- ref_{tipo} (número da referência)
- origem_{tipo}
- fornecedor_{tipo}
- materia_prima_{tipo}
- composicao_{tipo}
- gramatura_{tipo}
- aviamentos_{tipo}

Por Prova:
- tabela_medidas_{tipo} (file)
- data_recebimento_{tipo}
- tamanhos_recebidos_{tipo} (multiple)
- info_medidas_{tipo}
- data_prova_{tipo}
- time_qualidade_{tipo}
- checklist_qualidade_{tipo} (multiple)
- comentarios_qualidade_{tipo}
- obs_qualidade_{tipo}
- time_estilo_{tipo}
- checklist_estilo_{tipo} (multiple)
- comentarios_estilo_{tipo}
- obs_estilo_{tipo}
- time_modelagem_{tipo}
- checklist_modelagem_{tipo} (multiple)
- comentarios_modelagem_{tipo}
- obs_modelagem_{tipo}
- data_lacre_{tipo}
- numero_lacre_{tipo}
- info_adicionais_{tipo}

Fotos:
- fotos_desenho_{tipo}[] (multiple files)
- fotos_qualidade_{tipo}[] (multiple files)
- fotos_estilo_{tipo}[] (multiple files)
- fotos_modelagem_{tipo}[] (multiple files)
- fotos_amostra_{tipo}_{tamanho}[] (por tamanho)
- fotos_prova_modelo_{tipo}_{tamanho}[] (por tamanho)

#### 5.3 Gerenciamento de Provas

| Rota | Método | Auth | Descrição |
|------|--------|------|-----------|
| `/referencia/<id>/nova_prova` | GET, POST | Sim | Adiciona nova prova a referência |
| `/prova/atualizar_status` | POST | Sim | Atualiza status da prova |

**Status da Prova:**
- EM ANDAMENTO (padrão)
- APROVADA
- REPROVADA
- COMITÊ

**Atualização de Status:**

```python
# POST /prova/atualizar_status
{
    prova_id: int,
    novo_status: string,
    motivo: string (opcional)
}
```

#### 5.4 Exportação de Dados

| Rota | Método | Auth | Descrição |
|------|--------|------|-----------|
| `/exportar/excel` | GET | Sim | Exporta lista de relatórios (Excel) |
| `/relatorio/<id>/excel` | GET | Sim | Exporta detalhes de relatório (Excel) |
| `/importar/excel` | POST | Sim | Importa relatórios de Excel |

**Estrutura do Excel Exportado (Lista):**

Colunas:
- ID
- Código
- Coleção
- Descrição
- Temporada
- Ano
- Status Geral
- Referências
- Data Criação
- Última Atualização

**Estrutura do Excel Exportado (Detalhes):**

Abas:
1. **Informações Gerais:** Dados do relatório
2. **Referências:** Lista de referências com detalhes
3. **Provas:** Lista de provas com avaliações

#### 5.5 Analytics

| Rota | Método | Auth | Descrição |
|------|--------|------|-----------|
| `/analytics` | GET | Sim | Página de relatórios e gráficos |
| `/api/analytics/charts` | GET | Sim | API JSON com dados dos gráficos |
| `/analytics/exportar` | GET | Sim | Exporta dados filtrados (Excel) |

**Filtros Disponíveis:**

- status (EM ANDAMENTO, APROVADA, REPROVADA, COMITÊ)
- categoria (baby, kids, teen, adulto)
- colecao
- fornecedor
- referencia (busca parcial)
- data_inicio (YYYY-MM-DD)
- data_fim (YYYY-MM-DD)

**Estatísticas Calculadas:**

```python
# Gerais (sem filtros)
total_relatorios
total_referencias
total_provas
provas_aprovadas
provas_reprovadas
provas_em_andamento
provas_comite
taxa_aprovacao (%)
taxa_reprovacao (%)
taxa_retrabalho (%)

# Filtradas
total_filtrado
filtrado_aprovadas
filtrado_reprovadas
filtrado_em_andamento
filtrado_comite
taxa_aprovacao_filtrada (%)
```

**Dados para Gráficos (API JSON):**

```json
{
  "success": true,
  "data": {
    "statusChart": {
      "labels": ["APROVADA", "REPROVADA", ...],
      "values": [120, 30, ...]
    },
    "suppliersChart": {
      "suppliers": ["Fornecedor A", ...],
      "counts": [50, 40, ...]
    },
    "timelineChart": {
      "months": ["Jan", "Fev", ...],
      "counts": [10, 15, ...]
    },
    "categoryChart": {
      "categories": ["baby", "kids", ...],
      "counts": [80, 120, ...]
    },
    "sparklines": {
      "relatorios": [5, 8, 12, ...],
      "aprovacao": [75.5, 80.2, ...]
    },
    "mixedChart": {
      "labels": ["Jan", "Fev", ...],
      "totalProvas": [20, 25, ...],
      "taxaAprovacao": [78.5, 82.0, ...]
    },
    "colecoesChart": {
      "labels": ["Verão 2025", ...],
      "counts": [30, 25, ...]
    }
  }
}
```

**Insights Inteligentes:**

Sistema de insights baseado em regras:

```python
# Taxa de Aprovação
>= 80%: Success (Excelente Performance)
60-79%: Warning (Performance Moderada)
< 60%: Danger (Atenção Necessária)

# Retrabalho
> 30%: Warning (Alto Retrabalho)
1-30%: Info (Retrabalho Controlado)

# Provas Pendentes
> 10: Info (Muitas provas aguardando)

# Comitê
> 0: Primary (Provas para comitê)

# Top Fornecedor
Secondary: Fornecedor mais ativo
```

#### 5.6 Logs de Auditoria

| Rota | Método | Auth | Descrição |
|------|--------|------|-----------|
| `/logs` | GET | Sim (Admin) | Visualização de logs de auditoria |

**Filtros:**
- acao (criar, editar, excluir, login, etc.)
- usuario (busca parcial)
- entidade (relatorio, prova, referencia, usuario)

**Paginação:**
- 50 logs por página (configurável)
- Ordenação: mais recentes primeiro

**Estatísticas:**
- Total de logs
- Ações únicas (contagem por tipo)
- Top 10 usuários ativos

#### 5.7 Comandos CLI

**Criar Usuário Admin:**

```bash
flask create-admin
# Cria: admin / admin123 (senha temporária)
```

**Resetar Senhas:**

```bash
flask reset-all-passwords
# Reseta todas as senhas para: mudar123 (temporária)
```

---

### 6. utils.py - Utilitários

**Funções Principais:**

#### 6.1 save_file(file_storage, max_size_mb=16)

Salva arquivo com validações de segurança:

```python
Validações:
1. Verificar se arquivo existe
2. Validar extensão permitida
3. Sanitizar nome (secure_filename)
4. Verificar tamanho
5. Gerar nome único se existir
6. Validar imagens (PIL.Image.verify)

Retorna: filename ou None
```

#### 6.2 delete_file(filename)

Deleta arquivo do sistema:

```python
- Remove arquivo de UPLOAD_FOLDER
- Trata exceções silenciosamente
- Retorna bool (sucesso/falha)
```

#### 6.3 get_file_size_mb(filename)

Retorna tamanho do arquivo em MB.

#### 6.4 create_thumbnail(filename, size=(150,150))

Cria miniatura de imagem:

```python
- Usa PIL/Pillow
- Formato: {nome}_thumb{ext}
- Qualidade: 85
- Otimizado
```

---

### 7. excel_export.py - Exportação Excel

**Biblioteca:** openpyxl

#### 7.1 export_relatorios_to_excel(relatorios_data)

Exporta lista de relatórios:

```python
Colunas:
- ID, Código, Coleção, Descrição
- Temporada, Ano, Status Geral
- Referências, Data Criação, Última Atualização

Estilo:
- Header: Branco em fundo magenta (#e6007e)
- Auto-ajuste de largura de colunas
- Máximo 50 caracteres por coluna
```

#### 7.2 export_detalhes_to_excel(relatorio, referencias)

Exporta detalhes completos:

```python
Abas:
1. Informações Gerais
   - Campo / Valor
2. Referências
   - Todas as colunas de referências
3. Provas
   - Todas as colunas de provas
   - Avaliações completas
```

---

### 8. security.py - Segurança

#### 8.1 Geração de SECRET_KEY

```python
generate_secret_key()
# Gera 64 caracteres hexadecimais (secrets.token_hex(32))

save_secret_key_to_env()
# Salva em .env automaticamente
```

#### 8.2 InputValidator

Validação de inputs para prevenir XSS:

```python
DANGEROUS_PATTERNS = [
    '<script', 'javascript:', 'on\w+=',
    '<iframe', '<object', '<embed',
    'eval(', 'expression('
]

Métodos:
- sanitize_string(value, max_length)
- sanitize_filename(filename)
- validate_email(email)
- validate_username(username)
```

#### 8.3 RateLimiter

Rate limiting baseado em memória:

```python
@rate_limit(max_requests=60, window=60)
def minha_rota():
    ...

# 60 requisições por 60 segundos por IP
# Cleanup automático a cada 5 minutos
# Retorna 429 Too Many Requests se exceder
```

#### 8.4 SecurityHeaders

Headers de segurança adicionados automaticamente:

```http
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: (configurado)
Permissions-Policy: (restritivo)
```

**CSP Configurado:**

```
default-src 'self';
script-src 'self' 'unsafe-inline' cdn.jsdelivr.net cdnjs.cloudflare.com;
style-src 'self' 'unsafe-inline' cdn.jsdelivr.net fonts.googleapis.com;
font-src 'self' https: data:;
img-src 'self' data: https:;
connect-src 'self' cdn.jsdelivr.net;
frame-ancestors 'self';
base-uri 'self';
form-action 'self';
```

#### 8.5 FileUploadValidator

Validação de uploads:

```python
ALLOWED_EXTENSIONS = {
    'images': {'png', 'jpg', 'jpeg', 'gif'},
    'documents': {'pdf', 'xlsx', 'xls', 'ppt', 'pptx', 'doc', 'docx'}
}

MAGIC_NUMBERS = {
    'png': b'\x89PNG\r\n\x1a\n',
    'jpg': b'\xff\xd8\xff',
    'gif': b'GIF8',
    'pdf': b'%PDF'
}

MAX_SIZES = {
    'images': 10MB,
    'documents': 50MB
}
```

#### 8.6 PasswordValidator

Validação de força de senha:

```python
MIN_LENGTH = 8
Requer:
- Letra minúscula
- Letra maiúscula
- Número
- Caractere especial (!@#$%^&*(),.?":{}|<>)
```

---

### 9. error_handlers.py - Tratamento de Erros

**Erros Tratados:**

| Código | Handler | Descrição |
|--------|---------|-----------|
| 400 | bad_request | Requisição inválida |
| 403 | forbidden | Acesso proibido |
| 404 | not_found | Recurso não encontrado |
| 429 | too_many_requests | Rate limit excedido |
| 500 | internal_server_error | Erro interno |

**Comportamento:**

```python
# Requisições JSON
if request.accept_mimetypes.accept_json:
    return jsonify(error="mensagem"), codigo

# Requisições HTML
return render_template('errors/{codigo}.html', error=error), codigo
```

**Logging:**

- 400: Warning (URL + erro)
- 403: Warning (URL + IP)
- 404: Info (exceto paths conhecidos)
- 429: Warning (IP + URL)
- 500: Error (com stack trace)

**Paths Ignorados no 404:**

```python
ignored_paths = [
    '/.well-known/appspecific/com.chrome.devtools.json',
    '/apple-touch-icon',
    '/apple-touch-icon-precomposed.png'
]
```

---

### 10. audit_helpers.py - Sistema de Auditoria

**Constantes Definidas:**

```python
# Ações
AuditAction:
    LOGIN, LOGOUT, LOGIN_FAILED
    CREATE, UPDATE, DELETE, VIEW
    APPROVE, REJECT, SUBMIT
    PASSWORD_RESET, PASSWORD_CHANGE, ROLE_CHANGE
    USER_ACTIVATE, USER_DEACTIVATE
    FILE_UPLOAD, FILE_DELETE, FILE_DOWNLOAD
    EXPORT_PDF, EXPORT_CSV

# Entidades
AuditEntity:
    USUARIO, RELATORIO, REFERENCIA, PROVA, FOTO, SISTEMA

# Categorias
AuditCategory:
    AUTENTICACAO, USUARIOS, RELATORIOS, PROVAS
    APROVACOES, ARQUIVOS, SISTEMA, EXPORTACOES

# Severidade
AuditSeverity:
    INFO, WARNING, CRITICAL
```

**Funções Principais:**

```python
registrar_log(acao, entidade, descricao, entidade_id, dados_antes, dados_depois)
log_login(usuario, sucesso)
log_logout(usuario)
log_criacao(entidade, entidade_id, descricao, dados)
log_atualizacao(entidade, entidade_id, descricao, dados_antes, dados_depois)
log_exclusao(entidade, entidade_id, descricao, dados)
log_aprovacao(prova_id, status, motivo)
log_mudanca_role(usuario_id, role_antigo, role_novo)
log_reset_senha(usuario_id, usuario_nome)
log_exportacao(tipo, entidade, entidade_id)
```

**Helpers de Exibição:**

```python
get_acao_display(acao) -> string amigável
get_categoria_display(categoria) -> string amigável
get_severidade_badge(severidade) -> classe CSS Bootstrap
```

---

### 11. config.py - Configurações

**Classe Base: Config**

```python
# Flask
SECRET_KEY: env ou fallback
DEBUG: env (default False)

# Security
SESSION_COOKIE_SECURE: False (True em HTTPS)
SESSION_COOKIE_HTTPONLY: True
SESSION_COOKIE_SAMESITE: Lax
PERMANENT_SESSION_LIFETIME: 43200 (12 horas)
WTF_CSRF_ENABLED: True

# Database
SQLALCHEMY_DATABASE_URI: env ou sqlite:///instance/provas.db
SQLALCHEMY_TRACK_MODIFICATIONS: False
SQLALCHEMY_ENGINE_OPTIONS:
    pool_size: 10
    pool_recycle: 3600
    pool_pre_ping: True

# Upload
UPLOAD_FOLDER: uploads/
PDF_FOLDER: relatorios_pdf/
MAX_CONTENT_LENGTH: 16MB (env configurável)

# Extensões Permitidas
ALLOWED_EXTENSIONS: png,jpg,jpeg,gif,pdf,xlsx,xls,ppt,pptx (env)
IMAGE_EXTENSIONS: png,jpg,jpeg,gif
DOCUMENT_EXTENSIONS: pdf,xlsx,xls,ppt,pptx

# Logging
LOG_LEVEL: INFO (env)
LOG_FILE: None (env)
```

**Ambientes:**

```python
DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/provas.db'

ProductionConfig(Config):
    DEBUG = False
    Validações obrigatórias:
        - SECRET_KEY != fallback
        - DATABASE_URL configurada
```

**Funções Utilitárias:**

```python
allowed_file(filename) -> bool
get_file_extension(filename) -> string
is_image(filename) -> bool
is_document(filename) -> bool
```

---

### 12. db.py - Inicialização do Banco

**Função Principal:**

```python
def init_app(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()  # Cria todas as tabelas

        # Criar admin padrão se não existir
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
```

**Comportamento:**

- Executado na inicialização da aplicação
- Cria estrutura do banco automaticamente
- Cria usuário admin padrão
- Não sobrescreve dados existentes

---

## Fluxos Principais

### Fluxo 1: Login

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Flask
    participant Database

    User->>Browser: Acessa /
    Browser->>Flask: GET /
    Flask->>Browser: Redirect /login (401)
    Browser->>Flask: GET /login
    Flask->>Browser: Render login.html
    User->>Browser: Preenche credenciais
    Browser->>Flask: POST /login
    Flask->>Database: SELECT * FROM usuarios WHERE username=?
    Database->>Flask: User object
    Flask->>Flask: check_password_hash()
    alt Autenticado
        Flask->>Database: INSERT audit_log (LOGIN)
        Flask->>Browser: Set-Cookie (session)
        Browser->>Flask: GET /
        Flask->>Database: SELECT relatórios (paginado)
        Flask->>Browser: Render dashboard.html
    else Falha
        Flask->>Database: INSERT audit_log (LOGIN_FAILED)
        Flask->>Browser: Redirect /login (error)
    end
```

### Fluxo 2: Criar Relatório

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Flask
    participant Database
    participant FileSystem

    User->>Browser: Clica "Novo Relatório"
    Browser->>Flask: GET /novo
    Flask->>Browser: Render novo_relatorio.html
    User->>Browser: Preenche formulário + uploads
    Browser->>Flask: POST /novo (multipart/form-data)

    Flask->>Flask: validate inputs
    Flask->>FileSystem: save_file(ppt)
    FileSystem-->>Flask: ppt_filename
    Flask->>FileSystem: save_file(imagem_produto)
    Flask->>FileSystem: save_file(ficha_tecnica)

    Flask->>Database: BEGIN TRANSACTION
    Flask->>Database: INSERT relatorios
    Database-->>Flask: relatorio.id

    loop Para cada categoria
        Flask->>Database: INSERT referencias
        Database-->>Flask: referencia.id
        Flask->>FileSystem: save_file(tabela_medidas)
        Flask->>Database: INSERT provas
        Database-->>Flask: prova.id

        loop Para cada foto
            Flask->>FileSystem: save_file(foto)
            Flask->>Database: INSERT fotos
        end
    end

    Flask->>Database: COMMIT
    Flask->>Database: INSERT audit_log (CREATE)
    Flask->>Browser: Redirect /dashboard (success)
```

### Fluxo 3: Adicionar Nova Prova

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Flask
    participant Database

    User->>Browser: Clica "Nova Prova" em referência
    Browser->>Flask: GET /referencia/<id>/nova_prova
    Flask->>Database: SELECT referencia
    Flask->>Database: SELECT MAX(numero_prova)
    Flask->>Browser: Render nova_prova.html (numero = ultimo + 1)
    User->>Browser: Preenche formulário
    Browser->>Flask: POST /referencia/<id>/nova_prova

    Flask->>Database: BEGIN TRANSACTION
    Flask->>Database: INSERT provas (numero_prova++)
    Flask->>Database: INSERT fotos
    Flask->>Database: COMMIT
    Flask->>Database: INSERT audit_log (CREATE)
    Flask->>Browser: Redirect /relatorio/<id> (success)
```

### Fluxo 4: Atualizar Status da Prova

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Flask
    participant Database

    User->>Browser: Abre modal "Atualizar Status"
    User->>Browser: Seleciona novo status + motivo
    Browser->>Flask: POST /prova/atualizar_status
    Flask->>Database: SELECT prova
    Flask->>Database: UPDATE provas SET status=?, motivo=?
    Flask->>Database: INSERT audit_log (UPDATE)
    Flask->>Browser: Redirect /relatorio/<id> (success)
```

### Fluxo 5: Exportar Excel

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Flask
    participant Database
    participant Excel

    User->>Browser: Clica "Exportar Excel"
    Browser->>Flask: GET /exportar/excel
    Flask->>Database: SELECT * FROM relatorios
    Flask->>Database: SELECT * FROM referencias
    Flask->>Database: SELECT * FROM provas
    Flask->>Excel: Criar workbook
    Excel->>Excel: Formatar (headers, cores, ajustes)
    Excel-->>Flask: arquivo.xlsx
    Flask->>FileSystem: Salvar em PDF_FOLDER
    Flask->>Database: INSERT audit_log (EXPORT_CSV)
    Flask->>Browser: Download arquivo.xlsx
```

### Fluxo 6: Visualizar Analytics

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Flask
    participant Database

    User->>Browser: Acessa /analytics
    Browser->>Flask: GET /analytics
    Flask->>Database: Queries agregadas (estatísticas)
    Flask->>Flask: Calcular insights
    Flask->>Browser: Render analytics.html (servidor)
    Browser->>Browser: Render página
    Browser->>Flask: GET /api/analytics/charts
    Flask->>Database: Queries para gráficos
    Flask->>Browser: JSON com dados
    Browser->>Browser: Renderizar gráficos (Chart.js)
```

---

## Sistema de Permissões

### Matriz de Permissões

| Ação | Usuário | Gestor | Admin |
|------|---------|--------|-------|
| Login/Logout | Sim | Sim | Sim |
| Ver Dashboard | Sim | Sim | Sim |
| Criar Relatório | Sim | Sim | Sim |
| Editar Relatório | Proprietário | Todos | Todos |
| Excluir Relatório | Não | Proprietário | Todos |
| Adicionar Prova | Sim | Sim | Sim |
| Atualizar Status | Sim | Sim | Sim |
| Ver Analytics | Sim | Sim | Sim |
| Exportar Dados | Sim | Sim | Sim |
| Gerenciar Usuários | Não | Não | Sim |
| Ver Logs | Não | Não | Sim |
| Alterar Senha Própria | Sim | Sim | Sim |
| Resetar Senha Outros | Não | Não | Sim |

### Decorators de Autorização

```python
@login_required  # Flask-Login
# Redireciona para /login se não autenticado

@admin_required  # Customizado (admin.py)
# Verifica is_admin OU role == 'admin'
# Retorna 403 se não for admin
```

---

## Validações e Regras de Negócio

### Validações de Senha

```python
Requisitos:
- Mínimo 8 caracteres
- 1 letra maiúscula [A-Z]
- 1 letra minúscula [a-z]
- 1 número [0-9]
- 1 caractere especial [@$!%*?&]

Aplicado em:
- Criação de usuário
- Alteração de senha
- Reset de senha
- Definição manual de senha (admin)
```

### Validações de Upload

```python
Extensões permitidas:
- Imagens: png, jpg, jpeg, gif
- Documentos: pdf, xlsx, xls, ppt, pptx

Tamanho máximo:
- Default: 16MB (MAX_CONTENT_LENGTH)
- Configurável via save_file(max_size_mb)

Validações aplicadas:
1. Extensão permitida (config.allowed_file)
2. Sanitização de nome (secure_filename)
3. Tamanho do arquivo
4. Validação de imagem real (PIL.Image.verify)
5. Magic numbers (FileUploadValidator)
6. Nome único (adiciona _1, _2 se existir)
```

### Validações de Formulário

```python
# Campos obrigatórios
Relatório:
    - descricao_geral (required)

Referência:
    - numero_ref (required)
    - tipo_categoria (required)

Prova:
    - numero_prova (required)
    - status (default: EM ANDAMENTO)

# Sanitização
InputValidator.sanitize_string(value, max_length)
# Remove: <script>, javascript:, on*=, etc.
```

### Regras de Negócio

**Numeração de Provas:**

```python
# Sequencial por referência
# Começa em 1
# Incrementa a cada nova prova

Exemplo:
Referência #123:
    1ª Prova (numero_prova=1)
    2ª Prova (numero_prova=2)
    3ª Prova (numero_prova=3)
```

**Status da Prova:**

```python
Fluxo típico:
EM ANDAMENTO -> APROVADA
EM ANDAMENTO -> REPROVADA -> Nova Prova (EM ANDAMENTO)
EM ANDAMENTO -> COMITÊ -> APROVADA/REPROVADA

# Status é atualizado individualmente
# Motivo da alteração é registrado
```

**Status Geral do Relatório:**

```python
# Calculado automaticamente
# Baseado na última prova de qualquer referência
# Exibido no dashboard

status_atual = última_prova.status if última_prova else 'Novo'
```

**Exclusão em Cascata:**

```python
DELETE Relatorio
    -> DELETE Referencia (CASCADE)
        -> DELETE Prova (CASCADE)
            -> DELETE Foto (CASCADE)

# Arquivos físicos também são removidos
# Log de auditoria registra exclusão
```

---

## Segurança Implementada

### 1. Autenticação

- **Flask-Login:** Gerenciamento de sessões
- **Werkzeug:** Hashing de senhas (pbkdf2:sha256)
- **Senhas Fortes:** Validação obrigatória
- **Senhas Temporárias:** Flag de primeira troca
- **Reset Seguro:** Token de 32 bytes (expiração 24h)

### 2. Autorização

- **Role-Based Access Control (RBAC):** admin, gestor, usuario
- **Decorators:** @login_required, @admin_required
- **Verificação de Propriedade:** Editar apenas próprios registros (exceto admin)

### 3. Proteção de Dados

- **CSRF Protection:** WTF_CSRF_ENABLED
- **Session Security:**
  - HttpOnly cookies
  - SameSite=Lax
  - Secure (em HTTPS)
  - Timeout de 12 horas

### 4. Validação de Inputs

- **XSS Prevention:** InputValidator remove scripts
- **SQL Injection:** SQLAlchemy ORM (parametrização automática)
- **Path Traversal:** secure_filename + basename
- **File Upload:** Validação de extensão, tamanho e magic numbers

### 5. Headers de Segurança

```http
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: (restritivo)
Permissions-Policy: (restritivo)
```

### 6. Rate Limiting

- **Baseado em IP e endpoint**
- **Padrão:** 60 requisições por 60 segundos
- **Cleanup:** Automático a cada 5 minutos
- **Response:** 429 Too Many Requests

### 7. Logging e Auditoria

- **Todas as ações importantes são logadas**
- **Captura:** IP, User-Agent, timestamp
- **Rastreamento:** Usuário, ação, entidade, detalhes
- **Retenção:** Permanente (sem limpeza automática)

### 8. Tratamento de Erros

- **Sem exposição de stack traces**
- **Mensagens genéricas para usuários**
- **Logging detalhado para admin**
- **Templates customizados (400, 403, 404, 429, 500)**

---

## Performance e Otimização

### 1. Compressão HTTP

```python
Flask-Compress (GZIP):
- Nível 6 (balanceado)
- Mínimo 500 bytes
- MIME types: HTML, CSS, JS, JSON, XML, SVG
```

### 2. Cache Headers

```python
/static/: 1 ano (immutable)
/uploads/: 30 dias
HTML: no-cache
JSON: 5 minutos
```

### 3. Database

```python
SQLAlchemy Engine Options:
- pool_size: 10
- pool_recycle: 3600 (1 hora)
- pool_pre_ping: True (validação)

Indexes:
- username, email (usuarios)
- codigo (relatorios)
- relatorio_id (referencias)
- referencia_id (provas)
- prova_id (fotos)
- usuario_id, acao, created_at (audit_logs)
```

### 4. Lazy Loading

```python
# Relacionamentos carregados sob demanda
db.relationship('Referencia', lazy=True)
```

### 5. Paginação

```python
# Dashboard
paginate(page=1, per_page=20)

# Logs de Auditoria
paginate(page=1, per_page=50)
```

### 6. Queries Otimizadas

```python
# Dashboard: Query única com JOIN
Prova.query.join(Referencia).filter(...)

# Analytics: Agregações no banco
db.session.query(
    Prova.status,
    db.func.count(Prova.id)
).group_by(Prova.status)
```

---

## Dependências (requirements.txt)

```
Flask==3.0.0                # Framework web
Flask-SQLAlchemy==3.1.1     # ORM
Flask-Login==0.6.3          # Autenticação
Flask-Compress==1.14        # Compressão HTTP
Werkzeug==3.0.1             # WSGI utilities
xhtml2pdf==0.2.11           # Geração de PDF (desabilitado)
python-dotenv==1.0.0        # Variáveis de ambiente
pyodbc==5.0.1               # Driver SQL Server (opcional)
wfastcgi==3.0.0             # IIS deployment (opcional)
openpyxl==3.1.2             # Exportação Excel
Pillow==10.1.0              # Processamento de imagens
requests==2.31.0            # HTTP client
gunicorn==21.2.0            # WSGI server (produção)
psycopg2-binary==2.9.9      # Driver PostgreSQL
```

---

## Estrutura de Diretórios

```
prova_modelagem_app/
├── app.py                      # Aplicação principal
├── auth.py                     # Autenticação
├── admin.py                    # Painel admin
├── models.py                   # Modelos ORM
├── config.py                   # Configurações
├── db.py                       # Init DB
├── utils.py                    # Utilitários
├── security.py                 # Segurança
├── excel_export.py             # Exportação
├── error_handlers.py           # Tratamento de erros
├── audit_helpers.py            # Auditoria
├── requirements.txt            # Dependências
├── gunicorn_config.py          # Config Gunicorn
├── wsgi.py                     # WSGI entry point
│
├── instance/
│   └── provas.db              # SQLite (dev)
│
├── uploads/                   # Uploads de usuários
│   ├── fotos/
│   ├── documentos/
│   └── tabelas/
│
├── relatorios_pdf/            # PDFs e exportações
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── novo_relatorio.html
│   ├── editar_relatorio.html
│   ├── detalhes_relatorio.html
│   ├── nova_prova.html
│   ├── analytics.html
│   ├── logs.html
│   ├── alterar_senha.html
│   ├── esqueci_senha.html
│   ├── reset_senha.html
│   ├── relatorio_pdf.html     # Template PDF
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── users.html
│   │   ├── create_user.html
│   │   ├── edit_user.html
│   │   └── change_password.html
│   └── errors/
│       ├── 400.html
│       ├── 403.html
│       ├── 404.html
│       ├── 429.html
│       └── 500.html
│
├── static/
│   ├── css/
│   │   ├── custom.css
│   │   ├── components.css
│   │   ├── design-system.css
│   │   ├── mobile.css
│   │   ├── accessibility.css
│   │   └── ...
│   ├── js/
│   │   ├── app.js
│   │   ├── app-init.js
│   │   ├── charts-config.js
│   │   ├── wizard.js
│   │   └── ...
│   └── img/
│
└── logs/                      # Logs da aplicação (opcional)
    └── app.log
```

---

## Variáveis de Ambiente (.env)

```bash
# Flask
SECRET_KEY=<gerado automaticamente>
FLASK_DEBUG=False
FLASK_ENV=production

# Database
DATABASE_URL=postgresql://user:pass@localhost/provas

# Upload
MAX_CONTENT_LENGTH=16777216  # 16MB em bytes
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,pdf,xlsx,xls,ppt,pptx

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/app.log

# Server
HOST=0.0.0.0
PORT=5000
```

---

## Comandos de Execução

### Desenvolvimento

```bash
# Instalar dependências
pip install -r requirements.txt

# Criar banco de dados
flask shell
>>> from db import init_app
>>> init_app(app)
>>> exit()

# Executar
python app.py
# ou
flask run --host=0.0.0.0 --port=5000
```

### Produção

```bash
# Usar Gunicorn
gunicorn -c gunicorn_config.py wsgi:app

# Configuração Gunicorn (gunicorn_config.py)
workers = (2 * cpu_count) + 1
bind = "0.0.0.0:5000"
worker_class = "sync"
timeout = 120
```

### Comandos CLI

```bash
# Criar admin
flask create-admin

# Resetar senhas
flask reset-all-passwords

# Acessar shell
flask shell
```

---

## Mapa Completo de Rotas

### Autenticação (auth_bp)

| Rota | Método | Auth | Descrição |
|------|--------|------|-----------|
| `/login` | GET, POST | Não | Login de usuários |
| `/logout` | GET | Sim | Logout |
| `/alterar-senha` | GET, POST | Sim | Alterar própria senha |
| `/esqueci-senha` | GET, POST | Não | Solicitar reset |
| `/reset-senha/<token>` | GET, POST | Não | Reset via token |

### Administração (admin_bp)

| Rota | Método | Auth | Descrição |
|------|--------|------|-----------|
| `/admin/` | GET | Admin | Dashboard admin |
| `/admin/users` | GET | Admin | Lista usuários |
| `/admin/users/create` | GET, POST | Admin | Criar usuário |
| `/admin/users/edit/<id>` | GET, POST | Admin | Editar usuário |
| `/admin/users/set_password/<id>` | POST | Admin | Definir senha |
| `/admin/users/reset_password/<id>` | POST | Admin | Gerar senha |
| `/admin/users/toggle_active/<id>` | POST | Admin | Ativar/desativar |
| `/admin/users/delete/<id>` | POST | Admin | Soft delete |
| `/admin/change-my-password` | GET, POST | Admin | Alterar senha |

### Aplicação Principal (app.py)

| Rota | Método | Auth | Descrição |
|------|--------|------|-----------|
| `/` | GET | Sim | Dashboard |
| `/favicon.ico` | GET | Não | Favicon |
| `/uploads/<filename>` | GET | Sim | Serve uploads |
| `/novo` | GET, POST | Sim | Novo relatório |
| `/relatorio/<id>` | GET | Sim | Detalhes |
| `/relatorio/<id>/editar` | GET, POST | Sim | Editar |
| `/relatorio/<id>/excluir` | POST | Sim | Excluir |
| `/relatorio/<id>/pdf` | GET | Sim | PDF |
| `/relatorio/<id>/excel` | GET | Sim | Excel detalhes |
| `/referencia/<id>/nova_prova` | GET, POST | Sim | Nova prova |
| `/prova/atualizar_status` | POST | Sim | Atualizar status |
| `/exportar/excel` | GET | Sim | Excel lista |
| `/importar/excel` | POST | Sim | Importar |
| `/analytics` | GET | Sim | Analytics página |
| `/api/analytics/charts` | GET | Sim | API gráficos |
| `/analytics/exportar` | GET | Sim | Exportar filtros |
| `/logs` | GET | Admin | Logs auditoria |

**Total:** 32 rotas públicas

---

## Diagrama de Sequência - Sistema Completo

```mermaid
sequenceDiagram
    participant U as Usuário
    participant B as Browser
    participant A as app.py
    participant Auth as auth.py
    participant Adm as admin.py
    participant DB as Database
    participant FS as FileSystem
    participant Aud as Auditoria

    Note over U,Aud: FASE 1: LOGIN
    U->>B: Acessa sistema
    B->>A: GET /
    A->>B: Redirect /login
    B->>Auth: GET /login
    Auth->>B: Render login.html
    U->>B: Credenciais
    B->>Auth: POST /login
    Auth->>DB: SELECT User
    Auth->>Auth: Validar senha
    Auth->>Aud: log_login(sucesso)
    Auth->>B: Set session + Redirect /

    Note over U,Aud: FASE 2: DASHBOARD
    B->>A: GET /
    A->>DB: SELECT Relatorios (paginado)
    A->>DB: Queries de estatísticas
    A->>A: Calcular insights
    A->>B: Render dashboard.html

    Note over U,Aud: FASE 3: CRIAR RELATÓRIO
    U->>B: Clica "Novo"
    B->>A: GET /novo
    A->>B: Render form
    U->>B: Preenche dados + uploads
    B->>A: POST /novo (multipart)
    A->>FS: Save arquivos
    A->>DB: BEGIN TRANSACTION
    A->>DB: INSERT Relatorio
    loop Cada categoria
        A->>DB: INSERT Referencia
        A->>DB: INSERT Prova
        loop Fotos
            A->>DB: INSERT Foto
        end
    end
    A->>DB: COMMIT
    A->>Aud: registrar_log(CREATE)
    A->>B: Redirect / (success)

    Note over U,Aud: FASE 4: ADICIONAR PROVA
    U->>B: Clica "Nova Prova"
    B->>A: GET /referencia/<id>/nova_prova
    A->>DB: SELECT Referencia
    A->>DB: SELECT MAX(numero_prova)
    A->>B: Render form (numero++)
    U->>B: Preenche avaliações
    B->>A: POST /referencia/<id>/nova_prova
    A->>DB: INSERT Prova
    A->>FS: Save fotos
    A->>DB: INSERT Fotos
    A->>Aud: registrar_log(CREATE)
    A->>B: Redirect /relatorio/<id>

    Note over U,Aud: FASE 5: ATUALIZAR STATUS
    U->>B: Modal status
    B->>A: POST /prova/atualizar_status
    A->>DB: UPDATE Prova
    A->>Aud: registrar_log(UPDATE)
    A->>B: Redirect back

    Note over U,Aud: FASE 6: ANALYTICS
    U->>B: Clica "Analytics"
    B->>A: GET /analytics
    A->>DB: Queries agregadas
    A->>B: Render analytics.html
    B->>B: Inicializa Chart.js
    B->>A: GET /api/analytics/charts
    A->>DB: Queries para gráficos
    A->>B: JSON
    B->>B: Renderiza gráficos

    Note over U,Aud: FASE 7: ADMIN (se admin)
    U->>B: Clica "Admin"
    B->>Adm: GET /admin/users
    Adm->>Adm: Check @admin_required
    Adm->>DB: SELECT Users
    Adm->>B: Render users.html
    U->>B: Cria usuário
    B->>Adm: POST /admin/users/create
    Adm->>Adm: gerar_senha_aleatoria()
    Adm->>DB: INSERT User
    Adm->>Aud: log_criacao(USUARIO)
    Adm->>B: Redirect com senha
```

---

## Considerações Finais

### Pontos Fortes

1. **Arquitetura Modular:** Separação clara de responsabilidades
2. **Segurança Robusta:** Múltiplas camadas de proteção
3. **Auditoria Completa:** Rastreamento de todas as ações
4. **Performance Otimizada:** Cache, compressão, indexação
5. **Validações Abrangentes:** Inputs, uploads, senhas
6. **Exportação Rica:** PDF e Excel com formatação
7. **Analytics Detalhado:** Gráficos e insights inteligentes
8. **Sistema de Permissões:** RBAC implementado

### Melhorias Futuras

1. **Rate Limiting em Produção:** Migrar para Redis (flask-limiter)
2. **Celery para Tasks:** Geração de PDF assíncrona
3. **Testes Automatizados:** Unitários e de integração
4. **API RESTful Completa:** Documentada com Swagger
5. **Notificações por Email:** SMTP configurado
6. **Websockets:** Atualizações em tempo real
7. **Multi-tenancy:** Suporte a múltiplas empresas
8. **Backup Automático:** Agendamento de backups

### Observações Técnicas

- **Geração de PDF:** Atualmente desabilitada (xhtml2pdf comentado), usando WeasyPrint
- **Auditoria:** Logs armazenados permanentemente (considerar retenção)
- **SQLite em Dev:** Trocar para PostgreSQL em produção
- **Senha Padrão:** admin/admin123 (trocar após deploy)
- **HTTPS:** Habilitar SESSION_COOKIE_SECURE e HSTS

---

## Contatos e Documentação

**Desenvolvedor:** Sistema interno
**Versão:** 1.0.0
**Data:** Janeiro 2026
**Framework:** Flask 3.0.0
**Python:** 3.8+

**Documentação Adicional:**
- requirements.txt - Dependências
- gunicorn_config.py - Configuração de produção
- config.py - Configurações detalhadas
- models.py - Schema completo do banco

---

**FIM DA DOCUMENTAÇÃO**
