# 🎨 Biblioteca de Componentes CSS

Documentação completa dos componentes reutilizáveis do Design System.

---

## 📑 Índice

- [Botões](#botões)
- [Cards](#cards)
- [Formulários](#formulários)
- [Tabelas](#tabelas)
- [Badges e Tags](#badges-e-tags)
- [Modais](#modais)
- [Alerts e Toasts](#alerts-e-toasts)
- [Navegação](#navegação)
- [Upload de Arquivos](#upload-de-arquivos)
- [Galerias de Imagens](#galerias-de-imagens)

---

## 🔘 Botões

### Botão Primário

```html
<button class="btn btn-primary">
    <i class="bi bi-plus-circle"></i>
    Novo Relatório
</button>
```

**Variantes:**
```html
<button class="btn btn-primary">Primário</button>
<button class="btn btn-secondary">Secundário</button>
<button class="btn btn-success">Sucesso</button>
<button class="btn btn-danger">Perigo</button>
<button class="btn btn-warning">Aviso</button>
<button class="btn btn-info">Info</button>
<button class="btn btn-light">Claro</button>
<button class="btn btn-dark">Escuro</button>
```

**Tamanhos:**
```html
<button class="btn btn-primary btn-sm">Pequeno</button>
<button class="btn btn-primary">Normal</button>
<button class="btn btn-primary btn-lg">Grande</button>
```

**Estados:**
```html
<button class="btn btn-primary">Normal</button>
<button class="btn btn-primary" disabled>Desabilitado</button>
<button class="btn btn-primary active">Ativo</button>
<button class="btn btn-outline-primary">Outline</button>
```

**Com Ícone:**
```html
<!-- Ícone à esquerda -->
<button class="btn btn-primary">
    <i class="bi bi-download"></i>
    Download
</button>

<!-- Apenas ícone -->
<button class="btn btn-primary" aria-label="Editar">
    <i class="bi bi-pencil"></i>
</button>

<!-- Ícone à direita -->
<button class="btn btn-primary">
    Próximo
    <i class="bi bi-arrow-right"></i>
</button>
```

**Botão de Loading:**
```html
<button class="btn btn-primary" disabled>
    <span class="spinner-border spinner-border-sm" role="status"></span>
    Carregando...
</button>
```

---

## 🃏 Cards

### Card Básico

```html
<div class="card">
    <div class="card-header">
        <h5 class="card-title mb-0">Título do Card</h5>
    </div>
    <div class="card-body">
        <p class="card-text">Conteúdo do card</p>
    </div>
    <div class="card-footer text-muted">
        Rodapé do card
    </div>
</div>
```

### Card de Relatório

```html
<div class="card relatorio-card">
    <div class="card-header">
        <div class="d-flex justify-content-between align-items-center">
            <h5 class="card-title mb-0">Coleção Verão 2026</h5>
            <span class="badge bg-success">Aprovada</span>
        </div>
        <small class="text-muted">Primavera/Verão • Kids</small>
    </div>
    <div class="card-body">
        <p class="mb-2">
            <strong>Fornecedor:</strong> ABC Têxtil
        </p>
        <p class="mb-2">
            <strong>Provas:</strong> 3
        </p>
        <p class="mb-0">
            <strong>Criado:</strong> 16/01/2026
        </p>
    </div>
    <div class="card-footer">
        <div class="btn-group" role="group">
            <a href="#" class="btn btn-sm btn-primary">
                <i class="bi bi-eye"></i> Ver
            </a>
            <a href="#" class="btn btn-sm btn-secondary">
                <i class="bi bi-pencil"></i> Editar
            </a>
            <button class="btn btn-sm btn-danger">
                <i class="bi bi-trash"></i> Deletar
            </button>
        </div>
    </div>
</div>
```

### Card com Imagem

```html
<div class="card">
    <img src="image.jpg" class="card-img-top" alt="Descrição">
    <div class="card-body">
        <h5 class="card-title">Título</h5>
        <p class="card-text">Descrição</p>
        <a href="#" class="btn btn-primary">Ver Mais</a>
    </div>
</div>
```

### Card Hover (com efeito)

```html
<div class="card card-hover">
    <div class="card-body">
        <h5 class="card-title">Card com Hover</h5>
        <p class="card-text">Passa o mouse para ver o efeito</p>
    </div>
</div>

<style>
.card-hover {
    transition: transform 0.2s, box-shadow 0.2s;
}

.card-hover:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
</style>
```

---

## 📝 Formulários

### Input de Texto

```html
<div class="mb-3">
    <label for="colecao" class="form-label">
        Coleção <span class="text-danger">*</span>
    </label>
    <input
        type="text"
        class="form-control"
        id="colecao"
        name="colecao"
        placeholder="Ex: Verão 2026"
        required
    >
    <div class="form-text">Digite o nome da coleção</div>
</div>
```

### Input com Validação

```html
<!-- Válido -->
<div class="mb-3">
    <label for="email" class="form-label">Email</label>
    <input type="email" class="form-control is-valid" id="email" value="user@exemplo.com">
    <div class="valid-feedback">Email válido!</div>
</div>

<!-- Inválido -->
<div class="mb-3">
    <label for="senha" class="form-label">Senha</label>
    <input type="password" class="form-control is-invalid" id="senha">
    <div class="invalid-feedback">Senha deve ter no mínimo 8 caracteres</div>
</div>
```

### Select / Dropdown

```html
<div class="mb-3">
    <label for="categoria" class="form-label">Categoria</label>
    <select class="form-select" id="categoria" name="categoria" required>
        <option value="">Selecione...</option>
        <option value="Baby">Baby</option>
        <option value="Kids">Kids</option>
        <option value="Teen">Teen</option>
        <option value="Adulto">Adulto</option>
    </select>
</div>
```

### Textarea

```html
<div class="mb-3">
    <label for="observacoes" class="form-label">Observações</label>
    <textarea
        class="form-control"
        id="observacoes"
        name="observacoes"
        rows="4"
        placeholder="Digite suas observações..."
    ></textarea>
</div>
```

### Checkbox

```html
<!-- Checkbox único -->
<div class="mb-3 form-check">
    <input type="checkbox" class="form-check-input" id="concordo" name="concordo">
    <label class="form-check-label" for="concordo">
        Li e concordo com os termos
    </label>
</div>

<!-- Grupo de checkboxes -->
<fieldset class="mb-3">
    <legend class="form-label">Checklist de Qualidade</legend>
    <div class="form-check">
        <input type="checkbox" class="form-check-input" id="costura" name="checklist_costura">
        <label class="form-check-label" for="costura">Costura</label>
    </div>
    <div class="form-check">
        <input type="checkbox" class="form-check-input" id="acabamento" name="checklist_acabamento">
        <label class="form-check-label" for="acabamento">Acabamento</label>
    </div>
    <div class="form-check">
        <input type="checkbox" class="form-check-input" id="botoes" name="checklist_botoes">
        <label class="form-check-label" for="botoes">Botões</label>
    </div>
</fieldset>
```

### Radio Buttons

```html
<fieldset class="mb-3">
    <legend class="form-label">Status</legend>
    <div class="form-check">
        <input type="radio" class="form-check-input" id="andamento" name="status" value="Em Andamento" checked>
        <label class="form-check-label" for="andamento">Em Andamento</label>
    </div>
    <div class="form-check">
        <input type="radio" class="form-check-input" id="aprovada" name="status" value="Aprovada">
        <label class="form-check-label" for="aprovada">Aprovada</label>
    </div>
    <div class="form-check">
        <input type="radio" class="form-check-input" id="reprovada" name="status" value="Reprovada">
        <label class="form-check-label" for="reprovada">Reprovada</label>
    </div>
</fieldset>
```

### Upload de Arquivo

```html
<div class="mb-3">
    <label for="arquivo" class="form-label">Arquivo</label>
    <input type="file" class="form-control" id="arquivo" name="arquivo" accept=".pdf,.docx">
    <div class="form-text">Formatos aceitos: PDF, DOCX (máx. 25MB)</div>
</div>

<!-- Upload múltiplo -->
<div class="mb-3">
    <label for="fotos" class="form-label">Fotos</label>
    <input type="file" class="form-control" id="fotos" name="fotos[]" multiple accept="image/*">
    <div class="form-text">Selecione uma ou mais imagens</div>
</div>
```

### Input Group (com addon)

```html
<!-- Addon à esquerda -->
<div class="mb-3">
    <label for="gramatura" class="form-label">Gramatura</label>
    <div class="input-group">
        <input type="number" class="form-control" id="gramatura" placeholder="180">
        <span class="input-group-text">g/m²</span>
    </div>
</div>

<!-- Botão à direita -->
<div class="mb-3">
    <label for="busca" class="form-label">Buscar</label>
    <div class="input-group">
        <input type="text" class="form-control" id="busca" placeholder="Digite...">
        <button class="btn btn-primary" type="button">
            <i class="bi bi-search"></i>
        </button>
    </div>
</div>
```

---

## 📊 Tabelas

### Tabela Básica

```html
<div class="table-responsive">
    <table class="table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Coleção</th>
                <th>Status</th>
                <th>Data</th>
                <th>Ações</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>Verão 2026</td>
                <td><span class="badge bg-success">Aprovada</span></td>
                <td>16/01/2026</td>
                <td>
                    <button class="btn btn-sm btn-primary"><i class="bi bi-eye"></i></button>
                    <button class="btn btn-sm btn-secondary"><i class="bi bi-pencil"></i></button>
                </td>
            </tr>
        </tbody>
    </table>
</div>
```

### Tabela Striped e Hover

```html
<table class="table table-striped table-hover">
    <thead class="table-dark">
        <tr>
            <th>Coluna 1</th>
            <th>Coluna 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Dado 1</td>
            <td>Dado 2</td>
        </tr>
    </tbody>
</table>
```

### Tabela Responsiva com Cards Mobile

```html
<div class="table-responsive">
    <table class="table table-mobile-cards">
        <thead>
            <tr>
                <th data-label="ID">ID</th>
                <th data-label="Nome">Nome</th>
                <th data-label="Status">Status</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td data-label="ID">1</td>
                <td data-label="Nome">Item 1</td>
                <td data-label="Status"><span class="badge bg-success">Ativo</span></td>
            </tr>
        </tbody>
    </table>
</div>

<style>
@media (max-width: 768px) {
    .table-mobile-cards thead {
        display: none;
    }

    .table-mobile-cards tbody tr {
        display: block;
        margin-bottom: 1rem;
        border: 1px solid var(--bs-border-color);
        border-radius: 0.5rem;
        padding: 1rem;
    }

    .table-mobile-cards tbody td {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border: none;
    }

    .table-mobile-cards tbody td::before {
        content: attr(data-label);
        font-weight: 600;
        margin-right: 1rem;
    }
}
</style>
```

---

## 🏷️ Badges e Tags

### Badges de Status

```html
<span class="badge bg-primary">Primary</span>
<span class="badge bg-secondary">Secondary</span>
<span class="badge bg-success">Aprovada</span>
<span class="badge bg-danger">Reprovada</span>
<span class="badge bg-warning text-dark">Em Andamento</span>
<span class="badge bg-info text-dark">Comitê</span>
```

### Badges com Ícone

```html
<span class="badge bg-success">
    <i class="bi bi-check-circle"></i>
    Aprovada
</span>

<span class="badge bg-danger">
    <i class="bi bi-x-circle"></i>
    Reprovada
</span>
```

### Badge de Contador

```html
<button class="btn btn-primary position-relative">
    Notificações
    <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
        9+
        <span class="visually-hidden">novas notificações</span>
    </span>
</button>
```

### Pills (Badges Arredondados)

```html
<span class="badge rounded-pill bg-primary">Kids</span>
<span class="badge rounded-pill bg-secondary">Teen</span>
<span class="badge rounded-pill bg-success">Adulto</span>
```

---

## 🔔 Modais

### Modal Básico

```html
<!-- Botão que abre o modal -->
<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#meuModal">
    Abrir Modal
</button>

<!-- Modal -->
<div class="modal fade" id="meuModal" tabindex="-1" aria-labelledby="meuModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="meuModalLabel">Título do Modal</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
            </div>
            <div class="modal-body">
                <p>Conteúdo do modal...</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="button" class="btn btn-primary">Confirmar</button>
            </div>
        </div>
    </div>
</div>
```

### Modal de Confirmação de Deleção

```html
<div class="modal fade" id="confirmarDelecao" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header bg-danger text-white">
                <h5 class="modal-title">
                    <i class="bi bi-exclamation-triangle"></i>
                    Confirmar Deleção
                </h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <p>Tem certeza que deseja deletar este item?</p>
                <p class="text-danger"><strong>Esta ação não pode ser desfeita.</strong></p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="button" class="btn btn-danger">
                    <i class="bi bi-trash"></i>
                    Deletar
                </button>
            </div>
        </div>
    </div>
</div>
```

### Modal Grande / Fullscreen

```html
<!-- Modal grande -->
<div class="modal fade" id="modalGrande" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <!-- ... -->
        </div>
    </div>
</div>

<!-- Modal extra grande -->
<div class="modal fade" id="modalXL" tabindex="-1">
    <div class="modal-dialog modal-xl">
        <div class="modal-content">
            <!-- ... -->
        </div>
    </div>
</div>

<!-- Modal fullscreen -->
<div class="modal fade" id="modalFullscreen" tabindex="-1">
    <div class="modal-dialog modal-fullscreen">
        <div class="modal-content">
            <!-- ... -->
        </div>
    </div>
</div>
```

---

## ⚠️ Alerts e Toasts

### Alerts

```html
<div class="alert alert-primary" role="alert">
    Alerta primário
</div>

<div class="alert alert-success" role="alert">
    <i class="bi bi-check-circle"></i>
    Operação realizada com sucesso!
</div>

<div class="alert alert-danger" role="alert">
    <i class="bi bi-exclamation-triangle"></i>
    Erro ao processar sua requisição.
</div>

<div class="alert alert-warning" role="alert">
    <i class="bi bi-exclamation-circle"></i>
    Atenção: Verifique os dados antes de continuar.
</div>
```

### Alert Dismissible (Fechável)

```html
<div class="alert alert-info alert-dismissible fade show" role="alert">
    <strong>Informação!</strong> Você pode fechar este alerta.
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
</div>
```

### Toasts (Notificações)

```html
<div class="toast-container position-fixed bottom-0 end-0 p-3">
    <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header">
            <i class="bi bi-bell text-primary me-2"></i>
            <strong class="me-auto">Notificação</strong>
            <small>Agora</small>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Fechar"></button>
        </div>
        <div class="toast-body">
            Nova prova adicionada com sucesso!
        </div>
    </div>
</div>

<script>
// Mostrar toast
const toastElement = document.querySelector('.toast');
const toast = new bootstrap.Toast(toastElement);
toast.show();
</script>
```

---

## 🧭 Navegação

### Navbar

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
        <a class="navbar-brand" href="/">
            <img src="logo.png" alt="Logo" height="30">
            Prova Modelagem
        </a>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                    <a class="nav-link active" href="/dashboard">
                        <i class="bi bi-house"></i> Dashboard
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/analytics">
                        <i class="bi bi-bar-chart"></i> Analytics
                    </a>
                </li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown">
                        <i class="bi bi-person-circle"></i> Usuário
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li><a class="dropdown-item" href="/perfil">Perfil</a></li>
                        <li><a class="dropdown-item" href="/configuracoes">Configurações</a></li>
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item" href="/logout">Sair</a></li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

### Breadcrumb

```html
<nav aria-label="breadcrumb">
    <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/dashboard">Dashboard</a></li>
        <li class="breadcrumb-item"><a href="/relatorios">Relatórios</a></li>
        <li class="breadcrumb-item active" aria-current="page">Verão 2026</li>
    </ol>
</nav>
```

### Tabs (Abas)

```html
<ul class="nav nav-tabs" id="myTab" role="tablist">
    <li class="nav-item" role="presentation">
        <button class="nav-link active" id="info-tab" data-bs-toggle="tab" data-bs-target="#info" type="button" role="tab">
            <i class="bi bi-info-circle"></i> Informações
        </button>
    </li>
    <li class="nav-item" role="presentation">
        <button class="nav-link" id="provas-tab" data-bs-toggle="tab" data-bs-target="#provas" type="button" role="tab">
            <i class="bi bi-file-earmark-text"></i> Provas
        </button>
    </li>
    <li class="nav-item" role="presentation">
        <button class="nav-link" id="fotos-tab" data-bs-toggle="tab" data-bs-target="#fotos" type="button" role="tab">
            <i class="bi bi-camera"></i> Fotos
        </button>
    </li>
</ul>

<div class="tab-content" id="myTabContent">
    <div class="tab-pane fade show active" id="info" role="tabpanel">
        <p>Conteúdo da aba Informações...</p>
    </div>
    <div class="tab-pane fade" id="provas" role="tabpanel">
        <p>Conteúdo da aba Provas...</p>
    </div>
    <div class="tab-pane fade" id="fotos" role="tabpanel">
        <p>Conteúdo da aba Fotos...</p>
    </div>
</div>
```

### Pagination

```html
<nav aria-label="Navegação de página">
    <ul class="pagination">
        <li class="page-item disabled">
            <a class="page-link" href="#" tabindex="-1" aria-disabled="true">Anterior</a>
        </li>
        <li class="page-item active" aria-current="page">
            <a class="page-link" href="#">1</a>
        </li>
        <li class="page-item"><a class="page-link" href="#">2</a></li>
        <li class="page-item"><a class="page-link" href="#">3</a></li>
        <li class="page-item">
            <a class="page-link" href="#">Próximo</a>
        </li>
    </ul>
</nav>
```

---

## 📤 Upload de Arquivos

### Upload Drag & Drop

```html
<div class="file-upload-area" id="dropZone">
    <input type="file" id="fileInput" name="fotos[]" multiple accept="image/*" hidden>
    <div class="file-upload-content">
        <i class="bi bi-cloud-upload" style="font-size: 3rem;"></i>
        <p class="mt-3 mb-2"><strong>Arraste arquivos aqui</strong></p>
        <p class="text-muted">ou clique para selecionar</p>
        <button type="button" class="btn btn-primary mt-2" onclick="document.getElementById('fileInput').click()">
            Selecionar Arquivos
        </button>
    </div>
</div>

<div id="fileList" class="mt-3"></div>

<style>
.file-upload-area {
    border: 2px dashed var(--bs-border-color);
    border-radius: 0.5rem;
    padding: 3rem 2rem;
    text-align: center;
    transition: all 0.3s;
    cursor: pointer;
}

.file-upload-area:hover,
.file-upload-area.drag-over {
    border-color: var(--bs-primary);
    background-color: rgba(var(--bs-primary-rgb), 0.05);
}
</style>

<script>
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');

// Clique para abrir seletor
dropZone.addEventListener('click', (e) => {
    if (e.target !== fileInput) fileInput.click();
});

// Drag & drop
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => {
        dropZone.classList.add('drag-over');
    });
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => {
        dropZone.classList.remove('drag-over');
    });
});

dropZone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    fileInput.files = files;
    displayFiles(files);
});

fileInput.addEventListener('change', () => {
    displayFiles(fileInput.files);
});

function displayFiles(files) {
    fileList.innerHTML = '';
    Array.from(files).forEach(file => {
        const fileItem = document.createElement('div');
        fileItem.className = 'alert alert-info d-flex justify-content-between align-items-center';
        fileItem.innerHTML = `
            <span><i class="bi bi-file-earmark"></i> ${file.name} (${(file.size / 1024).toFixed(2)} KB)</span>
            <button type="button" class="btn-close" aria-label="Remover"></button>
        `;
        fileList.appendChild(fileItem);
    });
}
</script>
```

---

## 🖼️ Galerias de Imagens

### Grid de Fotos

```html
<div class="photo-grid">
    <div class="photo-item">
        <img src="foto1.jpg" alt="Foto 1" class="img-fluid" data-bs-toggle="modal" data-bs-target="#fotoModal">
        <div class="photo-overlay">
            <span class="badge bg-primary">Desenho</span>
            <span class="badge bg-secondary">Tamanho M</span>
        </div>
    </div>
    <div class="photo-item">
        <img src="foto2.jpg" alt="Foto 2" class="img-fluid">
        <div class="photo-overlay">
            <span class="badge bg-primary">Amostra</span>
        </div>
    </div>
    <!-- Mais fotos... -->
</div>

<style>
.photo-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1rem;
}

.photo-item {
    position: relative;
    overflow: hidden;
    border-radius: 0.5rem;
    cursor: pointer;
}

.photo-item img {
    width: 100%;
    height: 250px;
    object-fit: cover;
    transition: transform 0.3s;
}

.photo-item:hover img {
    transform: scale(1.05);
}

.photo-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 0.5rem;
    background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
    opacity: 0;
    transition: opacity 0.3s;
}

.photo-item:hover .photo-overlay {
    opacity: 1;
}
</style>
```

### Lightbox / Visualizador de Imagens

```html
<!-- Modal para visualizar imagem em tamanho grande -->
<div class="modal fade" id="fotoModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered modal-xl">
        <div class="modal-content bg-transparent border-0">
            <div class="modal-body p-0 text-center">
                <button type="button" class="btn-close btn-close-white position-absolute top-0 end-0 m-3" data-bs-dismiss="modal" style="z-index: 1050;"></button>
                <img src="" id="modalImage" class="img-fluid" alt="Foto ampliada">
            </div>
        </div>
    </div>
</div>

<script>
// Atualizar imagem do modal quando abrir
const fotoModal = document.getElementById('fotoModal');
fotoModal.addEventListener('show.bs.modal', (event) => {
    const trigger = event.relatedTarget;
    const imgSrc = trigger.getAttribute('src');
    const modalImage = document.getElementById('modalImage');
    modalImage.setAttribute('src', imgSrc);
});
</script>
```

---

## 🎯 Utilitários Rápidos

### Espaçamento

```html
<!-- Margin -->
<div class="m-0">Sem margem</div>
<div class="m-1">Margem pequena (0.25rem)</div>
<div class="m-3">Margem média (1rem)</div>
<div class="mb-3">Margem bottom</div>
<div class="mt-5">Margem top grande</div>

<!-- Padding -->
<div class="p-3">Padding médio</div>
<div class="px-4 py-2">Padding horizontal 4, vertical 2</div>
```

### Texto

```html
<p class="text-start">Alinhado à esquerda</p>
<p class="text-center">Centralizado</p>
<p class="text-end">Alinhado à direita</p>

<p class="text-primary">Texto primário</p>
<p class="text-success">Texto de sucesso</p>
<p class="text-danger">Texto de erro</p>
<p class="text-muted">Texto esmaecido</p>

<p class="fw-bold">Negrito</p>
<p class="fst-italic">Itálico</p>
<p class="text-uppercase">maiúsculas</p>
```

### Display

```html
<div class="d-none">Escondido</div>
<div class="d-block">Block</div>
<div class="d-flex">Flexbox</div>
<div class="d-grid">Grid</div>

<!-- Responsivo -->
<div class="d-none d-md-block">Visível apenas em md+</div>
<div class="d-block d-md-none">Visível apenas em mobile</div>
```

### Flexbox

```html
<div class="d-flex justify-content-between align-items-center">
    <span>Esquerda</span>
    <span>Direita</span>
</div>

<div class="d-flex flex-column gap-3">
    <div>Item 1</div>
    <div>Item 2</div>
</div>
```

---

## 🔗 Links Relacionados

- **[Design System](DESIGN_SYSTEM.md)** - Tokens e fundamentos
- **[UX Patterns](UX_PATTERNS.md)** - Padrões de interação
- **[Frontend Architecture](../architecture/FRONTEND.md)** - Estrutura de código

---

**[⬅ Voltar ao Índice](../INDEX.md)**
