# 📐 Nomenclatura Padrão - Sistema Prova Modelagem

## 🎯 Objetivo

Estabelecer nomenclatura consistente, profissional e escalável para todo o sistema.

---

## 🌍 Idioma: **PORTUGUÊS (PT-BR)**

**Decisão**: Usar português para nomes de negócio (tabelas, campos de dados) e inglês para código técnico.

**Motivo**:
- ✅ Facilita comunicação com stakeholders brasileiros
- ✅ Campos do banco refletem termos do negócio real
- ✅ Manutenibilidade por equipe brasileira
- ✅ Código técnico em inglês (padrão internacional)

---

## 📊 BANCO DE DADOS

### **Convenção Geral**
- Tabelas: `snake_case` plural
- Campos: `snake_case` singular
- PKs: sempre `id`
- FKs: `{tabela}_id`
- Timestamps: `created_at`, `updated_at`, `deleted_at`
- Soft Delete: `is_active` (boolean)

---

### **TABELA 1: `usuarios`** (antes: `users`)

**Propósito**: Usuários do sistema

```sql
CREATE TABLE usuarios (
    id                  INT PRIMARY KEY IDENTITY(1,1),
    username            NVARCHAR(150) NOT NULL UNIQUE,
    password_hash       NVARCHAR(255) NOT NULL,
    email               NVARCHAR(255) UNIQUE,
    nome_completo       NVARCHAR(255),
    is_admin            BIT DEFAULT 0,
    is_active           BIT DEFAULT 1,
    ultimo_acesso       DATETIME,
    created_at          DATETIME DEFAULT GETDATE(),
    updated_at          DATETIME,

    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_is_active (is_active)
);
```

**Campos novos adicionados**:
- `email` - Para recuperação de senha/notificações
- `nome_completo` - Nome real do usuário
- `is_active` - Soft delete
- `ultimo_acesso` - Tracking de uso
- `updated_at` - Auditoria

---

### **TABELA 2: `relatorios`** (mantém)

**Propósito**: Relatórios de coleção

```sql
CREATE TABLE relatorios (
    id                  INT PRIMARY KEY IDENTITY(1,1),
    codigo              NVARCHAR(50) UNIQUE,              -- Código único (ex: REL-2025-001)
    descricao_geral     NVARCHAR(500) NOT NULL,
    colecao             NVARCHAR(200),
    temporada           NVARCHAR(50),                     -- Ex: "Verão 2025", "Inverno 2024"
    ano                 INT,
    ppt_path            NVARCHAR(500),
    status_geral        NVARCHAR(50) DEFAULT 'Em Andamento', -- Agregado de todas as provas
    is_active           BIT DEFAULT 1,
    created_by          INT,                              -- FK para usuarios
    created_at          DATETIME DEFAULT GETDATE(),
    updated_at          DATETIME,

    FOREIGN KEY (created_by) REFERENCES usuarios(id),
    INDEX idx_codigo (codigo),
    INDEX idx_colecao (colecao),
    INDEX idx_temporada (temporada),
    INDEX idx_status (status_geral),
    INDEX idx_is_active (is_active)
);
```

**Campos novos**:
- `codigo` - Código sequencial único
- `temporada` - Verão/Inverno + Ano
- `ano` - Para filtros e relatórios
- `status_geral` - Visão consolidada
- `created_by` - Rastreabilidade

---

### **TABELA 3: `referencias`** (mantém)

**Propósito**: Referências por categoria (Baby/Kids/Teen/Adulto)

```sql
CREATE TABLE referencias (
    id                  INT PRIMARY KEY IDENTITY(1,1),
    relatorio_id        INT NOT NULL,
    codigo_referencia   NVARCHAR(100) UNIQUE,             -- Código único da ref (ex: REF-BABY-001)
    tipo_categoria      NVARCHAR(50) NOT NULL,            -- baby, kids, teen, adulto
    numero_ref          NVARCHAR(100),
    origem              NVARCHAR(100),
    fornecedor          NVARCHAR(200),
    fornecedor_contato  NVARCHAR(200),                    -- Email/Tel do fornecedor
    materia_prima       NVARCHAR(200),
    composicao          NVARCHAR(200),
    gramatura           NVARCHAR(100),
    aviamentos          NVARCHAR(500),
    observacoes         NVARCHAR(MAX),                     -- Notas gerais
    is_active           BIT DEFAULT 1,
    created_at          DATETIME DEFAULT GETDATE(),
    updated_at          DATETIME,

    FOREIGN KEY (relatorio_id) REFERENCES relatorios(id) ON DELETE CASCADE,
    INDEX idx_relatorio (relatorio_id),
    INDEX idx_codigo_ref (codigo_referencia),
    INDEX idx_tipo (tipo_categoria),
    INDEX idx_is_active (is_active)
);
```

**Campos renomeados**:
- `tipo` → `tipo_categoria` (mais descritivo)

**Campos novos**:
- `codigo_referencia` - Identificador único
- `fornecedor_contato` - Contato direto
- `observacoes` - Campo livre para notas

---

### **TABELA 4: `provas_modelagem`** (antes: `provas`)

**Propósito**: Provas individuais de cada referência

```sql
CREATE TABLE provas_modelagem (
    id                          INT PRIMARY KEY IDENTITY(1,1),
    referencia_id               INT NOT NULL,
    codigo_prova                NVARCHAR(100) UNIQUE,      -- PRV-REF-001-1 (ref + numero)
    numero_prova                INT NOT NULL,
    status_prova                NVARCHAR(50) DEFAULT 'Em Andamento',
    data_status                 DATETIME,                   -- Quando mudou status
    usuario_status              INT,                        -- Quem mudou status
    motivo_alteracao_status     NVARCHAR(MAX),

    -- Dados da prova
    tabela_medidas_path         NVARCHAR(500),
    data_recebimento_amostra    DATE,
    tamanhos_recebidos          NVARCHAR(200),
    informacoes_medidas         NVARCHAR(MAX),
    data_realizacao_prova       DATE,

    -- Feedback Qualidade
    responsavel_qualidade       NVARCHAR(200),
    comentarios_qualidade       NVARCHAR(MAX),
    observacoes_qualidade       NVARCHAR(MAX),
    data_feedback_qualidade     DATETIME,

    -- Feedback Estilo
    responsavel_estilo          NVARCHAR(200),
    comentarios_estilo          NVARCHAR(MAX),
    observacoes_estilo          NVARCHAR(MAX),
    data_feedback_estilo        DATETIME,

    -- Feedback Modelagem
    responsavel_modelagem       NVARCHAR(200),
    comentarios_modelagem       NVARCHAR(MAX),
    observacoes_modelagem       NVARCHAR(MAX),
    data_feedback_modelagem     DATETIME,

    -- Lacre
    data_liberacao_lacre        DATE,
    numero_lacre                NVARCHAR(100),

    -- Informações adicionais
    observacoes_gerais          NVARCHAR(MAX),
    is_active                   BIT DEFAULT 1,
    created_at                  DATETIME DEFAULT GETDATE(),
    updated_at                  DATETIME,

    FOREIGN KEY (referencia_id) REFERENCES referencias(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_status) REFERENCES usuarios(id),
    INDEX idx_referencia (referencia_id),
    INDEX idx_codigo_prova (codigo_prova),
    INDEX idx_numero (numero_prova),
    INDEX idx_status (status_prova),
    INDEX idx_is_active (is_active)
);
```

**Mudanças principais**:
- Tabela renomeada para `provas_modelagem` (mais específico)
- Campos renomeados para clareza:
  - `status` → `status_prova`
  - `motivo_ultima_alteracao` → `motivo_alteracao_status`
  - `data_recebimento` → `data_recebimento_amostra`
  - `info_medidas` → `informacoes_medidas`
  - `data_prova` → `data_realizacao_prova`
  - `time_*` → `responsavel_*`
  - `obs_*` → `observacoes_*`
  - `data_lacre` → `data_liberacao_lacre`
  - `info_adicionais` → `observacoes_gerais`

**Campos novos**:
- `codigo_prova` - Identificador único
- `data_status` - Quando mudou
- `usuario_status` - Quem mudou
- `data_feedback_*` - Timestamp dos feedbacks

---

### **TABELA 5: `fotos_provas`** (antes: `fotos`)

**Propósito**: Fotos das provas por contexto

```sql
CREATE TABLE fotos_provas (
    id                  INT PRIMARY KEY IDENTITY(1,1),
    prova_id            INT NOT NULL,
    contexto_foto       NVARCHAR(50) NOT NULL,             -- desenho_produto, qualidade, estilo, amostra, prova_modelo
    tamanho_amostra     NVARCHAR(50),                      -- Apenas para amostra/prova_modelo
    arquivo_path        NVARCHAR(500) NOT NULL,
    arquivo_nome        NVARCHAR(255),
    arquivo_tamanho     INT,                                -- Bytes
    arquivo_tipo        NVARCHAR(50),                       -- image/jpeg, image/png
    descricao           NVARCHAR(500),
    ordem_exibicao      INT DEFAULT 0,                      -- Para ordenar fotos
    is_active           BIT DEFAULT 1,
    uploaded_by         INT,                                -- Quem fez upload
    created_at          DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (prova_id) REFERENCES provas_modelagem(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES usuarios(id),
    INDEX idx_prova (prova_id),
    INDEX idx_contexto (contexto_foto),
    INDEX idx_is_active (is_active)
);
```

**Mudanças**:
- `fotos` → `fotos_provas`
- `contexto` → `contexto_foto`
- `tamanho` → `tamanho_amostra`
- `file_path` → `arquivo_path`

**Campos novos**:
- `arquivo_nome` - Nome original
- `arquivo_tamanho` - Para validação
- `arquivo_tipo` - MIME type
- `descricao` - Legenda da foto
- `ordem_exibicao` - Controle de ordenação
- `uploaded_by` - Rastreabilidade

---

### **TABELA 6: `historico_status`** (NOVA)

**Propósito**: Auditoria completa de mudanças de status

```sql
CREATE TABLE historico_status (
    id                  INT PRIMARY KEY IDENTITY(1,1),
    prova_id            INT NOT NULL,
    status_anterior     NVARCHAR(50),
    status_novo         NVARCHAR(50) NOT NULL,
    motivo              NVARCHAR(MAX),
    alterado_por        INT NOT NULL,
    data_alteracao      DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (prova_id) REFERENCES provas_modelagem(id) ON DELETE CASCADE,
    FOREIGN KEY (alterado_por) REFERENCES usuarios(id),
    INDEX idx_prova (prova_id),
    INDEX idx_data (data_alteracao)
);
```

---

### **TABELA 7: `configuracoes_sistema`** (NOVA)

**Propósito**: Configurações globais do sistema

```sql
CREATE TABLE configuracoes_sistema (
    id                  INT PRIMARY KEY IDENTITY(1,1),
    chave               NVARCHAR(100) NOT NULL UNIQUE,
    valor               NVARCHAR(MAX),
    tipo_dado           NVARCHAR(50),                      -- string, int, bool, json
    descricao           NVARCHAR(500),
    is_active           BIT DEFAULT 1,
    updated_at          DATETIME DEFAULT GETDATE(),

    INDEX idx_chave (chave)
);
```

---

## 🔧 CÓDIGO PYTHON

### **Classes de Modelo**
```python
# ✅ CORRETO
class Usuario(db.Model):
    __tablename__ = 'usuarios'

class Relatorio(db.Model):
    __tablename__ = 'relatorios'

class Referencia(db.Model):
    __tablename__ = 'referencias'

class ProvaModelagem(db.Model):
    __tablename__ = 'provas_modelagem'

class FotoProva(db.Model):
    __tablename__ = 'fotos_provas'

class HistoricoStatus(db.Model):
    __tablename__ = 'historico_status'
```

### **Funções e Métodos**
```python
# ✅ CORRETO - snake_case para funções
def criar_novo_relatorio():
    pass

def buscar_prova_por_id(prova_id):
    pass

def atualizar_status_prova(prova_id, novo_status):
    pass

# ✅ CORRETO - Métodos de classe também snake_case
class ProvaModelagem:
    def adicionar_foto(self, contexto, arquivo):
        pass

    def calcular_status_geral(self):
        pass
```

### **Variáveis**
```python
# ✅ CORRETO - snake_case
numero_prova = 1
codigo_referencia = "REF-001"
lista_provas = []

# ✅ CORRETO - Constantes em UPPER_CASE
STATUS_EM_ANDAMENTO = "Em Andamento"
STATUS_APROVADA = "Aprovada"
STATUS_REPROVADA = "Reprovada"
STATUS_COMITE = "Comitê"

CONTEXTOS_FOTO = ['desenho_produto', 'qualidade', 'estilo', 'amostra', 'prova_modelo']
TIPOS_CATEGORIA = ['baby', 'kids', 'teen', 'adulto']
```

---

## 📁 ARQUIVOS E DIRETÓRIOS

```
prova_modelagem_app/
├── models/                     # Modelos separados por contexto
│   ├── usuario.py
│   ├── relatorio.py
│   ├── referencia.py
│   ├── prova_modelagem.py
│   └── foto_prova.py
├── routes/                     # Rotas separadas
│   ├── auth_routes.py
│   ├── relatorio_routes.py
│   ├── prova_routes.py
│   └── api_routes.py
├── services/                   # Lógica de negócio
│   ├── relatorio_service.py
│   ├── prova_service.py
│   └── foto_service.py
├── utils/                      # Utilitários
│   ├── file_utils.py
│   ├── date_utils.py
│   └── validation_utils.py
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/
│       ├── ppts/
│       ├── tabelas_medidas/
│       └── fotos/
│           ├── desenho/
│           ├── qualidade/
│           ├── estilo/
│           ├── amostra/
│           └── prova_modelo/
└── templates/
    ├── auth/
    ├── relatorios/
    ├── provas/
    └── components/
```

---

## 🎨 TEMPLATES E FRONTEND

### **Arquivos HTML**
```
✅ CORRETO - snake_case.html
- login.html
- novo_relatorio.html
- editar_relatorio.html
- detalhes_prova.html
- lista_referencias.html
```

### **IDs e Classes CSS**
```html
<!-- ✅ CORRETO - kebab-case -->
<div id="card-relatorio" class="container-provas">
    <button class="btn-aprovar-prova">Aprovar</button>
</div>
```

### **JavaScript**
```javascript
// ✅ CORRETO - camelCase
const numeroProva = 1;
const statusProva = 'Aprovada';

function atualizarStatusProva(provaId, novoStatus) {
    // ...
}

class ModalAprovacao {
    constructor() {
        this.provaId = null;
    }

    abrir(provaId) {
        this.provaId = provaId;
    }
}
```

---

## 📝 CONSTANTES E ENUMS

### **Status de Prova**
```python
class StatusProva:
    EM_ANDAMENTO = "Em Andamento"
    APROVADA = "Aprovada"
    REPROVADA = "Reprovada"
    COMITE = "Comitê"
    CANCELADA = "Cancelada"

    @classmethod
    def choices(cls):
        return [cls.EM_ANDAMENTO, cls.APROVADA, cls.REPROVADA, cls.COMITE]
```

### **Contextos de Foto**
```python
class ContextoFoto:
    DESENHO_PRODUTO = "desenho_produto"
    QUALIDADE = "qualidade"
    ESTILO = "estilo"
    AMOSTRA = "amostra"
    PROVA_MODELO = "prova_modelo"

    @classmethod
    def choices(cls):
        return [cls.DESENHO_PRODUTO, cls.QUALIDADE, cls.ESTILO, cls.AMOSTRA, cls.PROVA_MODELO]
```

### **Tipos de Categoria**
```python
class TipoCategoria:
    BABY = "baby"
    KIDS = "kids"
    TEEN = "teen"
    ADULTO = "adulto"

    @classmethod
    def choices(cls):
        return [cls.BABY, cls.KIDS, cls.TEEN, cls.ADULTO]
```

---

## 🔒 RESUMO DAS REGRAS

| Contexto | Convenção | Exemplo |
|----------|-----------|---------|
| **Tabelas SQL** | `snake_case` plural | `provas_modelagem` |
| **Campos SQL** | `snake_case` singular | `data_recebimento_amostra` |
| **Classes Python** | `PascalCase` | `ProvaModelagem` |
| **Funções/Métodos** | `snake_case` | `criar_nova_prova()` |
| **Variáveis** | `snake_case` | `numero_prova` |
| **Constantes** | `UPPER_SNAKE_CASE` | `STATUS_APROVADA` |
| **Arquivos Python** | `snake_case.py` | `prova_service.py` |
| **Templates** | `snake_case.html` | `editar_prova.html` |
| **CSS IDs/Classes** | `kebab-case` | `card-prova` |
| **JavaScript** | `camelCase` | `numeroProva` |

---

## ✅ Benefícios da Nova Nomenclatura

1. ✅ **Clareza**: Nomes autoexplicativos
2. ✅ **Consistência**: Padrão único em todo sistema
3. ✅ **Manutenibilidade**: Fácil encontrar e entender código
4. ✅ **Escalabilidade**: Preparado para crescimento
5. ✅ **Profissionalismo**: Código de nível enterprise
6. ✅ **Rastreabilidade**: Histórico e auditoria completos
7. ✅ **Performance**: Índices bem planejados

---

**Atualizado em**: 2025-12-03
**Versão**: 2.0
