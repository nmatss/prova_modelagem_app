# 📚 Documentação Completa - Sistema de Provas de Modelagem Puket

> **Versão:** 2.0.0
> **Última Atualização:** 16 de Janeiro de 2026
> **Status:** ✅ Produção

---

## 🎯 Visão Geral

Sistema web profissional para gestão completa de provas de modelagem de vestuário, desenvolvido especificamente para a **Puket**. Gerencia todo o ciclo desde o recebimento de amostras até a aprovação final, incluindo avaliações de qualidade, estilo e modelagem.

### Stack Tecnológica

- **Backend:** Python 3.11 + Flask 3.0
- **Banco de Dados:** PostgreSQL 15 (Produção) / SQLite (Desenvolvimento)
- **Frontend:** Bootstrap 5.3 + JavaScript ES6+
- **Deploy:** Docker + Gunicorn + Nginx
- **Servidor Atual:** Ubuntu 24.04 LTS (192.168.168.124)

---

## 📖 Navegação Rápida

### 🚀 Para Começar

| Documento | Descrição | Tempo |
|-----------|-----------|-------|
| **[README Principal](../README.md)** | Visão geral e quick start | 5 min |
| **[Quick Start](QUICK_START.md)** | Guia de início rápido completo | 10 min |

### 🐳 Deploy e Infraestrutura

| Documento | Descrição | Público |
|-----------|-----------|---------|
| **[Deploy com Docker](deploy/DOCKER.md)** | Guia completo Docker (SQLite e PostgreSQL) | DevOps, Dev |
| **[Deploy em Produção](deploy/PRODUCAO.md)** | Deploy manual tradicional (Linux) | SysAdmin |
| **[Servidor Atual](deploy/SERVIDOR_ATUAL.md)** | Documentação do servidor 192.168.168.124 | Ops, Suporte |

### 🏗️ Arquitetura

| Documento | Descrição | Público |
|-----------|-----------|---------|
| **[Arquitetura Backend](architecture/BACKEND.md)** | Estrutura completa do backend | Dev Backend |
| **[Arquitetura Frontend](architecture/FRONTEND.md)** | Design system e componentes | Dev Frontend, Design |
| **[Banco de Dados](architecture/DATABASE.md)** | Schema e relacionamentos | Dev, DBA |

### 📘 Guias de Uso

| Documento | Descrição | Público |
|-----------|-----------|---------|
| **[Guia de Manutenção](guides/MAINTENANCE.md)** | Operações diárias e manutenção preventiva | Ops, SysAdmin |
| **[Guia de Desenvolvimento](guides/DEVELOPMENT.md)** | Padrões de código e workflows | Dev |
| **[Troubleshooting](guides/TROUBLESHOOTING.md)** | Resolução de problemas comuns | Todos |

### 🎨 Design e UX

| Documento | Descrição | Público |
|-----------|-----------|---------|
| **[Design System](design/DESIGN_SYSTEM.md)** | Tokens, cores e componentes | Design, Frontend |
| **[Componentes](design/COMPONENTS.md)** | Biblioteca de componentes | Frontend |
| **[Padrões de UX](design/UX_PATTERNS.md)** | Padrões de interface e interação | Design, UX |

### 🔌 API e Integrações

| Documento | Descrição | Público |
|-----------|-----------|---------|
| **[Referência de API](api/API_REFERENCE.md)** | Endpoints e exemplos | Dev, Integrações |

---

## 📂 Estrutura da Documentação

```
DOCS/
├── INDEX.md (este arquivo)
├── QUICK_START.md
│
├── deploy/
│   ├── DOCKER.md              # Deploy com Docker (recomendado)
│   ├── PRODUCAO.md            # Deploy manual
│   └── SERVIDOR_ATUAL.md      # Servidor 192.168.168.124
│
├── architecture/
│   ├── BACKEND.md             # Flask, modelos, rotas
│   ├── FRONTEND.md            # Templates, CSS, JS
│   └── DATABASE.md            # Schema, relacionamentos
│
├── guides/
│   ├── MAINTENANCE.md         # Manutenção e ops
│   ├── DEVELOPMENT.md         # Desenvolvimento
│   └── TROUBLESHOOTING.md     # Problemas comuns
│
├── design/
│   ├── DESIGN_SYSTEM.md       # Sistema de design
│   ├── COMPONENTS.md          # Biblioteca de componentes
│   └── UX_PATTERNS.md         # Padrões de UX
│
└── api/
    └── API_REFERENCE.md       # Referência completa de API
```

---

## 🎯 Guias Por Persona

### 👨‍💻 Desenvolvedor Backend

1. **[Arquitetura Backend](architecture/BACKEND.md)** - Entenda a estrutura
2. **[Banco de Dados](architecture/DATABASE.md)** - Schema e modelos
3. **[API Reference](api/API_REFERENCE.md)** - Endpoints disponíveis
4. **[Guia de Desenvolvimento](guides/DEVELOPMENT.md)** - Padrões de código

### 👨‍🎨 Desenvolvedor Frontend

1. **[Arquitetura Frontend](architecture/FRONTEND.md)** - Estrutura e componentes
2. **[Design System](design/DESIGN_SYSTEM.md)** - Tokens e variáveis
3. **[Componentes](design/COMPONENTS.md)** - Biblioteca reutilizável
4. **[Padrões UX](design/UX_PATTERNS.md)** - Interações e estados

### 🛠️ DevOps / SysAdmin

1. **[Deploy Docker](deploy/DOCKER.md)** - Containerização
2. **[Servidor Atual](deploy/SERVIDOR_ATUAL.md)** - Infraestrutura atual
3. **[Guia de Manutenção](guides/MAINTENANCE.md)** - Ops diárias
4. **[Troubleshooting](guides/TROUBLESHOOTING.md)** - Resolução de problemas

### 🎨 Designer / UX

1. **[Design System](design/DESIGN_SYSTEM.md)** - Sistema completo
2. **[Arquitetura Frontend](architecture/FRONTEND.md)** - Implementação
3. **[Componentes](design/COMPONENTS.md)** - Componentes disponíveis
4. **[Padrões UX](design/UX_PATTERNS.md)** - Best practices

### 👔 Product Owner / Gestor

1. **[README Principal](../README.md)** - Visão geral
2. **[Quick Start](QUICK_START.md)** - Início rápido
3. **[Servidor Atual](deploy/SERVIDOR_ATUAL.md)** - Status da infraestrutura

---

## 🔍 Busca Rápida

### Procurando por...

**"Como fazer deploy?"**
→ [Deploy Docker](deploy/DOCKER.md) (recomendado) ou [Deploy Produção](deploy/PRODUCAO.md)

**"Como acessar o servidor de produção?"**
→ [Servidor Atual](deploy/SERVIDOR_ATUAL.md) (credenciais e acesso)

**"Como funciona o backend?"**
→ [Arquitetura Backend](architecture/BACKEND.md) (estrutura completa)

**"Quais componentes CSS existem?"**
→ [Componentes](design/COMPONENTS.md) (biblioteca completa)

**"Como resolver erro X?"**
→ [Troubleshooting](guides/TROUBLESHOOTING.md) (problemas comuns)

**"Como fazer backup?"**
→ [Guia de Manutenção](guides/MAINTENANCE.md) (seção Backup)

**"Quais endpoints de API existem?"**
→ [API Reference](api/API_REFERENCE.md) (documentação completa)

**"Qual o schema do banco?"**
→ [Database](architecture/DATABASE.md) (diagramas e relações)

---

## 📊 Estatísticas do Sistema

### Código
- **Backend:** Python 3.11 (Flask 3.0)
- **Linhas de Código:** ~15.000 (Python) + ~10.000 (Templates/JS/CSS)
- **Módulos Python:** 15 arquivos principais
- **Templates:** 29 arquivos Jinja2
- **Endpoints:** 32 rotas

### Frontend
- **CSS:** 10 arquivos modulares (~5.000 linhas)
- **JavaScript:** 11 módulos (~3.000 linhas)
- **Componentes:** 50+ componentes reutilizáveis
- **Design Tokens:** 200+ variáveis CSS

### Infraestrutura
- **Servidor:** Ubuntu 24.04 LTS
- **CPU:** 12 vCPUs (Intel Xeon E5-2650 @ 2.00GHz)
- **RAM:** 9.7 GB
- **Disco:** 97 GB (35% usado)
- **Uptime:** 99.9%

### Banco de Dados
- **Tipo:** PostgreSQL 15 (Produção) / SQLite (Dev)
- **Tabelas:** 6 principais (usuarios, relatorios, referencias, provas, fotos, audit_logs)
- **Registros:** Variável por instalação
- **Backups:** Automáticos diários

---

## 🔐 Informações de Acesso

### Servidor de Produção

```
Host: 192.168.168.124
Usuário: nicolas
Porta SSH: 22
Aplicação: http://192.168.168.124:5000
```

> ⚠️ **Segurança:** Credenciais completas em [Servidor Atual](deploy/SERVIDOR_ATUAL.md)

### Aplicação Web

```
URL: http://192.168.168.124:5000
Admin: definido em .env (ADMIN_USERNAME/ADMIN_PASSWORD)
```

---

## 📝 Convenções da Documentação

### Ícones Utilizados

- 📚 Documentação geral
- 🚀 Deploy e produção
- 🏗️ Arquitetura e estrutura
- 🎨 Design e UX
- 🔌 API e integrações
- 🛠️ Manutenção e ops
- ⚠️ Avisos importantes
- ✅ Confirmações e status OK
- ❌ Erros e problemas
- 💡 Dicas e boas práticas

### Níveis de Prioridade

| Emoji | Nível | Descrição |
|-------|-------|-----------|
| ⭐⭐⭐ | Essencial | Leitura obrigatória |
| ⭐⭐ | Recomendado | Altamente recomendado |
| ⭐ | Opcional | Complementar |

---

## 🤝 Contribuindo

### Para Atualizar a Documentação

1. Mantenha o padrão de formatação Markdown
2. Use seções numeradas e hierárquicas
3. Adicione exemplos de código quando relevante
4. Inclua diagramas e tabelas
5. Atualize o índice (INDEX.md)
6. Mantenha links relativos funcionais

### Template de Nova Documentação

```markdown
# Título do Documento

> **Versão:** X.Y.Z
> **Última Atualização:** DD/MM/YYYY

---

## Índice

1. [Seção 1](#seção-1)
2. [Seção 2](#seção-2)

---

## Seção 1

Conteúdo...

### Subseção

Detalhes...

## Referências

- [Documento relacionado](link)
```

---

## 📞 Suporte

### Documentação

Para dúvidas sobre documentação:
- Consulte a seção de **Busca Rápida** acima
- Veja **Guias Por Persona** para navegação direcionada

### Problemas Técnicos

- **Troubleshooting:** [Guia de Resolução](guides/TROUBLESHOOTING.md)
- **Logs:** [Guia de Manutenção](guides/MAINTENANCE.md)
- **Deploy:** [Guias de Deploy](deploy/)

### Contato

- **Desenvolvedor:** Nicolas Matsuda
- **Empresa:** Puket / Grupo Único
- **Email:** nicolas.matsuda@grupounico.com

---

## 📈 Histórico de Versões

### v2.0.0 - 16/01/2026
- ✅ Reorganização completa da documentação
- ✅ Estrutura DOCS/ hierárquica
- ✅ Índice mestre navegável
- ✅ Guias consolidados por persona
- ✅ Documentação de servidor atualizada

### v1.0.0 - Dezembro 2024
- ✅ Documentação inicial
- ✅ README básico
- ✅ Guias de deploy

---

## 🎓 Recursos Adicionais

### Documentação Externa

- **Flask:** https://flask.palletsprojects.com/
- **Bootstrap 5:** https://getbootstrap.com/
- **PostgreSQL:** https://www.postgresql.org/docs/
- **Docker:** https://docs.docker.com/
- **Gunicorn:** https://docs.gunicorn.org/

### Ferramentas Recomendadas

- **IDE:** VS Code, PyCharm
- **API Testing:** Postman, Insomnia
- **Database:** pgAdmin, DBeaver
- **Containers:** Docker Desktop, Portainer

---

## ✅ Status da Documentação

| Categoria | Status | Completude |
|-----------|--------|------------|
| README Principal | ✅ Completo | 100% |
| Deploy | ✅ Completo | 100% |
| Arquitetura | ✅ Completo | 100% |
| Guias | ✅ Completo | 100% |
| Design System | ✅ Completo | 100% |
| API Reference | ✅ Completo | 100% |

**Documentação:** ✅ **FINALIZADA**
**Última Revisão:** 16/01/2026

---

<div align="center">

**Sistema de Gestão de Provas de Modelagem - Puket**
© 2024-2026 TI Unico Web. Todos os direitos reservados.

📚 **[Voltar ao Topo](#-documentação-completa---sistema-de-provas-de-modelagem-puket)**

</div>
