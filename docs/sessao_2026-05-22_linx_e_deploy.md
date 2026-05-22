# Sessão 22/05/2026 — Integração Linx, Deploy e Limpeza de Segurança

**Status:** ✅ Tudo deployado e validado em produção.
**Commits:** `922919c` → `482337f` → `6f7737e` (todos em `origin/main`).
**Container em prod:** `prova_modelagem_app` (servidor n8n, 192.168.168.124) — healthy.

---

## 1. Entregas — 11 itens da reunião 04/05/2026 com Alice/Nicolas

| # | Pedido da Alice | Implementação | Local |
|---|---|---|---|
| 1 | Anexar vários produtos de uma vez | Tela de seleção múltipla com checkbox + batch import | `templates/linx_anexar_produtos.html`, `linx_bp.py` |
| 2 | "Importar para o Excel" | Export já existia (`/exportar/excel`, `/relatorio/<id>/excel`) | `excel_export.py` |
| 3 | Fotos no kanban | Foto destaque renderizada nos cards | `kanban_bp.py:_foto_destaque`, `templates/kanban.html` |
| 4 | Round-trip Excel (exportar → editar → reimportar) | Fluxo upload → revisar → confirmar via `ImportJob` | `app.py` rotas `/importar/excel/*` |
| 5 | Campo país em fornecedores | Coluna `pais` em `fornecedores` + UI | `models.py`, `fornecedor_bp.py` |
| 6 | Integração com Linx | Cliente read-only ao `db_puket` em `db01.grupounico.com:1433` (SQL Server) | `linx_client.py`, `linx_bp.py` |
| 7 | Testes de qualidade | Checklist dinâmico (templates + respostas) | `checklist_bp.py`, `models.py` |
| 8 | Acesso para Cori | Tarefa administrativa (criar usuário) — fora de código | `/admin/users` |
| 9 | Site em inglês | Flask-Babel, locale switcher, .po/.mo gerados | `babel.cfg`, `translations/en/` |
| 10 | Link público read-only pra fornecedor | Token + expiração + permissões de download | `publico_bp.py`, modelo `LinkPublico` |
| 11 | Aba de manuais | Upload + categorias + download | `manuais_bp.py`, modelo `Manual` |

---

## 2. Integração Linx (item 6 + 1)

### Arquitetura
- **`linx_client.py`** — pyodbc, cache TTL 1h, timeout 5s, fallback gracioso (retorna `[]`/`None` se ERP off).
- **`linx_bp.py`** — Flask blueprint em `/linx`, 11 rotas:
  - `GET /linx/` (painel admin com status)
  - `GET /linx/status` (JSON do ping)
  - `POST /linx/cache/limpar`
  - `GET /linx/api/fornecedores?q=...` (autocomplete)
  - `GET /linx/api/fornecedores/<codigo>`
  - `GET /linx/api/produtos?q=...&colecao=...`
  - `GET /linx/api/produtos/<codigo>`
  - `GET /linx/api/colecoes`
  - `POST /linx/importar-fornecedor`
  - `GET /linx/anexar-produtos/<relatorio_id>`
  - `POST /linx/anexar-produtos/<relatorio_id>` (batch — máx. 100 produtos)
- **UI:** botões "Buscar no ERP" em `fornecedor_form.html` (autocomplete debounced 250ms), "Anexar produtos do ERP" em `detalhes_relatorio.html`, item "ERP Linx" na sidebar admin.
- **i18n:** todas as strings dos templates Linx envelopadas em `{{ _() }}`.

### Tabelas do `db_puket` usadas (read-only, `WITH (NOLOCK)`)
- `FORNECEDORES` — busca + detalhes
- `PRODUTOS` + `IMB_WF_PRODUTOS_DESENVOLVIMENTO` (left join opcional)
- `PRT_EXP_PROD_COLECAO` — coleções
- `PRODUTOS_LINHAS` — linhas

### Hardening profissional aplicado
- **Sanitização de logs:** regex robusta cobre `PWD=val`, `PWD={val}`, `PWD="val"`, `PWD='val'` (`linx_client._sanitize`). Erro do driver nunca expõe senha.
- **Escape SQL wildcards:** `_escape_like` neutraliza `%`, `_`, `[` no termo de busca antes de virar `LIKE %...%`.
- **Rollback transacional:** batch import envolto em `try/except SQLAlchemyError` com `db.session.rollback()` + flash de erro. Zero importação parcial.
- **Limite anti-abuso:** `ANEXAR_BATCH_MAX = 100`.
- **Dedup de códigos** via `dict.fromkeys` antes de processar.
- **`IntegrityError` handling** em criação de fornecedor (concorrência).
- **Audit log:** ações `IMPORT_LINX` e `IMPORT_LINX_BATCH` registradas via `app.registrar_log` (lazy import pra evitar ciclo).
- **Heurística de categoria** (`_mapear_categoria`): determinística, word-boundary, olha descrição+linha+sexo. MAIO BABY FOCA → `baby`.

### Erratas de schema descobertas em campo (vs `docs/linx_db_puket_analysis.md` inicial)
- `PRT_EXP_PROD_COLECAO.COLECAO` → `COD_PRODUTO_COLECAO`
- `PRT_EXP_PROD_COLECAO.COD_IDIOMA`: só `2` (EN) e `3` (ES), agregamos via `GROUP BY`
- `PRODUTOS_LINHAS.DESC_LINHA` não existe → use `LINHA` (texto) + `COD_LINHA` (código)

---

## 3. Vault de credenciais (`secrets/`)

```
secrets/
├── README.md          (versionado, explica o esquema)
├── .gitkeep           (mantém diretório)
└── linx.env           (chmod 600, GITIGNORED)
```

- `.gitignore` linha 28: `secrets/*` + exceções `README.md` e `.gitkeep`
- `config.py` carrega automaticamente qualquer `secrets/*.env` em boot com `override=True`
- Container vê secrets via bind mount `./secrets:/app/secrets:ro` no `docker-compose.sqlite.yml`
- Em prod: vault provisionado manualmente via scp (não vem por git pull)

Para adicionar credencial nova: criar `secrets/<nome>.env`, chmod 600, referenciar via `os.getenv()`/`Config.X`. Nunca hardcoded, nunca em `.env` versionado.

---

## 4. Infra atualizada (Dockerfile)

- Adicionado `unixodbc-dev` (build) e `unixodbc` + `msodbcsql18` (runtime) via repositório oficial da Microsoft (`packages.microsoft.com`), usando `gpg --dearmor` (sem `apt-key` deprecated).
- Sem isso, `pyodbc` não consegue conectar no SQL Server.

---

## 5. Limpeza de credenciais (commit `6f7737e`)

5 senhas/secrets reais estavam em texto plano no repo desde janeiro/2026:
1. Senha SSH `nicolas`
2. `ADMIN_PASSWORD` do app (`Space1234` e variação `!@#$Space1234`)
3. `SECRET_KEY` do Flask (hash hex 64 chars)
4. `admin123` em scripts e docs
5. Senha do `db_puket` — **NUNCA** estava no repo (só local em `secrets/linx.env`)

### Arquivos deletados (eram só credenciais)
- `DOCS/legacy/ACESSO_ADMIN.md`
- `DOCS/legacy/COMANDOS_PESQUISA.md` (28 ocorrências de `sshpass -p '...'`)
- `DOCS/legacy/SERVIDOR_PRODUCAO.md` (duplicata)

### Arquivos editados (preserva valor técnico)
- `DOCS/deploy/SERVIDOR_ATUAL.md` — redact + header avisando vault
- `DOCS/legacy/IMPLEMENTACAO_COMPLETA.md`
- `DOCS/architecture/BACKEND.md` + `DOCS/legacy/ARQUITETURA_BACKEND.md` — exemplo de código usa `os.environ['ADMIN_PASSWORD']`
- `DOCS/deploy/PRODUCAO.md` — remove fallback hardcoded

### Scripts/código refatorados
- `scripts/database/migrate_db.py` — exige `ADMIN_RESET_PASSWORD` via env, senha nunca em log
- `app.py` (CLI `create-admin`) — exige `ADMIN_PASSWORD` via env, validação ≥8 chars

### Pendência (decisão do usuário)
- Senhas no histórico git (commits anteriores a `6f7737e`) **continuam visíveis**.
- Usuário escolheu NÃO rotacionar (custo > benefício no contexto interno).
- Mitigação real seria: `passwd` SSH + nova `SECRET_KEY` + reset admin com `flask create-admin`. Documentado mas adiado.

---

## 6. Deploy executado (validado)

**Procedimento usado:**
1. Chave SSH `id_ed25519` autorizada via `ssh-copy-id` (sem mais senha)
2. Baseline do DB capturado via container: MD5 `aa41e12306e116b248838433fc61f8bd`, 749 registros
3. Backup via `docker compose exec -T app cp /app/data/provas.db /app/data/provas.db.pre_linx_20260522_151700`
4. `git pull origin main` no servidor (922919c → 482337f → 6f7737e)
5. Vault `secrets/linx.env` provisionado via scp + chmod 600
6. `docker compose -f docker-compose.sqlite.yml up -d --build` (rebuild com `msodbcsql18`)
7. Aguardo healthcheck 30s
8. Validação pós-deploy: MD5 idêntico, 749 registros, Linx ping 197ms, HTTP 302 OK

**Dados preservados (12 → 12 usuários, 136 → 136 relatórios, 169 → 169 referências, 168 → 168 provas, 238 → 238 fotos, 1 → 1 fornecedor, 3 → 3 checklist templates, 22 → 22 audit logs). MD5 idêntico = zero byte escrito.**

---

## 7. Como rodar testes manuais em prod

```bash
# Status do Linx
ssh nicolas@192.168.168.124 'docker compose -f ~/prova_modelagem_app/docker-compose.sqlite.yml exec -T app python -c "import linx_client; print(linx_client.ping())"'

# Busca real de fornecedores
ssh nicolas@192.168.168.124 'docker compose -f ~/prova_modelagem_app/docker-compose.sqlite.yml exec -T app python -c "import linx_client; r = linx_client.buscar_fornecedores(\"PUKET\"); print(len(r), r[:2])"'

# Validar integridade do DB
ssh nicolas@192.168.168.124 'docker compose -f ~/prova_modelagem_app/docker-compose.sqlite.yml exec -T app python -c "import sqlite3; conn=sqlite3.connect(\"/app/data/provas.db\"); print(conn.execute(\"PRAGMA integrity_check\").fetchone())"'

# Smoke HTTP
curl -sI http://192.168.168.124:5000/
```

---

## 8. Próximos passos sugeridos (não cobrado nesta sessão)

- [ ] (Opcional) Rotacionar senhas que vazaram no git history
- [ ] Calibrar com Alice o mapeamento de categoria (baby/kids/teen/adulto) — heurística atual é "best guess"
- [ ] Pre-commit hook que rejeita strings tipo `password=`/`secret_key=` com valores não-placeholder em arquivos `.env*` fora de `secrets/`
- [ ] Documentar fluxo "Anexar produtos do ERP" para a Alice + setor (manual de uso)

---

*Este documento foi gerado em 22/05/2026 ao final da sessão de implementação Linx + deploy.*
