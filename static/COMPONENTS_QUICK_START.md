# Biblioteca de Componentes - Quick Start Guide

## 📦 O que foi criado?

```
✅ components.css (31KB)           - Biblioteca CSS completa
✅ components-demo.html (43KB)     - Demo interativa
✅ COMPONENTS_DOCUMENTATION.md     - Documentação detalhada (29KB)
✅ COMPONENTS_CLASSES_LIST.md      - Referência de classes (16KB)
✅ COMPONENTS_README.md            - Guia de início (7KB)
```

**Total: 194 classes CSS únicas disponíveis!**

---

## 🚀 Começar em 3 Passos

### 1. Incluir no HTML
```html
<link rel="stylesheet" href="/static/css/components.css">
```

### 2. Ver a Demo
Abra em seu navegador:
```
http://localhost:5000/static/components-demo.html
```

### 3. Usar os Componentes
```html
<button class="btn btn-primary">Meu Botão</button>
```

---

## 📚 Documentação

### Para começar:
👉 **COMPONENTS_README.md** - Visão geral e exemplos básicos

### Para aprender:
👉 **components-demo.html** - Exemplos visuais interativos

### Para referência:
👉 **COMPONENTS_DOCUMENTATION.md** - Guia completo com exemplos
👉 **COMPONENTS_CLASSES_LIST.md** - Lista de todas as classes

---

## 🎨 Componentes Disponíveis

| Categoria | Classes | Descrição |
|-----------|---------|-----------|
| **1. Botões** | 25+ | Primário, secundário, outline, ghost, tamanhos, estados |
| **2. Formulários** | 30+ | Inputs, textareas, selects, checkbox, radio, switch |
| **3. Cards** | 15+ | Cards básicos, elevated, flat, grid responsivo |
| **4. Badges** | 22+ | Cores variadas, solid, pill, dot |
| **5. Alertas/Toasts** | 18+ | Success, error, warning, info, notifications |
| **6. Loading** | 20+ | Spinners, skeleton loaders, progress bars |
| **7. Modais** | 10+ | Tamanhos variados, header/body/footer |
| **8. Dropdowns** | 8+ | Menus, alinhamento, dividers |
| **9. Utilitários** | 60+ | Display, flex, spacing, text, colors |

---

## 💡 Exemplos de Uso Rápido

### Botão Primário
```html
<button class="btn btn-primary">Clique Aqui</button>
```

### Input com Validação
```html
<input type="text" class="form-control is-valid">
```

### Card Simples
```html
<div class="card">
  <h3 class="card-title">Título</h3>
  <p class="card-text">Conteúdo</p>
</div>
```

### Badge de Status
```html
<span class="badge badge-success">Ativo</span>
```

### Alerta
```html
<div class="alert alert-success">
  <div class="alert-content">
    <div class="alert-title">Sucesso!</div>
    <div class="alert-message">Mensagem aqui</div>
  </div>
</div>
```

### Spinner
```html
<div class="spinner"></div>
```

---

## 🎯 Padrões de Nomenclatura

```
[componente]-[variante]-[modificador]

btn-primary           # Botão primário
btn-outline-primary   # Botão outline primário
btn-sm                # Botão pequeno
card-elevated         # Card elevado
badge-solid-success   # Badge sólido de sucesso
```

---

## 🎨 Design Tokens (Variáveis CSS)

### Cores
```css
--primary: #e6007e     /* Rosa Puket */
--secondary: #6c757d   /* Cinza */
--success: #28a745     /* Verde */
--error: #dc3545       /* Vermelho */
--warning: #ffc107     /* Amarelo */
--info: #17a2b8        /* Azul */
```

### Espaçamento
```css
--space-1: 4px
--space-2: 8px
--space-3: 12px
--space-4: 16px
--space-5: 20px
--space-6: 24px
--space-8: 32px
```

### Tipografia
```css
--text-xs: 12px
--text-sm: 14px
--text-base: 16px
--text-lg: 18px
--text-xl: 20px
--text-2xl: 24px
--text-3xl: 30px
```

---

## 📋 Checklist de Classes Mais Usadas

### Botões
- [ ] `.btn .btn-primary`
- [ ] `.btn .btn-secondary`
- [ ] `.btn .btn-success`
- [ ] `.btn .btn-outline-primary`
- [ ] `.btn .btn-ghost`
- [ ] `.btn .btn-sm` / `.btn-lg`
- [ ] `.btn .btn-icon`

### Formulários
- [ ] `.form-control`
- [ ] `.form-label`
- [ ] `.is-valid` / `.is-invalid`
- [ ] `.form-check`
- [ ] `.form-switch`

### Cards
- [ ] `.card`
- [ ] `.card-title`
- [ ] `.card-text`
- [ ] `.card-header` / `.card-footer`
- [ ] `.card-grid`

### Badges
- [ ] `.badge .badge-success`
- [ ] `.badge .badge-error`
- [ ] `.badge .badge-solid-*`
- [ ] `.badge .badge-dot`

### Alertas
- [ ] `.alert .alert-success`
- [ ] `.alert .alert-error`
- [ ] `.toast .toast-success`

### Loading
- [ ] `.spinner`
- [ ] `.skeleton .skeleton-text`
- [ ] `.progress` / `.progress-bar`

### Utilitários
- [ ] `.d-flex`
- [ ] `.justify-center` / `.align-center`
- [ ] `.gap-4`
- [ ] `.m-4` / `.p-4`
- [ ] `.text-center`
- [ ] `.w-full`

---

## 🔧 Customização Rápida

### Mudar Cor Primária
```css
:root {
  --primary: #your-color;
  --primary-hover: #your-hover-color;
  --primary-light: rgba(your-color, 0.1);
}
```

### Criar Variante de Botão
```css
.btn-custom {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}
```

### Ajustar Espaçamento Padrão
```css
:root {
  --space-4: 1.5rem; /* Aumenta de 16px para 24px */
}
```

---

## 🎭 Combinações Populares

### Card com Botão
```html
<div class="card">
  <h3 class="card-title">Título</h3>
  <p class="card-text mb-4">Descrição</p>
  <button class="btn btn-primary w-full">Ação</button>
</div>
```

### Formulário Completo
```html
<div class="card">
  <form>
    <div class="form-group">
      <label class="form-label form-label-required">Nome</label>
      <input type="text" class="form-control">
    </div>

    <div class="form-check">
      <input type="checkbox" class="form-check-input" id="terms">
      <label class="form-check-label" for="terms">
        Aceito os termos
      </label>
    </div>

    <button type="submit" class="btn btn-primary w-full mt-4">
      Enviar
    </button>
  </form>
</div>
```

### Lista com Badges
```html
<div class="card">
  <div class="d-flex justify-between align-center mb-4">
    <h3 class="m-0">Item 1</h3>
    <span class="badge badge-success badge-dot">Ativo</span>
  </div>
  <p class="text-gray">Descrição do item</p>
  <div class="d-flex gap-2 mt-4">
    <button class="btn btn-sm btn-outline-primary">Editar</button>
    <button class="btn btn-sm btn-ghost text-error">Excluir</button>
  </div>
</div>
```

---

## ⚡ Dicas de Performance

1. **Inclua apenas uma vez** - O CSS já contém tudo
2. **Use classes nativas** - Não crie estilos inline quando possível
3. **Combine utilitários** - Ao invés de criar CSS custom
4. **Aproveite o cache** - O arquivo é pequeno (31KB)

---

## 🎯 Casos de Uso Comuns

### Dashboard
```html
<div class="card-grid">
  <div class="card">
    <div class="text-sm text-gray">Total</div>
    <div class="text-3xl font-bold text-primary">1,234</div>
    <span class="badge badge-success mt-2">+12%</span>
  </div>
  <!-- Mais cards... -->
</div>
```

### Formulário de Busca
```html
<div class="input-group">
  <input type="text" class="form-control" placeholder="Buscar...">
  <button class="btn btn-primary">🔍</button>
</div>
```

### Modal de Confirmação
```html
<div class="modal-backdrop">
  <div class="modal modal-sm">
    <div class="modal-header">
      <h3 class="modal-title">Confirmar</h3>
    </div>
    <div class="modal-body">
      <p>Deseja continuar?</p>
    </div>
    <div class="modal-footer">
      <button class="btn btn-ghost">Cancelar</button>
      <button class="btn btn-error">Confirmar</button>
    </div>
  </div>
</div>
```

### Lista de Tarefas
```html
<div class="card">
  <div class="d-flex justify-between align-center mb-4">
    <h3 class="m-0">Tarefas</h3>
    <button class="btn btn-sm btn-primary">+ Adicionar</button>
  </div>

  <div class="form-check">
    <input type="checkbox" class="form-check-input" checked>
    <label class="form-check-label">Tarefa concluída</label>
  </div>

  <div class="form-check">
    <input type="checkbox" class="form-check-input">
    <label class="form-check-label">Tarefa pendente</label>
  </div>
</div>
```

---

## 📱 Responsividade

Todos os componentes são **mobile-first** e se adaptam automaticamente:

```css
/* Cards se reorganizam em mobile */
.card-grid {
  grid-template-columns: 1fr; /* Mobile */
}

@media (min-width: 768px) {
  .card-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); /* Desktop */
  }
}
```

---

## ✨ Próximos Passos

1. ✅ **Abra a demo**: `/static/components-demo.html`
2. ✅ **Teste os componentes**: Copie e cole exemplos
3. ✅ **Customize**: Mude cores e espaçamentos
4. ✅ **Construa**: Crie suas próprias combinações!

---

## 📖 Recursos

| Arquivo | Quando Usar |
|---------|-------------|
| **components-demo.html** | Ver exemplos visuais |
| **COMPONENTS_README.md** | Visão geral rápida |
| **COMPONENTS_DOCUMENTATION.md** | Aprender em detalhes |
| **COMPONENTS_CLASSES_LIST.md** | Buscar classe específica |
| **COMPONENTS_QUICK_START.md** | Este arquivo - início rápido |

---

## 🎉 Pronto para Usar!

Você agora tem acesso a:
- ✅ **194 classes CSS** prontas para uso
- ✅ **8 categorias** de componentes
- ✅ **Demo interativa** completa
- ✅ **Documentação** detalhada
- ✅ **Design consistente** com tokens

**Comece agora mesmo!** 🚀

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="/static/css/components.css">
</head>
<body>
  <div class="card">
    <h1 class="card-title">Olá Mundo!</h1>
    <p class="card-text">Meu primeiro componente!</p>
    <button class="btn btn-primary">Clique aqui</button>
  </div>
</body>
</html>
```

---

**Versão 1.0.0** | Janeiro 2026
