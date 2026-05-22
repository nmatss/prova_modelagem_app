# Guia i18n (PT/EN)

Este projeto usa **Flask-Babel** para internacionalização. A fundação já está pronta com tradução starter da navegação. Este documento orienta como expandir para cobertura total.

## Estado atual

- **Idiomas suportados:** `pt` (padrão) e `en`
- **Coberto:** navegação lateral (sidebar) em `templates/base.html`, label de roles do usuário
- **Não coberto ainda:** dashboard, formulários, mensagens flash, modais, PDFs (~500-1000 strings restantes)

## Como o sistema escolhe o idioma

Ordem de precedência (definida em `app.py` na função `_get_locale`):

1. Query string `?lang=en` na URL (útil para link público de fornecedor estrangeiro) — também salva na sessão
2. `session['idioma']` (escolha temporária)
3. `current_user.idioma` (preferência salva no perfil do usuário, coluna `usuarios.idioma`)
4. Cabeçalho `Accept-Language` do navegador
5. Fallback: `pt`

## Como adicionar uma nova string traduzível

### Em templates Jinja
```jinja
{{ _('Texto a traduzir') }}
```

### Em código Python (mensagens flash, etc)
```python
from flask_babel import gettext as _
flash(_('Relatório salvo com sucesso'), 'success')
```

### Em código Python (string lazy — ex: defaults de coluna)
```python
from flask_babel import lazy_gettext as _l
class MeuForm(FlaskForm):
    nome = StringField(_l('Nome'))
```

## Workflow de extração e compilação

Após adicionar strings novas com `_('...')`:

```bash
# 1. Instalar Flask-Babel (uma vez)
pip install Flask-Babel

# 2. Extrair todas as strings marcadas para messages.pot
pybabel extract -F babel.cfg -k _l -o messages.pot .

# 3. Atualizar arquivos .po existentes com as strings novas
pybabel update -i messages.pot -d translations

# 4. Editar translations/en/LC_MESSAGES/messages.po — traduzir as strings novas

# 5. Compilar .po → .mo (Flask-Babel só lê .mo)
pybabel compile -d translations
```

## Workflow para primeiro setup (já feito neste projeto)

```bash
pybabel extract -F babel.cfg -k _l -o messages.pot .
pybabel init -i messages.pot -d translations -l pt
pybabel init -i messages.pot -d translations -l en
# Traduzir EN, depois:
pybabel compile -d translations
```

## Glossário de termos de domínio (acordado com o time)

Quando expandir as traduções, **manter consistência** com estes termos:

| Português | Inglês |
|---|---|
| Relatório | Report |
| Prova (peça de prova) | Fitting Sample |
| Modelagem | Pattern Making |
| Referência | Style / Reference |
| Coleção | Collection |
| Temporada | Season |
| Linha | Line |
| Fornecedor | Supplier |
| Categoria | Category |
| Tabela de medidas | Size chart |
| Lacre | Seal |
| Aprovada / Reprovada / Em Andamento / Comitê | Approved / Rejected / In Progress / Committee |
| Qualidade / Estilo / Modelagem | Quality / Style / Pattern |
| Aviamentos | Trims |
| Matéria-prima | Raw material |
| Manual | Manual |

**Termos sob revisão** (decidir com Alice antes de traduzir):
- "Prova" — `Fitting`, `Sample` ou `Try-on`? — depende do que faz mais sentido para fornecedores estrangeiros
- "Lacre" — `Seal` literal vs `Tag`/`Lock`

## Telas prioritárias para próxima expansão

Em ordem de impacto:

1. **`templates/dashboard.html`** — header, botões, KPIs, tabela
2. **`templates/login.html`** + auth screens — primeira impressão
3. **`templates/detalhes_relatorio.html`** — mais acessada
4. **`templates/editar_relatorio.html`** + `novo_relatorio.html` — formulários longos
5. **`templates/fornecedores.html`** + suporte
6. **`templates/kanban.html`**
7. **`templates/manuais.html`** + suporte
8. **`templates/publico/relatorio_view.html`** — IMPORTANTE para fornecedor estrangeiro
9. **Mensagens flash em `app.py`, blueprints**
10. **PDFs (`relatorio_pdf.html`)** — opcionalmente em inglês para fornecedor estrangeiro

## Como testar

1. Abra qualquer página do app
2. No menu lateral, mude o dropdown de idioma para `English`
3. A sidebar deve refletir os termos em inglês
4. Visite `/publico/<token>?lang=en` para testar o link público em inglês (não requer login)

## Fallback se Flask-Babel não estiver instalado

O código em `app.py` faz import com `try/except ImportError`. Se Flask-Babel não estiver instalado, `_()` vira função identidade (retorna a string original em português) e o site continua funcionando normalmente em PT. Isso permite que o deploy aconteça em fases:

1. Deploy com `requirements.txt` já com `Flask-Babel==4.0.0` mas sem rodar `pip install` ainda — site funciona em PT
2. Rebuild da imagem Docker (pip install pega Flask-Babel) → site passa a respeitar locale
3. `pybabel compile -d translations` antes do start (ou no entrypoint.sh) → traduções ficam ativas

## Limitações conhecidas

- Datas e números ainda usam formato fixo (dd/mm/yyyy). Para localizar, usar `format_datetime` do Flask-Babel
- PDFs gerados via WeasyPrint não respeitam locale automaticamente — o template precisa receber o locale como contexto explícito
- Strings em JS hardcoded (alerts, confirms) — futura migração para `window.translations` ou similar
