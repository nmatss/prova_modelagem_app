# Backlog — Integração Linx

**Status:** ✅ Implementada (POC mínima) em 2026-05-22. Veja `docs/linx_db_puket_analysis.md` para o mapeamento campo-a-campo e a seção "O que foi implementado" abaixo.

---

## O que foi implementado (POC, 2026-05-22)

- `linx_client.py` — cliente pyodbc read-only ao `db_puket` (db01) com cache TTL e timeout 5s.
- `linx_bp.py` — blueprint Flask com endpoints autocomplete (`/linx/api/fornecedores`, `/linx/api/produtos`) e fluxos de import (fornecedor único + batch de produtos para um relatório).
- Template `linx_anexar_produtos.html` — tela de seleção múltipla que **também resolve o item 1 da reunião** ("anexar vários produtos de uma vez"), pois cria N referências de uma vez a partir do catálogo do ERP.
- Botão "Buscar no ERP" em `fornecedor_form.html` (criar novo fornecedor pré-preenchendo do db_puket).
- Botão "Anexar produtos do ERP" em `detalhes_relatorio.html`.
- Link "ERP Linx" na sidebar (admin only, oculto se `LINX_DB_ENABLED=false`).
- Variáveis de ambiente: `LINX_DB_HOST`, `LINX_DB_PORT`, `LINX_DB_NAME`, `LINX_DB_USER`, `LINX_DB_PASSWORD`, `LINX_DB_DRIVER`, `LINX_DB_TIMEOUT`, `LINX_CACHE_TTL`, `LINX_DB_ENABLED`.

**Para ativar em produção:** preencher credenciais no `.env` do container, garantir ODBC Driver 18 instalado e setar `LINX_DB_ENABLED=true`. Sem credenciais a UI fica invisível — não derruba o app.

---

## Histórico do discovery (original, mantido para contexto)

---

## Perguntas a responder antes de codar

### 1. Qual produto Linx?
A Linx tem várias famílias de produto. **A pergunta primária é qual delas:**

- **Linx Microvix** — ERP/PDV cloud-first, voltado para varejo de moda/calçado. Tem API REST (`/api/v1/`). É o que **a empresa já tem integração existente**: ver projeto `/home/nicolas/microvix-integracao` no servidor `n8n` (container `monitoria-unico` ativo).
- **Linx Big** — ERP on-premise tradicional, integração via banco SQL Server ou web services SOAP.
- **Linx Commerce** (antigo Neemu) — plataforma de e-commerce.
- **Linx POS** — frente de caixa standalone.

**Padrão a seguir:** se for Microvix, **reutilizar abordagem do projeto `microvix-integracao`** (mesmas credenciais, mesmo padrão de autenticação, mesmos endpoints já mapeados). Estudar aquele código antes de começar.

### 2. Direção da sincronia
- **Linx → Prova App (read only)** — puxar cadastro de produtos/fornecedores/coleções da Linx para alimentar dropdowns / autocompletes no Prova App?
- **Prova App → Linx** — empurrar status de provas aprovadas de volta para Linx (ex: liberar SKU para produção)?
- **Bidirecional** — ambos os fluxos.

**Recomendação inicial:** começar **uni-direcional Linx → Prova App** (menor risco — não escreve no ERP). Provavelmente é o que a Alice quer (puxar produtos/fornecedores já cadastrados na Linx para evitar redigitação).

### 3. Quais entidades?
Marcar com Alice quais campos precisam vir da Linx:

- [ ] **Produtos/SKUs** — código, descrição, coleção, categoria
- [ ] **Fornecedores** — nome, CNPJ, contato, país
- [ ] **Coleções/Temporadas** — para auto-popular dropdowns
- [ ] **Pedidos de compra** — para vincular relatórios a pedidos reais
- [ ] **Estoque** — improvável que faça sentido aqui
- [ ] **NF de entrada** — improvável

### 4. Frequência
- **Real-time webhook** — Linx empurra evento ao Prova App quando algo muda (requer webhook na Linx, mais complexo)
- **Polling agendado** — Prova App busca atualizações 1x/dia ou 1x/hora (mais simples, latência aceitável)
- **Manual on-demand** — botão "Sincronizar agora" no admin (mais simples ainda)

**Recomendação:** começar com **polling 1x/dia** via cron / scheduled task no container. Reaproveitar `entrypoint.sh` para registrar o cron.

### 5. Credenciais e ambiente
- Quem detém credenciais Linx? Há ambiente sandbox?
- Onde guardar token/API key? **NÃO** em `.env` versionado — usar Vault (`vault-central` já está rodando no servidor) ou variável de ambiente injetada pelo docker-compose.
- Rate limits da API Linx?

### 6. Volume estimado
- Quantos produtos, fornecedores, registros por dia?
- Determina se polling diário é suficiente ou se precisa de paginação cuidadosa.

---

## Material de referência interno

### Projeto `/home/nicolas/microvix-integracao` (servidor `n8n`)
- Container ativo: `monitoria-unico` (`monitoria_unico_geral-monitoria`)
- Pasta no host: `/home/nicolas/microvix-integracao`
- Padrão de autenticação Microvix: usar como template para o que vier neste projeto
- **Antes de codar qualquer linha**, ler aquele projeto end-to-end. Possivelmente extrair um cliente reutilizável.

### Padrão de integrações já em vigor
Outros projetos no servidor usam:
- `requests` para HTTP (já está em `requirements.txt` mas não usado em produção no Prova App)
- `n8n` (containers `lab1085-n8n` e `n8n-enterprise-*`) — pode ser usado como middleware se a Linx tiver muitos endpoints e quisermos manter Prova App magro

---

## Estimativa de esforço (preliminar)

Assumindo Microvix + Linx→Prova App + 2 entidades (Produtos + Fornecedores) + polling diário:

| Etapa | Esforço |
|---|---|
| Discovery (chamadas com Alice + auditoria do código microvix) | 2 dias |
| Cliente Linx (reuso do microvix-integracao) | 1 dia |
| Modelagem (entidades intermediárias `ProdutoLinx`, `FornecedorLinx`?) | 1 dia |
| Sync handler + cron | 2 dias |
| Admin UI de monitoramento (último sync, erros) | 1 dia |
| Testes E2E em sandbox + bugs | 2 dias |
| **Total** | **~9 dias úteis (1 sprint)** |

Se for bidirecional ou outro produto Linx, **dobrar a estimativa**.

---

## Próximos passos

1. Marcar reunião de discovery com Alice (e quem mais tiver visibilidade dos sistemas Linx atuais)
2. Levantar credenciais sandbox / ambiente de teste
3. Estudar `microvix-integracao` e produzir documento técnico com a API que vamos consumir
4. Priorizar em sprint dedicado — **não tentar encaixar em sprints de outras features**
