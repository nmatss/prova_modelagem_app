# Design Tokens - Referência Rápida

## Índice
- [Cores](#cores)
- [Tipografia](#tipografia)
- [Espaçamento](#espaçamento)
- [Border Radius](#border-radius)
- [Sombras](#sombras)
- [Transições](#transições)
- [Z-Index](#z-index)
- [Breakpoints](#breakpoints)

---

## Cores

### Primary (Rosa Puket)
| Token | Valor | Uso |
|-------|-------|-----|
| `--primary-50` | `#FFF0F7` | Background ultra light |
| `--primary-100` | `#FFE0F0` | Background light |
| `--primary-200` | `#FFC2E0` | Hover states light |
| `--primary-300` | `#FF99CF` | Borders light |
| `--primary-400` | `#FF66B8` | Accents medium |
| `--primary-500` | `#E6007E` | **Base (padrão)** |
| `--primary-600` | `#C2008E` | Hover states |
| `--primary-700` | `#9E006F` | Active states |
| `--primary-800` | `#7A0050` | Dark accents |
| `--primary-900` | `#560031` | Ultra dark |
| `--primary` | `var(--primary-500)` | **Use este** |
| `--primary-hover` | `var(--primary-600)` | **Use este para hover** |
| `--primary-light` | `var(--primary-100)` | **Use este para bg light** |

### Secondary (Slate)
| Token | Valor | Uso |
|-------|-------|-----|
| `--secondary-50` | `#F8FAFC` | Background ultra light |
| `--secondary-100` | `#F1F5F9` | Background light |
| `--secondary-200` | `#E2E8F0` | Borders light |
| `--secondary-300` | `#CBD5E1` | Borders |
| `--secondary-400` | `#94A3B8` | Icons disabled |
| `--secondary-500` | `#64748B` | **Base (padrão)** |
| `--secondary-600` | `#475569` | Text secondary |
| `--secondary-700` | `#334155` | Text |
| `--secondary-800` | `#1E293B` | Text dark |
| `--secondary-900` | `#0F172A` | Text ultra dark |
| `--secondary` | `var(--secondary-500)` | **Use este** |

### Success (Verde)
| Token | Valor | Uso |
|-------|-------|-----|
| `--success-50` | `#ECFDF5` | Background ultra light |
| `--success-100` | `#D1FAE5` | Background light, alerts |
| `--success-200` | `#A7F3D0` | Borders light |
| `--success-300` | `#6EE7B7` | Hover light |
| `--success-400` | `#34D399` | Accents |
| `--success-500` | `#10B981` | **Base (padrão)** |
| `--success-600` | `#059669` | Hover states |
| `--success-700` | `#047857` | Active states |
| `--success-800` | `#065F46` | Dark accents |
| `--success-900` | `#064E3B` | Ultra dark |
| `--success` | `var(--success-500)` | **Use este** |
| `--success-hover` | `var(--success-600)` | **Use este para hover** |
| `--success-light` | `var(--success-100)` | **Use este para bg light** |

### Error/Danger (Vermelho)
| Token | Valor | Uso |
|-------|-------|-----|
| `--error-50` | `#FEF2F2` | Background ultra light |
| `--error-100` | `#FEE2E2` | Background light, alerts |
| `--error-200` | `#FECACA` | Borders light |
| `--error-300` | `#FCA5A5` | Hover light |
| `--error-400` | `#F87171` | Accents |
| `--error-500` | `#EF4444` | **Base (padrão)** |
| `--error-600` | `#DC2626` | Hover states |
| `--error-700` | `#B91C1C` | Active states |
| `--error-800` | `#991B1B` | Dark accents |
| `--error-900` | `#7F1D1D` | Ultra dark |
| `--error` | `var(--error-500)` | **Use este** |
| `--danger` | `var(--error-500)` | **Alias de error** |
| `--error-hover` | `var(--error-600)` | **Use este para hover** |
| `--error-light` | `var(--error-100)` | **Use este para bg light** |

### Warning (Âmbar)
| Token | Valor | Uso |
|-------|-------|-----|
| `--warning-50` | `#FFFBEB` | Background ultra light |
| `--warning-100` | `#FEF3C7` | Background light, alerts |
| `--warning-200` | `#FDE68A` | Borders light |
| `--warning-300` | `#FCD34D` | Hover light |
| `--warning-400` | `#FBBF24` | Accents |
| `--warning-500` | `#F59E0B` | **Base (padrão)** |
| `--warning-600` | `#D97706` | Hover states |
| `--warning-700` | `#B45309` | Active states |
| `--warning-800` | `#92400E` | Dark accents |
| `--warning-900` | `#78350F` | Ultra dark |
| `--warning` | `var(--warning-500)` | **Use este** |
| `--warning-hover` | `var(--warning-600)` | **Use este para hover** |
| `--warning-light` | `var(--warning-100)` | **Use este para bg light** |

### Info (Cyan)
| Token | Valor | Uso |
|-------|-------|-----|
| `--info-50` | `#ECFEFF` | Background ultra light |
| `--info-100` | `#CFFAFE` | Background light, alerts |
| `--info-200` | `#A5F3FC` | Borders light |
| `--info-300` | `#67E8F9` | Hover light |
| `--info-400` | `#22D3EE` | Accents |
| `--info-500` | `#06B6D4` | **Base (padrão)** |
| `--info-600` | `#0891B2` | Hover states |
| `--info-700` | `#0E7490` | Active states |
| `--info-800` | `#155E75` | Dark accents |
| `--info-900` | `#164E63` | Ultra dark |
| `--info` | `var(--info-500)` | **Use este** |
| `--info-hover` | `var(--info-600)` | **Use este para hover** |
| `--info-light` | `var(--info-100)` | **Use este para bg light** |

### Neutrals (Cinza)
| Token | Valor | Uso |
|-------|-------|-----|
| `--gray-50` | `#F9FAFB` | Background page |
| `--gray-100` | `#F3F4F6` | Background cards |
| `--gray-200` | `#E5E7EB` | Borders light |
| `--gray-300` | `#D1D5DB` | Borders |
| `--gray-400` | `#9CA3AF` | Placeholders, disabled |
| `--gray-500` | `#6B7280` | Icons, text disabled |
| `--gray-600` | `#4B5563` | Text secondary |
| `--gray-700` | `#374151` | Text labels |
| `--gray-800` | `#1F2937` | Text body |
| `--gray-900` | `#111827` | Text headings |
| `--gray-950` | `#030712` | Text ultra dark |
| `--white` | `#FFFFFF` | White |
| `--black` | `#000000` | Black |

### Legacy Support (Compatibilidade)
| Token Legacy | Novo Token |
|--------------|------------|
| `--cor-puket-rosa` | `var(--primary)` |
| `--cor-aprovada` | `var(--success)` |
| `--cor-reprovada` | `var(--error)` |
| `--cor-comite` | `var(--warning)` |
| `--cor-andamento` | `var(--info)` |
| `--cor-fundo` | `var(--gray-50)` |
| `--cor-texto` | `var(--gray-800)` |

---

## Tipografia

### Font Families
| Token | Valor |
|-------|-------|
| `--font-primary` | `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif` |
| `--font-mono` | `'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace` |

### Font Sizes
| Token | rem | px | Uso |
|-------|-----|----|----|
| `--text-xs` | `0.75rem` | `12px` | Captions, legendas |
| `--text-sm` | `0.875rem` | `14px` | Small text, labels |
| `--text-base` | `1rem` | `16px` | **Corpo de texto padrão** |
| `--text-lg` | `1.125rem` | `18px` | Destacado, leads |
| `--text-xl` | `1.25rem` | `20px` | Subtítulos |
| `--text-2xl` | `1.5rem` | `24px` | Títulos pequenos (h3) |
| `--text-3xl` | `1.875rem` | `30px` | Títulos médios (h2) |
| `--text-4xl` | `2.25rem` | `36px` | Títulos grandes (h1) |
| `--text-5xl` | `3rem` | `48px` | Hero titles |
| `--text-6xl` | `3.75rem` | `60px` | Display large |
| `--text-7xl` | `4.5rem` | `72px` | Display XL |

### Font Weights
| Token | Valor | Uso |
|-------|-------|-----|
| `--font-thin` | `100` | Ultra light |
| `--font-extralight` | `200` | Extra light |
| `--font-light` | `300` | Light |
| `--font-normal` | `400` | **Padrão** |
| `--font-medium` | `500` | Medium destaque |
| `--font-semibold` | `600` | Semi-bold |
| `--font-bold` | `700` | **Bold** |
| `--font-extrabold` | `800` | Extra bold |
| `--font-black` | `900` | Black |

### Line Heights
| Token | Valor | Uso |
|-------|-------|-----|
| `--leading-none` | `1` | Icons, tight spacing |
| `--leading-tight` | `1.25` | Títulos compactos |
| `--leading-snug` | `1.375` | Títulos |
| `--leading-normal` | `1.5` | **Corpo de texto** |
| `--leading-relaxed` | `1.625` | Confortável |
| `--leading-loose` | `2` | Espaçado |

### Letter Spacing
| Token | Valor | Uso |
|-------|-------|-----|
| `--tracking-tighter` | `-0.05em` | Títulos grandes |
| `--tracking-tight` | `-0.025em` | Títulos |
| `--tracking-normal` | `0em` | **Padrão** |
| `--tracking-wide` | `0.025em` | Buttons, labels |
| `--tracking-wider` | `0.05em` | All caps |
| `--tracking-widest` | `0.1em` | All caps wide |

---

## Espaçamento

### Escala de Espaçamento (Base: 4px)
| Token | rem | px | Uso Comum |
|-------|-----|----|----|
| `--space-0` | `0` | `0px` | Reset |
| `--space-1` | `0.25rem` | `4px` | Micro spacing |
| `--space-2` | `0.5rem` | `8px` | Tight spacing |
| `--space-3` | `0.75rem` | `12px` | Small spacing |
| `--space-4` | `1rem` | `16px` | **Base spacing** |
| `--space-5` | `1.25rem` | `20px` | Medium spacing |
| `--space-6` | `1.5rem` | `24px` | Large spacing |
| `--space-7` | `1.75rem` | `28px` | - |
| `--space-8` | `2rem` | `32px` | XL spacing |
| `--space-9` | `2.25rem` | `36px` | - |
| `--space-10` | `2.5rem` | `40px` | 2XL spacing |
| `--space-11` | `2.75rem` | `44px` | - |
| `--space-12` | `3rem` | `48px` | 3XL spacing |
| `--space-14` | `3.5rem` | `56px` | - |
| `--space-16` | `4rem` | `64px` | Section spacing |
| `--space-20` | `5rem` | `80px` | Large section |
| `--space-24` | `6rem` | `96px` | XL section |
| `--space-32` | `8rem` | `128px` | 2XL section |
| `--space-40` | `10rem` | `160px` | 3XL section |
| `--space-48` | `12rem` | `192px` | - |
| `--space-56` | `14rem` | `224px` | - |
| `--space-64` | `16rem` | `256px` | - |

### Legacy Support
| Token Legacy | Novo Token |
|--------------|------------|
| `--spacing-xs` | `var(--space-1)` (4px) |
| `--spacing-sm` | `var(--space-2)` (8px) |
| `--spacing-md` | `var(--space-4)` (16px) |
| `--spacing-lg` | `var(--space-6)` (24px) |
| `--spacing-xl` | `var(--space-8)` (32px) |
| `--spacing-2xl` | `var(--space-12)` (48px) |

---

## Border Radius

| Token | rem | px | Uso |
|-------|-----|----|----|
| `--radius-none` | `0` | `0px` | Sem arredondamento |
| `--radius-sm` | `0.25rem` | `4px` | Sutil |
| `--radius-md` | `0.5rem` | `8px` | **Padrão** |
| `--radius-lg` | `0.75rem` | `12px` | Cards |
| `--radius-xl` | `1rem` | `16px` | Modals |
| `--radius-2xl` | `1.5rem` | `24px` | Large cards |
| `--radius-3xl` | `2rem` | `32px` | Hero sections |
| `--radius-full` | `9999px` | `∞` | **Círculos, pills** |

---

## Sombras

### Elevation Shadows
| Token | Valor | Uso |
|-------|-------|-----|
| `--shadow-xs` | `0 1px 2px 0 rgba(0,0,0,0.05)` | Sutil |
| `--shadow-sm` | `0 1px 3px 0 rgba(0,0,0,0.1), 0 1px 2px -1px rgba(0,0,0,0.1)` | Leve |
| `--shadow-md` | `0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1)` | **Padrão** |
| `--shadow-lg` | `0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.1)` | Elevado |
| `--shadow-xl` | `0 20px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.1)` | Muito elevado |
| `--shadow-2xl` | `0 25px 50px -12px rgba(0,0,0,0.25)` | Máximo |
| `--shadow-inner` | `inset 0 2px 4px 0 rgba(0,0,0,0.05)` | Interno |
| `--shadow-none` | `none` | Sem sombra |

### Colored Shadows
| Token | Uso |
|-------|-----|
| `--shadow-primary` | Sombra rosa (primary) |
| `--shadow-success` | Sombra verde (success) |
| `--shadow-error` | Sombra vermelha (error) |
| `--shadow-warning` | Sombra amarela (warning) |
| `--shadow-info` | Sombra cyan (info) |

---

## Transições

### Duration (Duração)
| Token | ms | Uso |
|-------|----|----|
| `--duration-75` | `75ms` | Ultra rápido |
| `--duration-100` | `100ms` | Muito rápido |
| `--duration-150` | `150ms` | Rápido |
| `--duration-200` | `200ms` | - |
| `--duration-300` | `300ms` | **Padrão** |
| `--duration-500` | `500ms` | Médio |
| `--duration-700` | `700ms` | Lento |
| `--duration-1000` | `1000ms` | Muito lento |

### Easing Functions
| Token | Valor | Uso |
|-------|-------|-----|
| `--ease-linear` | `linear` | Linear |
| `--ease-in` | `cubic-bezier(0.4,0,1,1)` | Ease in |
| `--ease-out` | `cubic-bezier(0,0,0.2,1)` | Ease out |
| `--ease-in-out` | `cubic-bezier(0.4,0,0.2,1)` | **Ease in-out** |
| `--ease-bounce` | `cubic-bezier(0.68,-0.55,0.265,1.55)` | Bounce effect |

### Preset Transitions
| Token | Valor | Uso |
|-------|-------|-----|
| `--transition-fast` | `150ms cubic-bezier(0.4,0,0.2,1)` | Transições rápidas |
| `--transition-base` | `250ms cubic-bezier(0.4,0,0.2,1)` | **Padrão** |
| `--transition-slow` | `350ms cubic-bezier(0.4,0,0.2,1)` | Transições lentas |
| `--transition-all` | `all 250ms cubic-bezier(0.4,0,0.2,1)` | Todas as propriedades |

---

## Z-Index

| Token | Valor | Uso |
|-------|-------|-----|
| `--z-base` | `0` | Base layer |
| `--z-dropdown` | `1000` | Dropdowns |
| `--z-sticky` | `1020` | Sticky headers |
| `--z-fixed` | `1030` | Fixed elements |
| `--z-overlay` | `1040` | Overlays |
| `--z-modal-backdrop` | `1050` | Modal backdrop |
| `--z-modal` | `1055` | Modals |
| `--z-popover` | `1060` | Popovers |
| `--z-tooltip` | `1070` | Tooltips |
| `--z-notification` | `1080` | Notifications |
| `--z-max` | `9999` | Máximo |

---

## Breakpoints

| Token | Valor | Dispositivo |
|-------|-------|------------|
| `--breakpoint-xs` | `0` | Extra small |
| `--breakpoint-sm` | `576px` | **Mobile** |
| `--breakpoint-md` | `768px` | **Tablet** |
| `--breakpoint-lg` | `992px` | Desktop pequeno |
| `--breakpoint-xl` | `1200px` | **Desktop** |
| `--breakpoint-2xl` | `1400px` | Desktop grande |
| `--breakpoint-3xl` | `1600px` | Desktop ultra |

### Container Widths
| Token | Valor |
|-------|-------|
| `--container-sm` | `540px` |
| `--container-md` | `720px` |
| `--container-lg` | `960px` |
| `--container-xl` | `1140px` |
| `--container-2xl` | `1320px` |
| `--container-3xl` | `1600px` |

---

## Borders

| Token | Valor | Uso |
|-------|-------|-----|
| `--border-width-0` | `0` | Sem borda |
| `--border-width-1` | `1px` | Fina |
| `--border-width-2` | `2px` | **Padrão** |
| `--border-width-4` | `4px` | Grossa |
| `--border-width-8` | `8px` | Muito grossa |

---

## Blur

| Token | Valor | Uso |
|-------|-------|-----|
| `--blur-none` | `0` | Sem blur |
| `--blur-sm` | `4px` | Blur sutil |
| `--blur-md` | `8px` | **Blur padrão** |
| `--blur-lg` | `16px` | Blur forte |
| `--blur-xl` | `24px` | Blur muito forte |
| `--blur-2xl` | `40px` | Blur máximo |
| `--blur-3xl` | `64px` | Blur ultra |

---

## Opacity

| Token | Valor | % |
|-------|-------|---|
| `--opacity-0` | `0` | 0% |
| `--opacity-5` | `0.05` | 5% |
| `--opacity-10` | `0.1` | 10% |
| `--opacity-20` | `0.2` | 20% |
| `--opacity-25` | `0.25` | 25% |
| `--opacity-30` | `0.3` | 30% |
| `--opacity-40` | `0.4` | 40% |
| `--opacity-50` | `0.5` | 50% |
| `--opacity-60` | `0.6` | 60% |
| `--opacity-70` | `0.7` | 70% |
| `--opacity-75` | `0.75` | 75% |
| `--opacity-80` | `0.8` | 80% |
| `--opacity-90` | `0.9` | 90% |
| `--opacity-95` | `0.95` | 95% |
| `--opacity-100` | `1` | 100% |

---

## Resumo Total

### Contagem de Tokens

- **Cores**: 95+ tokens (incluindo escalas completas)
- **Tipografia**: 30+ tokens
- **Espaçamento**: 25+ tokens
- **Border Radius**: 8 tokens
- **Sombras**: 13 tokens (8 elevation + 5 colored)
- **Transições**: 12 tokens
- **Z-Index**: 11 tokens
- **Breakpoints**: 7 tokens
- **Container**: 6 tokens
- **Borders**: 5 tokens
- **Blur**: 7 tokens
- **Opacity**: 15 tokens

**Total**: 234+ Design Tokens

---

## Como Usar

### Em CSS
```css
.meu-componente {
  color: var(--primary);
  font-size: var(--text-lg);
  padding: var(--space-4) var(--space-6);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  transition: var(--transition-base);
}
```

### Em HTML com Utility Classes
```html
<div class="bg-primary text-white p-6 rounded-lg shadow-md">
  Conteúdo
</div>
```

### Em JavaScript
```javascript
const primaryColor = getComputedStyle(document.documentElement)
  .getPropertyValue('--primary')
  .trim();

console.log(primaryColor); // #E6007E
```

---

**Versão**: 2.0
**Última atualização**: 2026-01-16
