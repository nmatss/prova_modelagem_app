# Lista Completa de Classes - Biblioteca de Componentes

## Índice Rápido
- [Botões](#botões)
- [Formulários](#formulários)
- [Cards](#cards)
- [Badges](#badges)
- [Alertas e Toasts](#alertas-e-toasts)
- [Loading States](#loading-states)
- [Modais](#modais)
- [Dropdowns](#dropdowns)
- [Utilitários - Display](#utilitários---display)
- [Utilitários - Flexbox](#utilitários---flexbox)
- [Utilitários - Espaçamento](#utilitários---espaçamento)
- [Utilitários - Texto](#utilitários---texto)
- [Utilitários - Cores](#utilitários---cores)
- [Utilitários - Outros](#utilitários---outros)

---

## Botões

### Classes Base
```
.btn                    # Classe base (obrigatória)
```

### Variantes de Cor
```
.btn-primary           # Botão primário (rosa)
.btn-secondary         # Botão secundário (cinza)
.btn-success           # Botão de sucesso (verde)
.btn-error             # Botão de erro (vermelho)
.btn-warning           # Botão de aviso (amarelo)
.btn-info              # Botão informativo (azul)
```

### Variantes de Estilo
```
.btn-outline-primary   # Outline primário
.btn-outline-secondary # Outline secundário
.btn-ghost             # Botão ghost/text
```

### Tamanhos
```
.btn-xs                # Extra pequeno (28px altura)
.btn-sm                # Pequeno (32px altura)
                       # Default (40px altura)
.btn-lg                # Grande (48px altura)
.btn-xl                # Extra grande (56px altura)
```

### Formatos
```
.btn-icon              # Botão circular para ícone
.btn-rounded           # Bordas totalmente arredondadas
.btn-square            # Sem arredondamento
.btn-with-icon         # Botão com ícone e texto
```

### Estados
```
disabled               # Atributo HTML para desabilitar
.btn-loading           # Estado de carregamento
```

---

## Formulários

### Labels
```
.form-label            # Label padrão
.form-label-required   # Adiciona asterisco de obrigatório
```

### Inputs, Textareas e Selects
```
.form-control          # Classe base para inputs
.form-control-sm       # Input pequeno
.form-control-lg       # Input grande
```

### Estados do Input
```
.is-valid              # Input válido (verde)
.is-invalid            # Input inválido (vermelho)
disabled               # Atributo HTML para desabilitar
```

### Feedback
```
.form-feedback                # Mensagem de feedback base
.form-feedback-success        # Feedback de sucesso
.form-feedback-error          # Feedback de erro
.form-feedback-info           # Feedback informativo
```

### Checkbox e Radio
```
.form-check            # Container de checkbox/radio
.form-check-input      # Input checkbox ou radio
.form-check-label      # Label do checkbox/radio
```

### Switch
```
.form-switch           # Container do switch
.form-switch-input     # Input do switch
.form-switch-label     # Label do switch
```

### Input Group
```
.input-group           # Container do input group
.input-group-addon     # Prefixo ou sufixo
```

### Containers
```
.form-group            # Container de um campo
```

---

## Cards

### Classes Base
```
.card                  # Card base
.card-flat             # Remove hover effect
.card-elevated         # Sombra mais forte
```

### Tamanhos
```
.card-sm               # Card pequeno
                       # Default
.card-lg               # Card grande
```

### Partes do Card
```
.card-header           # Cabeçalho do card
.card-body             # Corpo do card
.card-footer           # Rodapé do card
.card-title            # Título do card
.card-subtitle         # Subtítulo do card
.card-text             # Texto do card
.card-img-top          # Imagem no topo
```

### Layout
```
.card-grid             # Grid responsivo de cards
```

---

## Badges

### Badges Light
```
.badge                 # Classe base
.badge-primary         # Badge primário light
.badge-secondary       # Badge secundário light
.badge-success         # Badge de sucesso light
.badge-error           # Badge de erro light
.badge-warning         # Badge de aviso light
.badge-info            # Badge informativo light
.badge-gray            # Badge cinza
```

### Badges Sólidos
```
.badge-solid-primary   # Badge primário sólido
.badge-solid-secondary # Badge secundário sólido
.badge-solid-success   # Badge de sucesso sólido
.badge-solid-error     # Badge de erro sólido
.badge-solid-warning   # Badge de aviso sólido
.badge-solid-info      # Badge informativo sólido
```

### Tamanhos
```
.badge-sm              # Badge pequeno
                       # Default
.badge-lg              # Badge grande
```

### Variações
```
.badge-dot             # Adiciona ponto antes do texto
.badge-icon            # Badge com ícone
.badge-pill            # Formato pill/cápsula
```

---

## Alertas e Toasts

### Alertas
```
.alert                 # Classe base de alerta
.alert-success         # Alerta de sucesso
.alert-error           # Alerta de erro
.alert-warning         # Alerta de aviso
.alert-info            # Alerta informativo
```

### Partes do Alerta
```
.alert-icon            # Container do ícone
.alert-content         # Container do conteúdo
.alert-title           # Título do alerta
.alert-message         # Mensagem do alerta
.alert-close           # Botão de fechar
```

### Toasts
```
.toast-container       # Container de toasts (fixo)
.toast                 # Classe base de toast
.toast-success         # Toast de sucesso
.toast-error           # Toast de erro
.toast-warning         # Toast de aviso
.toast-info            # Toast informativo
```

### Partes do Toast
```
.toast-icon            # Ícone do toast
.toast-content         # Container do conteúdo
.toast-title           # Título do toast
.toast-message         # Mensagem do toast
.toast-close           # Botão de fechar
.toast-exit            # Animação de saída
```

---

## Loading States

### Spinners
```
.spinner               # Spinner padrão (24px)
.spinner-sm            # Spinner pequeno (16px)
.spinner-lg            # Spinner grande (32px)
.spinner-xl            # Spinner extra grande (48px)
```

### Cores do Spinner
```
.spinner-primary       # Spinner colorido primário
.spinner-secondary     # Spinner colorido secundário
.spinner-success       # Spinner colorido sucesso
.spinner-white         # Spinner branco
```

### Skeleton Loaders
```
.skeleton              # Skeleton loader base
.skeleton-text         # Linha de texto
.skeleton-title        # Título (maior)
.skeleton-avatar       # Avatar circular
.skeleton-button       # Botão
.skeleton-card         # Card completo
```

### Progress Bar
```
.progress              # Container da barra
.progress-bar          # Barra de progresso interna
.progress-bar-striped  # Com listras
.progress-bar-animated # Animado
.progress-sm           # Barra pequena
.progress-lg           # Barra grande
```

### Loading Overlay
```
.loading-overlay          # Overlay de fundo
.loading-overlay-content  # Container do conteúdo
.loading-overlay-spinner  # Container do spinner
.loading-overlay-text     # Texto de carregamento
```

---

## Modais

### Modal Base
```
.modal-backdrop        # Fundo escuro overlay
.modal                 # Container do modal
```

### Tamanhos
```
.modal-sm              # Modal pequeno (400px)
                       # Default (500px)
.modal-lg              # Modal grande (800px)
.modal-xl              # Modal extra grande (1200px)
```

### Partes do Modal
```
.modal-header          # Cabeçalho do modal
.modal-title           # Título do modal
.modal-close           # Botão de fechar
.modal-body            # Corpo do modal
.modal-footer          # Rodapé do modal
```

---

## Dropdowns

### Dropdown Base
```
.dropdown              # Container do dropdown
.dropdown-menu         # Menu dropdown
.dropdown-menu-right   # Menu alinhado à direita
```

### Itens do Dropdown
```
.dropdown-item         # Item do menu
.dropdown-item-danger  # Item de perigo (vermelho)
.dropdown-header       # Cabeçalho do grupo
.dropdown-divider      # Divisor
```

### Estados
```
.show                  # Torna o menu visível
```

---

## Utilitários - Display

```
.d-none                # display: none
.d-block               # display: block
.d-inline              # display: inline
.d-inline-block        # display: inline-block
.d-flex                # display: flex
.d-inline-flex         # display: inline-flex
.d-grid                # display: grid
```

---

## Utilitários - Flexbox

### Direção
```
.flex-row              # flex-direction: row
.flex-column           # flex-direction: column
```

### Wrap
```
.flex-wrap             # flex-wrap: wrap
.flex-nowrap           # flex-wrap: nowrap
```

### Justify Content
```
.justify-start         # justify-content: flex-start
.justify-center        # justify-content: center
.justify-end           # justify-content: flex-end
.justify-between       # justify-content: space-between
```

### Align Items
```
.align-start           # align-items: flex-start
.align-center          # align-items: center
.align-end             # align-items: flex-end
```

### Gap
```
.gap-1                 # gap: 4px
.gap-2                 # gap: 8px
.gap-3                 # gap: 12px
.gap-4                 # gap: 16px
.gap-6                 # gap: 24px
```

---

## Utilitários - Espaçamento

### Margin
```
.m-0                   # margin: 0
.m-1                   # margin: 4px
.m-2                   # margin: 8px
.m-3                   # margin: 12px
.m-4                   # margin: 16px
.m-6                   # margin: 24px

.mt-0                  # margin-top: 0
.mt-2                  # margin-top: 8px
.mt-4                  # margin-top: 16px

.mb-0                  # margin-bottom: 0
.mb-2                  # margin-bottom: 8px
.mb-4                  # margin-bottom: 16px
```

### Padding
```
.p-0                   # padding: 0
.p-2                   # padding: 8px
.p-4                   # padding: 16px
.p-6                   # padding: 24px
```

---

## Utilitários - Texto

### Alinhamento
```
.text-left             # text-align: left
.text-center           # text-align: center
.text-right            # text-align: right
```

### Tamanhos
```
.text-xs               # font-size: 12px
.text-sm               # font-size: 14px
.text-base             # font-size: 16px
.text-lg               # font-size: 18px
.text-xl               # font-size: 20px
```

### Pesos
```
.font-normal           # font-weight: 400
.font-semibold         # font-weight: 600
.font-bold             # font-weight: 700
```

---

## Utilitários - Cores

### Cores de Texto
```
.text-primary          # Cor primária
.text-secondary        # Cor secundária
.text-success          # Cor de sucesso
.text-error            # Cor de erro
.text-warning          # Cor de aviso
.text-info             # Cor informativa
.text-gray             # Cor cinza
```

### Cores de Fundo
```
.bg-primary            # Fundo primário
.bg-secondary          # Fundo secundário
.bg-success            # Fundo de sucesso
.bg-error              # Fundo de erro
.bg-warning            # Fundo de aviso
.bg-info               # Fundo informativo
.bg-gray               # Fundo cinza
.bg-white              # Fundo branco
```

---

## Utilitários - Outros

### Width
```
.w-full                # width: 100%
.w-auto                # width: auto
```

### Border Radius
```
.rounded               # border-radius: 8px
.rounded-lg            # border-radius: 12px
.rounded-full          # border-radius: 9999px
```

### Shadow
```
.shadow-sm             # Sombra pequena
.shadow-md             # Sombra média
.shadow-lg             # Sombra grande
.shadow-none           # Sem sombra
```

### Cursor
```
.cursor-pointer        # cursor: pointer
.cursor-not-allowed    # cursor: not-allowed
```

### Overflow
```
.overflow-hidden       # overflow: hidden
.overflow-auto         # overflow: auto
```

---

## Design Tokens (CSS Variables)

### Cores Principais
```css
--primary              # #e6007e
--primary-hover        # #c00069
--primary-light        # rgba(230, 0, 126, 0.1)

--secondary            # #6c757d
--secondary-hover      # #5a6268
--secondary-light      # rgba(108, 117, 125, 0.1)

--success              # #28a745
--success-hover        # #218838
--success-light        # rgba(40, 167, 69, 0.1)

--error                # #dc3545
--error-hover          # #c82333
--error-light          # rgba(220, 53, 69, 0.1)

--warning              # #ffc107
--warning-hover        # #e0a800
--warning-light        # rgba(255, 193, 7, 0.1)

--info                 # #17a2b8
--info-hover           # #138496
--info-light           # rgba(23, 162, 184, 0.1)
```

### Escala de Cinza
```css
--gray-50              # #f8f9fa
--gray-100             # #f1f3f5
--gray-200             # #e9ecef
--gray-300             # #dee2e6
--gray-400             # #ced4da
--gray-500             # #adb5bd
--gray-600             # #6c757d
--gray-700             # #495057
--gray-800             # #343a40
--gray-900             # #212529
```

### Espaçamento
```css
--space-1              # 0.25rem (4px)
--space-2              # 0.5rem (8px)
--space-3              # 0.75rem (12px)
--space-4              # 1rem (16px)
--space-5              # 1.25rem (20px)
--space-6              # 1.5rem (24px)
--space-8              # 2rem (32px)
--space-10             # 2.5rem (40px)
--space-12             # 3rem (48px)
```

### Tipografia
```css
--text-xs              # 0.75rem (12px)
--text-sm              # 0.875rem (14px)
--text-base            # 1rem (16px)
--text-lg              # 1.125rem (18px)
--text-xl              # 1.25rem (20px)
--text-2xl             # 1.5rem (24px)
--text-3xl             # 1.875rem (30px)
```

### Border Radius
```css
--radius-sm            # 0.25rem (4px)
--radius-md            # 0.5rem (8px)
--radius-lg            # 0.75rem (12px)
--radius-xl            # 1rem (16px)
--radius-full          # 9999px
```

### Sombras
```css
--shadow-sm            # 0 1px 2px 0 rgba(0, 0, 0, 0.05)
--shadow-md            # 0 4px 6px -1px rgba(0, 0, 0, 0.1)...
--shadow-lg            # 0 10px 15px -3px rgba(0, 0, 0, 0.1)...
--shadow-xl            # 0 20px 25px -5px rgba(0, 0, 0, 0.1)...
```

### Transições
```css
--transition-fast      # 150ms ease-in-out
--transition-base      # 250ms ease-in-out
--transition-slow      # 350ms ease-in-out
```

### Z-index
```css
--z-dropdown           # 1000
--z-modal              # 1050
--z-tooltip            # 1100
```

---

## Resumo de Contagem

- **Botões**: 20+ classes
- **Formulários**: 25+ classes
- **Cards**: 12+ classes
- **Badges**: 20+ classes
- **Alertas/Toasts**: 15+ classes
- **Loading**: 15+ classes
- **Modais**: 8+ classes
- **Dropdowns**: 7+ classes
- **Utilitários**: 60+ classes

**Total**: Mais de 180 classes utilitárias disponíveis!

---

## Como Usar Esta Lista

1. **Busque por categoria** usando o índice no topo
2. **Combine classes** para criar componentes únicos
3. **Use Design Tokens** para customização consistente
4. **Consulte a documentação completa** para exemplos de uso

## Arquivos da Biblioteca

- `/static/css/components.css` - Arquivo CSS principal
- `/static/components-demo.html` - Demo interativa de todos os componentes
- `/static/COMPONENTS_DOCUMENTATION.md` - Documentação detalhada
- `/static/COMPONENTS_CLASSES_LIST.md` - Este arquivo (lista de classes)
