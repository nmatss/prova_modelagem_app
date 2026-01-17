# 📖 Manual do Usuário
# Sistema de Gestão de Provas de Modelagem

**Versão:** 1.0
**Data:** 03/12/2025

---

## 📋 Índice

1. [Introdução](#introdução)
2. [Acesso ao Sistema](#acesso-ao-sistema)
3. [Perfis de Usuário](#perfis-de-usuário)
4. [Dashboard Principal](#dashboard-principal)
5. [Gestão de Relatórios](#gestão-de-relatórios)
6. [Gestão de Referências](#gestão-de-referências)
7. [Gestão de Provas](#gestão-de-provas)
8. [Upload de Arquivos](#upload-de-arquivos)
9. [Workflow de Aprovação](#workflow-de-aprovação)
10. [Exportação de Dados](#exportação-de-dados)
11. [Administração](#administração)
12. [Auditoria](#auditoria)

---

## 🎯 Introdução

O Sistema de Gestão de Provas de Modelagem é uma aplicação web que permite gerenciar todo o ciclo de vida de provas de modelagem de produtos têxteis, desde a criação até a aprovação final.

### Principais Funcionalidades

- ✅ Criação e gestão de relatórios de coleção
- ✅ Catalogação de referências com fornecedores
- ✅ Registro completo de provas de modelagem
- ✅ Upload de fotos, PPTs e tabelas de medidas
- ✅ Workflow de aprovação (Qualidade, Estilo, Modelagem)
- ✅ Exportação em PDF e Excel
- ✅ Auditoria completa de ações
- ✅ Painel administrativo

---

## 🔐 Acesso ao Sistema

### Primeiro Acesso

1. Acesse a URL fornecida pelo administrador
2. Na tela de login, insira suas credenciais
3. Clique em "Entrar"

**Credenciais Padrão (Admin):**
- **Usuário:** `admin`
- **Senha:** `admin123`

⚠️ **IMPORTANTE:** Altere sua senha após o primeiro acesso!

### Alteração de Senha

1. Clique no seu nome no canto superior direito
2. Selecione "Alterar Senha" (futuro)
3. Ou solicite ao administrador um reset de senha

### Logout

1. Clique no seu nome no canto superior direito
2. Selecione "Sair"

---

## 👥 Perfis de Usuário

### 1. Administrador (admin)

**Permissões:**
- ✅ Acesso total ao sistema
- ✅ Gestão de usuários
- ✅ Visualização de auditoria
- ✅ Todas as funcionalidades de gestor e usuário

### 2. Gestor (gestor)

**Permissões:**
- ✅ Criar, editar e excluir relatórios
- ✅ Criar, editar e excluir referências
- ✅ Criar, editar e excluir provas
- ✅ Aprovar/reprovar provas
- ✅ Upload de arquivos
- ✅ Exportar relatórios
- ❌ Gestão de usuários
- ❌ Visualização de auditoria

### 3. Usuário (usuario)

**Permissões:**
- ✅ Visualizar relatórios
- ✅ Criar provas
- ✅ Upload de fotos
- ✅ Adicionar comentários
- ✅ Exportar relatórios (visualização)
- ❌ Excluir relatórios/provas
- ❌ Aprovar/reprovar provas

---

## 📊 Dashboard Principal

### Visão Geral

Ao fazer login, você verá o dashboard com cards de relatórios:

**Informações Exibidas:**
- Código do relatório (ex: REL-2025-001)
- Status (Em Andamento, Aprovado, Reprovado)
- Coleção
- Descrição
- Temporada e Ano
- Data de criação

**Ações Disponíveis:**
- **Ver Detalhes Completos:** Visualiza relatório completo
- **Exportar PDF:** Baixa relatório em PDF

### Filtros

- **Por Status:** Em Andamento, Aprovado, Reprovado
- **Por Coleção:** Verão 2025, Inverno 2024, etc.
- **Por Temporada:** Dropdown de temporadas

---

## 📝 Gestão de Relatórios

### Criar Novo Relatório

1. Clique no botão "**+ Novo Relatório**" no dashboard
2. Preencha o formulário:

**Campos Obrigatórios:**
- **Descrição Geral:** Descrição resumida do relatório
- **Coleção:** Nome da coleção (ex: Primavera Verão 2025)

**Campos Opcionais:**
- **Temporada:** Verão, Inverno, Meia Estação
- **Ano:** 2025, 2024, etc.
- **PPT da Coleção:** Upload de apresentação PowerPoint
- **Status Geral:** Em Andamento (padrão), Aprovado, Reprovado

3. Clique em "**Salvar Relatório**"
4. Você será redirecionado para a página de detalhes

**Código Automático:**
O sistema gera automaticamente um código único (ex: REL-2025-001)

### Visualizar Relatório

1. No dashboard, clique em "**Ver Detalhes Completos**"
2. Você verá:
   - Informações gerais do relatório
   - Lista de referências
   - Lista de provas de cada referência
   - Fotos das provas

### Editar Relatório

1. Na página de detalhes do relatório, clique em "**Editar Relatório**"
2. Modifique os campos desejados
3. Clique em "**Salvar Alterações**"

### Excluir Relatório

⚠️ **ATENÇÃO:** Esta ação é irreversível!

1. Na página de detalhes, clique em "**Excluir Relatório**"
2. Confirme a exclusão
3. Todos os dados relacionados (referências, provas, fotos) serão excluídos

---

## 🏷️ Gestão de Referências

### Adicionar Referência

1. Na página de edição do relatório, localize "**Adicionar Referência**"
2. Preencha o formulário:

**Informações Básicas:**
- **Tipo/Categoria:** baby, kids, teen, adulto
- **Número da Referência:** Código interno
- **Origem:** País ou região de origem

**Fornecedor:**
- **Nome do Fornecedor**
- **Contato do Fornecedor:** Telefone/email

**Matéria-Prima:**
- **Matéria-Prima:** Algodão, Poliéster, etc.
- **Composição:** % de cada material
- **Gramatura:** g/m²

**Aviamentos:**
- **Aviamentos:** Botões, zíperes, etiquetas, etc.

**Observações:**
- Campo livre para informações adicionais

3. Clique em "**Adicionar Referência**"

**Código Automático:**
Sistema gera código único para a referência

### Editar Referência

1. Na lista de referências, clique no ícone de edição (lápis)
2. Modifique os campos
3. Salve as alterações

### Excluir Referência

1. Clique no ícone de exclusão (lixeira)
2. Confirme a ação
3. Todas as provas relacionadas serão excluídas

---

## 🧵 Gestão de Provas

### Criar Nova Prova

1. Na página do relatório, localize a referência desejada
2. Clique em "**+ Nova Prova**"
3. Preencha o formulário:

**Informações de Recebimento:**
- **Data de Recebimento da Amostra**
- **Tamanhos Recebidos:** P, M, G, etc.
- **Informações de Medidas:** Observações sobre medidas
- **Data de Realização da Prova**

**Tabela de Medidas:**
- **Upload de Tabela de Medidas:** Arquivo Excel com medidas

**Status Inicial:**
- Automaticamente definido como "**Em Andamento**"

4. Clique em "**Salvar Prova**"

**Código Automático:**
Sistema gera código único (ex: PROVA-001) e número sequencial

### Visualizar Prova

Na lista de provas, clique no código da prova para ver:
- Todas as informações da prova
- Fotos organizadas por contexto
- Histórico de alterações de status
- Feedbacks de Qualidade, Estilo e Modelagem

### Upload de Fotos

1. Na página da prova, localize "**Upload de Fotos**"
2. Selecione o **contexto da foto:**
   - **Desenho:** Desenho técnico do produto
   - **Qualidade:** Fotos de análise de qualidade
   - **Estilo:** Fotos de análise de estilo
   - **Amostra:** Fotos da amostra recebida
   - **Prova com Modelo:** Fotos da prova vestida

3. Se for Amostra ou Prova com Modelo, selecione o **tamanho**
4. Adicione uma **descrição** (opcional)
5. Clique em "**Escolher Arquivo**"
6. Selecione a foto (formatos aceitos: PNG, JPG, JPEG, GIF)
7. Clique em "**Upload**"

**Limites:**
- Tamanho máximo: 10 MB por foto
- Formatos: PNG, JPG, JPEG, GIF

### Excluir Foto

1. Na galeria de fotos, clique no ícone de exclusão
2. Confirme a ação

---

## ✅ Workflow de Aprovação

### Responsáveis

Cada prova passa por 3 áreas de aprovação:
1. **Qualidade** - Análise de defeitos e conformidade
2. **Estilo** - Análise de design e estética
3. **Modelagem** - Análise de caimento e medidas

### Adicionar Feedback

#### 1. Feedback de Qualidade

1. Na página da prova, localize "**Qualidade**"
2. Preencha:
   - **Responsável pela Qualidade:** Nome do analista
   - **Comentários de Qualidade:** Pontos aprovados
   - **Observações de Qualidade:** Pontos de atenção ou reprovados
3. Clique em "**Salvar Feedback de Qualidade**"

#### 2. Feedback de Estilo

1. Localize "**Estilo**"
2. Preencha:
   - **Responsável pelo Estilo**
   - **Comentários de Estilo**
   - **Observações de Estilo**
3. Salve

#### 3. Feedback de Modelagem

1. Localize "**Modelagem**"
2. Preencha:
   - **Responsável pela Modelagem**
   - **Comentários de Modelagem**
   - **Observações de Modelagem**
3. Salve

### Atualizar Status da Prova

1. Após todos os feedbacks, localize "**Atualizar Status da Prova**"
2. Selecione o novo status:
   - **Em Andamento** - Ainda em análise
   - **Aprovada** - Aprovada por todas as áreas
   - **Reprovada** - Reprovada (especificar motivo)
   - **Aguardando Correção** - Necessita ajustes
   - **Corrigida** - Ajustes realizados
   - **Cancelada** - Cancelada

3. Adicione **Motivo da Alteração** (obrigatório)
4. Clique em "**Atualizar Status**"

**Histórico:**
Todas as mudanças de status são registradas e visíveis no histórico

### Liberação de Lacre

Quando a prova é aprovada:
1. Localize "**Liberação de Lacre**"
2. Preencha:
   - **Data de Liberação do Lacre**
   - **Número do Lacre**
3. Salve

---

## 📤 Exportação de Dados

### Exportar Relatório em PDF

1. No dashboard ou na página do relatório, clique em "**Exportar PDF**"
2. O sistema gera um PDF com:
   - Informações gerais do relatório
   - Todas as referências
   - Todas as provas com fotos
   - Feedbacks de aprovação
   - Histórico de status

3. O arquivo é baixado automaticamente

**Nome do Arquivo:**
`relatorio_{id}_{timestamp}.pdf`

### Exportar Relatório em Excel

1. Na página do relatório, clique em "**Exportar Excel**"
2. O sistema gera um arquivo XLSX com 3 abas:
   - **Aba 1:** Informações Gerais
   - **Aba 2:** Referências
   - **Aba 3:** Provas de Modelagem

3. O arquivo é baixado automaticamente

**Nome do Arquivo:**
`relatorio_{codigo}_{timestamp}.xlsx`

---

## ⚙️ Administração

### Acesso ao Painel Admin

**Apenas para administradores**

1. Clique em seu nome no canto superior direito
2. Selecione "**Administração**"
3. Ou acesse: Menu → Administração → Dashboard

### Dashboard Administrativo

**Estatísticas Exibidas:**
- Total de usuários
- Total de relatórios
- Total de provas
- Total de fotos

**Menu de Administração:**
- **Gerenciar Usuários:** CRUD de usuários
- **Auditoria:** Logs de atividades
- **Estatísticas:** Métricas do sistema

### Gestão de Usuários

#### Listar Usuários

1. Menu → Administração → Usuários
2. Visualize tabela com:
   - Username
   - Nome Completo
   - Email
   - Role (Perfil)
   - Status (Ativo/Inativo)
   - Último Acesso

#### Criar Novo Usuário

1. Clique em "**+ Criar Novo Usuário**"
2. Preencha o formulário:

**Campos:**
- **Username:** Login do usuário (único, alfanumérico)
- **Email:** Email válido (único)
- **Nome Completo:** Nome completo do usuário
- **Senha:** Mínimo 8 caracteres (maiúscula + minúscula + número + especial)
- **Confirmar Senha:** Mesma senha
- **Perfil (Role):**
  - `admin` - Administrador
  - `gestor` - Gestor
  - `usuario` - Usuário
- **Status:** Ativo/Inativo

3. Clique em "**Criar Usuário**"

**Validações:**
- Username único
- Email único e válido
- Senha forte (8+ chars, maiúsc, minúsc, núm, especial)

#### Editar Usuário

1. Na lista de usuários, clique no ícone de edição
2. Modifique os campos desejados
3. **Não é possível alterar a senha aqui** (use "Resetar Senha")
4. Clique em "**Salvar Alterações**"

#### Resetar Senha

1. Na lista de usuários, clique em "**Resetar Senha**"
2. O sistema gera uma **senha temporária**
3. A senha é exibida na tela (anote!)
4. Informe o usuário da nova senha
5. Usuário deve alterar a senha no próximo login

#### Ativar/Desativar Usuário

1. Na lista de usuários, clique no botão "**Ativar**" ou "**Desativar**"
2. Usuários inativos não podem fazer login
3. Dados são preservados

#### Excluir Usuário

⚠️ **CUIDADO:** Ação irreversível!

1. Clique em "**Excluir**"
2. Confirme a ação
3. Usuário e suas relações são removidos

---

## 🕵️ Auditoria

### Acesso aos Logs

**Apenas para administradores**

1. Menu → Administração → Auditoria
2. Visualize o dashboard de auditoria

### Dashboard de Auditoria

**Estatísticas Rápidas:**
- Total de logs
- Logs hoje
- Logs esta semana
- Logs este mês

**Filtros Avançados:**
- **Por Usuário:** Dropdown de usuários
- **Por Categoria:** Autenticação, Usuários, Relatórios, Provas, Aprovações
- **Por Ação:** CREATE, UPDATE, DELETE, LOGIN, LOGOUT, etc.
- **Por Severidade:** INFO, WARNING, CRITICAL
- **Por Data:** Data inicial e final
- **Busca:** Busca em descrições

### Visualizar Log

1. Na tabela de logs, clique no log desejado
2. Visualize detalhes:
   - **Quem:** Usuário que executou a ação
   - **O quê:** Ação realizada (CREATE, UPDATE, etc.)
   - **Quando:** Data e hora (timestamp)
   - **Onde:** IP, URL, User-Agent
   - **Detalhes:** Dados antes e depois (JSON)

### Timeline de Entidade

1. Selecione uma entidade (Relatório, Prova, etc.)
2. Visualize timeline cronológica de todas as ações

### Logs por Usuário

1. Selecione um usuário
2. Visualize todas as ações realizadas
3. Estatísticas:
   - Total de ações
   - Ações por categoria
   - Últimas atividades

### Exportar Logs

1. Configure os filtros desejados
2. Clique em "**Exportar CSV**"
3. Arquivo CSV é baixado com:
   - Data/Hora
   - Usuário
   - Ação
   - Entidade
   - Descrição
   - IP

---

## 🆘 Suporte

### Mensagens de Erro Comuns

#### "CSRF token missing or invalid"
- **Causa:** Sessão expirou
- **Solução:** Faça logout e login novamente

#### "Arquivo muito grande"
- **Causa:** Arquivo excede 10 MB (fotos) ou 50 MB (docs)
- **Solução:** Reduza o tamanho do arquivo

#### "Extensão não permitida"
- **Causa:** Tipo de arquivo não suportado
- **Solução:** Use PNG, JPG, PDF, XLSX, PPT

#### "Acesso negado"
- **Causa:** Sem permissão para a ação
- **Solução:** Contate um administrador

#### "Muitas requisições"
- **Causa:** Rate limit excedido
- **Solução:** Aguarde 60 segundos

### Dicas de Uso

✅ **Sempre adicione descrições detalhadas** nos relatórios e provas

✅ **Upload fotos em alta qualidade** para melhor visualização

✅ **Preencha todos os feedbacks** antes de aprovar uma prova

✅ **Use códigos de referência** consistentes para facilitar busca

✅ **Faça backup** dos arquivos importantes antes de excluir

✅ **Documente motivos** ao alterar status de provas

---

**Última Atualização:** 03/12/2025
**Versão:** 1.0
