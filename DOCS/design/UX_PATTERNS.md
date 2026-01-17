# 🎯 UX Patterns - Padrões de Interação

Guia de padrões de experiência do usuário e interações do sistema.

---

## 📑 Índice

- [Princípios de UX](#princípios-de-ux)
- [Feedback Visual](#feedback-visual)
- [Loading States](#loading-states)
- [Validação de Formulários](#validação-de-formulários)
- [Navegação](#navegação)
- [Gestão de Dados](#gestão-de-dados)
- [Empty States](#empty-states)
- [Error Handling](#error-handling)
- [Acessibilidade](#acessibilidade)
- [Mobile First](#mobile-first)

---

## 🎨 Princípios de UX

### 1. Clareza

✅ **Sempre comunique claramente o que está acontecendo**
- Labels descritivos
- Mensagens de erro específicas
- Feedback imediato de ações

❌ **Evite:**
- Mensagens genéricas ("Erro")
- Ações sem confirmação
- Estados sem feedback visual

### 2. Consistência

✅ **Mantenha padrões em todo o sistema**
- Mesmas cores para mesmas ações
- Posicionamento consistente de botões
- Nomenclatura uniforme

❌ **Evite:**
- Botões "Salvar" em um lugar e "Confirmar" em outro
- Cores diferentes para mesma ação
- Mudanças repentinas de layout

### 3. Eficiência

✅ **Minimize cliques e etapas**
- Atalhos de teclado
- Ações em lote
- Auto-save quando apropriado

❌ **Evite:**
- Múltiplos modais aninhados
- Formulários muito longos sem divisão
- Recarregar página inteira para pequenas mudanças

### 4. Prevenção de Erros

✅ **Evite erros antes que aconteçam**
- Validação em tempo real
- Confirmações para ações destrutivas
- Limites claros (máx. caracteres, tamanho de arquivo)

❌ **Evite:**
- Permitir ações destrutivas sem confirmação
- Validação apenas no submit
- Mensagens de erro confusas

---

## ✅ Feedback Visual

### Estados de Botões

```html
<!-- Normal -->
<button class="btn btn-primary">Salvar</button>

<!-- Hover -->
<button class="btn btn-primary" onmouseover="this.style.opacity='0.9'">Salvar</button>

<!-- Loading -->
<button class="btn btn-primary" disabled>
    <span class="spinner-border spinner-border-sm me-2"></span>
    Salvando...
</button>

<!-- Sucesso (temporário) -->
<button class="btn btn-success" disabled>
    <i class="bi bi-check-circle"></i>
    Salvo!
</button>

<!-- Disabled -->
<button class="btn btn-primary" disabled>Salvar</button>
```

**Implementação JavaScript:**
```javascript
function handleSave() {
    const btn = document.getElementById('saveBtn');

    // Estado: Loading
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Salvando...';

    // Fazer requisição...
    fetch('/api/save', { method: 'POST', body: data })
        .then(response => {
            if (response.ok) {
                // Estado: Sucesso
                btn.classList.remove('btn-primary');
                btn.classList.add('btn-success');
                btn.innerHTML = '<i class="bi bi-check-circle"></i> Salvo!';

                // Voltar ao normal após 2s
                setTimeout(() => {
                    btn.classList.remove('btn-success');
                    btn.classList.add('btn-primary');
                    btn.innerHTML = 'Salvar';
                    btn.disabled = false;
                }, 2000);
            } else {
                // Estado: Erro
                btn.classList.remove('btn-primary');
                btn.classList.add('btn-danger');
                btn.innerHTML = '<i class="bi bi-x-circle"></i> Erro';
                btn.disabled = false;
            }
        });
}
```

---

### Flash Messages / Toasts

```html
<!-- Container de toasts -->
<div class="toast-container position-fixed bottom-0 end-0 p-3" style="z-index: 9999"></div>

<script>
function showToast(message, type = 'success') {
    const container = document.querySelector('.toast-container');
    const iconMap = {
        success: 'bi-check-circle-fill text-success',
        error: 'bi-x-circle-fill text-danger',
        warning: 'bi-exclamation-triangle-fill text-warning',
        info: 'bi-info-circle-fill text-info'
    };

    const toastHTML = `
        <div class="toast align-items-center" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi ${iconMap[type]} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

    container.insertAdjacentHTML('beforeend', toastHTML);
    const toastElement = container.lastElementChild;
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 5000
    });

    toast.show();

    // Remover do DOM após fechar
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

// Uso:
showToast('Relatório criado com sucesso!', 'success');
showToast('Erro ao processar requisição', 'error');
showToast('Preencha todos os campos obrigatórios', 'warning');
</script>
```

---

### Transições Suaves

```css
/* Transição padrão para elementos interativos */
.btn,
.card,
.form-control,
.nav-link {
    transition: all 0.2s ease-in-out;
}

/* Hover suave em cards */
.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Fade in para elementos que aparecem */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in {
    animation: fadeIn 0.3s ease-out;
}

/* Pulse para indicar atenção */
@keyframes pulse {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: 0.7;
    }
}

.pulse {
    animation: pulse 2s ease-in-out infinite;
}
```

---

## ⏳ Loading States

### Skeleton Screens (Preferido)

```html
<!-- Em vez de spinner, mostrar estrutura da página -->
<div class="card">
    <div class="card-body">
        <div class="skeleton skeleton-title mb-3"></div>
        <div class="skeleton skeleton-text mb-2"></div>
        <div class="skeleton skeleton-text mb-2"></div>
        <div class="skeleton skeleton-text" style="width: 60%;"></div>
    </div>
</div>

<style>
.skeleton {
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: loading 1.5s ease-in-out infinite;
    border-radius: 4px;
}

@keyframes loading {
    0% {
        background-position: 200% 0;
    }
    100% {
        background-position: -200% 0;
    }
}

.skeleton-title {
    height: 24px;
    width: 50%;
}

.skeleton-text {
    height: 16px;
    width: 100%;
}
</style>
```

---

### Spinners

```html
<!-- Spinner centralizado (página inteira) -->
<div class="loading-overlay" id="loadingOverlay">
    <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
        <span class="visually-hidden">Carregando...</span>
    </div>
    <p class="mt-3 text-muted">Carregando...</p>
</div>

<style>
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.9);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 9998;
}
</style>

<script>
// Mostrar
function showLoading() {
    document.getElementById('loadingOverlay').classList.remove('d-none');
}

// Esconder
function hideLoading() {
    document.getElementById('loadingOverlay').classList.add('d-none');
}
</script>
```

---

### Progress Bar

```html
<div class="card">
    <div class="card-header">
        Upload de Fotos (3/10)
    </div>
    <div class="card-body">
        <div class="progress" style="height: 25px;">
            <div
                class="progress-bar progress-bar-striped progress-bar-animated"
                role="progressbar"
                style="width: 30%"
                aria-valuenow="30"
                aria-valuemin="0"
                aria-valuemax="100"
            >
                30%
            </div>
        </div>
    </div>
</div>

<script>
function updateProgress(current, total) {
    const percentage = Math.round((current / total) * 100);
    const progressBar = document.querySelector('.progress-bar');

    progressBar.style.width = percentage + '%';
    progressBar.setAttribute('aria-valuenow', percentage);
    progressBar.textContent = percentage + '%';

    if (percentage === 100) {
        progressBar.classList.remove('progress-bar-animated', 'progress-bar-striped');
        progressBar.classList.add('bg-success');
    }
}

// Uso
updateProgress(3, 10); // 30%
</script>
```

---

## 📝 Validação de Formulários

### Validação em Tempo Real

```html
<div class="mb-3">
    <label for="email" class="form-label">Email</label>
    <input
        type="email"
        class="form-control"
        id="email"
        name="email"
        required
        data-validate="email"
    >
    <div class="invalid-feedback"></div>
    <div class="valid-feedback">Email válido!</div>
</div>

<script>
const emailInput = document.getElementById('email');

emailInput.addEventListener('blur', (e) => {
    validateField(e.target);
});

emailInput.addEventListener('input', (e) => {
    // Validar apenas se já tiver sido tocado
    if (e.target.classList.contains('is-invalid') || e.target.classList.contains('is-valid')) {
        validateField(e.target);
    }
});

function validateField(field) {
    const value = field.value.trim();
    const type = field.getAttribute('data-validate');
    let isValid = true;
    let errorMessage = '';

    if (field.required && !value) {
        isValid = false;
        errorMessage = 'Este campo é obrigatório';
    } else if (type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            errorMessage = 'Digite um email válido';
        }
    }

    // Aplicar classes
    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
        field.nextElementSibling.textContent = errorMessage;
    }

    return isValid;
}

// Validar formulário completo antes de submit
document.getElementById('myForm').addEventListener('submit', (e) => {
    e.preventDefault();

    const fields = document.querySelectorAll('[data-validate]');
    let allValid = true;

    fields.forEach(field => {
        if (!validateField(field)) {
            allValid = false;
        }
    });

    if (allValid) {
        // Submit form
        e.target.submit();
    } else {
        // Focar no primeiro campo inválido
        const firstInvalid = document.querySelector('.is-invalid');
        if (firstInvalid) {
            firstInvalid.focus();
        }

        showToast('Corrija os erros antes de continuar', 'error');
    }
});
</script>
```

---

### Validação de Senha Forte

```html
<div class="mb-3">
    <label for="senha" class="form-label">Senha</label>
    <input type="password" class="form-control" id="senha" name="senha" required>

    <div class="password-strength mt-2">
        <div class="progress" style="height: 5px;">
            <div class="progress-bar" id="strengthBar" style="width: 0%"></div>
        </div>
        <small id="strengthText" class="text-muted">Digite uma senha</small>
    </div>

    <ul class="password-requirements mt-2 small text-muted">
        <li id="req-length"><i class="bi bi-x-circle text-danger"></i> Mínimo 8 caracteres</li>
        <li id="req-uppercase"><i class="bi bi-x-circle text-danger"></i> Uma letra maiúscula</li>
        <li id="req-lowercase"><i class="bi bi-x-circle text-danger"></i> Uma letra minúscula</li>
        <li id="req-number"><i class="bi bi-x-circle text-danger"></i> Um número</li>
        <li id="req-special"><i class="bi bi-x-circle text-danger"></i> Um caractere especial</li>
    </ul>
</div>

<script>
const senhaInput = document.getElementById('senha');
const strengthBar = document.getElementById('strengthBar');
const strengthText = document.getElementById('strengthText');

const requirements = {
    length: { regex: /.{8,}/, element: document.getElementById('req-length') },
    uppercase: { regex: /[A-Z]/, element: document.getElementById('req-uppercase') },
    lowercase: { regex: /[a-z]/, element: document.getElementById('req-lowercase') },
    number: { regex: /[0-9]/, element: document.getElementById('req-number') },
    special: { regex: /[!@#$%^&*(),.?":{}|<>]/, element: document.getElementById('req-special') }
};

senhaInput.addEventListener('input', (e) => {
    const senha = e.target.value;
    let metRequirements = 0;

    // Verificar cada requisito
    Object.keys(requirements).forEach(key => {
        const req = requirements[key];
        const met = req.regex.test(senha);

        if (met) {
            metRequirements++;
            req.element.innerHTML = '<i class="bi bi-check-circle text-success"></i> ' +
                                    req.element.textContent.replace(/✗|✓/, '').trim();
        } else {
            req.element.innerHTML = '<i class="bi bi-x-circle text-danger"></i> ' +
                                    req.element.textContent.replace(/✗|✓/, '').trim();
        }
    });

    // Calcular força
    const strength = (metRequirements / 5) * 100;
    strengthBar.style.width = strength + '%';

    // Cor e texto
    if (strength < 40) {
        strengthBar.className = 'progress-bar bg-danger';
        strengthText.textContent = 'Senha fraca';
        strengthText.className = 'text-danger';
    } else if (strength < 80) {
        strengthBar.className = 'progress-bar bg-warning';
        strengthText.textContent = 'Senha média';
        strengthText.className = 'text-warning';
    } else {
        strengthBar.className = 'progress-bar bg-success';
        strengthText.textContent = 'Senha forte';
        strengthText.className = 'text-success';
    }
});
</script>
```

---

## 🧭 Navegação

### Breadcrumbs Dinâmicos

```javascript
// Gerar breadcrumbs automaticamente baseado na URL
function generateBreadcrumbs() {
    const path = window.location.pathname;
    const segments = path.split('/').filter(seg => seg);

    const breadcrumbNav = document.getElementById('breadcrumb');
    const breadcrumbList = breadcrumbNav.querySelector('ol');
    breadcrumbList.innerHTML = '<li class="breadcrumb-item"><a href="/dashboard">Dashboard</a></li>';

    let currentPath = '';
    segments.forEach((segment, index) => {
        currentPath += '/' + segment;

        // Nome legível
        const name = segment
            .replace(/-/g, ' ')
            .replace(/\b\w/g, l => l.toUpperCase());

        if (index === segments.length - 1) {
            // Último item (atual)
            breadcrumbList.innerHTML += `
                <li class="breadcrumb-item active" aria-current="page">${name}</li>
            `;
        } else {
            breadcrumbList.innerHTML += `
                <li class="breadcrumb-item"><a href="${currentPath}">${name}</a></li>
            `;
        }
    });
}

// Chamar ao carregar página
document.addEventListener('DOMContentLoaded', generateBreadcrumbs);
```

---

### Tab Persistence (Manter aba ativa)

```javascript
// Salvar aba ativa no localStorage
document.querySelectorAll('[data-bs-toggle="tab"]').forEach(tabButton => {
    tabButton.addEventListener('shown.bs.tab', (e) => {
        const tabId = e.target.getAttribute('data-bs-target');
        localStorage.setItem('activeTab', tabId);
    });
});

// Restaurar aba ativa ao carregar página
document.addEventListener('DOMContentLoaded', () => {
    const activeTab = localStorage.getItem('activeTab');
    if (activeTab) {
        const tabButton = document.querySelector(`[data-bs-target="${activeTab}"]`);
        if (tabButton) {
            new bootstrap.Tab(tabButton).show();
        }
    }
});
```

---

## 💾 Gestão de Dados

### Confirmação de Ações Destrutivas

```html
<!-- Botão de deletar com modal de confirmação -->
<button
    class="btn btn-danger"
    data-bs-toggle="modal"
    data-bs-target="#confirmarDelecao"
    data-item-id="123"
    data-item-name="Coleção Verão 2026"
>
    <i class="bi bi-trash"></i> Deletar
</button>

<!-- Modal de confirmação -->
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
                <p>Tem certeza que deseja deletar <strong id="itemName"></strong>?</p>
                <div class="alert alert-danger">
                    <i class="bi bi-exclamation-circle"></i>
                    <strong>Atenção:</strong> Esta ação não pode ser desfeita.
                    Todos os dados relacionados (provas, fotos, feedbacks) também serão removidos.
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <form id="deleteForm" method="POST" style="display: inline;">
                    <button type="submit" class="btn btn-danger">
                        <i class="bi bi-trash"></i>
                        Confirmar Deleção
                    </button>
                </form>
            </div>
        </div>
    </div>
</div>

<script>
const modal = document.getElementById('confirmarDelecao');

modal.addEventListener('show.bs.modal', (event) => {
    const button = event.relatedTarget;
    const itemId = button.getAttribute('data-item-id');
    const itemName = button.getAttribute('data-item-name');

    // Atualizar texto
    document.getElementById('itemName').textContent = itemName;

    // Atualizar action do form
    document.getElementById('deleteForm').action = `/deletar-relatorio/${itemId}`;
});
</script>
```

---

### Auto-Save (Draft)

```javascript
let autoSaveTimeout;

// Salvar rascunho a cada 30 segundos de inatividade
document.querySelectorAll('input, textarea, select').forEach(field => {
    field.addEventListener('input', () => {
        clearTimeout(autoSaveTimeout);

        // Mostrar indicador
        showSavingIndicator();

        autoSaveTimeout = setTimeout(() => {
            saveDraft();
        }, 30000); // 30 segundos
    });
});

function showSavingIndicator() {
    const indicator = document.getElementById('saveIndicator');
    indicator.innerHTML = '<i class="bi bi-clock text-warning"></i> Salvamento automático pendente...';
}

function saveDraft() {
    const formData = new FormData(document.getElementById('myForm'));
    const indicator = document.getElementById('saveIndicator');

    indicator.innerHTML = '<i class="bi bi-arrow-repeat text-primary"></i> Salvando rascunho...';

    fetch('/api/save-draft', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        indicator.innerHTML = '<i class="bi bi-check-circle text-success"></i> Rascunho salvo às ' +
                              new Date().toLocaleTimeString();

        // Esconder após 3 segundos
        setTimeout(() => {
            indicator.innerHTML = '';
        }, 3000);
    })
    .catch(error => {
        indicator.innerHTML = '<i class="bi bi-x-circle text-danger"></i> Erro ao salvar';
    });
}

// Salvar antes de sair da página
window.addEventListener('beforeunload', (e) => {
    if (document.querySelector('form').dataset.modified === 'true') {
        e.preventDefault();
        e.returnValue = 'Você tem alterações não salvas. Deseja realmente sair?';
    }
});
```

---

## 🚫 Empty States

### Lista Vazia

```html
<div class="empty-state text-center py-5">
    <i class="bi bi-inbox" style="font-size: 4rem; color: var(--bs-secondary);"></i>
    <h3 class="mt-3">Nenhum relatório encontrado</h3>
    <p class="text-muted mb-4">
        Comece criando seu primeiro relatório de prova de modelagem
    </p>
    <a href="/novo-relatorio" class="btn btn-primary btn-lg">
        <i class="bi bi-plus-circle"></i>
        Criar Primeiro Relatório
    </a>
</div>
```

---

### Busca Sem Resultados

```html
<div class="no-results text-center py-5">
    <i class="bi bi-search" style="font-size: 4rem; color: var(--bs-secondary);"></i>
    <h3 class="mt-3">Nenhum resultado encontrado</h3>
    <p class="text-muted mb-4">
        Tente usar palavras-chave diferentes ou <a href="#" onclick="clearSearch()">limpar os filtros</a>
    </p>

    <div class="suggestions">
        <p class="small text-muted mb-2">Sugestões:</p>
        <div class="d-flex flex-wrap gap-2 justify-content-center">
            <button class="btn btn-sm btn-outline-secondary" onclick="search('Verão')">Verão</button>
            <button class="btn btn-sm btn-outline-secondary" onclick="search('Kids')">Kids</button>
            <button class="btn btn-sm btn-outline-secondary" onclick="search('Aprovada')">Aprovada</button>
        </div>
    </div>
</div>
```

---

## ⚠️ Error Handling

### Erro de Rede (Offline)

```javascript
window.addEventListener('offline', () => {
    showToast('Você está offline. Algumas funcionalidades podem não funcionar.', 'warning');

    // Mostrar banner
    const banner = document.createElement('div');
    banner.id = 'offlineBanner';
    banner.className = 'alert alert-warning alert-dismissible fixed-top m-0 rounded-0';
    banner.innerHTML = `
        <i class="bi bi-wifi-off"></i>
        <strong>Sem conexão com a internet.</strong> Verifique sua rede.
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.prepend(banner);
});

window.addEventListener('online', () => {
    showToast('Conexão restaurada!', 'success');

    const banner = document.getElementById('offlineBanner');
    if (banner) banner.remove();
});
```

---

### Erro 404 Friendly

```html
<div class="error-page text-center py-5">
    <div class="error-code" style="font-size: 8rem; font-weight: 700; color: var(--bs-primary);">
        404
    </div>
    <h1 class="mt-3">Página não encontrada</h1>
    <p class="lead text-muted mb-4">
        A página que você procura não existe ou foi movida
    </p>

    <div class="d-flex gap-2 justify-content-center">
        <a href="/dashboard" class="btn btn-primary">
            <i class="bi bi-house"></i>
            Ir para Dashboard
        </a>
        <button onclick="history.back()" class="btn btn-outline-secondary">
            <i class="bi bi-arrow-left"></i>
            Voltar
        </button>
    </div>

    <div class="mt-5">
        <p class="small text-muted">Links úteis:</p>
        <div class="d-flex flex-wrap gap-2 justify-content-center">
            <a href="/novo-relatorio" class="btn btn-sm btn-link">Novo Relatório</a>
            <a href="/analytics" class="btn btn-sm btn-link">Analytics</a>
            <a href="/auditoria" class="btn btn-sm btn-link">Auditoria</a>
        </div>
    </div>
</div>
```

---

## ♿ Acessibilidade

### Skip to Content

```html
<!-- Primeiro elemento do body -->
<a href="#main-content" class="skip-to-content">
    Pular para conteúdo principal
</a>

<style>
.skip-to-content {
    position: absolute;
    top: -40px;
    left: 0;
    background: var(--bs-primary);
    color: white;
    padding: 8px 16px;
    text-decoration: none;
    z-index: 10000;
}

.skip-to-content:focus {
    top: 0;
}
</style>

<main id="main-content" tabindex="-1">
    <!-- Conteúdo principal -->
</main>
```

---

### Labels e ARIA

```html
<!-- Sempre usar labels -->
<label for="busca">Buscar relatórios</label>
<input type="search" id="busca" name="busca" placeholder="Digite para buscar...">

<!-- ARIA para elementos dinâmicos -->
<div role="alert" aria-live="polite" id="searchResults">
    10 resultados encontrados
</div>

<!-- ARIA para botões com apenas ícone -->
<button class="btn btn-primary" aria-label="Editar relatório">
    <i class="bi bi-pencil" aria-hidden="true"></i>
</button>

<!-- Loading states -->
<button class="btn btn-primary" aria-busy="true" disabled>
    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    <span class="visually-hidden">Carregando...</span>
    Carregando
</button>
```

---

### Navegação por Teclado

```javascript
// Trap focus dentro de modal
const modal = document.getElementById('myModal');
const focusableElements = modal.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
);

const firstFocusable = focusableElements[0];
const lastFocusable = focusableElements[focusableElements.length - 1];

modal.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
        if (e.shiftKey) {
            // Shift + Tab
            if (document.activeElement === firstFocusable) {
                lastFocusable.focus();
                e.preventDefault();
            }
        } else {
            // Tab
            if (document.activeElement === lastFocusable) {
                firstFocusable.focus();
                e.preventDefault();
            }
        }
    }

    // Fechar modal com ESC
    if (e.key === 'Escape') {
        bootstrap.Modal.getInstance(modal).hide();
    }
});

// Focar primeiro elemento ao abrir
modal.addEventListener('shown.bs.modal', () => {
    firstFocusable.focus();
});
```

---

## 📱 Mobile First

### Touch-Friendly Buttons

```css
/* Tamanho mínimo de toque: 44x44px (WCAG 2.1) */
.btn-sm {
    min-height: 44px;
    min-width: 44px;
    padding: 0.5rem 1rem;
}

/* Espaçamento em listas mobile */
@media (max-width: 768px) {
    .btn-group .btn {
        display: block;
        width: 100%;
        margin-bottom: 0.5rem;
    }
}
```

---

### Responsive Tables

```html
<!-- Desktop: tabela normal -->
<!-- Mobile: cards -->
<div class="table-responsive">
    <table class="table mobile-table">
        <thead>
            <tr>
                <th>Coleção</th>
                <th>Status</th>
                <th>Data</th>
                <th>Ações</th>
            </tr>
        </thead>
        <tbody>
            {% for rel in relatorios %}
            <tr>
                <td data-label="Coleção">{{ rel.colecao }}</td>
                <td data-label="Status">
                    <span class="badge bg-success">{{ rel.status }}</span>
                </td>
                <td data-label="Data">{{ rel.created_at|date }}</td>
                <td data-label="Ações">
                    <a href="{{ url_for('detalhes', id=rel.id) }}" class="btn btn-sm btn-primary">Ver</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

<style>
@media (max-width: 768px) {
    .mobile-table thead {
        display: none;
    }

    .mobile-table tr {
        display: block;
        margin-bottom: 1rem;
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        padding: 1rem;
    }

    .mobile-table td {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border: none;
    }

    .mobile-table td::before {
        content: attr(data-label);
        font-weight: 600;
        flex: 0 0 40%;
    }
}
</style>
```

---

## 🔗 Links Relacionados

- **[Components](COMPONENTS.md)** - Biblioteca de componentes
- **[Design System](DESIGN_SYSTEM.md)** - Tokens e fundamentos
- **[Accessibility Guide](../../GUIA_TESTES_ACESSIBILIDADE.md)** - Testes de acessibilidade

---

**[⬅ Voltar ao Índice](../INDEX.md)**
