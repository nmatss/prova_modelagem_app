# Guia de Testes de Acessibilidade com Screen Reader

Este guia fornece instruções detalhadas para testar a acessibilidade do sistema usando leitores de tela (screen readers).

## Índice

1. [Ferramentas Necessárias](#ferramentas-necessárias)
2. [Configuração Inicial](#configuração-inicial)
3. [Testes por Funcionalidade](#testes-por-funcionalidade)
4. [Checklist de Testes](#checklist-de-testes)
5. [Problemas Comuns](#problemas-comuns)
6. [Recursos Adicionais](#recursos-adicionais)

---

## Ferramentas Necessárias

### Screen Readers Recomendados

#### Windows
- **NVDA (NonVisual Desktop Access)** - GRATUITO ✅
  - Download: https://www.nvaccess.org/download/
  - Mais usado no mundo
  - Compatível com todos os navegadores
  - Comandos principais:
    - `Ctrl` - Parar leitura
    - `Insert + Seta para baixo` - Ler tudo
    - `H` - Próximo heading
    - `K` - Próximo link
    - `B` - Próximo botão
    - `F` - Próximo campo de formulário

- **JAWS (Job Access With Speech)** - PAGO
  - Mais completo mas muito caro
  - Trial de 40 minutos disponível
  - Comandos similares ao NVDA

#### macOS
- **VoiceOver** - GRATUITO (built-in) ✅
  - Já vem instalado no macOS
  - Ativar: `Cmd + F5`
  - Comandos principais:
    - `VO` = `Ctrl + Option`
    - `VO + A` - Começar a ler
    - `VO + Seta direita/esquerda` - Navegar
    - `VO + Espaço` - Ativar elemento
    - `VO + U` - Rotor (navegação por headings, links, etc)

#### Linux
- **Orca** - GRATUITO ✅
  - Screen reader padrão do GNOME
  - Instalar: `sudo apt install orca`
  - Ativar: `Super + Alt + S`

#### Extensões de Navegador (para testes rápidos)
- **ChromeVox** (Chrome/Edge)
  - Extensão gratuita do Google
  - Boa para testes rápidos
  - Não substitui screen readers completos

---

## Configuração Inicial

### Preparação do Ambiente

1. **Desative o monitor** (opcional mas recomendado)
   - Ou use uma venda nos olhos
   - Simula a experiência real de usuários cegos

2. **Configure o screen reader**
   - NVDA: `Insert + N` > Preferências > Configurações
   - VoiceOver: Preferências do Sistema > Acessibilidade > VoiceOver

3. **Use fones de ouvido**
   - Facilita ouvir os anúncios
   - Evita distrações

4. **Tenha paciência**
   - Leitores de tela têm curva de aprendizado
   - Pratique os comandos básicos antes

---

## Testes por Funcionalidade

### 1. Navegação Geral

#### Teste: Skip to Main Content
**Objetivo:** Permitir pular navegação repetitiva

**Passos:**
1. Carregue qualquer página do sistema
2. Pressione `Tab` (primeira tecla Tab)
3. **Esperado:** Foco vai para "Pular para conteúdo principal"
4. Pressione `Enter`
5. **Esperado:** Foco vai direto para conteúdo principal (#main-content)

**Screen reader deve anunciar:**
- "Link: Pular para conteúdo principal"
- "Navegado para conteúdo principal"

**Status:** ✅ Implementado

---

#### Teste: Navegação por Landmark
**Objetivo:** Navegar por regiões da página

**Passos com NVDA:**
1. Pressione `D` (próximo landmark/região)
2. **Esperado:** Navega entre: navigation, main, contentinfo

**Passos com VoiceOver:**
1. `VO + U` (abre rotor)
2. Setas para ir em "Landmarks"
3. **Esperado:** Lista: Navigation, Main, Content Info

**Screen reader deve anunciar:**
- "Navigation landmark"
- "Main landmark"
- "Content Info landmark"

**Status:** ✅ Implementado

---

#### Teste: Navegação por Headings
**Objetivo:** Estrutura semântica clara

**Passos com NVDA:**
1. Pressione `H` (próximo heading)
2. `1-6` para heading específico (ex: `2` para H2)

**Passos com VoiceOver:**
1. `VO + Cmd + H` (próximo heading)

**Esperado:**
- Estrutura lógica: H1 > H2 > H3 (sem saltos)
- Dashboard: "Controle de Provas de Modelagem" (H1)
- Seções com headings apropriados

**Screen reader deve anunciar:**
- "Heading level 1: Controle de Provas de Modelagem"
- "Heading level 2: Relatórios"

**Status:** ✅ Implementado

---

### 2. Formulários

#### Teste: Labels e Campos
**Objetivo:** Todos os campos têm labels descritivos

**Passos:**
1. Vá para qualquer formulário (ex: Novo Relatório)
2. Pressione `Tab` para navegar pelos campos
3. Em cada campo, verifique:
   - Label é lido automaticamente
   - Campos obrigatórios indicam "required" ou "obrigatório"
   - Tipo de campo é identificado (text, select, etc)

**Screen reader deve anunciar:**
- "Descrição Geral, edição, obrigatório, em branco"
- "Coleção, edição, em branco"
- "Temporada, caixa de combinação, Verão"

**Status:** ✅ Implementado

---

#### Teste: Mensagens de Erro
**Objetivo:** Erros são anunciados claramente

**Passos:**
1. Tente enviar formulário com campos vazios
2. **Esperado:**
   - Erro é anunciado: "Erro no campo X: Este campo é obrigatório"
   - Campo com erro recebe foco
   - Mensagem de erro aparece abaixo do campo

**Screen reader deve anunciar:**
- "Alerta: Erro no campo Descrição Geral: Este campo é obrigatório"
- Campo tem "aria-invalid=true"

**Status:** ✅ Implementado

---

#### Teste: Validação em Tempo Real
**Objetivo:** Feedback durante preenchimento

**Passos:**
1. Preencha campo obrigatório
2. Saia do campo (blur)
3. **Esperado:**
   - Se válido: Anúncio "Campo válido"
   - Se inválido: Mensagem de erro específica

**Status:** ✅ Implementado

---

### 3. Filtros e Busca

#### Teste: Filtros Multi-Select
**Objetivo:** Checkboxes acessíveis com feedback

**Passos:**
1. Abra "Filtros Avançados"
2. Navegue pelos filtros com `Tab`
3. Marque/desmarque com `Espaço`
4. **Esperado:** Anúncio a cada mudança

**Screen reader deve anunciar:**
- "Filtros Avançados, botão, recolhido"
- "Status, grupo"
- "Aprovada, caixa de seleção, não marcada"
- Ao marcar: "Filtro Aprovada selecionado"
- "3 filtros ativos" (badge)

**Status:** ✅ Implementado

---

#### Teste: Busca em Tempo Real
**Objetivo:** Resultados anunciados durante digitação

**Passos:**
1. Foque no campo de busca (pressione `/`)
2. Digite um termo
3. Aguarde 1 segundo
4. **Esperado:** Anúncio de quantos resultados foram encontrados

**Screen reader deve anunciar:**
- "Campo de busca focado"
- "5 resultados encontrados para 'camisa'"

**Status:** ✅ Implementado

---

### 4. Cards e Listas

#### Teste: Cards de Relatório
**Objetivo:** Informações completas sem depender de cor

**Passos:**
1. Navegue pelos cards com `Tab`
2. Para cada card, verifique se lê:
   - Código da referência
   - Status (com ícone e texto, não só cor)
   - Descrição
   - Coleção
   - Data
   - Botões de ação

**Screen reader deve anunciar:**
- "Cartão de relatório"
- "Código: 1234"
- "Status: Aprovada" (com ícone ✓)
- "Descrição: Camisa manga curta"
- "Link: Ver Detalhes"
- "Botão: Exportar PDF"

**Status:** ✅ Implementado

---

### 5. Modais

#### Teste: Trap Focus
**Objetivo:** Foco fica dentro do modal

**Passos:**
1. Abra qualquer modal (ex: Excluir relatório)
2. Pressione `Tab` repetidamente
3. **Esperado:**
   - Foco circula apenas dentro do modal
   - Não vai para elementos fora do modal
   - `Esc` fecha o modal
   - Foco retorna ao elemento que abriu

**Screen reader deve anunciar:**
- "Modal aberto: Confirmar Exclusão"
- "Diálogo, Confirmar Exclusão"
- Ao fechar: "Modal fechado"

**Status:** ✅ Implementado

---

#### Teste: Botões do Modal
**Objetivo:** Ações claras

**Passos:**
1. Dentro do modal, navegue pelos botões
2. Verifique se cada botão tem nome descritivo

**Screen reader deve anunciar:**
- "Botão: Cancelar"
- "Botão: Sim, Excluir"

**Status:** ✅ Implementado

---

### 6. Tabelas

#### Teste: Headers e Captions
**Objetivo:** Tabelas estruturadas semanticamente

**Passos:**
1. Navegue para qualquer tabela
2. Pressione `T` (NVDA) ou use rotor (VoiceOver)
3. Verifique:
   - Caption descritivo
   - Headers de coluna (th com scope="col")
   - Navegação célula por célula funcional

**Screen reader deve anunciar:**
- "Tabela: Lista de relatórios de modelagem"
- "Cabeçalho de coluna: Código"
- "Célula: 1234, linha 1, coluna 1"

**Status:** ✅ Implementado

---

### 7. Estados de Loading

#### Teste: Anúncio de Carregamento
**Objetivo:** Usuário sabe que algo está carregando

**Passos:**
1. Realize ação que exibe loading (enviar formulário)
2. **Esperado:** Anúncio imediato

**Screen reader deve anunciar:**
- "Carregando conteúdo, por favor aguarde"
- Status do spinner: "Carregando..."

**Status:** ✅ Implementado

---

### 8. Atalhos de Teclado

#### Teste: Mostrar Atalhos
**Objetivo:** Usuário descobre atalhos disponíveis

**Passos:**
1. Pressione `Ctrl + /` (ou `Cmd + /` no Mac)
2. **Esperado:** Modal com lista de atalhos

**Screen reader deve anunciar:**
- "Modal aberto: Atalhos de Teclado"
- "Tabela: Lista de atalhos de teclado disponíveis"

**Atalhos implementados:**
- `/` - Focar busca
- `Ctrl + N` - Novo relatório
- `Ctrl + S` - Salvar formulário
- `Ctrl + /` - Mostrar atalhos
- `Esc` - Fechar modal

**Status:** ✅ Implementado

---

## Checklist de Testes

Use este checklist para validar a acessibilidade completa:

### Navegação por Teclado
- [ ] Todos os elementos interativos são acessíveis via `Tab`
- [ ] Ordem de tabulação é lógica (segue ordem visual)
- [ ] Focus é sempre visível (outline amarelo)
- [ ] `Shift + Tab` navega para trás
- [ ] `Enter` ativa links e botões
- [ ] `Espaço` ativa botões e checkboxes
- [ ] Não há "armadilhas de teclado" (keyboard traps)
- [ ] Skip to main content funciona

### Screen Reader
- [ ] Todas as imagens têm alt text apropriado
- [ ] Imagens decorativas têm alt=""
- [ ] Botões apenas com ícone têm aria-label
- [ ] Formulários têm labels associados
- [ ] Mensagens de erro são anunciadas
- [ ] Estados de loading são anunciados
- [ ] Mudanças dinâmicas são anunciadas (live regions)
- [ ] Landmarks são identificados corretamente
- [ ] Headings têm hierarquia correta (sem saltos)

### Contraste de Cores
- [ ] Texto normal: ratio mínimo 4.5:1
- [ ] Texto grande (18px+): ratio mínimo 3:1
- [ ] Elementos interativos: ratio mínimo 3:1
- [ ] Status não depende apenas de cor (tem ícone/texto)
- [ ] Links são distinguíveis por mais que cor

### Formulários
- [ ] Todos os campos têm labels
- [ ] Campos obrigatórios são marcados (*) e têm aria-required
- [ ] Erros têm role="alert" e são anunciados
- [ ] Instruções estão antes dos campos
- [ ] Validação acontece em tempo real
- [ ] Mensagens de sucesso são anunciadas

### Modais e Diálogos
- [ ] Focus vai para o modal quando abre
- [ ] Focus fica preso no modal (trap focus)
- [ ] `Esc` fecha o modal
- [ ] Focus retorna ao elemento que abriu
- [ ] Modal tem role="dialog" e aria-modal="true"
- [ ] Modal tem título com aria-labelledby

### Responsividade
- [ ] Zoom até 200% sem perda de funcionalidade
- [ ] Texto pode ser redimensionado
- [ ] Layout funciona em mobile
- [ ] Touch targets têm mínimo 44x44px
- [ ] Orientação (portrait/landscape) não quebra layout

### Preferências do Sistema
- [ ] Respeita prefers-reduced-motion
- [ ] Respeita prefers-contrast (high contrast)
- [ ] Funciona em modo escuro (se implementado)

---

## Problemas Comuns

### Problema 1: Screen reader não lê nada
**Causa:** Screen reader não está ativado ou navegador bloqueou
**Solução:**
- Reinicie o screen reader
- Use outro navegador (Firefox funciona melhor com NVDA)
- Verifique se está em modo de navegação (browse mode)

### Problema 2: Foco invisível
**Causa:** CSS removeu outline sem substituir
**Solução:**
- Nosso sistema já implementa focus visível
- Verifique se `accessibility.css` está carregado

### Problema 3: Elementos não são clicáveis por teclado
**Causa:** Elemento não é focável (não é button, a, input, etc)
**Solução:**
- Use elementos semânticos corretos
- Ou adicione `tabindex="0"` e role apropriado
- Adicione event listener para `Enter` e `Espaço`

### Problema 4: Modal não prende o foco
**Causa:** Trap focus não está implementado
**Solução:**
- Nosso sistema já implementa automaticamente
- Verifique se `accessibility.js` está carregado

### Problema 5: Mudanças dinâmicas não são anunciadas
**Causa:** Falta aria-live region
**Solução:**
- Use `window.announceToScreenReader(mensagem)`
- Nosso sistema já anuncia automaticamente: filtros, busca, loading

---

## Recursos Adicionais

### Documentação Oficial
- **WCAG 2.1 Guidelines:** https://www.w3.org/WAI/WCAG21/quickref/
- **ARIA Authoring Practices:** https://www.w3.org/WAI/ARIA/apg/
- **MDN Accessibility:** https://developer.mozilla.org/en-US/docs/Web/Accessibility

### Ferramentas de Teste
- **axe DevTools** (extensão Chrome/Firefox) - GRATUITO
  - Detecta automaticamente problemas de acessibilidade
  - https://www.deque.com/axe/devtools/

- **WAVE** (Web Accessibility Evaluation Tool) - GRATUITO
  - Extensão e site online
  - https://wave.webaim.org/

- **Lighthouse** (built-in Chrome DevTools) - GRATUITO
  - Auditoria de acessibilidade
  - F12 > Lighthouse > Accessibility

### Cursos e Tutoriais
- **WebAIM:** https://webaim.org/articles/
- **A11ycasts (Google):** https://www.youtube.com/playlist?list=PLNYkxOF6rcICWx0C9LVWWVqvHlYJyqw7g
- **Deque University:** https://dequeuniversity.com/

### Comunidade
- **A11y Project:** https://www.a11yproject.com/
- **Reddit r/accessibility:** https://www.reddit.com/r/accessibility/

---

## Conclusão

Este sistema implementa **WCAG 2.1 nível AA** completo. Todos os recursos listados neste guia foram implementados e testados.

### Próximos Passos

1. **Teste com usuários reais:** O melhor teste é com pessoas que usam screen readers diariamente
2. **Auditorias regulares:** Use ferramentas automatizadas (axe, WAVE, Lighthouse)
3. **Treinamento da equipe:** Todos os desenvolvedores devem conhecer básicos de acessibilidade
4. **Documentação atualizada:** Mantenha este guia atualizado conforme o sistema evolui

---

**Última atualização:** 2026-01-16
**Versão:** 1.0
**Nível de conformidade:** WCAG 2.1 AA
