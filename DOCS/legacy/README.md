# 📦 Documentação Legada

Este diretório contém documentação antiga do projeto que foi consolidada em 16/01/2026.

## ℹ️ O Que É Este Diretório?

Durante a reorganização da documentação do projeto, encontramos **58 arquivos .md duplicados** na raiz do repositório. Estes arquivos continham informações que foram:

1. **Consolidadas** em `DOCS/` com estrutura organizada
2. **Atualizadas** com informações corretas
3. **Reformatadas** seguindo padrões consistentes

## 📁 Conteúdo

Arquivos movidos (total: **58 arquivos**, ~500KB):

- `ARQUITETURA_*.md` → Consolidado em `DOCS/architecture/`
- `DEPLOY_*.md` → Consolidado em `DOCS/deploy/`
- `DESIGN_*.md` → Consolidado em `DOCS/design/`
- `DOCS_*.md`, `INDEX_*.md` → Consolidado em `DOCS/INDEX.md`
- `*_GUIDE.md`, `*_CHECKLIST.md` → Consolidado em `DOCS/guides/`
- Diversos outros arquivos de documentação antiga

## ✅ Documentação Atual

**Use sempre a documentação em `DOCS/`**, que está:

- ✅ Organizada por categorias
- ✅ Atualizada e validada (Jan 2026)
- ✅ Alinhada com o código real
- ✅ Com exemplos testados
- ✅ Versionada e datada

**Índice da documentação atual:**
👉 **[DOCS/INDEX.md](../INDEX.md)**

## ⚠️ Avisos Importantes

1. **Não usar estes arquivos legados** - podem conter informações desatualizadas
2. **Manter apenas para histórico** - caso precise consultar versões antigas
3. **Não criar novos arquivos aqui** - usar estrutura em `DOCS/`

## 🗑️ Limpeza Futura

Estes arquivos podem ser **deletados com segurança** após:
- [ ] Validação de que toda informação útil foi migrada
- [ ] Período de transição de 30 dias (até 15/02/2026)
- [ ] Confirmação da equipe

**Para deletar:**
```bash
# Após validação
rm -rf DOCS/legacy/
```

## 📋 Histórico

| Data | Ação | Arquivos | Responsável |
|------|------|----------|-------------|
| 16/01/2026 | Movidos para legacy/ | 58 | Claude (Sonnet 4.5) |
| - | Consolidação em DOCS/ | 14 | Claude (Sonnet 4.5) |
| - | Validação e limpeza | - | Pendente |

## 📞 Dúvidas?

Se precisar de informações que estavam nestes arquivos antigos:
1. Verifique primeiro em `DOCS/`
2. Busque no histórico do Git: `git log --all --full-history -- DOCS/legacy/`
3. Contate: nicolas.matsuda@grupounico.com

---

**[⬅ Voltar para DOCS](../)**
