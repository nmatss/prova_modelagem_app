# Análise da DB_puket — Integração Prova App ↔ Linx ERP

**Atualização**: 2026-05-21
**Fonte**: análise direta na base `db_puket` em `db01.grupounico.com:1433`
**Credenciais usadas**: `nicolas.matsuda` (mesmas do `puket-app` em produção)

Este documento **substitui** a parte de discovery em `linx_discovery.md` agora que temos acesso confirmado e schema mapeado.

---

## 1. Resumo executivo

A `db_puket` **NÃO é diretamente uma base Linx Microvix**. É um SQL Server interno **muito grande** (centenas de milhões de linhas em tabelas operacionais como `PortalEstoquesLojasDia`, `IMB_ESTOQUE_HISTORICO_PA`, etc.) que **consome dados do Linx ERP** (provavelmente Linx Big, pelos padrões de nomenclatura: `CTB_*`, `LF_*`, `IMB_*`, `PKT_*`).

**Para a integração Prova App, só precisamos de ~10 tabelas-mestre de cadastro** (catalog data), todas estáveis e relativamente pequenas. Não precisamos tocar nas tabelas operacionais.

**Recomendação:** integração **read-only via SQL direto** (não via API Linx). Já temos credenciais funcionando em outros projetos (`puket-app`, `portal-transportes`, `monitoria-unico`), e o servidor `n8n` tem rota IP até `db01.grupounico.com`.

---

## 2. Mapeamento campo-a-campo: Prova App ↔ DB_puket

### Relatório / Produto em desenvolvimento

| Prova App (`Relatorio`) | DB_puket | Observação |
|---|---|---|
| `descricao_geral` | `IMB_WF_PRODUTOS_DESENVOLVIMENTO.DESC_PRODUTO` ou `PRODUTOS.DESC_PRODUTO` | varchar(40) |
| `codigo` | `PRODUTOS.PRODUTO` | char(12) — código interno Puket |
| `colecao` | `PRODUTOS.COLECAO` + `PRT_EXP_PROD_COLECAO.DESC_COLECAO` | join por código |
| `temporada` | (derivado de `COLECAO`) | semântica: "VERAO 2026" |
| `ano` | (derivado de `COLECAO`) | parse manual |
| `linha` | `PRODUTOS.LINHA` ↔ `PRODUTOS_LINHAS` | 20 linhas (PRAIA, ACESSORIO, etc.) |
| **(novo)** | `IMB_WF_PRODUTOS_DESENVOLVIMENTO.SEXO` (1=masc, 2=fem) | poderia popular Categoria |
| **(novo)** | `IMB_WF_PRODUTOS_DESENVOLVIMENTO.FACCAO` | indica se é facção (terceirizado) |

**Tabela de ouro:** `IMB_WF_PRODUTOS_DESENVOLVIMENTO` — workflow de desenvolvimento de produtos. 19.420 linhas. Modelo conceitual idêntico ao nosso `Relatorio`. Provavelmente é onde Alice e o setor já registram produtos hoje.

### Referência

| Prova App (`Referencia`) | DB_puket | Observação |
|---|---|---|
| `numero_ref` | `PRODUTOS.PRODUTO` ou `PRODUTOS.REFER_FABRICANTE` | char(12) ou varchar(25) |
| `tipo_categoria` | `PRODUTOS.LINHA` + `IMB_WF_PRODUTOS_DESENVOLVIMENTO.SEXO` | mapear baby/kids/teen/adulto |
| `materia_prima` | `PRODUTOS_FORNECEDOR.DESC_PRODUTO_FORNECEDOR` ou `MATERIAIS_FORNECEDOR` | |
| `composicao` | `PRODUTO_VERSAO_MATERIAL` (492k linhas) | composição detalhada |
| `gramatura` | `PRODUTOS.PESO` | numeric |
| `fornecedor_id` (FK) | `PRODUTOS_FORNECEDOR.FORNECEDOR` ou `PRODUTOS.FABRICANTE` | varchar(25) |
| `codigo_referencia` | `PRODUTOS.REFER_FABRICANTE` | código do fornecedor |

### Fornecedor

| Prova App (`Fornecedor`) | DB_puket (`FORNECEDORES`) | Observação |
|---|---|---|
| `nome` | `FORNECEDOR` | varchar(25) — nome interno |
| `cnpj` | `CGC_CPF` | varchar(19) com máscara |
| `contato` | (não direto) | precisa join com `CLIFOR_CONTATOS` |
| `pais` | (derivado de endereço fiscal) | requer query adicional em `CLIFOR_ENDERECOS` |
| **(novo)** | `TIPO` + `SUBTIPO_FORNECEDOR` | classificação |
| **(novo)** | `BENEFICIADOR` (bit) | indica facção |
| **(novo)** | `INATIVO` (bit) | filtrar = 0 |
| **(novo)** | `LICENCIADO` (smallint) | tem licença de marca? |

### Tabela de medidas

| Prova App (`Prova.tabela_medidas_path`) | DB_puket | Observação |
|---|---|---|
| (arquivo PDF/imagem) | `PRODUTOS_TAB_MEDIDAS.FOTO_DIANTEIRO` + `FOTO_TRASEIRO` | varchar(100) — caminho da foto |
| (medidas estruturadas) | `PRODUTOS_TAB_MEDIDAS.OBS` (text) | conteúdo textual |
| **(novo)** | `TABELA_MEDIDAS` (varchar 25) | código da tabela aplicada |
| **(novo)** | `TAMANHO_BASE` | tamanho de referência |

**Importante:** A `PRODUTOS_TAB_MEDIDAS` tem 5.875 linhas — significa que existe um catálogo grande de tabelas de medidas reutilizáveis. Isso é OURO para autopreenchimento no Prova App.

---

## 3. Estratégia de integração recomendada

### Direção: Linx → Prova App (uni-direcional, read-only)

**Por quê:**
- Risco zero de corromper dados de produção (ERP da empresa)
- Setor de modelagem da Alice nunca vai querer escrever direto no ERP
- Pipeline natural: marketing/produto cria SKU no Linx → setor de modelagem puxa no Prova App para fazer suas provas

### Casos de uso prioritários

1. **Autocomplete de Fornecedor** (alto valor, baixo risco)
   - Quando Alice clica em "Novo Fornecedor", pode buscar de `FORNECEDORES` para evitar redigitação
   - Já existe endpoint `/fornecedor/api/buscar` interno — adicionar um botão "Buscar no ERP" que consulta `db_puket`
   - **Esforço: 1-2 dias**

2. **Autocomplete de Referência/Produto** (alto valor)
   - Quando criando um novo Relatorio, o campo `Referência` poderia auto-sugerir produtos de `PRODUTOS` ou `IMB_WF_PRODUTOS_DESENVOLVIMENTO`
   - Ao selecionar, pré-popula: descricao, coleção, linha, fornecedor, matéria-prima
   - **Esforço: 2-3 dias**

3. **Importar tabela de medidas pronta** (médio valor)
   - Botão "Importar do ERP" na seção tabela de medidas
   - Lê `PRODUTOS_TAB_MEDIDAS` filtrando pelo `GRUPO_PRODUTO` e mostra opções
   - **Esforço: 2 dias**

4. **Lista de coleções/temporadas vivas** (baixo valor)
   - Dropdown de coleção populado de `PRT_EXP_PROD_COLECAO` ao invés de digitação livre
   - **Esforço: 1 dia**

5. **Espelhar `IMB_WF_PRODUTOS_DESENVOLVIMENTO`** (alto valor mas custo alto)
   - Sincronizar diariamente os novos itens em desenvolvimento como Relatórios pendentes no Prova App
   - **Esforço: 5-7 dias** (precisa lógica de matching, dedupe, conflict resolution)

### Arquitetura técnica

```
┌─────────────────────────┐                ┌──────────────────────┐
│  Prova App (Flask)      │                │  DB_puket (MSSQL)    │
│  SQLite local           │                │  db01.grupounico.com │
│                         │                │                      │
│  ┌──────────────────┐   │                │  ┌────────────────┐  │
│  │ linx_client.py   │───┼──── pyodbc ───>│  │ FORNECEDORES   │  │
│  │                  │   │   read-only    │  │ PRODUTOS       │  │
│  │ - buscar_fornec  │   │                │  │ PRODUTOS_TAB_  │  │
│  │ - buscar_produto │   │                │  │   MEDIDAS      │  │
│  │ - listar_colecoes│   │                │  │ ...            │  │
│  └──────────────────┘   │                │  └────────────────┘  │
└─────────────────────────┘                └──────────────────────┘
```

**Componentes a adicionar:**

1. **`linx_client.py`** — módulo com funções de busca read-only
2. **Variáveis de ambiente** no `.env`:
   ```
   LINX_DB_HOST=db01.grupounico.com
   LINX_DB_PORT=1433
   LINX_DB_NAME=db_puket
   LINX_DB_USER=nicolas.matsuda
   LINX_DB_PASSWORD=*** (via Vault)
   ```
3. **Dependência**: `pymssql` ou `pyodbc` (já em `requirements.txt`)
4. **Endpoints REST internos** que consomem o linx_client:
   - `GET /api/linx/fornecedores?q=...`
   - `GET /api/linx/produtos?q=...`
   - `GET /api/linx/tabelas-medidas?grupo=...`
5. **JS no front-end** que chama esses endpoints (autocomplete style)
6. **Cache curto** (Redis ou in-memory com TTL de 1h) — as tabelas de catalog são estáveis, não precisam consultar a cada keystroke

### Considerações de segurança

- **Credencial guardada em Vault** (`vault-central` já roda no servidor `n8n`), não em `.env` versionado
- **Conexão dedicada read-only** se possível (pedir DBA criar role `prova_app_reader`)
- **Timeout agressivo** (5s) — se db_puket cair, Prova App continua funcionando sem o autocomplete
- **Rate limit** nos endpoints `/api/linx/*` para não saturar db_puket

### Considerações de performance

- A `PRODUTOS` tem 58.858 linhas (ok para LIKE % com índice em `DESC_PRODUTO`)
- A `FORNECEDORES` tem 21.408 (ok)
- A `PRODUTOS_TAB_MEDIDAS` tem 5.875 (ok)
- **NÃO usar** tabelas com >1M linhas (LOG_*, PortalEstoquesLojasDia, etc.) — fora do escopo
- Adicionar `WITH (NOLOCK)` nas queries para evitar locks em prod

---

## 4. POC mínima (2 dias)

Antes de prometer integração completa, fazer POC:

```python
# linx_client.py
import pyodbc
from config import Config

def _get_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={Config.LINX_DB_HOST},{Config.LINX_DB_PORT};"
        f"DATABASE={Config.LINX_DB_NAME};"
        f"UID={Config.LINX_DB_USER};"
        f"PWD={Config.LINX_DB_PASSWORD};"
        f"TrustServerCertificate=yes;"
        f"Connection Timeout=5;"
    )
    return pyodbc.connect(conn_str)

def buscar_fornecedores(q, limit=10):
    with _get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT TOP (?) FORNECEDOR, COD_FORNECEDOR, CGC_CPF, TIPO,
                   CASE WHEN BENEFICIADOR=1 THEN 'Facção' ELSE 'Fornecedor' END as tipo_completo
            FROM FORNECEDORES WITH (NOLOCK)
            WHERE INATIVO = 0
              AND (FORNECEDOR LIKE ? OR CGC_CPF LIKE ?)
            ORDER BY FORNECEDOR
        """, limit, f'%{q}%', f'%{q}%')
        return [
            {
                'nome': r[0].strip(),
                'codigo': r[1].strip(),
                'cnpj': r[2].strip() if r[2] else '',
                'tipo': r[3],
                'tipo_completo': r[4],
            }
            for r in cur
        ]
```

**Critério de sucesso da POC:**
1. Endpoint `/api/linx/fornecedores?q=PUKET` retorna lista em <500ms
2. Funciona via Docker no servidor `n8n` (db01 alcançável)
3. Não trava se db01 estiver lento (timeout 5s)

---

## 5. Próximos passos sugeridos

1. **Decisão com Alice:** quais dos 5 casos de uso priorizar? (recomendo #1 e #2 — autocomplete de fornecedor e referência)
2. **DBA do Linx/db_puket:** pedir role read-only dedicada `prova_app_reader` em vez de usar `nicolas.matsuda`
3. **Vault:** mover credencial para Vault e expor via env injetado no container
4. **POC (2 dias)** — entregar autocomplete de fornecedor funcionando
5. **Iteração** baseada em uso real antes de prometer casos de uso adicionais
6. **Documentação técnica final** após POC, com benchmark de queries em produção

---

## 6. O que NÃO fazer

❌ **Escrever em `db_puket`** — sem consenso com TI, isso é destrutivo. Manter integração read-only por enquanto.

❌ **Sincronizar via job batch noturno copiando tudo** — tentador mas cria duplicação de dados e problemas de consistência. Preferir read-on-demand com cache.

❌ **Usar API Linx Microvix** quando temos acesso direto ao SQL — desnecessariamente complexo. A API faz sentido se quisermos integrar com lojas que NÃO são Puket (Imaginarium, Tex, etc.).

❌ **Mapear tabelas operacionais (`LOG_*`, `PKT_*`, `LOJA_VENDA_*`)** — fora do escopo, são gigantes e instáveis.

❌ **Hardcodar credenciais** — qualquer credencial vai pro Vault.

---

## Anexo A — Inventário das 10 tabelas-chave

| Tabela | Linhas | Uso |
|---|---|---|
| `PRODUTOS` | 58.858 | Catalog principal de SKUs |
| `FORNECEDORES` | 21.408 | Cadastro mestre |
| `IMB_WF_PRODUTOS_DESENVOLVIMENTO` | 19.420 | Pipeline de novos produtos (★) |
| `MATERIAIS_FORNECEDOR` | 9.849 | Materiais por fornecedor |
| `PRODUTOS_TAB_MEDIDAS` | 5.875 | Catálogo de tabelas de medidas (★) |
| `PRODUTOS_GRUPO` | 231 | Grupos (camiseta, calça, etc.) |
| `PRODUTOS_CATEGORIA` | 96 | Categorias |
| `PRT_EXP_PROD_COLECAO` | 125 | Coleções nomeadas |
| `PRODUTOS_REF_FORNECEDOR` | 122 | Códigos do fornecedor |
| `PRODUTOS_LINHAS` | 20 | Linhas (PRAIA, ACESSORIO, etc.) |

(★) = mais relevantes para o Prova App

---

**Status:** análise concluída. Pronto para POC quando Alice priorizar.
