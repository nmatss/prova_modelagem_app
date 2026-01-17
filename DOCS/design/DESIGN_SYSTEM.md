# Design System - Guia de Uso Completo

## Índice
1. [Visão Geral](#visão-geral)
2. [Estrutura de Arquivos](#estrutura-de-arquivos)
3. [Design Tokens](#design-tokens)
4. [Sistema de Cores](#sistema-de-cores)
5. [Tipografia](#tipografia)
6. [Espaçamento](#espaçamento)
7. [Componentes](#componentes)
8. [Utility Classes](#utility-classes)
9. [Antes e Depois](#antes-e-depois)
10. [Migração](#migração)
11. [Boas Práticas](#boas-práticas)

---

## Visão Geral

Este Design System foi criado para o projeto Prova Modelagem, fornecendo uma base sólida, consistente e escalável para todo o desenvolvimento front-end. Ele é baseado em:

- **Design Tokens**: Variáveis CSS reutilizáveis
- **Utility-First**: Classes utilitárias prontas para uso
- **Mobile-First**: Responsivo por padrão
- **Acessibilidade**: Foco em A11Y
- **Performance**: Otimizado para produção

### Arquivos do Design System

```
static/css/
├── design-system.css   ← Sistema de Design completo (NOVO)
├── custom.css          ← Estilos customizados do projeto
└── style.css           ← Estilos legados (dashboard)
```

### Como Integrar

No seu arquivo HTML `base.html`:

```html
<head>
    <!-- Bootstrap (se estiver usando) -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Design System (SEMPRE PRIMEIRO) -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/design-system.css') }}">

    <!-- Custom Styles -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/custom.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
```

---

## Design Tokens

### O Que São Design Tokens?

Design Tokens são variáveis CSS que armazenam valores de design. Eles garantem consistência visual em todo o projeto.

### Estrutura Hierárquica

```css
/* Tier 1: Base Colors (nunca use diretamente) */
--primary-500: #E6007E;

/* Tier 2: Semantic Tokens (use estes) */
--primary: var(--primary-500);
--primary-hover: var(--primary-600);
--primary-light: var(--primary-100);
```

### Benefícios

✅ **Consistência**: Todos usam os mesmos valores
✅ **Manutenção**: Altere em um lugar, atualiza em todos
✅ **Escalabilidade**: Fácil adicionar novos tokens
✅ **Dark Mode**: Pronto para temas alternativos

---

## Sistema de Cores

### Paleta Primária (Rosa Puket)

```css
/* Uso recomendado */
var(--primary)        /* #E6007E - Uso principal */
var(--primary-hover)  /* #C2008E - Estados hover */
var(--primary-light)  /* #FFE0F0 - Backgrounds leves */

/* Escala completa (50-900) */
--primary-50   /* #FFF0F7 - Ultra light */
--primary-100  /* #FFE0F0 - Very light */
--primary-200  /* #FFC2E0 - Light */
--primary-300  /* #FF99CF - Medium light */
--primary-400  /* #FF66B8 - Medium */
--primary-500  /* #E6007E - Base (default) */
--primary-600  /* #C2008E - Medium dark */
--primary-700  /* #9E006F - Dark */
--primary-800  /* #7A0050 - Very dark */
--primary-900  /* #560031 - Ultra dark */
```

### Cores Semânticas

#### Success (Verde)
```css
var(--success)        /* #10B981 - Ações positivas */
var(--success-hover)  /* #059669 - Hover state */
var(--success-light)  /* #D1FAE5 - Background leve */
```

#### Error/Danger (Vermelho)
```css
var(--error)          /* #EF4444 - Erros e ações destrutivas */
var(--danger)         /* Alias de --error */
var(--error-hover)    /* #DC2626 - Hover state */
var(--error-light)    /* #FEE2E2 - Background leve */
```

#### Warning (Amarelo)
```css
var(--warning)        /* #F59E0B - Avisos e alertas */
var(--warning-hover)  /* #D97706 - Hover state */
var(--warning-light)  /* #FEF3C7 - Background leve */
```

#### Info (Cyan)
```css
var(--info)           /* #06B6D4 - Informações */
var(--info-hover)     /* #0891B2 - Hover state */
var(--info-light)     /* #CFFAFE - Background leve */
```

### Neutrals (Escalas de Cinza)

```css
--gray-50   /* #F9FAFB - Backgrounds */
--gray-100  /* #F3F4F6 - Backgrounds suaves */
--gray-200  /* #E5E7EB - Bordas */
--gray-300  /* #D1D5DB - Bordas */
--gray-400  /* #9CA3AF - Placeholders */
--gray-500  /* #6B7280 - Texto desabilitado */
--gray-600  /* #4B5563 - Texto secundário */
--gray-700  /* #374151 - Texto secundário escuro */
--gray-800  /* #1F2937 - Texto principal */
--gray-900  /* #111827 - Texto em destaque */
```

### Exemplos de Uso

#### CSS Puro
```css
.meu-botao {
  background-color: var(--primary);
  color: var(--white);
  border: 2px solid var(--primary);
}

.meu-botao:hover {
  background-color: var(--primary-hover);
  border-color: var(--primary-hover);
}

.meu-card {
  background: var(--white);
  border: 1px solid var(--gray-200);
  color: var(--gray-800);
}
```

#### Utility Classes
```html
<!-- Background Colors -->
<div class="bg-primary text-white">Primary Button</div>
<div class="bg-success text-white">Success Alert</div>
<div class="bg-gray-50">Light Background</div>

<!-- Text Colors -->
<p class="text-primary">Texto em rosa</p>
<p class="text-gray-600">Texto secundário</p>
<p class="text-error">Mensagem de erro</p>

<!-- Border Colors -->
<div class="border-2 border-primary">Card com borda rosa</div>
```

---

## Tipografia

### Font Families

```css
--font-primary: 'Inter', -apple-system, ...;  /* Uso geral */
--font-mono: 'SF Mono', Monaco, ...;          /* Código */
```

### Font Sizes (Sistema de 8 níveis)

```css
--text-xs:    0.75rem    /* 12px - Legendas, captions */
--text-sm:    0.875rem   /* 14px - Texto pequeno */
--text-base:  1rem       /* 16px - Corpo de texto padrão */
--text-lg:    1.125rem   /* 18px - Texto destacado */
--text-xl:    1.25rem    /* 20px - Subtítulos */
--text-2xl:   1.5rem     /* 24px - Títulos pequenos */
--text-3xl:   1.875rem   /* 30px - Títulos médios */
--text-4xl:   2.25rem    /* 36px - Títulos grandes */
--text-5xl:   3rem       /* 48px - Hero titles */
--text-6xl:   3.75rem    /* 60px - Display text */
```

### Font Weights

```css
--font-light:      300  /* Texto leve */
--font-normal:     400  /* Padrão */
--font-medium:     500  /* Destaque sutil */
--font-semibold:   600  /* Destaque médio */
--font-bold:       700  /* Destaque forte */
--font-extrabold:  800  /* Extra destaque */
```

### Line Heights

```css
--leading-tight:    1.25   /* Títulos compactos */
--leading-snug:     1.375  /* Títulos normais */
--leading-normal:   1.5    /* Corpo de texto */
--leading-relaxed:  1.625  /* Texto confortável */
--leading-loose:    2      /* Texto muito espaçado */
```

### Exemplos de Uso

#### CSS
```css
h1 {
  font-size: var(--text-4xl);
  font-weight: var(--font-bold);
  line-height: var(--leading-tight);
  color: var(--gray-900);
}

p {
  font-size: var(--text-base);
  font-weight: var(--font-normal);
  line-height: var(--leading-normal);
  color: var(--gray-700);
}
```

#### HTML com Utility Classes
```html
<!-- Font Sizes -->
<h1 class="text-4xl font-bold">Título Principal</h1>
<h2 class="text-2xl font-semibold">Subtítulo</h2>
<p class="text-base">Corpo de texto padrão</p>
<small class="text-sm text-gray-600">Texto pequeno</small>

<!-- Font Weights -->
<p class="font-light">Leve</p>
<p class="font-normal">Normal</p>
<p class="font-semibold">Semi-negrito</p>
<p class="font-bold">Negrito</p>

<!-- Line Heights -->
<p class="leading-tight">Linha apertada</p>
<p class="leading-normal">Linha normal</p>
<p class="leading-relaxed">Linha relaxada</p>

<!-- Combinações -->
<h2 class="text-3xl font-bold text-primary leading-tight">
  Título com Múltiplas Classes
</h2>
```

---

## Espaçamento

### Sistema de Espaçamento (Base 4px)

```css
--space-0:   0         /* 0px */
--space-1:   0.25rem   /* 4px */
--space-2:   0.5rem    /* 8px */
--space-3:   0.75rem   /* 12px */
--space-4:   1rem      /* 16px */
--space-5:   1.25rem   /* 20px */
--space-6:   1.5rem    /* 24px */
--space-8:   2rem      /* 32px */
--space-10:  2.5rem    /* 40px */
--space-12:  3rem      /* 48px */
--space-16:  4rem      /* 64px */
--space-20:  5rem      /* 80px */
--space-24:  6rem      /* 96px */
```

### Padding Utilities

```html
<!-- Todos os lados -->
<div class="p-4">padding: 16px</div>
<div class="p-8">padding: 32px</div>

<!-- Horizontal (X axis) -->
<div class="px-4">padding-left: 16px; padding-right: 16px</div>

<!-- Vertical (Y axis) -->
<div class="py-6">padding-top: 24px; padding-bottom: 24px</div>

<!-- Lados individuais -->
<div class="pt-4">padding-top: 16px</div>
<div class="pb-6">padding-bottom: 24px</div>
<div class="pl-3">padding-left: 12px</div>
<div class="pr-8">padding-right: 32px</div>
```

### Margin Utilities

```html
<!-- Todos os lados -->
<div class="m-4">margin: 16px</div>
<div class="m-8">margin: 32px</div>

<!-- Horizontal (X axis) -->
<div class="mx-auto">margin-left: auto; margin-right: auto</div>
<div class="mx-4">margin-left: 16px; margin-right: 16px</div>

<!-- Vertical (Y axis) -->
<div class="my-6">margin-top: 24px; margin-bottom: 24px</div>

<!-- Lados individuais -->
<div class="mt-4">margin-top: 16px</div>
<div class="mb-6">margin-bottom: 24px</div>
<div class="ml-auto">margin-left: auto</div>
<div class="mr-2">margin-right: 8px</div>
```

### Gap (Flexbox/Grid)

```html
<!-- Flexbox com gap -->
<div class="d-flex gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

<!-- Grid com gap -->
<div class="d-grid grid-cols-3 gap-6">
  <div>Card 1</div>
  <div>Card 2</div>
  <div>Card 3</div>
</div>
```

---

## Componentes

### Buttons

```html
<!-- Primary Button -->
<button class="btn bg-gradient-primary text-white px-6 py-3 rounded-lg shadow-md hover-lift">
  Botão Principal
</button>

<!-- Success Button -->
<button class="btn bg-gradient-success text-white px-4 py-2 rounded-md">
  Salvar
</button>

<!-- Outline Button -->
<button class="btn border-2 border-primary text-primary px-4 py-2 rounded-md hover-shadow">
  Cancelar
</button>

<!-- Icon Button -->
<button class="btn bg-primary text-white p-3 rounded-full shadow-primary">
  <i class="fas fa-plus"></i>
</button>
```

### Cards

```html
<!-- Basic Card -->
<div class="card bg-white rounded-lg shadow-md p-6">
  <h3 class="text-xl font-semibold mb-3">Título do Card</h3>
  <p class="text-gray-600">Conteúdo do card aqui.</p>
</div>

<!-- Card with Border Accent -->
<div class="card bg-white rounded-lg shadow-sm border-l-4 border-primary p-6 hover-lift">
  <h3 class="text-lg font-semibold text-gray-900">Card Destacado</h3>
  <p class="text-sm text-gray-600 mt-2">Com borda lateral colorida.</p>
</div>

<!-- Glass Card -->
<div class="card glass rounded-xl p-8 shadow-xl">
  <h2 class="text-2xl font-bold text-gray-900 mb-4">Glass Effect</h2>
  <p class="text-gray-700">Card com efeito de vidro fosco.</p>
</div>
```

### Badges

```html
<span class="badge bg-success text-white px-3 py-1 rounded-full text-sm font-semibold">
  Aprovada
</span>

<span class="badge bg-error text-white px-3 py-1 rounded-lg text-xs uppercase tracking-wide">
  Reprovada
</span>

<span class="badge bg-warning text-gray-900 px-4 py-2 rounded-md font-medium">
  Comitê
</span>
```

### Alerts

```html
<!-- Success Alert -->
<div class="alert bg-success-light border-l-4 border-success p-4 rounded-lg">
  <p class="text-success-600 font-medium">Operação realizada com sucesso!</p>
</div>

<!-- Error Alert -->
<div class="alert bg-error-light border-l-4 border-error p-4 rounded-lg">
  <p class="text-error-600 font-medium">Ocorreu um erro. Tente novamente.</p>
</div>

<!-- Info Alert -->
<div class="alert bg-info-light border-l-4 border-info p-4 rounded-lg">
  <div class="d-flex items-center gap-3">
    <i class="fas fa-info-circle text-info text-xl"></i>
    <p class="text-info-700">Informação importante para o usuário.</p>
  </div>
</div>
```

### Forms

```html
<!-- Form Group -->
<div class="mb-4">
  <label class="form-label text-sm font-semibold text-gray-700 mb-2">
    Nome Completo
  </label>
  <input
    type="text"
    class="form-control w-full px-4 py-2 border-2 border-gray-200 rounded-md focus-ring"
    placeholder="Digite seu nome"
  >
</div>

<!-- Select -->
<div class="mb-4">
  <label class="form-label text-sm font-semibold text-gray-700 mb-2">
    Categoria
  </label>
  <select class="form-select w-full px-4 py-2 border-2 border-gray-200 rounded-md">
    <option>Selecione...</option>
    <option>Infantil</option>
    <option>Adulto</option>
  </select>
</div>

<!-- Textarea -->
<div class="mb-4">
  <label class="form-label text-sm font-semibold text-gray-700 mb-2">
    Observações
  </label>
  <textarea
    class="form-control w-full px-4 py-3 border-2 border-gray-200 rounded-md"
    rows="4"
    placeholder="Escreva suas observações..."
  ></textarea>
</div>
```

### Modals

```html
<!-- Modal Structure -->
<div class="modal" id="meuModal">
  <div class="modal-dialog rounded-xl shadow-2xl">
    <div class="modal-content">
      <!-- Header -->
      <div class="modal-header bg-gray-50 px-6 py-4 border-b-2 border-gray-200">
        <h5 class="modal-title text-xl font-bold text-gray-900">Título do Modal</h5>
        <button class="btn-close" data-bs-dismiss="modal"></button>
      </div>

      <!-- Body -->
      <div class="modal-body px-6 py-6">
        <p class="text-gray-700">Conteúdo do modal aqui.</p>
      </div>

      <!-- Footer -->
      <div class="modal-footer bg-gray-50 px-6 py-4 border-t border-gray-200">
        <button class="btn border-2 border-gray-300 px-4 py-2 rounded-md">
          Cancelar
        </button>
        <button class="btn bg-gradient-primary text-white px-6 py-2 rounded-md shadow-md">
          Confirmar
        </button>
      </div>
    </div>
  </div>
</div>
```

---

## Utility Classes

### Layout

```html
<!-- Display -->
<div class="d-none">Escondido</div>
<div class="d-block">Block</div>
<div class="d-flex">Flexbox</div>
<div class="d-grid">Grid</div>

<!-- Flexbox -->
<div class="d-flex justify-center items-center gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

<div class="d-flex flex-column justify-between items-stretch">
  <div>Top</div>
  <div>Bottom</div>
</div>

<!-- Grid -->
<div class="d-grid grid-cols-3 gap-4">
  <div>1</div>
  <div>2</div>
  <div>3</div>
</div>

<!-- Width & Height -->
<div class="w-full h-full">100% width and height</div>
<div class="w-50">50% width</div>
```

### Borders & Radius

```html
<!-- Border Radius -->
<div class="rounded-sm">Small radius (4px)</div>
<div class="rounded-md">Medium radius (8px)</div>
<div class="rounded-lg">Large radius (12px)</div>
<div class="rounded-xl">Extra large (16px)</div>
<div class="rounded-full">Circle/Pill shape</div>

<!-- Border Width -->
<div class="border-2 border-gray-300">2px border</div>
<div class="border-l-4 border-primary">Left border 4px</div>
<div class="border-t-2 border-success">Top border 2px</div>
```

### Shadows

```html
<!-- Elevation -->
<div class="shadow-sm">Small shadow</div>
<div class="shadow-md">Medium shadow</div>
<div class="shadow-lg">Large shadow</div>
<div class="shadow-xl">Extra large shadow</div>
<div class="shadow-2xl">2XL shadow</div>

<!-- Colored Shadows -->
<div class="shadow-primary">Primary colored shadow</div>
<div class="shadow-success">Success colored shadow</div>
```

### Effects

```html
<!-- Opacity -->
<div class="opacity-0">Invisível</div>
<div class="opacity-50">50% transparente</div>
<div class="opacity-100">100% opaco</div>

<!-- Blur -->
<div class="backdrop-blur-sm">Blur background</div>
<div class="backdrop-blur-lg">Strong blur</div>

<!-- Cursor -->
<div class="cursor-pointer">Pointer cursor</div>
<div class="cursor-not-allowed">Not allowed cursor</div>

<!-- Hover Effects -->
<div class="hover-lift">Levanta ao passar o mouse</div>
<div class="hover-scale">Aumenta ao passar o mouse</div>
<div class="hover-shadow">Sombra ao passar o mouse</div>
```

### Transitions

```html
<!-- Transition Classes -->
<button class="btn transition-all hover:scale-105">
  Smooth transition
</button>

<div class="card transition-transform hover-lift">
  Card com transição
</div>

<a href="#" class="text-primary transition-colors hover:text-primary-hover">
  Link com transição de cor
</a>
```

### Text Utilities

```html
<!-- Alignment -->
<p class="text-left">Alinhado à esquerda</p>
<p class="text-center">Centralizado</p>
<p class="text-right">Alinhado à direita</p>

<!-- Transform -->
<p class="uppercase">MAIÚSCULAS</p>
<p class="lowercase">minúsculas</p>
<p class="capitalize">Primeira Letra Maiúscula</p>

<!-- Decoration -->
<p class="underline">Sublinhado</p>
<p class="no-underline">Sem sublinhado</p>
<p class="line-through">Riscado</p>

<!-- Truncate -->
<p class="truncate">Texto muito longo que será cortado com reticências...</p>
<p class="line-clamp-2">Texto limitado a 2 linhas com reticências...</p>
```

---

## Antes e Depois

### Antes (Hard-coded)

```html
<!-- ❌ Ruim: Valores hard-coded -->
<style>
.meu-botao {
  background-color: #e6007e;
  padding: 12px 24px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.meu-botao:hover {
  background-color: #c20069;
  transform: translateY(-2px);
}
</style>

<button class="meu-botao">Clique Aqui</button>
```

### Depois (Design System)

```html
<!-- ✅ Bom: Usando Design System -->
<button class="btn bg-gradient-primary text-white px-6 py-3 rounded-md shadow-md hover-lift transition-all">
  Clique Aqui
</button>

<!-- Ou com variáveis CSS -->
<style>
.meu-botao {
  background-color: var(--primary);
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  transition: var(--transition-all);
}

.meu-botao:hover {
  background-color: var(--primary-hover);
  transform: translateY(-2px);
}
</style>
```

### Comparação de Cards

#### Antes
```html
<div style="background: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
  <h3 style="color: #e6007e; font-size: 18px; font-weight: 600;">Título</h3>
  <p style="color: #6c757d; font-size: 14px; margin-top: 8px;">Descrição</p>
</div>
```

#### Depois
```html
<div class="card bg-white rounded-lg p-5 shadow-md">
  <h3 class="text-primary text-lg font-semibold">Título</h3>
  <p class="text-gray-600 text-sm mt-2">Descrição</p>
</div>
```

---

## Migração

### Checklist de Migração

- [ ] **Passo 1**: Adicionar `design-system.css` ao projeto
- [ ] **Passo 2**: Importar no `base.html` ANTES de outros CSS
- [ ] **Passo 3**: Identificar cores hard-coded e substituir por variáveis
- [ ] **Passo 4**: Identificar valores de espaçamento hard-coded
- [ ] **Passo 5**: Substituir utility classes inline por classes do design system
- [ ] **Passo 6**: Testar em todos os breakpoints
- [ ] **Passo 7**: Validar acessibilidade
- [ ] **Passo 8**: Remover código duplicado

### Estratégia de Migração Gradual

#### 1. Comece pelos componentes mais usados
```
Prioridade Alta:
- Buttons
- Cards
- Forms
- Alerts

Prioridade Média:
- Modals
- Badges
- Navigation

Prioridade Baixa:
- Animações customizadas
- Componentes únicos
```

#### 2. Migre página por página
```
1. Dashboard (páginas principais)
2. Formulários (novo_relatorio, editar)
3. Páginas de detalhes
4. Admin pages
5. Error pages
```

#### 3. Refatore CSS customizado

**Antes (custom.css):**
```css
.btn-primary {
  background: linear-gradient(135deg, #e6007e 0%, #c20069 100%);
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
}
```

**Depois (custom.css):**
```css
.btn-primary {
  background: var(--bg-gradient-primary);
  color: var(--white);
  padding: var(--space-3) var(--space-5);
  border-radius: var(--radius-md);
}
```

### Exemplo Completo de Migração

#### Antes: dashboard.html
```html
<div style="background: white; padding: 20px; margin-bottom: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
  <h2 style="color: #e6007e; font-size: 24px; margin-bottom: 15px;">Relatórios Recentes</h2>

  <div style="display: flex; gap: 15px; flex-wrap: wrap;">
    <div style="flex: 1; min-width: 200px; background: #f9fafb; padding: 15px; border-radius: 8px;">
      <h4 style="color: #1f2937; font-size: 16px;">Relatório #001</h4>
      <p style="color: #6b7280; font-size: 14px; margin-top: 8px;">Descrição do relatório</p>
      <span style="background: #10b981; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px;">Aprovada</span>
    </div>
  </div>
</div>
```

#### Depois: dashboard.html
```html
<div class="card bg-white p-5 mb-5 rounded-lg shadow-md">
  <h2 class="text-primary text-2xl font-semibold mb-4">Relatórios Recentes</h2>

  <div class="d-flex gap-4 flex-wrap">
    <div class="flex-1" style="min-width: 200px;">
      <div class="bg-gray-50 p-4 rounded-md">
        <h4 class="text-gray-900 text-base font-medium">Relatório #001</h4>
        <p class="text-gray-600 text-sm mt-2">Descrição do relatório</p>
        <span class="badge bg-success text-white px-3 py-1 rounded-full text-xs mt-3 d-inline-block">
          Aprovada
        </span>
      </div>
    </div>
  </div>
</div>
```

---

## Boas Práticas

### ✅ DO (Faça)

1. **Use variáveis CSS sempre que possível**
   ```css
   /* ✅ Bom */
   .minha-classe {
     color: var(--primary);
     padding: var(--space-4);
   }
   ```

2. **Use utility classes para estilos simples**
   ```html
   <!-- ✅ Bom -->
   <div class="mt-4 p-6 bg-white rounded-lg shadow-md">
   ```

3. **Combine utility classes com classes semânticas**
   ```html
   <!-- ✅ Bom -->
   <button class="btn-submit bg-gradient-primary text-white px-6 py-3 rounded-md hover-lift">
     Enviar
   </button>
   ```

4. **Use a escala de espaçamento**
   ```css
   /* ✅ Bom */
   margin-top: var(--space-4);    /* 16px */
   margin-bottom: var(--space-6); /* 24px */
   ```

5. **Use cores semânticas**
   ```html
   <!-- ✅ Bom -->
   <div class="alert bg-success-light text-success-700">Sucesso!</div>
   ```

### ❌ DON'T (Não Faça)

1. **Não use valores hard-coded**
   ```css
   /* ❌ Ruim */
   .minha-classe {
     color: #e6007e;
     padding: 16px;
   }
   ```

2. **Não crie utility classes duplicadas**
   ```css
   /* ❌ Ruim - já existe .mt-4 */
   .margin-top-16 {
     margin-top: 16px;
   }
   ```

3. **Não use !important desnecessariamente**
   ```css
   /* ❌ Ruim */
   .minha-classe {
     color: var(--primary) !important;
   }
   ```

4. **Não ignore a escala de cores**
   ```css
   /* ❌ Ruim */
   .custom-green {
     background: #12d34e; /* Cor fora da paleta */
   }

   /* ✅ Bom */
   .custom-green {
     background: var(--success); /* Usa cor da paleta */
   }
   ```

5. **Não crie espaçamentos aleatórios**
   ```css
   /* ❌ Ruim */
   padding: 13px 27px;

   /* ✅ Bom */
   padding: var(--space-3) var(--space-6); /* 12px 24px */
   ```

### Performance

1. **Carregue o design-system.css primeiro**
   ```html
   <!-- ✅ Ordem correta -->
   <link rel="stylesheet" href="design-system.css">
   <link rel="stylesheet" href="custom.css">
   ```

2. **Use CSS variables no navegador (não processa no servidor)**
   ```css
   /* ✅ Rápido no navegador */
   color: var(--primary);
   ```

3. **Evite animações pesadas em mobile**
   ```css
   /* ✅ Bom: Simplifica em mobile */
   @media (max-width: 768px) {
     .hover-lift:hover {
       transform: none; /* Remove animação em mobile */
     }
   }
   ```

### Acessibilidade

1. **Use contraste adequado**
   ```html
   <!-- ✅ Bom contraste -->
   <button class="bg-primary text-white">Botão</button>

   <!-- ❌ Contraste ruim -->
   <button class="bg-gray-200 text-gray-300">Botão</button>
   ```

2. **Adicione estados de foco**
   ```html
   <button class="btn focus-ring">Botão Acessível</button>
   ```

3. **Use tamanhos de fonte legíveis**
   ```css
   /* ✅ Bom: mínimo 14px em mobile */
   font-size: var(--text-sm); /* 14px */

   /* ❌ Ruim: muito pequeno */
   font-size: 10px;
   ```

### Responsividade

1. **Pense Mobile-First**
   ```css
   /* ✅ Mobile first */
   .card {
     padding: var(--space-4);
   }

   @media (min-width: 768px) {
     .card {
       padding: var(--space-6);
     }
   }
   ```

2. **Use utility classes responsivas**
   ```html
   <div class="d-block hide-mobile">Mostra apenas em desktop</div>
   <div class="d-none show-mobile">Mostra apenas em mobile</div>
   ```

---

## Recursos Adicionais

### Referências Rápidas

#### Cores mais usadas
```
Primary:   var(--primary)       #E6007E
Success:   var(--success)       #10B981
Error:     var(--error)         #EF4444
Warning:   var(--warning)       #F59E0B
Info:      var(--info)          #06B6D4
Gray:      var(--gray-600)      #4B5563
```

#### Espaçamentos mais usados
```
Small:     var(--space-2)       8px
Medium:    var(--space-4)       16px
Large:     var(--space-6)       24px
XLarge:    var(--space-8)       32px
```

#### Font sizes mais usados
```
Small:     var(--text-sm)       14px
Base:      var(--text-base)     16px
Large:     var(--text-lg)       18px
Title:     var(--text-2xl)      24px
Hero:      var(--text-4xl)      36px
```

### Ferramentas Úteis

- **Browser DevTools**: Inspecione e teste variáveis CSS
- **Contrast Checker**: Verifique contraste de cores (WCAG)
- **Responsive Design Mode**: Teste em diferentes tamanhos

### Contato e Suporte

Para dúvidas ou sugestões sobre o Design System:
- Abra uma issue no repositório
- Consulte a documentação oficial
- Entre em contato com a equipe de desenvolvimento

---

**Versão**: 2.0
**Última atualização**: 2026-01-16
**Autor**: Design System Team - Prova Modelagem
