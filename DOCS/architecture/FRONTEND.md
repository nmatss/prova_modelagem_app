# ARQUITETURA FRONTEND - PROVA DE MODELAGEM APP

## Índice

1. [Visão Geral](#visão-geral)
2. [Estrutura de Templates](#estrutura-de-templates)
3. [Design System](#design-system)
4. [Componentes CSS](#componentes-css)
5. [Sistema de Navegação](#sistema-de-navegação)
6. [JavaScript Modular](#javascript-modular)
7. [Responsividade](#responsividade)
8. [Acessibilidade](#acessibilidade)
9. [Performance](#performance)
10. [Padrões de UX/UI](#padrões-de-uxui)

---

## Visão Geral

O frontend do **Prova de Modelagem App** foi desenvolvido com foco em:

- **Mobile First**: Design responsivo com prioridade para dispositivos móveis
- **Design System**: Sistema de design consistente com tokens reutilizáveis
- **Acessibilidade**: WCAG 2.1 AA compliance
- **Performance**: Lazy loading, minificação e otimizações
- **Modularidade**: Código JavaScript organizado e reutilizável
- **UX Moderna**: Interface clean, profissional e intuitiva

### Stack Tecnológica

- **Framework CSS**: Bootstrap 5.3.0
- **Ícones**: Bootstrap Icons 1.11.0
- **Fonte**: Google Fonts - Inter (300-800)
- **Charts**: Chart.js v4.4.0 (lazy loaded)
- **JavaScript**: Vanilla JS (ES6+) modular

---

## Estrutura de Templates

### Hierarquia de Templates (Jinja2)

```
templates/
├── base.html                    # Template base (herança)
├── login.html                   # Página de login (sem sidebar)
├── dashboard.html               # Dashboard principal
├── analytics.html               # Analytics e gráficos
├── novo_relatorio.html          # Wizard multi-step
├── editar_relatorio.html        # Edição de relatório
├── detalhes_relatorio.html      # Visualização detalhada
├── alterar_senha.html           # Alteração de senha
├── esqueci_senha.html           # Recuperação de senha
├── reset_senha.html             # Reset de senha
├── logs.html                    # Logs de auditoria
├── admin/
│   ├── dashboard.html           # Dashboard admin
│   ├── users.html               # Gerenciamento de usuários
│   ├── create_user.html         # Criar usuário
│   ├── edit_user.html           # Editar usuário
│   └── change_password.html     # Alterar senha (admin)
├── audit/
│   ├── index.html               # Logs de auditoria
│   ├── timeline.html            # Timeline de eventos
│   ├── estatisticas.html        # Estatísticas
│   ├── por_usuario.html         # Logs por usuário
│   └── detalhes.html            # Detalhes de log
├── errors/
│   ├── 403.html                 # Forbidden
│   ├── 404.html                 # Not Found
│   ├── 413.html                 # Payload Too Large
│   ├── 429.html                 # Too Many Requests
│   └── 500.html                 # Internal Server Error
└── relatorio_pdf.html           # Template para PDF
```

### Template Base (base.html)

O `base.html` é o template pai que define a estrutura comum:

#### Seções Principais

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <!-- Meta tags, favicon, fonts -->
    <!-- CSS (ordem otimizada) -->
    {% block styles %}{% endblock %}
</head>
<body>
    <!-- Skip Link (acessibilidade) -->
    <a href="#main-content" class="skip-link">Pular para o conteúdo principal</a>

    {% if current_user.is_authenticated %}
        <!-- App Wrapper -->
        <div class="app-wrapper">
            <!-- Sidebar -->
            <aside class="sidebar" id="sidebar">...</aside>

            <!-- Sidebar Backdrop (Mobile) -->
            <div class="sidebar-backdrop" id="sidebarBackdrop"></div>

            <!-- Main Wrapper -->
            <div class="main-wrapper">
                <!-- Top Header -->
                <header class="top-header">
                    <!-- Breadcrumbs -->
                    {% block breadcrumb %}{% endblock %}
                    <!-- User Actions -->
                </header>

                <!-- Content Wrapper -->
                <main class="content-wrapper" id="main-content">
                    <!-- Flash Messages -->
                    <!-- Page Content -->
                    {% block main_content %}{% endblock %}
                </main>
            </div>

            <!-- Bottom Navigation (Mobile Only) -->
            <nav class="bottom-nav">...</nav>
        </div>
    {% else %}
        <!-- Login Page (Without Sidebar) -->
        <main class="main-container">
            {% block login_content %}{% endblock %}
        </main>
    {% endif %}

    <!-- Modals Block -->
    {% block modals %}{% endblock %}

    <!-- JavaScript (ordem otimizada) -->
    {% block scripts %}{% endblock %}
</body>
</html>
```

#### Ordem de Carregamento CSS

```html
<!-- 1. Design System (Tokens e variáveis base) -->
<link rel="stylesheet" href="css/design-system.css">

<!-- 2. Components Library (Componentes reutilizáveis) -->
<link rel="stylesheet" href="css/components.css">

<!-- 3. Navigation (Sidebar e menus) -->
<link rel="stylesheet" href="css/navigation.css">

<!-- 4. Feature-specific -->
<link rel="stylesheet" href="css/wizard.css">
<link rel="stylesheet" href="css/table.css">
<link rel="stylesheet" href="css/file-upload.css">

<!-- 5. Responsiveness & Mobile -->
<link rel="stylesheet" href="css/mobile.css">

<!-- 6. Accessibility (WCAG 2.1 AA) -->
<link rel="stylesheet" href="css/accessibility.css">

<!-- 7. Custom overrides (última prioridade) -->
<link rel="stylesheet" href="css/custom.css">

<!-- 8. Base styles (extracted inline CSS) -->
<link rel="stylesheet" href="css/base-styles.css">
```

#### Ordem de Carregamento JavaScript

```html
<!-- 1. Third-party Libraries (Critical) -->
<script src="bootstrap.bundle.min.js"></script>

<!-- 2. Configuration & Data -->
<script src="js/charts-config.js"></script>

<!-- 3. Core Features -->
<script src="js/accessibility.js"></script>
<script src="js/date-picker.js"></script>

<!-- 4. Legacy App.js (compatibilidade) -->
<script src="js/app.js"></script>
<script src="js/main.js"></script>

<!-- 5. Feature Modules (lazy loaded) -->
<script src="js/wizard.js" defer></script>
<script src="js/file-upload.js" defer></script>
<script src="js/datatable.js" defer></script>

<!-- 6. Performance & Monitoring -->
<script src="js/lazy-chart-loader.js"></script>
<script src="js/lazy-loading.js" defer></script>

<!-- 7. App Initialization (Último) -->
<script src="js/app-init.js" defer></script>
```

---

## Design System

### Arquivo: `static/css/design-system.css`

Sistema completo de design tokens centralizados.

### 1. Design Tokens - Core Foundation

#### Cores Primárias

```css
:root {
    /* PRIMARY COLORS - Rosa Puket */
    --primary: #E6007E;              /* Rosa principal */
    --primary-50: #FFF0F7;           /* Ultra light */
    --primary-100: #FFE0F0;          /* Very light */
    --primary-200: #FFC2E0;
    --primary-300: #FF99CF;
    --primary-400: #FF66B8;
    --primary-500: #E6007E;          /* Base */
    --primary-600: #C2008E;
    --primary-700: #9E006F;
    --primary-800: #7A0050;
    --primary-900: #560031;

    /* Legacy support */
    --primary-hover: var(--primary-600);
    --primary-light: var(--primary-100);
    --cor-puket-rosa: var(--primary);
}
```

#### Cores Secundárias (WCAG 2.1 AA Compliant)

```css
--secondary: #475569;            /* Slate gray */
--secondary-50: #F8FAFC;
--secondary-100: #F1F5F9;
/* ... */
--secondary-600: #334155;        /* 12.31:1 contrast */
--secondary-700: #1E293B;        /* 15.72:1 contrast */
--secondary-800: #0F172A;        /* 18.35:1 contrast */
```

#### Cores Semânticas

```css
/* Success - Green */
--success: #10B981;
--success-hover: var(--success-600);
--cor-aprovada: var(--success);

/* Error/Danger - Red */
--error: #EF4444;
--danger: var(--error);
--cor-reprovada: var(--error);

/* Warning - Amber */
--warning: #F59E0B;
--cor-comite: var(--warning);

/* Info - Cyan */
--info: #06B6D4;
--cor-andamento: var(--info);
```

#### Escala de Cinzas (WCAG Compliant)

```css
--gray-50: #F9FAFB;
--gray-100: #F3F4F6;
--gray-400: #6B7280;        /* 4.54:1 contrast */
--gray-500: #4B5563;        /* 7.54:1 contrast */
--gray-600: #374151;        /* 10.69:1 contrast */
--gray-700: #1F2937;        /* 14.76:1 contrast */
--gray-800: #111827;        /* 17.44:1 contrast */
--gray-900: #030712;        /* 19.82:1 contrast */
```

### 2. Tipografia

```css
/* Font Families */
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--font-mono: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace;

/* Font Sizes */
--text-xs: 0.75rem;      /* 12px */
--text-sm: 0.875rem;     /* 14px */
--text-base: 1rem;       /* 16px */
--text-lg: 1.125rem;     /* 18px */
--text-xl: 1.25rem;      /* 20px */
--text-2xl: 1.5rem;      /* 24px */
--text-3xl: 1.875rem;    /* 30px */
--text-4xl: 2.25rem;     /* 36px */

/* Font Weights */
--font-light: 300;
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
--font-extrabold: 800;

/* Line Heights */
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.625;
```

### 3. Espaçamento (Base: 4px)

```css
--space-0: 0;
--space-1: 0.25rem;      /* 4px */
--space-2: 0.5rem;       /* 8px */
--space-3: 0.75rem;      /* 12px */
--space-4: 1rem;         /* 16px */
--space-5: 1.25rem;      /* 20px */
--space-6: 1.5rem;       /* 24px */
--space-8: 2rem;         /* 32px */
--space-12: 3rem;        /* 48px */
--space-16: 4rem;        /* 64px */
```

### 4. Border Radius

```css
--radius-sm: 0.25rem;    /* 4px */
--radius-md: 0.5rem;     /* 8px */
--radius-lg: 0.75rem;    /* 12px */
--radius-xl: 1rem;       /* 16px */
--radius-2xl: 1.5rem;    /* 24px */
--radius-full: 9999px;   /* Circle */
```

### 5. Sombras (Elevation)

```css
--shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
--shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);

/* Colored shadows */
--shadow-primary: 0 10px 20px -5px rgba(230, 0, 126, 0.3);
--shadow-success: 0 10px 20px -5px rgba(16, 185, 129, 0.3);
```

### 6. Transições

```css
--duration-150: 150ms;
--duration-200: 200ms;
--duration-300: 300ms;

--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);

--transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-slow: 350ms cubic-bezier(0.4, 0, 0.2, 1);
```

### 7. Z-Index Layers

```css
--z-base: 0;
--z-dropdown: 1000;
--z-sticky: 1020;
--z-fixed: 1030;
--z-overlay: 1040;
--z-modal-backdrop: 1050;
--z-modal: 1055;
--z-popover: 1060;
--z-tooltip: 1070;
--z-notification: 1080;
--z-max: 9999;
```

### 8. Breakpoints

```css
--breakpoint-xs: 0;
--breakpoint-sm: 576px;
--breakpoint-md: 768px;
--breakpoint-lg: 992px;
--breakpoint-xl: 1200px;
--breakpoint-2xl: 1400px;
--breakpoint-3xl: 1600px;
```

---

## Componentes CSS

### Arquivo: `static/css/components.css`

Biblioteca completa de componentes reutilizáveis.

### 1. Botões

#### Variantes

```css
.btn-primary     /* Gradiente rosa */
.btn-secondary   /* Cinza */
.btn-success     /* Verde */
.btn-error       /* Vermelho */
.btn-warning     /* Amarelo */
.btn-info        /* Azul */

/* Outline */
.btn-outline-primary
.btn-outline-secondary

/* Ghost */
.btn-ghost       /* Transparente */
```

#### Tamanhos

```css
.btn-xs          /* 28px */
.btn-sm          /* 32px */
.btn             /* 40px (padrão) */
.btn-lg          /* 48px */
.btn-xl          /* 56px */
```

#### Variações

```css
.btn-rounded     /* Border radius full */
.btn-square      /* Border radius 0 */
.btn-icon        /* Botão quadrado com ícone */
```

#### Estados de Loading

```css
.btn-loading     /* Estado de carregamento */

/* Uso em JavaScript */
setButtonLoading(button, true, 'Salvando...');
setButtonLoading(button, false);
```

### 2. Form Controls

#### Input Básico

```css
.form-control {
    width: 100%;
    height: 40px;
    padding: 0 var(--space-4);
    border: 2px solid var(--gray-300);
    border-radius: var(--radius-md);
    transition: var(--transition-base);
}

.form-control:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px var(--primary-light);
}
```

#### Estados

```css
.form-control.is-invalid    /* Borda vermelha + ícone */
.form-control.is-valid      /* Borda verde + ícone */
.form-control:disabled      /* Background cinza */
```

#### Tamanhos

```css
.form-control-sm    /* 32px */
.form-control       /* 40px */
.form-control-lg    /* 48px */
```

#### Checkbox & Radio

```css
.form-check
.form-check-input
.form-check-label

/* Switch */
.form-switch
.form-switch-input
.form-switch-label
```

### 3. Cards

```css
.card {
    background: white;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    padding: var(--space-6);
    transition: var(--transition-base);
}

.card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}

/* Variantes */
.card-flat       /* Sem sombra */
.card-elevated   /* Sombra maior */

/* Tamanhos */
.card-sm         /* Padding menor */
.card-lg         /* Padding maior */

/* Partes */
.card-header
.card-body
.card-footer
.card-title
.card-subtitle
```

### 4. Badges

```css
.badge {
    display: inline-flex;
    padding: var(--space-1) var(--space-3);
    border-radius: var(--radius-full);
    font-size: var(--text-xs);
    font-weight: 600;
}

/* Variantes */
.badge-primary
.badge-success
.badge-error
.badge-warning
.badge-info

/* Solid */
.badge-solid-primary
.badge-solid-success

/* Com ícone */
.badge-dot
.badge-icon
```

### 5. Alerts & Toasts

```css
.alert {
    padding: var(--space-4);
    border-radius: var(--radius-lg);
    border-left: 4px solid;
    display: flex;
    gap: var(--space-3);
}

.alert-success
.alert-error
.alert-warning
.alert-info

/* Toasts */
.toast-container    /* Fixed top-right */
.toast
.toast-success
.toast-error
```

### 6. Loading States

#### Spinners

```css
.spinner         /* 24px padrão */
.spinner-sm      /* 16px */
.spinner-lg      /* 32px */
.spinner-xl      /* 48px */

/* Cores */
.spinner-primary
.spinner-success
.spinner-white
```

#### Skeleton Loaders

```css
.skeleton
.skeleton-text
.skeleton-title
.skeleton-avatar
.skeleton-button
.skeleton-card
```

#### Loading Overlay

```css
.loading-overlay    /* Full screen */
.loading-container  /* Inline */

/* Uso em JavaScript */
showLoading();
hideLoading();
showSpinner(container, 'md', 'primary', 'Carregando...');
```

### 7. Progress Bar

```css
.progress
.progress-bar
.progress-bar-striped
.progress-bar-animated

.progress-sm     /* 4px */
.progress        /* 8px */
.progress-lg     /* 12px */
```

---

## Sistema de Navegação

### Arquivos:
- `static/css/navigation.css`
- `static/css/mobile.css`

### 1. Sidebar (Desktop)

#### Estrutura

```html
<aside class="sidebar" id="sidebar">
    <!-- Header -->
    <div class="sidebar-header">
        <a href="/" class="sidebar-logo">
            <img src="logo.png" alt="Logo">
            <span class="sidebar-logo-text">Puket</span>
        </a>
    </div>

    <!-- Toggle Button -->
    <button class="sidebar-toggle-btn" id="sidebarToggle">
        <span class="toggle-icon">
            <i class="bi bi-chevron-bar-left"></i>
        </span>
    </button>

    <!-- Menu -->
    <nav class="sidebar-menu">
        <div class="menu-item">
            <a href="/" class="menu-link active">
                <i class="bi bi-house-door-fill"></i>
                <span class="menu-link-text">Início</span>
            </a>
        </div>
        <!-- ... -->
    </nav>

    <!-- Footer -->
    <div class="sidebar-footer">
        <a href="/perfil" class="user-profile">
            <div class="user-avatar">U</div>
            <div class="user-info">
                <span class="user-name">Username</span>
                <span class="user-role">Usuário</span>
            </div>
        </a>
    </div>
</aside>
```

#### Estados

```css
/* Normal: 260px */
.sidebar {
    width: var(--sidebar-width);
}

/* Collapsed: 60px */
.sidebar.collapsed {
    width: var(--sidebar-collapsed-width);
}

/* Mobile: Overlay */
@media (max-width: 992px) {
    .sidebar {
        transform: translateX(-100%);
    }

    .sidebar.mobile-open {
        transform: translateX(0);
    }
}
```

#### Botão de Toggle

```css
.sidebar-toggle-btn {
    position: absolute;
    top: 16px;
    right: -20px;
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: 3px solid white;
    border-radius: 50%;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.sidebar-toggle-btn:hover {
    transform: scale(1.1);
}

/* Animação de pulsação */
.sidebar-toggle-btn.pulse {
    animation: pulse 2s infinite;
}
```

#### Persistência com localStorage

```javascript
// Salvar estado
localStorage.setItem('sidebarCollapsed', 'true');

// Restaurar estado
const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
if (isCollapsed) {
    sidebar.classList.add('collapsed');
}
```

### 2. Top Header

```html
<header class="top-header">
    <!-- Breadcrumbs -->
    <div class="breadcrumb-nav">
        <button class="mobile-menu-toggle" id="mobileMenuToggle">
            <i class="bi bi-list"></i>
        </button>
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item">
                    <a href="/">Home</a>
                </li>
                <li class="breadcrumb-item active">Dashboard</li>
            </ol>
        </nav>
    </div>

    <!-- User Actions -->
    <div class="header-actions">
        <a href="/logout" class="btn-logout">
            <i class="bi bi-box-arrow-right"></i>
            <span>Sair</span>
        </a>
    </div>
</header>
```

### 3. Bottom Navigation (Mobile Only)

Visível apenas em telas < 640px.

```html
<nav class="bottom-nav">
    <a href="/" class="bottom-nav-item active">
        <i class="bi bi-house-fill"></i>
        <span>Home</span>
    </a>
    <a href="/analytics" class="bottom-nav-item">
        <i class="bi bi-graph-up-arrow"></i>
        <span>Analytics</span>
    </a>
    <a href="/novo" class="bottom-nav-item bottom-nav-item-primary">
        <i class="bi bi-plus-circle-fill"></i>
    </a>
    <a href="/usuarios" class="bottom-nav-item">
        <i class="bi bi-people-fill"></i>
        <span>Usuários</span>
    </a>
    <a href="/perfil" class="bottom-nav-item">
        <i class="bi bi-key-fill"></i>
        <span>Perfil</span>
    </a>
</nav>
```

#### Características

- **Fixo no rodapé**: `position: fixed; bottom: 0;`
- **5 itens**: Home, Analytics, Ação Principal, Usuários, Perfil
- **Botão Central Destacado**: Círculo elevado com gradiente
- **Touch-friendly**: Min-height 44px
- **Z-index**: 1000 (abaixo de modais)

---

## JavaScript Modular

### Arquivos Principais

```
static/js/
├── app.js                   # UX enhancements (loading, validação)
├── main.js                  # Inicialização geral
├── app-init.js              # Orquestração final
├── accessibility.js         # Recursos de acessibilidade
├── charts-config.js         # Configuração Chart.js
├── wizard.js                # Wizard multi-step
├── file-upload.js           # Upload de arquivos
├── datatable.js             # Tabelas dinâmicas
├── date-picker.js           # Date pickers
├── lazy-loading.js          # Lazy loading de imagens
└── lazy-chart-loader.js     # Lazy loading de Chart.js
```

### 1. App.js - UX Enhancements

#### Loading Overlay

```javascript
// Criar overlay
function createLoadingOverlay() { ... }

// Mostrar loading
function showLoading() {
    if (document.querySelector('.modal.show')) {
        return; // Não mostrar se modal aberto
    }
    document.getElementById('loadingOverlay').classList.add('show');
}

// Esconder loading
function hideLoading() {
    document.getElementById('loadingOverlay').classList.remove('show');
}

// Uso
showLoading();
// ... operação assíncrona
hideLoading();
```

#### Button Loading States

```javascript
/**
 * @param {HTMLElement|string} button
 * @param {boolean} loading
 * @param {string} loadingText
 */
function setButtonLoading(button, loading, loadingText = null) {
    const btn = typeof button === 'string'
        ? document.querySelector(button)
        : button;

    if (loading) {
        btn.dataset.originalText = btn.innerHTML;
        btn.disabled = true;
        btn.classList.add('btn-loading');
        if (loadingText) btn.innerHTML = loadingText;
    } else {
        btn.classList.remove('btn-loading');
        btn.disabled = false;
        btn.innerHTML = btn.dataset.originalText;
    }
}

// Uso
const btn = document.querySelector('#submitBtn');
setButtonLoading(btn, true, 'Salvando...');
// ... operação
setButtonLoading(btn, false);
```

#### Validação de Formulários

```javascript
// Adicionar asterisco em campos obrigatórios
document.querySelectorAll('[required]').forEach(field => {
    const label = field.previousElementSibling;
    if (label && label.tagName === 'LABEL') {
        label.innerHTML += ' <span class="text-danger">*</span>';
    }
});

// Validação em tempo real
field.addEventListener('blur', function() {
    if (this.hasAttribute('required') && !this.value.trim()) {
        this.classList.add('is-invalid');
    } else {
        this.classList.remove('is-invalid');
        this.classList.add('is-valid');
    }
});
```

#### Tooltips Bootstrap 5

```javascript
// Inicializar todos os tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(el =>
    new bootstrap.Tooltip(el, {
        delay: { show: 500, hide: 100 },
        placement: 'top',
        trigger: 'hover focus',
        boundary: 'viewport'
    })
);

// Tooltips específicos da sidebar (só mostrar quando collapsed)
const sidebar = document.getElementById('sidebar');
if (sidebar) {
    const sidebarTooltips = sidebar.querySelectorAll('[data-bs-toggle="tooltip"]');
    sidebarTooltips.forEach(el => {
        const tooltip = bootstrap.Tooltip.getInstance(el);
        if (tooltip) {
            el.addEventListener('mouseenter', function() {
                if (!sidebar.classList.contains('collapsed') || window.innerWidth < 992) {
                    tooltip.disable();
                } else {
                    tooltip.enable();
                }
            });
        }
    });
}
```

#### Outros Recursos

```javascript
// Auto-dismiss alerts (5 segundos)
document.querySelectorAll('.alert:not(.alert-permanent)').forEach(alert => {
    setTimeout(() => new bootstrap.Alert(alert).close(), 5000);
});

// Confirmação de ações perigosas
document.querySelectorAll('[data-confirm]').forEach(element => {
    element.addEventListener('click', function(e) {
        const message = this.getAttribute('data-confirm') || 'Tem certeza?';
        if (!confirm(message)) {
            e.preventDefault();
            return false;
        }
    });
});

// Preview de imagem
input.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
            previewContainer.innerHTML = `<img src="${e.target.result}" class="image-preview">`;
        };
        reader.readAsDataURL(file);
    }
});

// Scroll to top button
window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        scrollTopBtn.style.display = 'block';
    } else {
        scrollTopBtn.style.display = 'none';
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + S para salvar
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        document.querySelector('form [type="submit"]')?.click();
    }

    // ESC para fechar modais
    if (e.key === 'Escape') {
        const modal = bootstrap.Modal.getInstance(document.querySelector('.modal.show'));
        modal?.hide();
    }
});
```

### 2. Wizard.js - Multi-Step Forms

```javascript
class ReportWizard {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 5;
        this.formData = this.loadFromStorage() || {};
        this.init();
    }

    init() {
        this.setupElements();
        this.setupEventListeners();
        this.updateProgress();
        this.restoreFormData();
        this.setupAutoSave();
    }

    nextStep() {
        if (this.validateCurrentStep()) {
            this.markStepAsCompleted(this.currentStep);
            this.saveToStorage();
            if (this.currentStep < this.totalSteps) {
                this.currentStep++;
                this.updateProgress();
            }
        }
    }

    previousStep() {
        if (this.currentStep > 1) {
            this.currentStep--;
            this.updateProgress();
        }
    }

    validateCurrentStep() {
        // Validação específica por step
        switch(this.currentStep) {
            case 1: return this.validateStep1();
            case 2: return this.validateStep2();
            // ...
        }
    }

    saveToStorage() {
        const data = {
            ...this.formData,
            currentStep: this.currentStep,
            timestamp: new Date().toISOString()
        };
        localStorage.setItem('wizard_draft', JSON.stringify(data));
    }

    loadFromStorage() {
        const stored = localStorage.getItem('wizard_draft');
        if (stored) {
            const data = JSON.parse(stored);
            // Verificar se não é muito antigo (24h)
            const hoursDiff = (new Date() - new Date(data.timestamp)) / (1000 * 60 * 60);
            if (hoursDiff < 24) return data;
            localStorage.removeItem('wizard_draft');
        }
        return null;
    }

    setupAutoSave() {
        // Auto-save a cada 30 segundos
        setInterval(() => this.saveToStorage(), 30000);
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('wizardForm')) {
        window.reportWizard = new ReportWizard();
    }
});
```

### 3. Charts-config.js - Chart.js

```javascript
// Configuração global
const CHART_COLORS = {
    primary: '#E600AA',
    success: '#22C55E',
    danger: '#EF4444',
    warning: '#F59E0B',
    info: '#3B82F6'
};

const STATUS_COLORS = {
    'Aprovada': CHART_COLORS.success,
    'Reprovada': CHART_COLORS.danger,
    'Em Andamento': CHART_COLORS.warning,
    'Comitê': CHART_COLORS.info
};

// Função helper para criar gráfico de pizza
function createStatusChart(canvasId, data, type = 'doughnut') {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx, {
        type: type,
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: data.labels.map(label => STATUS_COLORS[label] || CHART_COLORS.gray)
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Função helper para gráfico de barras
function createBarChart(canvasId, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: data.label,
                data: data.values,
                backgroundColor: CHART_COLORS.primary
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
```

### 4. Accessibility.js

```javascript
// Gerenciar foco em modais
document.addEventListener('shown.bs.modal', function(e) {
    const modal = e.target;
    const firstFocusable = modal.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    firstFocusable?.focus();
});

// Trap focus dentro de modais
function trapFocus(element) {
    const focusableElements = element.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];

    element.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            if (e.shiftKey && document.activeElement === firstFocusable) {
                lastFocusable.focus();
                e.preventDefault();
            } else if (!e.shiftKey && document.activeElement === lastFocusable) {
                firstFocusable.focus();
                e.preventDefault();
            }
        }
    });
}

// Anúncios para screen readers
function announceToScreenReader(message, priority = 'polite') {
    const announcement = document.createElement('div');
    announcement.setAttribute('role', priority === 'assertive' ? 'alert' : 'status');
    announcement.setAttribute('aria-live', priority);
    announcement.classList.add('sr-only');
    announcement.textContent = message;
    document.body.appendChild(announcement);

    setTimeout(() => announcement.remove(), 1000);
}

// Uso
announceToScreenReader('Formulário enviado com sucesso', 'polite');
announceToScreenReader('Erro ao processar', 'assertive');
```

---

## Responsividade

### Breakpoints System

```css
/* Mobile First Approach */

/* Base Mobile (< 576px) */
@media (max-width: 575px) {
    body { font-size: 0.9375rem; }
    .btn { min-height: 48px; width: 100%; }
    .form-control { font-size: 16px; } /* Previne zoom no iOS */
}

/* Mobile Large (576px - 767px) */
@media (min-width: 576px) and (max-width: 767px) {
    .stats-grid { grid-template-columns: repeat(2, 1fr); }
}

/* Tablet Portrait (768px - 991px) */
@media (min-width: 768px) and (max-width: 991px) {
    .stats-grid { grid-template-columns: repeat(2, 1fr); }
}

/* Tablet Landscape & Desktop (992px+) */
@media (min-width: 992px) {
    .sidebar { transform: translateX(0); }
    .bottom-nav { display: none; }
}

/* Desktop (1200px+) */
@media (min-width: 1200px) {
    .stats-grid { grid-template-columns: repeat(4, 1fr); }
}

/* Large Desktop (1400px+) */
@media (min-width: 1401px) {
    .container { max-width: 1600px; }
}
```

### Mobile-Specific Features

#### Bottom Navigation

```css
@media (max-width: 639px) {
    .bottom-nav { display: flex; }
    body { padding-bottom: 80px; }
}
```

#### Touch Targets

```css
/* WCAG: Mínimo 44x44px para elementos tocáveis */
:root {
    --touch-target-min: 44px;
    --touch-target-comfortable: 48px;
}

@media (max-width: 639px) {
    .btn { min-height: var(--touch-target-comfortable); }
    .form-check { min-height: var(--touch-target-min); }
}
```

#### Tables Responsive

```css
/* Opção 1: Cards em mobile */
@media (max-width: 639px) {
    .table thead { display: none; }
    .table tr { display: block; margin-bottom: 1rem; }
    .table td {
        display: block;
        padding-left: 50%;
        position: relative;
    }
    .table td::before {
        content: attr(data-label);
        position: absolute;
        left: 0.5rem;
        font-weight: 600;
    }
}

/* Opção 2: Scroll horizontal */
.table-scroll-mobile {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}
```

#### Modals Full Screen

```css
@media (max-width: 639px) {
    .modal-fullscreen-sm-down {
        max-width: 100%;
        margin: 0;
        height: 100vh;
    }

    .modal-fullscreen-sm-down .modal-content {
        height: 100%;
        border-radius: 0;
    }
}
```

---

## Acessibilidade

### WCAG 2.1 AA Compliance

#### 1. Cores e Contraste

Todas as cores atendem a razão de contraste mínima de **4.5:1** para texto normal e **3:1** para texto grande.

```css
/* Texto normal: mínimo 4.5:1 */
--gray-500: #4B5563;        /* 7.54:1 ✓ */
--gray-600: #374151;        /* 10.69:1 ✓ */
--gray-700: #1F2937;        /* 14.76:1 ✓ */

/* Texto grande (18px+): mínimo 3:1 */
--gray-400: #6B7280;        /* 4.54:1 ✓ */
```

#### 2. Skip Links

```html
<a href="#main-content" class="skip-link">Pular para o conteúdo principal</a>

<style>
.skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: #000;
    color: #fff;
    padding: 8px 16px;
}

.skip-link:focus {
    top: 0;
    outline: 3px solid #fbbf24;
}
</style>
```

#### 3. Focus Indicators

```css
/* Todos os elementos focáveis têm outline visível */
a:focus,
button:focus,
input:focus,
select:focus,
textarea:focus {
    outline: 3px solid #fbbf24;
    outline-offset: 2px;
}
```

#### 4. ARIA Labels

```html
<!-- Sidebar -->
<aside class="sidebar" role="complementary" aria-label="Menu de navegação lateral">
    <nav role="navigation" aria-label="Principal">
        <!-- ... -->
    </nav>
</aside>

<!-- Main Content -->
<main class="content-wrapper" id="main-content" role="main" aria-label="Conteúdo principal">
    <!-- ... -->
</main>

<!-- Buttons -->
<button aria-label="Recolher/Expandir menu" title="Recolher menu">
    <i class="bi bi-chevron-bar-left"></i>
</button>

<!-- Forms -->
<label for="email">Email <span class="sr-only">(obrigatório)</span></label>
<input id="email" type="email" required aria-required="true" aria-describedby="email-help">
<small id="email-help">Digite seu endereço de email</small>
```

#### 5. Screen Reader Only

```css
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
}
```

#### 6. Form Validation

```html
<input
    type="text"
    id="nome"
    required
    aria-required="true"
    aria-invalid="false"
    aria-describedby="nome-error">
<div id="nome-error" class="invalid-feedback" role="alert">
    Campo obrigatório
</div>
```

#### 7. Live Regions

```html
<!-- Anúncios dinâmicos -->
<div role="status" aria-live="polite" aria-atomic="true" class="sr-only">
    Formulário enviado com sucesso
</div>

<!-- Alertas urgentes -->
<div role="alert" aria-live="assertive" aria-atomic="true">
    Erro ao processar requisição
</div>
```

#### 8. Keyboard Navigation

```javascript
// Trap focus em modais
document.addEventListener('shown.bs.modal', function(e) {
    const modal = e.target;
    const focusableElements = modal.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];

    modal.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            if (e.shiftKey && document.activeElement === firstFocusable) {
                lastFocusable.focus();
                e.preventDefault();
            } else if (!e.shiftKey && document.activeElement === lastFocusable) {
                firstFocusable.focus();
                e.preventDefault();
            }
        }
    });
});

// ESC para fechar
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const modal = bootstrap.Modal.getInstance(document.querySelector('.modal.show'));
        modal?.hide();
    }
});
```

#### 9. Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
```

---

## Performance

### 1. CSS Otimização

#### Minificação

Todos os arquivos CSS possuem versões minificadas:

```
design-system.css → design-system.min.css
components.css → components.min.css
navigation.css → navigation.min.css
mobile.css → mobile.min.css
```

#### Critical CSS Inlining

Estilos críticos extraídos para `base-styles.css` (carregado por último para cache).

#### Ordem de Carregamento

```html
<!-- 1. Design System (tokens) -->
<!-- 2. Components (reutilizáveis) -->
<!-- 3. Feature-specific (wizard, tables) -->
<!-- 4. Responsive (mobile) -->
<!-- 5. Accessibility -->
<!-- 6. Custom overrides -->
```

### 2. JavaScript Otimização

#### Lazy Loading de Chart.js

```javascript
// lazy-chart-loader.js
function loadChartJS(callback) {
    if (typeof Chart !== 'undefined') {
        callback();
        return;
    }

    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js';
    script.onload = callback;
    document.head.appendChild(script);
}

// Uso
if (document.querySelector('.chart-container')) {
    loadChartJS(() => {
        createStatusChart('statusChart', chartData);
    });
}
```

#### Defer & Async

```html
<!-- Defer: executar após DOM carregar -->
<script src="js/wizard.js" defer></script>
<script src="js/file-upload.js" defer></script>

<!-- Async: carregar em paralelo -->
<script src="js/analytics.js" async></script>
```

#### Minificação

```
app.js → app.min.js
wizard.js → wizard.min.js
charts-config.js → charts-config.min.js
```

### 3. Imagens

#### Lazy Loading Nativo

```html
<img src="produto.jpg" loading="lazy" alt="Produto">
```

#### WebP com Fallback

```html
<picture>
    <source srcset="produto.webp" type="image/webp">
    <img src="produto.jpg" alt="Produto">
</picture>
```

#### Responsive Images

```html
<img
    src="produto-800.jpg"
    srcset="produto-400.jpg 400w, produto-800.jpg 800w, produto-1200.jpg 1200w"
    sizes="(max-width: 600px) 400px, (max-width: 1000px) 800px, 1200px"
    alt="Produto">
```

### 4. Fonts

#### Preload

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
```

#### Font Display Swap

```css
@font-face {
    font-family: 'Inter';
    font-display: swap;
}
```

### 5. Caching

#### Service Worker (Futuro)

```javascript
// sw.js
const CACHE_NAME = 'prova-modelagem-v1';
const urlsToCache = [
    '/',
    '/static/css/design-system.min.css',
    '/static/css/components.min.css',
    '/static/js/app.min.js'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});
```

---

## Padrões de UX/UI

### 1. Feedback Visual

#### Loading States

```html
<!-- Button loading -->
<button class="btn btn-primary btn-loading" disabled>
    Salvando...
</button>

<!-- Overlay global -->
<div id="loadingOverlay" class="loading-overlay show">
    <div class="spinner-container">
        <div class="spinner-border text-light"></div>
        <p class="mt-3 fw-bold">Processando...</p>
    </div>
</div>

<!-- Skeleton loaders -->
<div class="skeleton skeleton-text"></div>
<div class="skeleton skeleton-title"></div>
<div class="skeleton skeleton-card"></div>
```

#### Toast Notifications

```javascript
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <i class="bi bi-check-circle-fill toast-icon"></i>
        <div class="toast-content">
            <strong class="toast-title">${type === 'success' ? 'Sucesso' : 'Notificação'}</strong>
            <p class="toast-message">${message}</p>
        </div>
        <button class="toast-close">&times;</button>
    `;

    document.querySelector('.toast-container').appendChild(toast);

    setTimeout(() => {
        toast.classList.add('toast-exit');
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// Uso
showToast('Relatório salvo com sucesso', 'success');
showToast('Erro ao processar', 'error');
```

### 2. Animações

#### Hover Effects

```css
.hover-lift {
    transition: transform var(--transition-base);
}

.hover-lift:hover {
    transform: translateY(-4px);
}

.hover-scale {
    transition: transform var(--transition-base);
}

.hover-scale:hover {
    transform: scale(1.05);
}

.hover-shadow {
    transition: box-shadow var(--transition-base);
}

.hover-shadow:hover {
    box-shadow: var(--shadow-xl);
}
```

#### Page Transitions

```css
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-fade-in {
    animation: fadeIn 0.3s ease-out;
}

.animate-slide-in-up {
    animation: slideInUp 0.4s ease-out;
}
```

### 3. Micro-interactions

#### Button Active State

```css
.btn:active {
    transform: scale(0.98);
}
```

#### Input Focus

```css
.form-control:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px var(--primary-light);
    transform: scale(1.01);
}
```

#### Toggle Animation

```css
.form-switch-input::before {
    transition: left var(--transition-base);
}

.form-switch-input:checked::before {
    left: 22px;
}
```

### 4. Empty States

```html
<div class="empty-state">
    <div class="empty-icon">
        <i class="bi bi-inbox"></i>
    </div>
    <h3>Nenhum relatório encontrado</h3>
    <p>Comece criando seu primeiro relatório</p>
    <a href="/novo" class="btn btn-primary">
        <i class="bi bi-plus-circle me-2"></i>
        Novo Relatório
    </a>
</div>

<style>
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
}

.empty-icon {
    width: 80px;
    height: 80px;
    margin: 0 auto 1.5rem;
    border-radius: 50%;
    background: var(--gray-100);
    display: flex;
    align-items: center;
    justify-content: center;
}

.empty-icon i {
    font-size: 2rem;
    color: var(--gray-400);
}
</style>
```

### 5. Confirmações

```javascript
// Confirmação simples
const confirmed = confirm('Tem certeza que deseja excluir?');

// Confirmação com modal
function showConfirmModal(title, message, onConfirm) {
    const modal = new bootstrap.Modal(document.getElementById('confirmModal'));
    document.getElementById('confirmTitle').textContent = title;
    document.getElementById('confirmMessage').textContent = message;

    document.getElementById('confirmBtn').onclick = () => {
        onConfirm();
        modal.hide();
    };

    modal.show();
}

// Uso
showConfirmModal(
    'Excluir Relatório',
    'Esta ação não pode ser desfeita. Deseja continuar?',
    () => {
        deleteReport(reportId);
    }
);
```

### 6. Progress Indicators

#### Step Wizard

```html
<div class="wizard-progress">
    <div class="wizard-steps">
        <div class="wizard-step active">
            <div class="step-number">1</div>
            <span class="step-label">Informações</span>
        </div>
        <div class="wizard-step">
            <div class="step-number">2</div>
            <span class="step-label">Categoria</span>
        </div>
        <div class="wizard-step">
            <div class="step-number">3</div>
            <span class="step-label">Referência</span>
        </div>
    </div>
    <div class="wizard-progress-bar">
        <div class="wizard-progress-line" style="width: 33%"></div>
    </div>
</div>
```

#### Progress Bar

```html
<div class="progress">
    <div class="progress-bar progress-bar-striped progress-bar-animated"
         role="progressbar"
         style="width: 75%"
         aria-valuenow="75"
         aria-valuemin="0"
         aria-valuemax="100">
        75%
    </div>
</div>
```

---

## Resumo de Arquivos

### Templates (29 arquivos)

```
templates/
├── base.html
├── login.html
├── dashboard.html
├── analytics.html
├── novo_relatorio.html
├── editar_relatorio.html
├── detalhes_relatorio.html
├── alterar_senha.html
├── esqueci_senha.html
├── reset_senha.html
├── logs.html
├── table_example.html
├── analytics_charts.html
├── relatorio_pdf.html
├── admin/ (5 arquivos)
│   ├── dashboard.html
│   ├── users.html
│   ├── create_user.html
│   ├── edit_user.html
│   └── change_password.html
├── audit/ (5 arquivos)
│   ├── index.html
│   ├── timeline.html
│   ├── estatisticas.html
│   ├── por_usuario.html
│   └── detalhes.html
└── errors/ (5 arquivos)
    ├── 403.html
    ├── 404.html
    ├── 413.html
    ├── 429.html
    └── 500.html
```

### CSS (20 arquivos - 10 originais + 10 minificados)

```
static/css/
├── design-system.css (+ .min.css)
├── components.css (+ .min.css)
├── navigation.css (+ .min.css)
├── mobile.css (+ .min.css)
├── accessibility.css (+ .min.css)
├── wizard.css (+ .min.css)
├── table.css (+ .min.css)
├── file-upload.css (+ .min.css)
├── custom.css (+ .min.css)
└── base-styles.css (+ .min.css)
```

### JavaScript (20 arquivos - 10 originais + 10 minificados)

```
static/js/
├── app.js (+ .min.js)
├── main.js (+ .min.js)
├── app-init.js (+ .min.js)
├── accessibility.js (+ .min.js)
├── charts-config.js (+ .min.js)
├── wizard.js (+ .min.js)
├── file-upload.js (+ .min.js)
├── datatable.js (+ .min.js)
├── date-picker.js (+ .min.js)
├── lazy-loading.js (+ .min.js)
└── lazy-chart-loader.js (+ .min.js)
```

### Imagens

```
static/img/
├── Puket.png (Logo principal)
├── Puket_small.png (Logo pequeno para sidebar)
└── placeholder.png.svg (Placeholder SVG)
```

---

## Checklist de Manutenção

### Ao Adicionar Novo Componente

- [ ] Documentar no `components.css` com comentários
- [ ] Adicionar variantes (cores, tamanhos)
- [ ] Testar responsividade (mobile, tablet, desktop)
- [ ] Verificar contraste de cores (WCAG 2.1 AA)
- [ ] Adicionar estados (hover, focus, active, disabled)
- [ ] Implementar versão acessível (ARIA, keyboard)
- [ ] Criar exemplo no `components-demo.html`
- [ ] Minificar arquivo final

### Ao Adicionar Nova Página

- [ ] Estender `base.html`
- [ ] Definir `{% block title %}`
- [ ] Definir `{% block breadcrumb %}`
- [ ] Adicionar ao menu de navegação
- [ ] Testar em mobile (bottom-nav)
- [ ] Verificar acessibilidade (skip links, ARIA)
- [ ] Implementar loading states
- [ ] Adicionar meta description
- [ ] Testar em diferentes navegadores

### Performance Checklist

- [ ] Minificar CSS e JS
- [ ] Otimizar imagens (WebP, lazy loading)
- [ ] Implementar cache HTTP
- [ ] Reduzir requests (concatenar arquivos)
- [ ] Defer/async scripts não-críticos
- [ ] Preload recursos críticos
- [ ] Comprimir arquivos (gzip/brotli)
- [ ] Testar com Lighthouse (score > 90)

---

## Referências

### Documentação Externa

- **Bootstrap 5**: https://getbootstrap.com/docs/5.3/
- **Bootstrap Icons**: https://icons.getbootstrap.com/
- **Chart.js**: https://www.chartjs.org/docs/latest/
- **WCAG 2.1**: https://www.w3.org/WAI/WCAG21/quickref/
- **MDN Web Docs**: https://developer.mozilla.org/

### Ferramentas de Teste

- **Lighthouse**: Chrome DevTools
- **axe DevTools**: Extensão de acessibilidade
- **WAVE**: Web Accessibility Evaluation Tool
- **Contrast Checker**: WebAIM Contrast Checker
- **Responsively**: App para testar múltiplos devices

---

**Documentação criada em**: 2026-01-16
**Versão**: 2.0
**Autor**: Sistema de Prova de Modelagem App
