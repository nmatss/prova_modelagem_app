# Biblioteca de Componentes Reutilizáveis

## Início Rápido

### 1. Incluir no seu HTML

```html
<link rel="stylesheet" href="/static/css/components.css">
```

### 2. Ver a Demo

Abra o arquivo `/static/components-demo.html` no navegador para ver todos os componentes em ação.

### 3. Documentação

- **Documentação Completa**: `COMPONENTS_DOCUMENTATION.md` - Guia detalhado com exemplos
- **Lista de Classes**: `COMPONENTS_CLASSES_LIST.md` - Referência rápida de todas as classes

---

## Arquivos da Biblioteca

```
/static/
├── css/
│   └── components.css                    # 31KB - Arquivo CSS principal
├── components-demo.html                  # 43KB - Demo interativa
├── COMPONENTS_DOCUMENTATION.md           # 29KB - Documentação completa
├── COMPONENTS_CLASSES_LIST.md            # 16KB - Lista de classes
└── COMPONENTS_README.md                  # Este arquivo
```

---

## Componentes Disponíveis

### 1. Botões
- 6 variantes de cor (primary, secondary, success, error, warning, info)
- 3 estilos (sólido, outline, ghost)
- 5 tamanhos (xs, sm, default, lg, xl)
- Estados: normal, hover, disabled, loading
- Botões com ícone

### 2. Formulários
- Inputs, textareas, selects
- Estados: válido, inválido, desabilitado
- Checkbox, radio, switch
- Input groups (prefixo/sufixo)
- Validação visual integrada

### 3. Cards
- 3 variações (normal, flat, elevated)
- 3 tamanhos (sm, default, lg)
- Header, body, footer
- Grid responsivo

### 4. Badges
- 7 cores (primary, secondary, success, error, warning, info, gray)
- Versões light e solid
- 3 tamanhos (sm, default, lg)
- Badge com dot, pill

### 5. Alertas e Toasts
- 4 tipos (success, error, warning, info)
- Alertas inline
- Toast notifications (posição fixa)
- Animações de entrada/saída

### 6. Loading States
- Spinners (4 tamanhos, cores customizáveis)
- Skeleton loaders
- Progress bars (com variantes striped e animated)
- Loading overlay

### 7. Modais
- 4 tamanhos (sm, default, lg, xl)
- Header, body, footer
- Backdrop escuro
- Animações suaves

### 8. Dropdowns
- Dropdown menu
- Alinhamento esquerda/direita
- Headers, dividers
- Item de perigo

### 9. Classes Utilitárias
- Display (flex, grid, block, etc)
- Flexbox (justify, align, gap)
- Espaçamento (margin, padding)
- Tipografia (tamanhos, pesos, alinhamento)
- Cores (texto e fundo)
- Border radius, shadow, cursor, overflow

---

## Design Tokens

A biblioteca usa **CSS Custom Properties (variáveis)** para facilitar a customização:

```css
/* Cores */
--primary: #e6007e;
--secondary: #6c757d;
--success: #28a745;
--error: #dc3545;
--warning: #ffc107;
--info: #17a2b8;

/* Espaçamento */
--space-1 a --space-12

/* Tipografia */
--text-xs a --text-3xl

/* Border Radius */
--radius-sm a --radius-full

/* Sombras */
--shadow-sm a --shadow-xl
```

---

## Exemplos Rápidos

### Botão Primário
```html
<button class="btn btn-primary">Clique Aqui</button>
```

### Formulário com Validação
```html
<div class="form-group">
  <label class="form-label form-label-required">Email</label>
  <input type="email" class="form-control is-valid">
  <div class="form-feedback form-feedback-success">Email válido!</div>
</div>
```

### Card Simples
```html
<div class="card">
  <h3 class="card-title">Título</h3>
  <p class="card-text">Conteúdo do card</p>
  <button class="btn btn-primary">Ação</button>
</div>
```

### Badge de Status
```html
<span class="badge badge-success badge-dot">Ativo</span>
```

### Alerta de Sucesso
```html
<div class="alert alert-success">
  <div class="alert-icon">✓</div>
  <div class="alert-content">
    <div class="alert-title">Sucesso!</div>
    <div class="alert-message">Operação concluída.</div>
  </div>
</div>
```

### Spinner de Loading
```html
<div class="spinner"></div>
```

### Modal Básico
```html
<div class="modal-backdrop">
  <div class="modal">
    <div class="modal-header">
      <h3 class="modal-title">Título</h3>
      <button class="modal-close">✕</button>
    </div>
    <div class="modal-body">Conteúdo...</div>
    <div class="modal-footer">
      <button class="btn btn-primary">Confirmar</button>
    </div>
  </div>
</div>
```

---

## Customização

### Sobrescrever Cores

Crie seu próprio CSS após incluir `components.css`:

```css
:root {
  --primary: #your-color;
  --primary-hover: #your-hover-color;
  --primary-light: rgba(your-color, 0.1);
}
```

### Criar Variantes Personalizadas

```css
.btn-custom {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.btn-custom:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}
```

---

## Boas Práticas

### 1. Sempre use a classe base
```html
✅ <button class="btn btn-primary">Botão</button>
❌ <button class="btn-primary">Botão</button>
```

### 2. Combine classes utilitárias
```html
<div class="card d-flex flex-column gap-4 p-6">
  <!-- Conteúdo -->
</div>
```

### 3. Use design tokens para consistência
```css
/* Ao invés de */
padding: 16px;

/* Use */
padding: var(--space-4);
```

### 4. Mobile-first
```css
/* A biblioteca é mobile-first */
/* Componentes se adaptam automaticamente */
```

---

## Estrutura de Classes

A biblioteca segue um padrão de nomenclatura consistente:

```
[componente]-[variante]-[modificador]

Exemplos:
btn-primary          # Botão primário
btn-outline-primary  # Botão outline primário
btn-primary-sm       # Botão primário pequeno
card-elevated        # Card elevado
badge-solid-success  # Badge sólido de sucesso
```

---

## Características

✅ **180+ classes utilitárias**
✅ **Design consistente** com sistema de tokens
✅ **Totalmente responsivo** (mobile-first)
✅ **Leve e performático** (31KB CSS)
✅ **Fácil customização** via CSS custom properties
✅ **Animações suaves** em todos os componentes
✅ **Acessível** com semântica HTML apropriada
✅ **Sem dependências** (CSS puro)

---

## Compatibilidade

- ✅ Chrome/Edge (últimas 2 versões)
- ✅ Firefox (últimas 2 versões)
- ✅ Safari (últimas 2 versões)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

---

## Suporte

Para dúvidas ou sugestões, consulte:
1. **Demo**: `/static/components-demo.html` - Exemplos visuais
2. **Documentação**: `COMPONENTS_DOCUMENTATION.md` - Guia completo
3. **Lista de Classes**: `COMPONENTS_CLASSES_LIST.md` - Referência rápida

---

## Versão

**v1.0.0** - Janeiro 2026

**Criado por**: Sistema de Design Interno

---

## Próximos Passos

1. ✅ Explore a demo: `/static/components-demo.html`
2. ✅ Leia a documentação: `COMPONENTS_DOCUMENTATION.md`
3. ✅ Consulte as classes: `COMPONENTS_CLASSES_LIST.md`
4. ✅ Comece a usar nos seus projetos!

---

## Changelog

### v1.0.0 (2026-01-16)
- 🎉 Release inicial
- ✨ 8 categorias de componentes
- ✨ 180+ classes utilitárias
- ✨ Design tokens completo
- ✨ Demo interativa
- ✨ Documentação completa
