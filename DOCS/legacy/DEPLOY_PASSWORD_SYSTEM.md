# 🔐 Guia de Deploy - Sistema de Redefinição de Senha

Este documento descreve como atualizar o sistema em produção com o novo recurso de redefinição de senha.

## 📋 Visão Geral das Mudanças

### Novos Recursos Implementados:

1. ✅ **Alteração de Senha pelo Usuário**
   - Rota: `/alterar-senha`
   - Usuários logados podem alterar sua própria senha
   - Validações de senha atual, nova senha e confirmação

2. ✅ **Esqueci Minha Senha**
   - Rota: `/esqueci-senha`
   - Gera token de recuperação de senha
   - Token válido por 24 horas

3. ✅ **Reset de Senha com Token**
   - Rota: `/reset-senha/<token>`
   - Permite redefinir senha usando token válido

4. ✅ **Reset de Senha pelo Admin**
   - Já existente na área administrativa
   - Rota: `/admin/users/reset_password/<user_id>`

### Mudanças no Banco de Dados:

Foram adicionadas 2 novas colunas na tabela `usuarios`:
- `reset_token` (VARCHAR(100))
- `reset_token_expires` (DATETIME)

---

## 🚀 Passo a Passo para Deploy

### 1. **Backup do Banco de Dados**

```bash
# Faça backup do banco de dados atual
cp data/provas.db data/provas.db.backup_$(date +%Y%m%d_%H%M%S)
```

### 2. **Atualizar Código no Servidor**

```bash
# No servidor de produção
cd /caminho/do/seu/projeto
git pull origin main
# OU faça upload manual dos arquivos via FTP/SFTP
```

### 3. **Executar Migração do Banco de Dados**

```bash
# Execute o script de migração
python3 migrate_db.py
```

**Saída esperada:**
```
======================================================================
   MIGRAÇÃO DO BANCO DE DADOS - SISTEMA DE RESET DE SENHA
======================================================================

🔧 Iniciando migração do banco de dados...
   Arquivo: data/provas.db
   Data: 2026-01-16 13:58:36

✅ Backup criado: data/provas.db.backup_20260116_135836
✅ Coluna 'reset_token' adicionada
✅ Coluna 'reset_token_expires' adicionada

✅ Migração concluída com sucesso!
✅ MIGRAÇÃO CONCLUÍDA E VERIFICADA COM SUCESSO!
```

### 4. **Reiniciar a Aplicação**

```bash
# Se estiver usando systemd
sudo systemctl restart prova_modelagem

# Ou se estiver usando gunicorn manualmente
pkill gunicorn
gunicorn -c gunicorn_config.py app:app

# Ou se estiver usando supervisor
sudo supervisorctl restart prova_modelagem
```

### 5. **Verificar Logs**

```bash
# Verificar se a aplicação iniciou corretamente
tail -f logs/app.log

# Verificar logs do servidor web
tail -f /var/log/nginx/error.log  # Se estiver usando Nginx
```

---

## ✅ Checklist de Testes Pós-Deploy

Após o deploy, teste as seguintes funcionalidades:

### Teste 1: Alteração de Senha (Usuário Logado)
- [ ] Login no sistema
- [ ] Acessar menu do usuário → "Alterar Senha"
- [ ] Tentar alterar senha com senha atual incorreta (deve falhar)
- [ ] Alterar senha corretamente
- [ ] Fazer logout e login com a nova senha

### Teste 2: Esqueci Minha Senha
- [ ] Na tela de login, clicar em "Esqueci minha senha"
- [ ] Preencher usuário e email
- [ ] Verificar se token foi gerado (aparecerá na mensagem)
- [ ] **Nota:** Em desenvolvimento o token aparece na tela. Em produção, configure email para envio automático.

### Teste 3: Reset de Senha com Token
- [ ] Acessar `/reset-senha/<token>` com um token válido
- [ ] Definir nova senha
- [ ] Fazer login com a nova senha

### Teste 4: Reset pelo Admin
- [ ] Login como administrador
- [ ] Acessar "Admin" → "Usuários"
- [ ] Resetar senha de um usuário
- [ ] Verificar se a nova senha funciona

### Teste 5: Validações
- [ ] Tentar usar senha com menos de 6 caracteres (deve falhar)
- [ ] Tentar usar token expirado ou inválido (deve falhar)
- [ ] Verificar se mensagens de erro são claras

---

## 📝 Arquivos Modificados

```
✏️  Modificados:
├── models.py                         # Adicionadas colunas reset_token e reset_token_expires
├── auth.py                           # Novas rotas de alteração e reset de senha
├── templates/base.html               # Link "Alterar Senha" no menu do usuário
└── templates/login.html              # Link "Esqueci minha senha"

📄 Novos:
├── templates/alterar_senha.html      # Página de alteração de senha
├── templates/esqueci_senha.html      # Página "esqueci minha senha"
├── templates/reset_senha.html        # Página de reset com token
├── migrate_db.py                     # Script de migração do banco
└── DEPLOY_PASSWORD_SYSTEM.md         # Esta documentação
```

---

## 🔒 Segurança

### Configurações Importantes:

1. **Tokens de Reset:**
   - Tokens são gerados com `secrets.token_urlsafe(32)` (criptograficamente seguros)
   - Validade: 24 horas
   - Tokens são invalidados após o uso

2. **Senhas:**
   - Hash usando `werkzeug.security.generate_password_hash`
   - Mínimo 6 caracteres (pode aumentar se necessário)
   - Senhas nunca são armazenadas em texto plano

3. **Validações:**
   - Senha atual é verificada antes de permitir alteração
   - Nova senha deve corresponder à confirmação
   - Token é validado antes de permitir reset

### Recomendações de Segurança:

- [ ] Configure HTTPS em produção
- [ ] Configure rate limiting para evitar ataques de força bruta
- [ ] Configure envio de email para tokens de reset (atualmente apenas exibe na tela)
- [ ] Monitore tentativas de login falhadas
- [ ] Considere implementar autenticação de dois fatores (2FA)

---

## 📧 Configurar Envio de Email (Opcional - Recomendado para Produção)

Para produção, é recomendado configurar envio de email para os tokens de reset:

### 1. Instalar Flask-Mail:

```bash
pip install Flask-Mail
```

### 2. Configurar em `config.py`:

```python
MAIL_SERVER = 'smtp.gmail.com'  # Ou seu servidor SMTP
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'seu-email@exemplo.com'
MAIL_PASSWORD = 'sua-senha-app'
MAIL_DEFAULT_SENDER = 'noreply@seudominio.com'
```

### 3. Atualizar `auth.py` na função `esqueci_senha`:

```python
from flask_mail import Mail, Message

mail = Mail(app)

# Substituir a linha que mostra o token por:
reset_url = url_for('auth.reset_senha', token=token, _external=True)

msg = Message(
    'Recuperação de Senha - Sistema de Provas',
    recipients=[user.email]
)
msg.body = f'''
Olá {user.username},

Você solicitou a recuperação de senha.

Clique no link abaixo para redefinir sua senha:
{reset_url}

Este link é válido por 24 horas.

Se você não solicitou esta alteração, ignore este email.

Atenciosamente,
Equipe do Sistema
'''
mail.send(msg)

flash('Instruções de recuperação enviadas para seu email!', 'success')
```

---

## 🐛 Solução de Problemas

### Problema: Migração falha

**Solução:**
```bash
# Verificar permissões do banco de dados
ls -la data/provas.db

# Dar permissão se necessário
chmod 664 data/provas.db

# Executar migração novamente
python3 migrate_db.py
```

### Problema: Erro 500 ao acessar /alterar-senha

**Solução:**
```bash
# Verificar logs
tail -f logs/app.log

# Verificar se migração foi executada
python3 migrate_db.py

# Reiniciar aplicação
sudo systemctl restart prova_modelagem
```

### Problema: Link "Alterar Senha" não aparece no menu

**Solução:**
- Limpar cache do navegador (Ctrl+Shift+R)
- Verificar se templates foram atualizados
- Reiniciar aplicação

---

## 📞 Suporte

Se encontrar problemas durante o deploy:

1. Verifique os logs: `tail -f logs/app.log`
2. Verifique se a migração foi concluída com sucesso
3. Restaure o backup se necessário: `cp data/provas.db.backup_* data/provas.db`
4. Entre em contato com o desenvolvedor

---

## ✨ Funcionalidades Futuras (Opcionais)

- [ ] Histórico de alterações de senha
- [ ] Política de senha forte (maiúsculas, números, caracteres especiais)
- [ ] Expiração de senha obrigatória a cada X dias
- [ ] Autenticação de dois fatores (2FA)
- [ ] Login social (Google, Microsoft)
- [ ] Bloqueio de conta após X tentativas falhadas

---

**Data da Documentação:** 16/01/2026
**Versão do Sistema:** 2.0 (com sistema de redefinição de senha)
**Compatibilidade:** SQLite (local) e PostgreSQL (produção com adaptação)
