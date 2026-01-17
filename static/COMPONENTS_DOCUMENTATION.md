# Biblioteca de Componentes Reutilizáveis

## Índice
1. [Introdução](#introdução)
2. [Instalação](#instalação)
3. [Design Tokens](#design-tokens)
4. [Componentes](#componentes)
   - [Botões](#botões)
   - [Formulários](#formulários)
   - [Cards](#cards)
   - [Badges](#badges)
   - [Alertas e Toasts](#alertas-e-toasts)
   - [Loading States](#loading-states)
   - [Modais](#modais)
   - [Dropdowns](#dropdowns)
5. [Classes Utilitárias](#classes-utilitárias)
6. [Exemplos de Uso](#exemplos-de-uso)

---

## Introdução

Esta biblioteca de componentes fornece um conjunto completo de elementos UI padronizados e reutilizáveis. Todos os componentes seguem princípios de design consistentes e são totalmente responsivos.

### Características
- **Design consistente** com sistema de tokens
- **Totalmente responsivo** (mobile-first)
- **Acessível** com semântica HTML apropriada
- **Leve** e performático
- **Fácil customização** via CSS custom properties

---

## Instalação

### 1. Incluir o CSS no seu HTML

```html
<link rel="stylesheet" href="/static/css/components.css">
```

### 2. Visualizar a Demo

Acesse `/static/components-demo.html` para ver todos os componentes em ação.

---

## Design Tokens

Todos os componentes utilizam CSS custom properties (variáveis) para facilitar a customização.

### Cores

```css
/* Cores Principais */
--primary: #e6007e;
--secondary: #6c757d;
--success: #28a745;
--error: #dc3545;
--warning: #ffc107;
--info: #17a2b8;

/* Escala de Cinza */
--gray-50 a --gray-900
```

### Espaçamento

```css
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-3: 0.75rem;  /* 12px */
--space-4: 1rem;     /* 16px */
--space-5: 1.25rem;  /* 20px */
--space-6: 1.5rem;   /* 24px */
--space-8: 2rem;     /* 32px */
--space-10: 2.5rem;  /* 40px */
--space-12: 3rem;    /* 48px */
```

### Tipografia

```css
--text-xs: 0.75rem;     /* 12px */
--text-sm: 0.875rem;    /* 14px */
--text-base: 1rem;      /* 16px */
--text-lg: 1.125rem;    /* 18px */
--text-xl: 1.25rem;     /* 20px */
--text-2xl: 1.5rem;     /* 24px */
--text-3xl: 1.875rem;   /* 30px */
```

### Border Radius

```css
--radius-sm: 0.25rem;   /* 4px */
--radius-md: 0.5rem;    /* 8px */
--radius-lg: 0.75rem;   /* 12px */
--radius-xl: 1rem;      /* 16px */
--radius-full: 9999px;
```

### Sombras

```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
```

---

## Componentes

### Botões

#### Classes Básicas

```html
<!-- Botão Primário -->
<button class="btn btn-primary">Primary</button>

<!-- Botão Secundário -->
<button class="btn btn-secondary">Secondary</button>

<!-- Botão de Sucesso -->
<button class="btn btn-success">Success</button>

<!-- Botão de Erro -->
<button class="btn btn-error">Error</button>

<!-- Botão de Aviso -->
<button class="btn btn-warning">Warning</button>

<!-- Botão Informativo -->
<button class="btn btn-info">Info</button>
```

#### Variações

```html
<!-- Outline -->
<button class="btn btn-outline-primary">Outline</button>

<!-- Ghost/Text -->
<button class="btn btn-ghost">Ghost</button>
```

#### Tamanhos

```html
<button class="btn btn-primary btn-xs">Extra Small</button>
<button class="btn btn-primary btn-sm">Small</button>
<button class="btn btn-primary">Default</button>
<button class="btn btn-primary btn-lg">Large</button>
<button class="btn btn-primary btn-xl">Extra Large</button>
```

#### Botões com Ícone

```html
<!-- Botão de ícone apenas -->
<button class="btn btn-primary btn-icon">+</button>

<!-- Botão com ícone e texto -->
<button class="btn btn-primary btn-with-icon">
  <span>+</span>
  <span>Adicionar</span>
</button>
```

#### Estados

```html
<!-- Desabilitado -->
<button class="btn btn-primary" disabled>Disabled</button>

<!-- Loading -->
<button class="btn btn-primary btn-loading">Loading</button>
```

#### Classes Disponíveis

| Classe | Descrição |
|--------|-----------|
| `.btn` | Classe base (obrigatória) |
| `.btn-primary` | Estilo primário |
| `.btn-secondary` | Estilo secundário |
| `.btn-success` | Estilo de sucesso |
| `.btn-error` | Estilo de erro |
| `.btn-warning` | Estilo de aviso |
| `.btn-info` | Estilo informativo |
| `.btn-outline-*` | Versão outline |
| `.btn-ghost` | Versão ghost |
| `.btn-xs` | Extra pequeno |
| `.btn-sm` | Pequeno |
| `.btn-lg` | Grande |
| `.btn-xl` | Extra grande |
| `.btn-icon` | Botão circular para ícone |
| `.btn-rounded` | Bordas totalmente arredondadas |
| `.btn-loading` | Estado de carregamento |

---

### Formulários

#### Input Básico

```html
<div class="form-group">
  <label class="form-label">Nome</label>
  <input type="text" class="form-control" placeholder="Digite seu nome">
</div>
```

#### Label Obrigatória

```html
<label class="form-label form-label-required">Campo Obrigatório</label>
```

#### Estados do Input

```html
<!-- Input Válido -->
<input type="text" class="form-control is-valid" value="Input válido">
<div class="form-feedback form-feedback-success">Campo correto!</div>

<!-- Input Inválido -->
<input type="text" class="form-control is-invalid" value="Input inválido">
<div class="form-feedback form-feedback-error">Campo obrigatório.</div>

<!-- Input Desabilitado -->
<input type="text" class="form-control" disabled>
```

#### Tamanhos

```html
<input type="text" class="form-control form-control-sm">
<input type="text" class="form-control">
<input type="text" class="form-control form-control-lg">
```

#### Textarea

```html
<textarea class="form-control" rows="4" placeholder="Digite aqui..."></textarea>
```

#### Select

```html
<select class="form-control">
  <option>Opção 1</option>
  <option>Opção 2</option>
  <option>Opção 3</option>
</select>
```

#### Checkbox e Radio

```html
<!-- Checkbox -->
<div class="form-check">
  <input type="checkbox" class="form-check-input" id="check1">
  <label class="form-check-label" for="check1">Aceito os termos</label>
</div>

<!-- Radio -->
<div class="form-check">
  <input type="radio" class="form-check-input" name="opcao" id="radio1">
  <label class="form-check-label" for="radio1">Opção 1</label>
</div>
```

#### Switch

```html
<label class="form-switch">
  <input type="checkbox" class="form-switch-input">
  <span class="form-switch-label">Ativar notificações</span>
</label>
```

#### Input Group

```html
<!-- Prefixo -->
<div class="input-group">
  <span class="input-group-addon">R$</span>
  <input type="text" class="form-control" placeholder="0,00">
</div>

<!-- Sufixo -->
<div class="input-group">
  <input type="text" class="form-control">
  <span class="input-group-addon">.com</span>
</div>
```

#### Classes Disponíveis

| Classe | Descrição |
|--------|-----------|
| `.form-group` | Container do campo |
| `.form-label` | Label do campo |
| `.form-label-required` | Adiciona asterisco de obrigatório |
| `.form-control` | Input, textarea ou select |
| `.form-control-sm` | Input pequeno |
| `.form-control-lg` | Input grande |
| `.is-valid` | Estado válido |
| `.is-invalid` | Estado inválido |
| `.form-feedback` | Mensagem de feedback |
| `.form-feedback-success` | Feedback de sucesso |
| `.form-feedback-error` | Feedback de erro |
| `.form-check` | Container de checkbox/radio |
| `.form-check-input` | Checkbox ou radio |
| `.form-check-label` | Label de checkbox/radio |
| `.form-switch` | Container de switch |
| `.form-switch-input` | Input do switch |
| `.form-switch-label` | Label do switch |
| `.input-group` | Agrupa input com addons |
| `.input-group-addon` | Prefixo ou sufixo |

---

### Cards

#### Card Básico

```html
<div class="card">
  <h3 class="card-title">Título do Card</h3>
  <p class="card-subtitle">Subtítulo opcional</p>
  <p class="card-text">Conteúdo do card...</p>
  <button class="btn btn-primary">Ação</button>
</div>
```

#### Card com Header e Footer

```html
<div class="card">
  <div class="card-header">Header do Card</div>
  <div class="card-body">
    <h3 class="card-title">Título</h3>
    <p class="card-text">Conteúdo...</p>
  </div>
  <div class="card-footer">
    <button class="btn btn-primary">Confirmar</button>
  </div>
</div>
```

#### Variações

```html
<!-- Card Normal (hover com elevação) -->
<div class="card">...</div>

<!-- Card Flat (sem hover) -->
<div class="card card-flat">...</div>

<!-- Card Elevated (sombra mais forte) -->
<div class="card card-elevated">...</div>
```

#### Tamanhos

```html
<div class="card card-sm">Card pequeno</div>
<div class="card">Card padrão</div>
<div class="card card-lg">Card grande</div>
```

#### Card com Imagem

```html
<div class="card">
  <img src="image.jpg" class="card-img-top" alt="Imagem">
  <h3 class="card-title">Título</h3>
  <p class="card-text">Conteúdo...</p>
</div>
```

#### Grid de Cards

```html
<div class="card-grid">
  <div class="card">Card 1</div>
  <div class="card">Card 2</div>
  <div class="card">Card 3</div>
</div>
```

#### Classes Disponíveis

| Classe | Descrição |
|--------|-----------|
| `.card` | Classe base do card |
| `.card-flat` | Remove hover effect |
| `.card-elevated` | Sombra elevada |
| `.card-sm` | Card pequeno |
| `.card-lg` | Card grande |
| `.card-header` | Cabeçalho do card |
| `.card-body` | Corpo do card |
| `.card-footer` | Rodapé do card |
| `.card-title` | Título do card |
| `.card-subtitle` | Subtítulo do card |
| `.card-text` | Texto do card |
| `.card-img-top` | Imagem no topo |
| `.card-grid` | Grid responsivo de cards |

---

### Badges

#### Badges Básicos

```html
<span class="badge badge-primary">Primary</span>
<span class="badge badge-secondary">Secondary</span>
<span class="badge badge-success">Success</span>
<span class="badge badge-error">Error</span>
<span class="badge badge-warning">Warning</span>
<span class="badge badge-info">Info</span>
<span class="badge badge-gray">Gray</span>
```

#### Badges Sólidos

```html
<span class="badge badge-solid-primary">Primary</span>
<span class="badge badge-solid-success">Success</span>
<span class="badge badge-solid-error">Error</span>
```

#### Tamanhos

```html
<span class="badge badge-primary badge-sm">Small</span>
<span class="badge badge-primary">Default</span>
<span class="badge badge-primary badge-lg">Large</span>
```

#### Badge com Ponto

```html
<span class="badge badge-success badge-dot">Online</span>
<span class="badge badge-error badge-dot">Offline</span>
```

#### Pill Badge

```html
<span class="badge badge-primary badge-pill">Nova</span>
```

#### Classes Disponíveis

| Classe | Descrição |
|--------|-----------|
| `.badge` | Classe base |
| `.badge-primary` | Badge primário (light) |
| `.badge-secondary` | Badge secundário (light) |
| `.badge-success` | Badge de sucesso (light) |
| `.badge-error` | Badge de erro (light) |
| `.badge-warning` | Badge de aviso (light) |
| `.badge-info` | Badge informativo (light) |
| `.badge-gray` | Badge cinza |
| `.badge-solid-*` | Versão sólida |
| `.badge-sm` | Badge pequeno |
| `.badge-lg` | Badge grande |
| `.badge-dot` | Adiciona ponto antes |
| `.badge-pill` | Formato pill |

---

### Alertas e Toasts

#### Alertas

```html
<!-- Alerta de Sucesso -->
<div class="alert alert-success">
  <div class="alert-icon">✓</div>
  <div class="alert-content">
    <div class="alert-title">Sucesso!</div>
    <div class="alert-message">Operação concluída.</div>
  </div>
  <button class="alert-close">✕</button>
</div>

<!-- Alerta de Erro -->
<div class="alert alert-error">
  <div class="alert-icon">✕</div>
  <div class="alert-content">
    <div class="alert-title">Erro</div>
    <div class="alert-message">Ocorreu um erro.</div>
  </div>
</div>

<!-- Alerta de Aviso -->
<div class="alert alert-warning">
  <div class="alert-icon">⚠</div>
  <div class="alert-content">
    <div class="alert-title">Atenção</div>
    <div class="alert-message">Esta ação não pode ser desfeita.</div>
  </div>
</div>

<!-- Alerta Informativo -->
<div class="alert alert-info">
  <div class="alert-icon">ℹ</div>
  <div class="alert-content">
    <div class="alert-title">Informação</div>
    <div class="alert-message">Mensagem informativa.</div>
  </div>
</div>
```

#### Toast Notifications

```html
<!-- Container de Toasts (fixo no topo direito) -->
<div class="toast-container">

  <!-- Toast de Sucesso -->
  <div class="toast toast-success">
    <div class="toast-icon">✓</div>
    <div class="toast-content">
      <div class="toast-title">Sucesso</div>
      <div class="toast-message">Operação concluída!</div>
    </div>
    <button class="toast-close">✕</button>
  </div>

</div>
```

#### JavaScript para Toasts

```javascript
function showToast(type, title, message) {
  const container = document.querySelector('.toast-container');

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <div class="toast-icon">${getIcon(type)}</div>
    <div class="toast-content">
      <div class="toast-title">${title}</div>
      <div class="toast-message">${message}</div>
    </div>
    <button class="toast-close" onclick="this.parentElement.remove()">✕</button>
  `;

  container.appendChild(toast);

  // Auto remove após 5 segundos
  setTimeout(() => {
    toast.classList.add('toast-exit');
    setTimeout(() => toast.remove(), 300);
  }, 5000);
}

function getIcon(type) {
  const icons = {
    success: '✓',
    error: '✕',
    warning: '⚠',
    info: 'ℹ'
  };
  return icons[type] || 'ℹ';
}

// Uso
showToast('success', 'Sucesso!', 'Operação concluída.');
```

#### Classes Disponíveis

| Classe | Descrição |
|--------|-----------|
| `.alert` | Classe base de alerta |
| `.alert-success` | Alerta de sucesso |
| `.alert-error` | Alerta de erro |
| `.alert-warning` | Alerta de aviso |
| `.alert-info` | Alerta informativo |
| `.alert-icon` | Container do ícone |
| `.alert-content` | Container do conteúdo |
| `.alert-title` | Título do alerta |
| `.alert-message` | Mensagem do alerta |
| `.alert-close` | Botão de fechar |
| `.toast-container` | Container de toasts |
| `.toast` | Classe base de toast |
| `.toast-success` | Toast de sucesso |
| `.toast-error` | Toast de erro |
| `.toast-warning` | Toast de aviso |
| `.toast-info` | Toast informativo |
| `.toast-icon` | Ícone do toast |
| `.toast-content` | Conteúdo do toast |
| `.toast-title` | Título do toast |
| `.toast-message` | Mensagem do toast |
| `.toast-close` | Botão fechar toast |
| `.toast-exit` | Animação de saída |

---

### Loading States

#### Spinners

```html
<!-- Tamanhos -->
<div class="spinner spinner-sm"></div>
<div class="spinner"></div>
<div class="spinner spinner-lg"></div>
<div class="spinner spinner-xl"></div>

<!-- Cores -->
<div class="spinner spinner-primary"></div>
<div class="spinner spinner-secondary"></div>
<div class="spinner spinner-success"></div>
<div class="spinner spinner-white"></div>
```

#### Skeleton Loaders

```html
<!-- Texto -->
<div class="skeleton skeleton-text"></div>
<div class="skeleton skeleton-text"></div>

<!-- Título -->
<div class="skeleton skeleton-title"></div>

<!-- Avatar -->
<div class="skeleton skeleton-avatar"></div>

<!-- Botão -->
<div class="skeleton skeleton-button"></div>

<!-- Card -->
<div class="skeleton skeleton-card"></div>
```

#### Barra de Progresso

```html
<!-- Básica -->
<div class="progress">
  <div class="progress-bar" style="width: 60%;"></div>
</div>

<!-- Com listras -->
<div class="progress">
  <div class="progress-bar progress-bar-striped" style="width: 75%;"></div>
</div>

<!-- Animada -->
<div class="progress">
  <div class="progress-bar progress-bar-striped progress-bar-animated"
       style="width: 100%;"></div>
</div>

<!-- Tamanhos -->
<div class="progress progress-sm">
  <div class="progress-bar" style="width: 50%;"></div>
</div>

<div class="progress progress-lg">
  <div class="progress-bar" style="width: 80%;"></div>
</div>
```

#### Loading Overlay

```html
<div class="loading-overlay">
  <div class="loading-overlay-content">
    <div class="loading-overlay-spinner">
      <div class="spinner spinner-lg spinner-primary"></div>
    </div>
    <p class="loading-overlay-text">Carregando...</p>
  </div>
</div>
```

#### Classes Disponíveis

| Classe | Descrição |
|--------|-----------|
| `.spinner` | Spinner padrão |
| `.spinner-sm` | Spinner pequeno |
| `.spinner-lg` | Spinner grande |
| `.spinner-xl` | Spinner extra grande |
| `.spinner-primary` | Spinner colorido |
| `.spinner-white` | Spinner branco |
| `.skeleton` | Skeleton loader base |
| `.skeleton-text` | Linha de texto |
| `.skeleton-title` | Título |
| `.skeleton-avatar` | Avatar circular |
| `.skeleton-button` | Botão |
| `.skeleton-card` | Card completo |
| `.progress` | Barra de progresso |
| `.progress-bar` | Barra interna |
| `.progress-bar-striped` | Com listras |
| `.progress-bar-animated` | Animado |
| `.progress-sm` | Pequeno |
| `.progress-lg` | Grande |
| `.loading-overlay` | Overlay de loading |

---

### Modais

#### Modal Básico

```html
<!-- Backdrop (fundo escuro) -->
<div class="modal-backdrop">

  <!-- Modal -->
  <div class="modal">

    <!-- Header -->
    <div class="modal-header">
      <h3 class="modal-title">Título do Modal</h3>
      <button class="modal-close">✕</button>
    </div>

    <!-- Body -->
    <div class="modal-body">
      <p>Conteúdo do modal...</p>
    </div>

    <!-- Footer -->
    <div class="modal-footer">
      <button class="btn btn-ghost">Cancelar</button>
      <button class="btn btn-primary">Confirmar</button>
    </div>

  </div>
</div>
```

#### Tamanhos de Modal

```html
<!-- Modal Pequeno -->
<div class="modal modal-sm">...</div>

<!-- Modal Padrão -->
<div class="modal">...</div>

<!-- Modal Grande -->
<div class="modal modal-lg">...</div>

<!-- Modal Extra Grande -->
<div class="modal modal-xl">...</div>
```

#### JavaScript para Modal

```javascript
function showModal(modalId) {
  const modal = document.getElementById(modalId);
  modal.style.display = 'flex';
}

function hideModal(modalId) {
  const modal = document.getElementById(modalId);
  modal.style.display = 'none';
}

// Fechar ao clicar fora
document.querySelector('.modal-backdrop').addEventListener('click', function(e) {
  if (e.target === this) {
    hideModal('meuModal');
  }
});
```

#### Classes Disponíveis

| Classe | Descrição |
|--------|-----------|
| `.modal-backdrop` | Fundo escuro overlay |
| `.modal` | Container do modal |
| `.modal-sm` | Modal pequeno (400px) |
| `.modal-lg` | Modal grande (800px) |
| `.modal-xl` | Modal extra grande (1200px) |
| `.modal-header` | Cabeçalho |
| `.modal-title` | Título do modal |
| `.modal-close` | Botão fechar |
| `.modal-body` | Corpo do modal |
| `.modal-footer` | Rodapé do modal |

---

### Dropdowns

#### Dropdown Básico

```html
<div class="dropdown">
  <!-- Trigger -->
  <button class="btn btn-primary" onclick="toggleDropdown('menu1')">
    Menu ▼
  </button>

  <!-- Menu -->
  <div class="dropdown-menu" id="menu1">
    <div class="dropdown-header">Ações</div>
    <a href="#" class="dropdown-item">Editar</a>
    <a href="#" class="dropdown-item">Duplicar</a>
    <div class="dropdown-divider"></div>
    <a href="#" class="dropdown-item dropdown-item-danger">Excluir</a>
  </div>
</div>
```

#### Dropdown Alinhado à Direita

```html
<div class="dropdown">
  <button class="btn btn-primary">Menu ▼</button>
  <div class="dropdown-menu dropdown-menu-right">
    <a href="#" class="dropdown-item">Opção 1</a>
    <a href="#" class="dropdown-item">Opção 2</a>
  </div>
</div>
```

#### JavaScript para Dropdown

```javascript
function toggleDropdown(menuId) {
  const menu = document.getElementById(menuId);
  menu.classList.toggle('show');
}

// Fechar ao clicar fora
document.addEventListener('click', function(event) {
  if (!event.target.closest('.dropdown')) {
    document.querySelectorAll('.dropdown-menu').forEach(menu => {
      menu.classList.remove('show');
    });
  }
});
```

#### Classes Disponíveis

| Classe | Descrição |
|--------|-----------|
| `.dropdown` | Container do dropdown |
| `.dropdown-menu` | Menu dropdown |
| `.dropdown-menu-right` | Alinhado à direita |
| `.dropdown-item` | Item do menu |
| `.dropdown-item-danger` | Item de perigo (vermelho) |
| `.dropdown-header` | Cabeçalho do grupo |
| `.dropdown-divider` | Divisor |
| `.show` | Torna o menu visível |

---

## Classes Utilitárias

### Display

```html
<div class="d-none">Escondido</div>
<div class="d-block">Block</div>
<div class="d-inline">Inline</div>
<div class="d-inline-block">Inline Block</div>
<div class="d-flex">Flex</div>
<div class="d-inline-flex">Inline Flex</div>
<div class="d-grid">Grid</div>
```

### Flexbox

```html
<div class="d-flex flex-row">Horizontal</div>
<div class="d-flex flex-column">Vertical</div>
<div class="d-flex justify-center">Centralizado</div>
<div class="d-flex justify-between">Espaçado</div>
<div class="d-flex align-center">Alinhado Centro</div>
<div class="d-flex gap-4">Com espaçamento</div>
```

### Espaçamento

```html
<!-- Margin -->
<div class="m-0">Sem margem</div>
<div class="m-4">Margem padrão</div>
<div class="mt-4">Margem top</div>
<div class="mb-4">Margem bottom</div>

<!-- Padding -->
<div class="p-0">Sem padding</div>
<div class="p-4">Padding padrão</div>
```

### Texto

```html
<p class="text-left">Esquerda</p>
<p class="text-center">Centro</p>
<p class="text-right">Direita</p>

<p class="text-xs">Extra pequeno</p>
<p class="text-sm">Pequeno</p>
<p class="text-base">Base</p>
<p class="text-lg">Grande</p>

<p class="font-normal">Normal</p>
<p class="font-semibold">Semi-negrito</p>
<p class="font-bold">Negrito</p>
```

### Cores

```html
<!-- Text Colors -->
<span class="text-primary">Primário</span>
<span class="text-success">Sucesso</span>
<span class="text-error">Erro</span>
<span class="text-warning">Aviso</span>

<!-- Background Colors -->
<div class="bg-primary">Fundo primário</div>
<div class="bg-success">Fundo sucesso</div>
<div class="bg-gray">Fundo cinza</div>
<div class="bg-white">Fundo branco</div>
```

### Outros

```html
<!-- Width -->
<div class="w-full">Largura total</div>
<div class="w-auto">Largura automática</div>

<!-- Border Radius -->
<div class="rounded">Arredondado médio</div>
<div class="rounded-lg">Arredondado grande</div>
<div class="rounded-full">Totalmente arredondado</div>

<!-- Shadow -->
<div class="shadow-sm">Sombra pequena</div>
<div class="shadow-md">Sombra média</div>
<div class="shadow-lg">Sombra grande</div>
<div class="shadow-none">Sem sombra</div>

<!-- Cursor -->
<div class="cursor-pointer">Ponteiro</div>
<div class="cursor-not-allowed">Não permitido</div>

<!-- Overflow -->
<div class="overflow-hidden">Overflow escondido</div>
<div class="overflow-auto">Overflow automático</div>
```

---

## Exemplos de Uso

### Formulário de Login

```html
<div class="card" style="max-width: 400px; margin: 0 auto;">
  <h2 class="card-title text-center">Login</h2>

  <form>
    <div class="form-group">
      <label class="form-label form-label-required">Email</label>
      <input type="email" class="form-control" placeholder="seu@email.com">
    </div>

    <div class="form-group">
      <label class="form-label form-label-required">Senha</label>
      <input type="password" class="form-control">
    </div>

    <div class="form-check">
      <input type="checkbox" class="form-check-input" id="remember">
      <label class="form-check-label" for="remember">Lembrar-me</label>
    </div>

    <button type="submit" class="btn btn-primary w-full mt-4">
      Entrar
    </button>
  </form>

  <div class="text-center mt-4">
    <a href="#" class="text-primary">Esqueceu a senha?</a>
  </div>
</div>
```

### Card de Produto

```html
<div class="card">
  <img src="produto.jpg" class="card-img-top" alt="Produto">

  <div class="d-flex justify-between align-center mb-2">
    <h3 class="card-title m-0">Nome do Produto</h3>
    <span class="badge badge-success">Novo</span>
  </div>

  <p class="card-text text-gray">
    Descrição breve do produto com informações relevantes.
  </p>

  <div class="d-flex justify-between align-center mt-4">
    <span class="text-xl font-bold text-primary">R$ 99,90</span>
    <button class="btn btn-primary">Comprar</button>
  </div>
</div>
```

### Modal de Confirmação

```html
<div id="confirmModal" class="modal-backdrop" style="display: none;">
  <div class="modal modal-sm">
    <div class="modal-header">
      <h3 class="modal-title">Confirmar Exclusão</h3>
      <button class="modal-close" onclick="hideModal('confirmModal')">✕</button>
    </div>

    <div class="modal-body">
      <p>Tem certeza que deseja excluir este item? Esta ação não pode ser desfeita.</p>
    </div>

    <div class="modal-footer">
      <button class="btn btn-ghost" onclick="hideModal('confirmModal')">
        Cancelar
      </button>
      <button class="btn btn-error" onclick="confirmarExclusao()">
        Excluir
      </button>
    </div>
  </div>
</div>
```

### Tabela com Ações

```html
<div class="card">
  <div class="card-header">
    <div class="d-flex justify-between align-center">
      <h3 class="m-0">Usuários</h3>
      <button class="btn btn-primary btn-sm">+ Adicionar</button>
    </div>
  </div>

  <div class="card-body p-0">
    <table style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr style="background: var(--gray-50); border-bottom: 1px solid var(--gray-200);">
          <th style="padding: var(--space-4); text-align: left;">Nome</th>
          <th style="padding: var(--space-4); text-align: left;">Status</th>
          <th style="padding: var(--space-4); text-align: right;">Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom: 1px solid var(--gray-200);">
          <td style="padding: var(--space-4);">João Silva</td>
          <td style="padding: var(--space-4);">
            <span class="badge badge-success badge-dot">Ativo</span>
          </td>
          <td style="padding: var(--space-4); text-align: right;">
            <button class="btn btn-ghost btn-sm">Editar</button>
            <button class="btn btn-ghost btn-sm text-error">Excluir</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
```

### Dashboard com Grid

```html
<div class="card-grid">
  <!-- Card de Estatística -->
  <div class="card">
    <div class="d-flex justify-between align-center mb-4">
      <div>
        <p class="text-sm text-gray m-0">Total de Usuários</p>
        <h2 class="text-3xl font-bold text-primary m-0">1,234</h2>
      </div>
      <div class="bg-primary" style="width: 48px; height: 48px; border-radius: var(--radius-lg); display: flex; align-items: center; justify-content: center; color: white; font-size: 24px;">
        👥
      </div>
    </div>
    <div class="d-flex align-center gap-2">
      <span class="badge badge-success">+12%</span>
      <span class="text-sm text-gray">vs. mês anterior</span>
    </div>
  </div>

  <!-- Mais cards... -->
</div>
```

---

## Customização

### Personalizando Cores

Você pode sobrescrever as cores do sistema criando seu próprio CSS:

```css
:root {
  --primary: #your-color;
  --primary-hover: #your-hover-color;
  --primary-light: rgba(your-color, 0.1);
}
```

### Adicionando Novas Variantes

Você pode criar novas variantes de botões, badges, etc:

```css
.btn-custom {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.badge-custom {
  background: #667eea;
  color: white;
}
```

### Ajustando Espaçamentos

```css
:root {
  --space-4: 1.5rem; /* Aumentar espaçamento padrão */
}
```

---

## Suporte e Contribuição

Para reportar bugs ou sugerir melhorias, entre em contato com a equipe de desenvolvimento.

### Versão
**v1.0.0** - Janeiro 2026

---

## Licença

Este sistema de componentes é de uso interno da organização.
