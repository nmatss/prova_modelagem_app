# Vault local — `secrets/`

Diretório isolado para credenciais sensíveis (Linx, futuras integrações).

## Como funciona

- O `config.py` carrega automaticamente **qualquer** arquivo `secrets/*.env`
  com `override=True`. Assim os segredos sobrescrevem defaults do `.env`.
- O conteúdo deste diretório **não vai pro git** (ver `.gitignore`:
  `secrets/*`, com exceção deste README e `.gitkeep`).
- Permissões esperadas: diretório `chmod 700`, arquivos `chmod 600`.

## Layout

```
secrets/
├── README.md         (este arquivo — versionado, sem segredos)
├── .gitkeep          (mantém o diretório no git)
└── linx.env          (NUNCA commitar — credenciais Linx)
```

## Adicionar uma nova integração com segredo

1. Criar `secrets/<integracao>.env`:
   ```bash
   touch secrets/microvix.env
   chmod 600 secrets/microvix.env
   ```
2. Editar e preencher variáveis (`MICROVIX_API_KEY=...` etc.).
3. Pronto — o `config.py` carrega no próximo boot. Use `Config.MICROVIX_API_KEY`
   ou `os.getenv('MICROVIX_API_KEY')` no código.

## Rotação de senha (procedimento)

Se uma credencial vazar (ex: foi enviada em mensagem, log, screenshot):

1. Pedir ao DBA / admin da integração para gerar nova senha.
2. Atualizar `secrets/<integracao>.env` localmente.
3. Atualizar o cofre de produção (Docker secrets / systemd LoadCredential / vault-central).
4. Reiniciar containers afetados.
5. Confirmar funcionamento via endpoint de status (ex: `/linx/status`).

## Produção (NÃO copiar `secrets/*.env` daqui para o servidor)

Para produção, use um destes mecanismos em vez de arquivos `secrets/`:

**Opção A — Docker Compose secrets** (recomendado):
```yaml
services:
  app:
    secrets:
      - linx_env
    environment:
      ENV_FILE: /run/secrets/linx_env  # ou monte como secrets/linx.env

secrets:
  linx_env:
    file: /opt/secrets/linx.env  # arquivo no host com chmod 600
```

**Opção B — systemd LoadCredential** (bare-metal):
```ini
[Service]
LoadCredential=linx.env:/etc/secrets/linx.env
EnvironmentFile=%d/linx.env
```

**Opção C — vault-central** (já roda no servidor `n8n`):
- Buscar dinamicamente em runtime via API do Vault.
- Requer alterar `linx_client._get_connection()` para puxar a senha do Vault
  a cada chamada (com cache curto).

## Checklist de segurança

- [ ] Diretório `secrets/` com `chmod 700`
- [ ] Arquivos `secrets/*.env` com `chmod 600`
- [ ] `.gitignore` cobre `secrets/*` (mantém só README e .gitkeep)
- [ ] Nenhum segredo aparece em logs (`linx_client.py` mascara passwords no log)
- [ ] Endpoint `/linx/status` retorna `ok: true` em produção
- [ ] Senha rotacionada se algum dia foi exposta em chat/PR/screenshot
