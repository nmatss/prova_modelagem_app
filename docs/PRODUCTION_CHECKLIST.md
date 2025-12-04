# ✅ Checklist de Produção

Use este checklist antes de fazer deploy em produção.

## 🔐 Segurança

- [ ] `SECRET_KEY` única gerada (não usar a padrão)
- [ ] `FLASK_DEBUG=False` no `.env.production`
- [ ] `FLASK_ENV=production` no `.env.production`
- [ ] Arquivo `.env.production` NÃO está no Git
- [ ] Senha do banco de dados é forte
- [ ] Usuários padrão foram removidos/senha alterada
- [ ] Firewall configurado (permitir apenas 80/443)
- [ ] Porta 8000 (Gunicorn) não está exposta externamente

## 🗄️ Banco de Dados

- [ ] PostgreSQL ou MySQL configurado (não usar SQLite)
- [ ] `DATABASE_URL` configurada corretamente
- [ ] Banco de dados criado
- [ ] Usuário do banco criado com permissões corretas
- [ ] Conexão testada
- [ ] Tabelas criadas (`migrate_to_postgres.py`)
- [ ] Usuário admin criado

## 🌐 Servidor Web

- [ ] Nginx instalado e configurado
- [ ] Arquivo `nginx.conf` copiado para `/etc/nginx/sites-available/`
- [ ] Link simbólico criado em `/etc/nginx/sites-enabled/`
- [ ] Caminhos no `nginx.conf` ajustados
- [ ] `server_name` configurado (domínio ou IP)
- [ ] `nginx -t` passou sem erros
- [ ] Nginx recarregado/reiniciado

## 🐍 Aplicação Python

- [ ] Virtual environment criado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Gunicorn instalado
- [ ] `wsgi.py` e `gunicorn_config.py` configurados
- [ ] Scripts `start.sh`, `stop.sh`, etc. têm permissão de execução
- [ ] Aplicação inicia sem erros (`./start.sh`)

## 📁 Diretórios e Permissões

- [ ] `/var/www/provas_app` criado
- [ ] `/var/log/provas_app` criado
- [ ] `/var/run/provas_app` criado (ou alternativo local)
- [ ] `uploads/` tem permissão 775
- [ ] `relatorios_pdf/` tem permissão 775
- [ ] `instance/` tem permissão 775
- [ ] Proprietário correto (ex: `provas:www-data`)

## 📝 Logs

- [ ] Diretório de logs criado
- [ ] `LOG_FILE` configurado no `.env.production`
- [ ] Logs estão sendo gerados
- [ ] Permissões de escrita corretas
- [ ] Rotação de logs configurada (opcional)

## 🔄 Systemd (Opcional)

- [ ] Arquivo `.service` copiado para `/etc/systemd/system/`
- [ ] Caminhos ajustados no arquivo `.service`
- [ ] `systemctl daemon-reload` executado
- [ ] Serviço habilitado (`systemctl enable`)
- [ ] Serviço inicia (`systemctl start`)
- [ ] Status OK (`systemctl status`)

## 🔒 SSL/HTTPS (Recomendado)

- [ ] Certificado SSL obtido (Let's Encrypt ou próprio)
- [ ] Configuração HTTPS no `nginx.conf` descomentada
- [ ] Caminhos dos certificados corretos
- [ ] Redirecionamento HTTP → HTTPS configurado
- [ ] HTTPS testado no navegador

## 🧪 Testes

- [ ] Aplicação acessível via navegador
- [ ] Login funciona
- [ ] Criar novo relatório funciona
- [ ] Upload de arquivos funciona
- [ ] Geração de PDF funciona
- [ ] Navegação entre páginas funciona
- [ ] Logs não mostram erros críticos

## 📊 Monitoramento

- [ ] Verificar status: `./status.sh`
- [ ] Logs da aplicação: `tail -f /var/log/provas_app/app.log`
- [ ] Logs do Nginx: `tail -f /var/log/nginx/provas_app_*.log`
- [ ] CPU e memória sob controle
- [ ] Espaço em disco suficiente

## 🔄 Backup (Planejamento)

- [ ] Estratégia de backup do banco definida
- [ ] Backup dos uploads planejado
- [ ] Teste de restauração realizado (recomendado)

## 📚 Documentação

- [ ] README.md atualizado
- [ ] DEPLOY.md revisado
- [ ] Credenciais documentadas em local seguro
- [ ] IPs/domínios documentados
- [ ] Procedimentos de manutenção documentados

## 🎯 Pós-Deploy

- [ ] Informar usuários sobre URL de acesso
- [ ] Fornecer credenciais iniciais
- [ ] Agendar revisão após 24h
- [ ] Monitorar logs por 48h

---

## 🚨 Itens Críticos (Não Pular!)

1. ✅ SECRET_KEY única
2. ✅ DEBUG=False
3. ✅ PostgreSQL/MySQL (não SQLite)
4. ✅ Nginx configurado
5. ✅ Aplicação iniciando sem erros
6. ✅ Login funcionando
7. ✅ Logs sendo gerados

---

**Data do Deploy:** ___/___/______
**Responsável:** _________________
**Versão:** _____________________
