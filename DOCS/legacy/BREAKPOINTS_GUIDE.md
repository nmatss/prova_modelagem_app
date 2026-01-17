# Guia Visual de Breakpoints - Sistema Mobile-First

## Filosofia Mobile-First

O sistema foi desenvolvido com **Mobile-First**, ou seja:
- Estilos base são para mobile (< 640px)
- Media queries adicionam features para telas maiores
- Performance otimizada para dispositivos móveis

---

## Sistema de Breakpoints

```css
/* ========================================
   BREAKPOINTS HIERARCHY
   ======================================== */

/* BASE: Mobile (< 640px) */
/* Estilos padrão - aplicados primeiro */

@media (min-width: 640px) {
    /* TABLET: 640px - 1023px */
}

@media (min-width: 1024px) {
    /* DESKTOP: 1024px - 1279px */
}

@media (min-width: 1280px) {
    /* LARGE DESKTOP: 1280px+ */
}
```

---

## Breakpoint 1: Very Small Mobile (< 375px)

### Dispositivos
- iPhone SE (1st gen): 320px
- iPhone 5/5S: 320px
- Small Android phones: 320px - 360px

### Layout
```
┌─────────────────────┐
│   [Logo]    [Menu]  │ ← Navbar compacta (32px height)
├─────────────────────┤
│                     │
│  ┌───────────────┐  │
│  │  Stat Card    │  │ ← Stats: 1 coluna
│  │  [Icon] 150   │  │
│  │  Relatórios   │  │
│  └───────────────┘  │
│                     │
│  ┌───────────────┐  │
│  │  Report Card  │  │ ← Reports: 1 coluna
│  │  [Image]      │  │
│  │  Title        │  │
│  │  [View] [PDF] │  │
│  └───────────────┘  │
│                     │
├─────────────────────┤
│ [H] [A] [+] [R] [P] │ ← Bottom Nav (64px)
└─────────────────────┘
```

### Características
- Font-size: 0.875rem
- Padding: 0.5rem
- Buttons: 100% width, 48px height
- Bottom nav: 56-64px height
- Cards: 12px border-radius

---

## Breakpoint 2: Small Mobile (375px - 639px)

### Dispositivos
- iPhone 12/13 Mini: 375px
- iPhone 6/7/8: 375px
- iPhone SE (2nd/3rd gen): 375px
- Standard Android: 360px - 412px

### Layout
```
┌─────────────────────────┐
│  [Logo]        [Menu]   │ ← Navbar (32px)
├─────────────────────────┤
│                         │
│  ┌─────────────────┐    │
│  │  Stat Card      │    │ ← Stats: 1 coluna
│  │  [Icon] 250     │    │   (melhor espaçado)
│  │  Relatórios     │    │
│  └─────────────────┘    │
│                         │
│  ┌─────────────────┐    │
│  │  Report Card    │    │ ← Reports: 1 coluna
│  │  [Image 200px]  │    │   (imagens maiores)
│  │  Description    │    │
│  │  Meta info      │    │
│  │  [View] [PDF]   │    │
│  └─────────────────┘    │
│                         │
├─────────────────────────┤
│ [Home][Ana][+][Rep][👤] │ ← Bottom Nav (64px)
└─────────────────────────┘
```

### Características
- Font-size: 0.9375rem (padrão)
- Padding: 0.75rem
- Better touch targets: 48px
- Search bar: full width
- Filters: collapsible

---

## Breakpoint 3: Large Mobile (414px - 639px)

### Dispositivos
- iPhone 11/12/13 Pro Max: 428px
- iPhone XR/11: 414px
- Large Android phones: 412px+

### Layout
```
┌──────────────────────────────┐
│  [Logo]           [Menu]     │ ← Navbar
├──────────────────────────────┤
│                              │
│  ┌──────────┐ ┌──────────┐  │
│  │Stat Card │ │Stat Card │  │ ← Stats: 2x2 grid
│  │[Icon]150 │ │[Icon]45  │  │   (opcional)
│  └──────────┘ └──────────┘  │
│                              │
│  ┌──────────────────────┐    │
│  │  Report Card         │    │ ← Reports: 1 coluna
│  │  [Image 220px]       │    │   (confortável)
│  │  Full description    │    │
│  │  Meta information    │    │
│  │  [View]    [PDF]     │    │
│  └──────────────────────┘    │
│                              │
├──────────────────────────────┤
│ [Home] [Ana] [+] [Rep] [👤]  │ ← Bottom Nav
└──────────────────────────────┘
```

### Características
- Melhor aproveitamento de espaço
- Stats podem ser 2x2
- Cards mais espaçados
- Imagens maiores (220px)

---

## Breakpoint 4: Tablet Portrait (640px - 767px)

### Dispositivos
- iPad Mini: 768px
- Small tablets: 600px - 768px

### Layout
```
┌──────────────────────────────────────┐
│ [≡] Sidebar    [Breadcrumb]  [Sair] │ ← Top Header
├──────────────────────────────────────┤
│ [≡]│                                 │
│ [H]│  ┌────────┐ ┌────────┐         │
│ [R]│  │Stat 1  │ │Stat 2  │         │ ← Stats: 2x2
│ [A]│  └────────┘ └────────┘         │
│ [U]│  ┌────────┐ ┌────────┐         │
│ [⚙]│  │Stat 3  │ │Stat 4  │         │
│    │  └────────┘ └────────┘         │
│    │                                 │
│    │  ┌────────┐ ┌────────┐         │
│    │  │Report 1│ │Report 2│         │ ← Reports: 2 cols
│    │  │[Image] │ │[Image] │         │
│    │  └────────┘ └────────┘         │
└────┴──────────────────────────────┴──┘
```

### Características
- **BOTTOM NAV OCULTO** ✨
- Sidebar visível (colapsável)
- Stats: 2 colunas
- Reports: 2 colunas
- Desktop navigation restaurada
- Top header funcional

---

## Breakpoint 5: Tablet Landscape (768px - 1023px)

### Dispositivos
- iPad (10.2"): 1024px
- iPad Air: 820px
- Large tablets: 768px+

### Layout
```
┌────────────────────────────────────────────────┐
│ [≡]Sidebar  [Home > Dashboard]      [Logout]  │
├────────────────────────────────────────────────┤
│ [H]│  ┌──────┐ ┌──────┐ ┌──────┐             │
│ [R]│  │Stat1 │ │Stat2 │ │Stat3 │             │
│ [A]│  └──────┘ └──────┘ └──────┘             │
│ [A]│  ┌──────┐ ┌──────┐ ┌──────┐             │
│ [U]│  │Rep 1 │ │Rep 2 │ │Rep 3 │             │
│ [⚙]│  │[Img] │ │[Img] │ │[Img] │             │
│    │  │Title │ │Title │ │Title │             │
│    │  └──────┘ └──────┘ └──────┘             │
│    │  ┌──────┐ ┌──────┐ ┌──────┐             │
│    │  │Rep 4 │ │Rep 5 │ │Rep 6 │             │
└────┴──────────────────────────────────────────┘
```

### Características
- Sidebar completa
- Stats: 2-3 colunas
- Reports: 2-3 colunas
- Breadcrumb visível
- Filters expandidos
- Desktop experience

---

## Breakpoint 6: Desktop (1024px - 1279px)

### Dispositivos
- MacBook Air: 1280px
- Standard laptops: 1366px
- HD displays: 1920px

### Layout
```
┌──────────────────────────────────────────────────────┐
│ [≡] Sidebar      [Home > Dashboard]       [Logout]  │
├──────────────────────────────────────────────────────┤
│ [H]│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐         │
│ [R]│  │Stat1 │ │Stat2 │ │Stat3 │ │Stat4 │         │
│ [A]│  └──────┘ └──────┘ └──────┘ └──────┘         │
│ [A]│                                               │
│ [U]│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐           │
│ [⚙]│  │Rep1 │ │Rep2 │ │Rep3 │ │Rep4 │           │
│ [👤]│  │[Img]│ │[Img]│ │[Img]│ │[Img]│           │
│    │  │Title│ │Title│ │Title│ │Title│           │
│    │  └─────┘ └─────┘ └─────┘ └─────┘           │
└────┴─────────────────────────────────────────────┴──┘
```

### Características
- Stats: 4 colunas
- Reports: 3-4 colunas (auto-fill minmax(320px, 1fr))
- Sidebar full width (240px)
- All features visible
- Hover effects enabled
- Optimal spacing

---

## Breakpoint 7: Large Desktop (1280px+)

### Dispositivos
- iMac: 2560px
- 4K displays: 3840px
- External monitors: 1920px+

### Layout
```
┌────────────────────────────────────────────────────────────────────┐
│ [≡] Sidebar       [Home > Dashboard]                    [Logout]  │
├────────────────────────────────────────────────────────────────────┤
│ [H]│                                                               │
│ [R]│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐               │
│ [A]│  │ Stat 1 │ │ Stat 2 │ │ Stat 3 │ │ Stat 4 │               │
│ [A]│  └────────┘ └────────┘ └────────┘ └────────┘               │
│ [U]│                                                               │
│ [⚙]│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                  │
│ [👤]│  │Rep1 │ │Rep2 │ │Rep3 │ │Rep4 │ │Rep5 │                  │
│    │  │[Img]│ │[Img]│ │[Img]│ │[Img]│ │[Img]│                  │
│    │  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘                  │
│    │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                  │
│    │  │Rep6 │ │Rep7 │ │Rep8 │ │Rep9 │ │Rep10│                  │
└────┴──────────────────────────────────────────────────────────────┘
```

### Características
- Max-width: 1400px (centralizado)
- Reports: 4-5 colunas (minmax(360px, 1fr))
- Generous spacing
- Optimal readability
- No wasted space

---

## Landscape Mode (Mobile)

### Layout (896px x 414px)
```
┌────────────────────────────────────────────────────────────┐
│ [Logo] [≡]           [Breadcrumb]             [Logout]    │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │  Stat 1  │ │  Stat 2  │ │  Stat 3  │ │  Stat 4  │    │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘    │
│                                                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                  │
│  │ Report 1 │ │ Report 2 │ │ Report 3 │                  │
│  └──────────┘ └──────────┘ └──────────┘                  │
├────────────────────────────────────────────────────────────┤
│ [Home] [Analytics] [+] [Reports] [Profile]                │
└────────────────────────────────────────────────────────────┘
```

### Características
- Navbar compacta: 28px
- Stats: 2x2 ou 4x1
- Reports: 2-3 colunas
- Bottom nav: 56px height
- Modal max-height: 60vh
- Compact spacing

---

## Navigation Comparison

### Mobile Navigation (< 640px)
```
Bottom Navigation Bar:
┌──────────────────────────────────────┐
│                                      │
│  [Home]  [Analytics]  [+]  [Rep] [👤]│
│   ⬆        ⬆         ⬆     ⬆     ⬆ │
│  active  inactive  primary inactive  │
│                                      │
└──────────────────────────────────────┘
```

### Desktop Navigation (≥ 640px)
```
Sidebar:
┌─────────────┐
│ [Logo]      │
│             │
│ [≡] Home    │ ← Active
│ [📊] Reports│
│ [📈] Analytics│
│ ─────────── │
│ [⚙] Settings│
│             │
│ [👤] User   │
└─────────────┘
```

---

## Component Behavior by Breakpoint

### Stats Grid

| Breakpoint | Columns | Gap | Height |
|------------|---------|-----|--------|
| < 375px | 1 | 12px | ~90px |
| 375px - 639px | 1 | 12px | ~100px |
| 640px - 1023px | 2 | 16px | ~110px |
| 1024px+ | 4 | 16px | ~120px |

### Reports Grid

| Breakpoint | Columns | Card Width | Image Height |
|------------|---------|------------|--------------|
| < 640px | 1 | 100% | 200px |
| 640px - 767px | 2 | ~48% | 180px |
| 768px - 1023px | 2-3 | ~32% | 180px |
| 1024px+ | auto-fill | 320px min | 180px |

### Modals

| Breakpoint | Width | Margin | Footer |
|------------|-------|--------|--------|
| < 640px | 100% | 0.5rem | Column |
| 640px - 1023px | 90% | 1rem | Row |
| 1024px+ | 600px | auto | Row |

---

## Bottom Navigation Details

### Structure
```html
<nav class="bottom-nav">
  <a href="/" class="bottom-nav-item active">
    <i class="bi bi-house-fill"></i>
    <span>Home</span>
  </a>
  <!-- 4 more items -->
</nav>
```

### Styling
```css
.bottom-nav {
  position: fixed;
  bottom: 0;
  height: 64px;
  background: white;
  box-shadow: 0 -4px 12px rgba(0,0,0,0.1);
  z-index: 1000;
}

.bottom-nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 44px;
}

.bottom-nav-item-primary {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ec4899, #8b5cf6);
  margin-top: -20px; /* Elevado */
}
```

---

## Touch Target Guidelines

### Mínimos Recomendados
```
iOS Human Interface Guidelines: 44x44 pt
Android Material Design: 48x48 dp
Web Best Practice: 44-48px
```

### Implementação
```css
/* Touch devices */
@media (hover: none) and (pointer: coarse) {
  a, button, .btn, [role="button"] {
    min-height: 44px;
    min-width: 44px;
  }

  /* Comfortable touch target */
  .btn {
    min-height: 48px;
  }
}
```

---

## Testing Viewports

### Priority Devices (Must Test)
1. iPhone SE: 320 x 568
2. iPhone 12/13: 390 x 844
3. iPhone 12 Pro Max: 428 x 926
4. iPad Mini: 768 x 1024
5. Desktop: 1280 x 720

### Secondary Devices (Should Test)
6. Pixel 5: 393 x 851
7. Galaxy S21: 360 x 800
8. iPad Air: 820 x 1180
9. Desktop: 1920 x 1080

---

## Quick Reference Table

| Device Class | Width Range | Layout Type | Navigation | Grid Columns |
|--------------|-------------|-------------|------------|--------------|
| Very Small | < 375px | Stacked | Bottom | 1 |
| Small Mobile | 375-639px | Stacked | Bottom | 1 |
| Tablet Portrait | 640-767px | Flexible | Sidebar | 2 |
| Tablet Landscape | 768-1023px | Flexible | Sidebar | 2-3 |
| Desktop | 1024-1279px | Grid | Sidebar | 3-4 |
| Large Desktop | 1280px+ | Grid | Sidebar | 4+ |

---

## CSS Variables Reference

```css
:root {
  /* Z-Index */
  --z-bottom-nav: 1000;
  --z-fixed: 1020;
  --z-sticky: 1030;
  --z-modal: 1050;

  /* Touch */
  --touch-target-min: 44px;
  --touch-target-comfortable: 48px;

  /* Spacing Mobile */
  --mobile-spacing-xs: 0.5rem;
  --mobile-spacing-sm: 0.75rem;
  --mobile-spacing-md: 1rem;
  --mobile-spacing-lg: 1.25rem;
}
```

---

## Conclusion

Este guia visual fornece uma referência completa de como o sistema se comporta em diferentes breakpoints. Use-o como referência durante o desenvolvimento e testes.

**Versão**: 1.0
**Data**: 2026-01-16
**Autor**: Sistema de Gestão de Provas de Modelagem
