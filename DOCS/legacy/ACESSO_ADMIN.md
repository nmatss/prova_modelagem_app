# 🔐 CREDENCIAIS DE ACESSO - PAINEL ADMINISTRATIVO

## 🌐 URL da Aplicação
```
http://127.0.0.1:5000
```

## 👤 Credenciais do Admin

**Username:** `admin`
**Senha:** `!@#$Space1234`

---

## 📋 APÓS LOGIN - MENU DISPONÍVEL

### Para Administradores:

1. **Dashboard Principal** (`/`)
   - Visualizar relatórios
   - Criar/editar provas
   - Gerenciar referências

2. **Painel Administrativo** (`/admin/`)
   - 📊 Estatísticas gerais do sistema
   - 🎯 Cards com totais (Usuários, Relatórios, Referências, Provas)
   - 🔧 Acesso rápido às ferramentas de admin

3. **Gerenciar Usuários** (`/admin/users`)
   - ✅ Criar novos usuários
   - ✅ Editar usuários existentes
   - ✅ Resetar senhas
   - ✅ Ativar/Desativar usuários
   - ✅ Definir níveis de acesso (admin, gestor, usuario)

4. **Sistema de Auditoria** (`/admin/audit/`)
   - 📝 Dashboard com filtros avançados
   - 🔍 Busca por usuário, categoria, ação, severidade, data
   - 📊 Estatísticas de atividades
   - 📥 Exportação em CSV
   - 🕐 Timeline de atividades por entidade
   - 👤 Histórico completo por usuário

5. **Estatísticas de Auditoria** (`/admin/audit/estatisticas`)
   - 📈 Total de logs (hoje, semana, mês)
   - 📊 Distribuição por categoria
   - ⚠️ Distribuição por severidade
   - 👥 Usuários mais ativos
   - 📅 Atividade diária (últimos 30 dias)

---

## 🎨 LAYOUT CORRIGIDO

### ✅ O que foi corrigido:

**Problema:** O dashboard admin estava usando classes Tailwind CSS, causando layout quebrado.

**Solução:** Template completamente reescrito usando **Bootstrap 5**

### Novo Layout Inclui:

1. **Cards de Estatísticas** (4 cards responsivos)
   - Usuários (azul)
   - Relatórios (verde)
   - Referências (amarelo)
   - Provas (azul claro)

2. **Menu de Administração** (3 grandes cards)
   - Gerenciar Usuários
   - Sistema de Auditoria
   - Estatísticas

3. **Informações do Sistema**
   - Status dos componentes
   - Informações de segurança

### Design:
- ✅ Bootstrap 5 completo
- ✅ Bootstrap Icons
- ✅ Cards com bordas coloridas
- ✅ Layout responsivo (mobile-first)
- ✅ Sombras e espaçamento adequados
- ✅ Botões com ícones
- ✅ Cores consistentes com o tema

---

## 🚀 COMO INICIAR

```bash
# 1. Ativar ambiente virtual
source .venv/bin/activate

# 2. Iniciar aplicação
python3 app.py

# 3. Acessar no navegador
# http://127.0.0.1:5000
```

---

## 🎯 FUNCIONALIDADES DISPONÍVEIS

### Como Admin, você pode:

✅ **Gerenciar Usuários**
- Criar usuários com senhas auto-geradas
- Definir roles (admin, gestor, usuario)
- Resetar senhas
- Ativar/desativar contas

✅ **Visualizar Auditoria**
- Ver todos os logs de atividades
- Filtrar por usuário, data, categoria
- Exportar relatórios em CSV
- Ver timeline de mudanças

✅ **Acompanhar Estatísticas**
- Usuários mais ativos
- Ações mais comuns
- Distribuição de atividades
- Gráficos de atividade diária

✅ **Gerenciar Provas e Relatórios**
- Dashboard principal do sistema
- CRUD completo de provas
- Aprovações e rejeições
- Upload de fotos

---

## 📸 PREVIEW DO NOVO LAYOUT

### Painel Administrativo (`/admin/`):

```
┌─────────────────────────────────────────────────────┐
│  🏠 Painel Administrativo                           │
├─────────────┬─────────────┬─────────────┬──────────┤
│  USUÁRIOS   │  RELATÓRIOS │ REFERÊNCIAS │  PROVAS  │
│     X       │      Y      │      Z      │    W     │
│ [Gerenciar] │   [Ver]     │    [Ver]    │  [Ver]   │
└─────────────┴─────────────┴─────────────┴──────────┘

┌─────────────────────────────────────────────────────┐
│  🔧 Menu de Administração                           │
├────────────────┬────────────────┬───────────────────┤
│   USUÁRIOS     │   AUDITORIA    │  ESTATÍSTICAS    │
│   👥 ícone     │   🕐 ícone     │   📊 ícone       │
│   [Acessar]    │   [Acessar]    │   [Acessar]      │
└────────────────┴────────────────┴───────────────────┘

┌─────────────────────────────────────────────────────┐
│  ℹ️ Informações do Sistema                          │
│  ✅ Sistema de Auditoria: Ativo                     │
│  ✅ Logs de Atividades: Habilitado                  │
│  🔒 Controle de Acesso: Baseado em Roles            │
└─────────────────────────────────────────────────────┘
```

---

## ✅ STATUS

**Página Admin:** ✅ CORRIGIDA
**Layout:** ✅ Bootstrap 5
**Responsivo:** ✅ SIM
**Funcional:** ✅ SIM

**Pronto para uso!** 🎉
