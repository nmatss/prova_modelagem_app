# Checklist de Testes Mobile - Sistema de Gestão de Provas de Modelagem

## Breakpoints Implementados

O sistema agora utiliza uma abordagem Mobile-First com os seguintes breakpoints:

```css
/* Base: Mobile (< 640px) */
/* Tablet: 640px - 1023px */
/* Desktop: 1024px+ */
/* Large Desktop: 1280px+ */
```

## Testes por Resolução

### 1. Very Small Mobile (320px x 568px)
**Dispositivo de referência**: iPhone SE (1st gen), iPhone 5/5S

#### Dashboard
- [ ] Stats cards aparecem em coluna única (1fr)
- [ ] Bottom navigation visível e funcional
- [ ] Cards de relatório legíveis e não quebrados
- [ ] Botões têm min-height de 48px
- [ ] Texto é legível (mínimo 14px nos inputs)
- [ ] Filtros colapsados por padrão
- [ ] Pills de filtro cabem sem quebrar linha excessivamente

#### Analytics
- [ ] KPIs aparecem em coluna única
- [ ] Gráficos são visíveis e responsivos
- [ ] Tabelas com scroll horizontal funcionam
- [ ] Filtros são acessíveis

#### Navegação
- [ ] Bottom nav tem 64px de altura
- [ ] Ícones são clicáveis (44px touch target)
- [ ] Botão primary central destacado
- [ ] Todos os items são acessíveis

---

### 2. Small Mobile (375px x 667px)
**Dispositivo de referência**: iPhone 6/7/8, iPhone SE (2nd gen)

#### Dashboard
- [ ] Stats grid: 1 coluna em vertical
- [ ] Reports grid: 1 coluna
- [ ] Imagens de produtos carregam corretamente
- [ ] Modais ocupam 90% da tela
- [ ] Search bar ocupa largura total
- [ ] Bottom nav centralizado e espaçado

#### Forms
- [ ] Inputs têm height de 48px
- [ ] Font-size 16px (previne zoom iOS)
- [ ] Labels legíveis
- [ ] Botões ocupam largura total
- [ ] Dropdown acessíveis

#### Modais
- [ ] Modal header compacto
- [ ] Modal body scrollável
- [ ] Botões em coluna (não lado a lado)
- [ ] Fechar modal funciona

---

### 3. Medium Mobile (414px x 896px)
**Dispositivo de referência**: iPhone 11 Pro Max, iPhone XR

#### Dashboard
- [ ] Stats grid ainda em 1 coluna ou 2x2
- [ ] Melhor aproveitamento do espaço
- [ ] Cards de relatório não muito largos
- [ ] Bottom nav bem distribuído

#### Landscape Mode (896px x 414px)
- [ ] Bottom nav reduz height para 56px
- [ ] Navbar compacta (28px altura)
- [ ] Stats grid muda para 2 colunas
- [ ] Modal body com max-height 60vh

---

### 4. Large Mobile (428px x 926px)
**Dispositivo de referência**: iPhone 13 Pro Max, iPhone 14 Plus

#### Dashboard
- [ ] Layout otimizado para tela maior
- [ ] Stats podem ser 2x2
- [ ] Reports grid aproveitando espaço

---

### 5. Tablet Portrait (640px - 767px)
**Dispositivo de referência**: iPad Mini

#### Dashboard
- [ ] Bottom nav OCULTO
- [ ] Stats grid: 2 colunas
- [ ] Reports grid: 2 colunas
- [ ] Sidebar disponível
- [ ] Navegação desktop restaurada

---

### 6. Tablet Landscape (768px - 1023px)
**Dispositivo de referência**: iPad (10.2"), iPad Air

#### Dashboard
- [ ] Stats grid: 2 ou 3 colunas
- [ ] Reports grid: 2-3 colunas
- [ ] Sidebar completa visível
- [ ] Top header funcional
- [ ] Breadcrumb visível

---

### 7. Desktop (1024px - 1279px)
**Dispositivo de referência**: Laptops padrão

#### Dashboard
- [ ] Stats grid: 4 colunas
- [ ] Reports grid: 3+ colunas
- [ ] Layout completo desktop
- [ ] Todas as features visíveis

---

### 8. Large Desktop (1280px+)
**Dispositivo de referência**: Monitores externos, iMac

#### Dashboard
- [ ] Container max-width: 1400px
- [ ] Grid otimizado para espaço
- [ ] Sem espaço desperdiçado

---

## Testes de Interação Touch

### Touch Targets
- [ ] Todos os botões: mínimo 44x44px
- [ ] Links importantes: mínimo 44x44px
- [ ] Bottom nav items: mínimo 44px height
- [ ] Inputs: mínimo 48px height em mobile

### Gestos
- [ ] Scroll suave em listas
- [ ] Swipe para fechar modais (se implementado)
- [ ] Pull to refresh (se implementado)
- [ ] Tap feedback visual

### Prevenção de Zoom iOS
- [ ] Inputs com font-size: 16px
- [ ] Selects com font-size: 16px
- [ ] Textareas com font-size: 16px
- [ ] Meta viewport configurado corretamente

---

## Testes de Navegação

### Bottom Navigation (Mobile < 640px)
- [ ] Aparece apenas em mobile
- [ ] Fixed na parte inferior
- [ ] 5 items visíveis
- [ ] Item ativo destacado
- [ ] Botão primary circular e elevado
- [ ] Z-index correto (não sobrepõe modais)
- [ ] Padding-bottom no body (80px)

### Sidebar (Tablet/Desktop ≥ 640px)
- [ ] Visível em tablet+
- [ ] Colapsável
- [ ] Estado persistido
- [ ] Animação suave
- [ ] Backdrop em mobile (quando aberto)

---

## Testes de Componentes

### Cards
- [ ] Border-radius ajustado em mobile (12px)
- [ ] Padding reduzido em mobile
- [ ] Hover effects desabilitados em touch
- [ ] Sombras leves

### Tables
- [ ] Scroll horizontal em mobile
- [ ] Indicador de scroll ("→ Deslize")
- [ ] Headers ocultos em mobile (stacked layout)
- [ ] Dados empilhados verticalmente

### Modais
- [ ] Margin 0.5rem em mobile
- [ ] Max-width ajustado
- [ ] Header compacto
- [ ] Body scrollável (max-height 60vh)
- [ ] Footer buttons em coluna
- [ ] Botões largura total em mobile

### Forms
- [ ] Labels legíveis (0.875rem)
- [ ] Inputs touch-friendly (48px)
- [ ] Botões largura total em mobile
- [ ] Checkboxes maiores (1.25rem)
- [ ] Validation visible

### Tabs
- [ ] Scroll horizontal em mobile
- [ ] Sem wrap
- [ ] Smooth scroll
- [ ] Indicador de scroll
- [ ] Tabs não quebram

### Badges
- [ ] Font-size reduzido (0.7rem)
- [ ] Padding ajustado
- [ ] Legível

---

## Testes de Performance

### Loading
- [ ] Lazy loading de imagens
- [ ] Skeleton loaders
- [ ] Transições suaves
- [ ] Sem layout shift

### Scroll
- [ ] Smooth scroll habilitado
- [ ] Sem lag em listas longas
- [ ] Virtual scroll (se implementado)

### Network
- [ ] Funciona em 3G
- [ ] Assets minificados
- [ ] Images otimizadas

---

## Testes de Acessibilidade

### ARIA
- [ ] Roles corretos
- [ ] Labels descritivos
- [ ] aria-label em ícones
- [ ] aria-expanded em dropdowns

### Keyboard
- [ ] Tab navigation funciona
- [ ] Enter/Space ativam botões
- [ ] Esc fecha modais
- [ ] Focus visible

### Screen Readers
- [ ] Textos alternativos
- [ ] Estrutura semântica
- [ ] Anúncios de mudanças

---

## Testes de Compatibilidade

### iOS Safari
- [ ] Layout correto
- [ ] Inputs não causam zoom
- [ ] Bottom nav fixado
- [ ] Scroll suave
- [ ] Touch events funcionam

### Android Chrome
- [ ] Layout correto
- [ ] Bottom nav fixado
- [ ] Scroll suave
- [ ] Touch events funcionam

### Firefox Mobile
- [ ] Layout consistente
- [ ] Todos os recursos funcionam

---

## Testes de Orientação

### Portrait para Landscape
- [ ] Layout se adapta
- [ ] Bottom nav ajusta
- [ ] Stats grid muda para 2 colunas
- [ ] Modal se adapta
- [ ] Sem conteúdo cortado

### Landscape para Portrait
- [ ] Layout retorna ao padrão
- [ ] Bottom nav restaurado
- [ ] Grid volta ao mobile
- [ ] Sem quebras

---

## Testes de Recursos Específicos

### Dashboard
- [ ] Stats cards compactos
- [ ] Filtros colapsáveis
- [ ] Search funciona
- [ ] View toggle (grid/list)
- [ ] Export buttons acessíveis
- [ ] Cards de relatório otimizados
- [ ] Imagens carregam corretamente
- [ ] Actions empilhados em mobile

### Analytics
- [ ] KPIs responsivos
- [ ] Gráficos renderizam
- [ ] Filtros compactos
- [ ] Tabela scrollável
- [ ] Export funciona

### Novo Relatório
- [ ] Form responsivo
- [ ] Upload de imagens
- [ ] Tabs scrolláveis
- [ ] Submit funciona

### Detalhes do Relatório
- [ ] Imagens responsivas
- [ ] Tabs scrolláveis
- [ ] Actions acessíveis
- [ ] PDF export funciona

---

## Utilitários CSS Implementados

### Show/Hide
- [ ] `.hide-mobile` - oculta em mobile
- [ ] `.show-mobile` - mostra apenas em mobile
- [ ] `.show-mobile-inline` - inline em mobile
- [ ] `.show-mobile-flex` - flex em mobile

### Spacing Mobile
- [ ] `.mb-mobile-{0-3}` - margin-bottom mobile
- [ ] `.p-mobile-{0-3}` - padding mobile

### Text Size
- [ ] `.text-mobile-sm` - texto menor em mobile
- [ ] `.text-mobile-xs` - texto extra small em mobile

---

## Checklist de Testes Finais

### Funcionalidade
- [ ] Login funciona em todos os tamanhos
- [ ] Dashboard carrega corretamente
- [ ] CRUD de relatórios funciona
- [ ] Upload de arquivos funciona
- [ ] Export PDF/Excel funciona
- [ ] Filtros funcionam
- [ ] Search funciona
- [ ] Modais abrem e fecham
- [ ] Navegação funciona

### Visual
- [ ] Sem overflow horizontal
- [ ] Sem texto cortado
- [ ] Botões alinhados
- [ ] Spacing consistente
- [ ] Cores contrastantes
- [ ] Ícones centralizados

### UX
- [ ] Feedback visual em todos os cliques
- [ ] Loading states visíveis
- [ ] Erros claramente mostrados
- [ ] Sucesso confirmado
- [ ] Navegação intuitiva
- [ ] Bottom nav sempre acessível

---

## Ferramentas de Teste Recomendadas

### Browsers DevTools
1. Chrome DevTools
   - Device toolbar (Cmd/Ctrl + Shift + M)
   - Network throttling
   - Touch simulation

2. Firefox Responsive Design Mode
   - Cmd/Ctrl + Shift + M

3. Safari Web Inspector
   - Develop > Enter Responsive Design Mode

### Dispositivos Físicos
- iPhone SE (320px)
- iPhone 12/13 (390px)
- iPhone 12/13 Pro Max (428px)
- iPad Mini (768px)
- iPad Air/Pro (820px)
- Android Phone (360px - 412px)
- Android Tablet (600px+)

### Emuladores
- Xcode Simulator (iOS)
- Android Studio (Android)
- BrowserStack (Multiple devices)

---

## Comandos para Teste Local

```bash
# Iniciar servidor Flask
python app.py

# Acessar via IP local para testar em dispositivos reais
# http://SEU_IP_LOCAL:5000

# Usar ngrok para teste remoto
ngrok http 5000
```

---

## Notas de Implementação

### Arquivos Modificados
1. `/static/css/mobile.css` - **NOVO** - Estilos mobile-first completos
2. `/templates/base.html` - Adicionado link para mobile.css e bottom navigation
3. `/static/css/custom.css` - Já possui responsividade básica
4. `/static/css/navigation.css` - Sidebar responsiva

### Breakpoint System
- Mobile-first approach
- Base styles para < 640px
- Media queries para tamanhos maiores
- Touch optimizations separadas

### Z-Index Layers
```css
--z-bottom-nav: 1000;
--z-fixed: 1020;
--z-sticky: 1030;
--z-modal-backdrop: 1040;
--z-modal: 1050;
--z-toast: 1060;
```

---

## Próximos Passos (Melhorias Futuras)

1. PWA Support
   - Service Worker
   - Offline capability
   - Add to Home Screen
   - Push notifications

2. Advanced Mobile Features
   - Pull to refresh
   - Swipe gestures
   - Haptic feedback
   - Camera integration

3. Performance
   - Image lazy loading avançado
   - Virtual scrolling
   - Code splitting
   - Preloading crítico

4. Accessibility
   - High contrast mode
   - Font size adjustment
   - Voice commands
   - Better screen reader support

---

**Data de Criação**: 2026-01-16
**Versão**: 1.0
**Autor**: Sistema de Gestão de Provas de Modelagem
