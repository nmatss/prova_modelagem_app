# Design System - Cheat Sheet

## 🚀 Referência Rápida para Desenvolvedores

---

## 🎨 Cores - Uso Mais Comum

### Cores Principais
```html
<!-- Primary (Rosa Puket) -->
<div class="bg-primary text-white">Primary</div>
<div class="text-primary">Texto rosa</div>
<div class="border-2 border-primary">Borda rosa</div>

<!-- Success (Verde) -->
<div class="bg-success text-white">Success</div>
<span class="badge bg-success text-white">Aprovada</span>

<!-- Error (Vermelho) -->
<div class="bg-error text-white">Error</div>
<div class="alert bg-error-light text-error-700">Erro!</div>

<!-- Warning (Amarelo) -->
<div class="bg-warning text-white">Warning</div>

<!-- Info (Cyan) -->
<div class="bg-info text-white">Info</div>
```

### CSS Variables
```css
color: var(--primary);        /* #E6007E */
color: var(--success);        /* #10B981 */
color: var(--error);          /* #EF4444 */
color: var(--warning);        /* #F59E0B */
color: var(--info);           /* #06B6D4 */

/* Hover states */
background: var(--primary-hover);
background: var(--success-hover);

/* Light backgrounds */
background: var(--primary-light);
background: var(--success-light);
```

---

## 📏 Espaçamento

### Padding
```html
<div class="p-4">padding: 16px (todos os lados)</div>
<div class="px-6">padding: 24px (horizontal)</div>
<div class="py-3">padding: 12px (vertical)</div>
<div class="pt-2">padding-top: 8px</div>
<div class="pb-8">padding-bottom: 32px</div>
```

### Margin
```html
<div class="m-4">margin: 16px</div>
<div class="mx-auto">margin: 0 auto (centralizar)</div>
<div class="my-6">margin: 24px 0 (vertical)</div>
<div class="mt-8">margin-top: 32px</div>
<div class="mb-0">margin-bottom: 0</div>
```

### Valores Rápidos
```
1 = 4px    |  2 = 8px    |  3 = 12px   |  4 = 16px
5 = 20px   |  6 = 24px   |  8 = 32px   | 10 = 40px
12 = 48px  | 16 = 64px
```

### CSS Variables
```css
padding: var(--space-4);      /* 16px */
margin: var(--space-6);       /* 24px */
gap: var(--space-3);          /* 12px */
```

---

## 📝 Tipografia

### Font Sizes
```html
<p class="text-xs">12px - Legendas</p>
<p class="text-sm">14px - Texto pequeno</p>
<p class="text-base">16px - Corpo padrão</p>
<p class="text-lg">18px - Texto destacado</p>
<p class="text-xl">20px - Subtítulos</p>
<p class="text-2xl">24px - Títulos (h3)</p>
<p class="text-3xl">30px - Títulos (h2)</p>
<p class="text-4xl">36px - Títulos (h1)</p>
```

### Font Weights
```html
<p class="font-light">300 - Leve</p>
<p class="font-normal">400 - Normal</p>
<p class="font-medium">500 - Médio</p>
<p class="font-semibold">600 - Semi-negrito</p>
<p class="font-bold">700 - Negrito</p>
```

### Text Utilities
```html
<p class="text-left">Alinhado à esquerda</p>
<p class="text-center">Centralizado</p>
<p class="text-right">Alinhado à direita</p>

<p class="uppercase">MAIÚSCULAS</p>
<p class="lowercase">minúsculas</p>
<p class="capitalize">Primeira Maiúscula</p>

<p class="underline">Sublinhado</p>
<p class="truncate">Texto cortado...</p>
```

---

## 🎯 Layout

### Flexbox
```html
<!-- Container Flex -->
<div class="d-flex">Flexbox básico</div>

<!-- Direção -->
<div class="d-flex flex-row">Linha (padrão)</div>
<div class="d-flex flex-column">Coluna</div>

<!-- Alinhamento Horizontal -->
<div class="d-flex justify-start">Início</div>
<div class="d-flex justify-center">Centro</div>
<div class="d-flex justify-end">Fim</div>
<div class="d-flex justify-between">Space-between</div>

<!-- Alinhamento Vertical -->
<div class="d-flex items-start">Topo</div>
<div class="d-flex items-center">Centro</div>
<div class="d-flex items-end">Base</div>

<!-- Combinações Comuns -->
<div class="d-flex justify-center items-center">Centralizado total</div>
<div class="d-flex justify-between items-center">Navbar layout</div>

<!-- Gap -->
<div class="d-flex gap-4">Gap de 16px entre items</div>
```

### Grid
```html
<div class="d-grid grid-cols-2 gap-4">2 colunas</div>
<div class="d-grid grid-cols-3 gap-6">3 colunas</div>
<div class="d-grid grid-cols-4 gap-8">4 colunas</div>
```

### Display
```html
<div class="d-none">Escondido</div>
<div class="d-block">Block</div>
<div class="d-inline-block">Inline-block</div>
```

---

## 🔲 Borders & Radius

### Border Radius
```html
<div class="rounded-sm">4px - Sutil</div>
<div class="rounded-md">8px - Padrão</div>
<div class="rounded-lg">12px - Cards</div>
<div class="rounded-xl">16px - Modals</div>
<div class="rounded-full">Círculo/Pill</div>
```

### Border Width
```html
<div class="border-2 border-gray-300">Borda 2px</div>
<div class="border-l-4 border-primary">Borda esquerda 4px</div>
<div class="border-t-2 border-success">Borda topo 2px</div>
```

---

## 🌑 Sombras

```html
<!-- Elevação -->
<div class="shadow-sm">Leve</div>
<div class="shadow-md">Padrão</div>
<div class="shadow-lg">Elevado</div>
<div class="shadow-xl">Muito elevado</div>

<!-- Coloridas -->
<div class="shadow-primary">Sombra rosa</div>
<div class="shadow-success">Sombra verde</div>
```

### CSS Variables
```css
box-shadow: var(--shadow-md);
box-shadow: var(--shadow-primary);
```

---

## ✨ Efeitos

### Hover Effects
```html
<div class="hover-lift">Levanta ao hover</div>
<div class="hover-scale">Aumenta ao hover</div>
<div class="hover-shadow">Sombra ao hover</div>
```

### Transitions
```html
<div class="transition-all">Transição em tudo</div>
<div class="transition-colors">Só cores</div>
<div class="transition-transform">Só transforms</div>
```

### Opacity
```html
<div class="opacity-0">Invisível</div>
<div class="opacity-50">50% transparente</div>
<div class="opacity-100">100% opaco</div>
```

### Cursor
```html
<div class="cursor-pointer">Pointer</div>
<div class="cursor-not-allowed">Não permitido</div>
```

---

## 🎁 Componentes Prontos

### Botões
```html
<!-- Primary Button -->
<button class="btn bg-gradient-primary text-white px-6 py-3 rounded-md shadow-md hover-lift">
  Salvar
</button>

<!-- Success Button -->
<button class="btn bg-gradient-success text-white px-4 py-2 rounded-md">
  Confirmar
</button>

<!-- Outline Button -->
<button class="btn border-2 border-primary text-primary px-4 py-2 rounded-md hover-shadow">
  Cancelar
</button>

<!-- Icon Button -->
<button class="btn bg-primary text-white p-3 rounded-full">
  <i class="fas fa-plus"></i>
</button>
```

### Cards
```html
<!-- Card Básico -->
<div class="card bg-white rounded-lg p-6 shadow-md">
  <h3 class="text-xl font-semibold mb-3">Título</h3>
  <p class="text-gray-600">Conteúdo</p>
</div>

<!-- Card com Accent -->
<div class="card bg-white rounded-lg p-6 shadow-md border-l-4 border-primary hover-lift">
  <h3 class="text-lg font-semibold text-gray-900">Card Destacado</h3>
  <p class="text-sm text-gray-600 mt-2">Com borda lateral.</p>
</div>
```

### Badges
```html
<span class="badge bg-success text-white px-3 py-1 rounded-full text-xs font-bold">
  Aprovada
</span>

<span class="badge bg-error text-white px-3 py-1 rounded-lg text-sm">
  Reprovada
</span>

<span class="badge bg-warning text-gray-900 px-4 py-2 rounded-md">
  Comitê
</span>
```

### Alerts
```html
<!-- Success -->
<div class="alert bg-success-light border-l-4 border-success p-4 rounded-lg">
  <p class="text-success-700 font-medium">Sucesso!</p>
</div>

<!-- Error -->
<div class="alert bg-error-light border-l-4 border-error p-4 rounded-lg">
  <p class="text-error-700 font-medium">Erro!</p>
</div>

<!-- Warning -->
<div class="alert bg-warning-light border-l-4 border-warning p-4 rounded-lg">
  <p class="text-warning-800 font-medium">Atenção!</p>
</div>
```

### Forms
```html
<div class="mb-4">
  <label class="form-label text-sm font-semibold text-gray-700 mb-2">
    Label
  </label>
  <input type="text" class="form-control w-full px-4 py-3 border-2 border-gray-200 rounded-md focus-ring">
</div>

<div class="mb-4">
  <label class="form-label text-sm font-semibold text-gray-700 mb-2">
    Select
  </label>
  <select class="form-select w-full px-4 py-3 border-2 border-gray-200 rounded-md bg-white">
    <option>Opção 1</option>
  </select>
</div>
```

---

## 🎯 Patterns Comuns

### Card de Dashboard
```html
<div class="card bg-white rounded-xl p-6 shadow-md hover-lift transition-base">
  <h4 class="text-gray-900 text-lg mb-3 font-semibold">Total</h4>
  <p class="text-primary text-4xl font-bold m-0">127</p>
</div>
```

### Card de Relatório
```html
<div class="card bg-white rounded-lg p-5 shadow-md border-l-4 border-primary hover-lift">
  <h3 class="text-primary text-lg font-semibold mb-2">Relatório #001</h3>
  <p class="text-gray-600 text-sm mb-2">Data: 15/01/2024</p>
  <span class="badge bg-success text-white px-3 py-1 rounded-full text-xs">Aprovada</span>
  <div class="mt-4">
    <a href="#" class="btn bg-gradient-primary text-white px-4 py-2 rounded-md text-sm">
      Ver Detalhes
    </a>
  </div>
</div>
```

### Formulário
```html
<form>
  <div class="mb-4">
    <label class="form-label text-sm font-semibold text-gray-700 mb-2">Nome</label>
    <input type="text" class="form-control w-full px-4 py-3 border-2 border-gray-200 rounded-md">
  </div>

  <button class="btn bg-gradient-primary text-white px-6 py-3 rounded-md w-full">
    Salvar
  </button>
</form>
```

### Grid de Cards
```html
<div class="d-grid grid-cols-3 gap-6 my-8">
  <div class="card bg-white rounded-xl p-6 shadow-md">Card 1</div>
  <div class="card bg-white rounded-xl p-6 shadow-md">Card 2</div>
  <div class="card bg-white rounded-xl p-6 shadow-md">Card 3</div>
</div>
```

### Header de Página
```html
<div class="page-header bg-white p-6 rounded-lg shadow-sm mb-6">
  <h1 class="text-4xl font-bold text-gray-900 m-0">Título da Página</h1>
  <p class="text-gray-600 mt-2">Descrição opcional</p>
</div>
```

---

## 📱 Responsividade

### Hide/Show por Device
```html
<div class="hide-mobile">Desktop apenas</div>
<div class="hide-tablet">Não mostra em tablet</div>
<div class="show-mobile">Mobile apenas</div>
```

### Breakpoints
```
xs:  0px      (Mobile small)
sm:  576px    (Mobile)
md:  768px    (Tablet)
lg:  992px    (Desktop small)
xl:  1200px   (Desktop)
2xl: 1400px   (Desktop large)
```

---

## 🚀 Quick Start

### 1. Adicione ao HTML
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/design-system.css') }}">
```

### 2. Use Utility Classes
```html
<button class="btn bg-gradient-primary text-white px-6 py-3 rounded-md shadow-md hover-lift">
  Clique Aqui
</button>
```

### 3. Ou Use Variáveis CSS
```css
.meu-componente {
  color: var(--primary);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
}
```

---

## 🎨 Paleta de Cores Visual

```
PRIMARY (Rosa Puket)
███████ #E6007E    var(--primary)
██████  #C2008E    var(--primary-hover)
█       #FFE0F0    var(--primary-light)

SUCCESS (Verde)
███████ #10B981    var(--success)
██████  #059669    var(--success-hover)
█       #D1FAE5    var(--success-light)

ERROR (Vermelho)
███████ #EF4444    var(--error)
██████  #DC2626    var(--error-hover)
█       #FEE2E2    var(--error-light)

WARNING (Âmbar)
███████ #F59E0B    var(--warning)
██████  #D97706    var(--warning-hover)
█       #FEF3C7    var(--warning-light)

INFO (Cyan)
███████ #06B6D4    var(--info)
██████  #0891B2    var(--info-hover)
█       #CFFAFE    var(--info-light)

GRAY (Neutrals)
███████ #111827    var(--gray-900)  Headings
██████  #1F2937    var(--gray-800)  Body text
█████   #4B5563    var(--gray-600)  Secondary
████    #9CA3AF    var(--gray-400)  Placeholder
███     #D1D5DB    var(--gray-300)  Borders
██      #E5E7EB    var(--gray-200)  Borders light
█       #F9FAFB    var(--gray-50)   Background
```

---

## 💡 Dicas Rápidas

### ✅ DOs (Faça)
```html
<!-- ✅ Use variáveis -->
<div style="color: var(--primary)">

<!-- ✅ Use utility classes -->
<div class="text-primary px-4 py-2">

<!-- ✅ Combine classes -->
<button class="btn bg-gradient-primary text-white px-6 py-3 rounded-md hover-lift">
```

### ❌ DON'Ts (Não Faça)
```html
<!-- ❌ Hard-coded values -->
<div style="color: #e6007e">

<!-- ❌ Random spacing -->
<div style="padding: 13px 27px">

<!-- ❌ Sem utility classes -->
<div style="background: white; padding: 20px; border-radius: 10px">
```

---

## 📚 Referências Rápidas

### Documentação Completa
- `DESIGN_SYSTEM_GUIDE.md` - Guia completo
- `DESIGN_TOKENS.md` - Todos os tokens
- `BEFORE_AFTER_EXAMPLES.md` - Exemplos práticos

### Valores Mais Usados
```css
/* Cores */
--primary: #E6007E
--success: #10B981
--error: #EF4444

/* Spacing */
--space-4: 16px
--space-6: 24px

/* Typography */
--text-base: 16px
--text-lg: 18px
--text-2xl: 24px

/* Border */
--radius-md: 8px
--radius-lg: 12px

/* Shadow */
--shadow-md: 0 4px 6px rgba(0,0,0,0.1)
```

---

**Design System v2.0** | Prova Modelagem | 2026-01-16
