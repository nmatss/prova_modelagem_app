# 🚀 Acesso para Homologação - Sistema de Provas

**Status:** ✅ Sistema rodando e acessível na rede local

---

## 📍 Endereços de Acesso

### 1. **Acesso Local (nesta máquina)**
```
http://127.0.0.1:5000
http://localhost:5000
```

### 2. **Acesso na Rede Local (outros computadores)**
```
http://172.28.225.112:5000
```

**Compartilhe este endereço com os usuários para homologação:**
```
🔗 http://172.28.225.112:5000
```

---

## 👤 Credenciais de Acesso

### Administrador
- **Usuário:** `admin`
- **Senha:** `admin123`
- **Perfil:** Administrador (acesso total)

### ⚠️ Importante
- Alterar a senha do admin após primeiro acesso
- Criar usuários específicos para cada pessoa que vai testar

---

## 🖥️ Requisitos para os Usuários

### Navegadores Compatíveis
- ✅ Google Chrome 90+
- ✅ Microsoft Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+

### Conexão de Rede
- ✅ Estar na mesma rede local
- ✅ Ter acesso ao IP `172.28.225.112`
- ✅ Porta `5000` não estar bloqueada pelo firewall

---

## 🧪 Checklist de Teste para Homologação

### 1. Autenticação
- [ ] Login com usuário admin
- [ ] Logout do sistema
- [ ] Tentativa de acesso sem login (deve redirecionar)

### 2. Gestão de Usuários (Admin)
- [ ] Criar novo usuário
- [ ] Editar usuário existente
- [ ] Resetar senha de usuário
- [ ] Ativar/Desativar usuário
- [ ] Verificar diferentes perfis (admin, gestor, usuario)

### 3. Gestão de Relatórios
- [ ] Criar novo relatório de coleção
- [ ] Editar relatório existente
- [ ] Visualizar detalhes do relatório
- [ ] Excluir relatório

### 4. Gestão de Referências
- [ ] Adicionar referência a um relatório
- [ ] Preencher todos os campos (fornecedor, matéria-prima, etc.)
- [ ] Editar referência
- [ ] Visualizar referências no relatório

### 5. Gestão de Provas
- [ ] Criar nova prova de modelagem
- [ ] Upload de tabela de medidas
- [ ] Adicionar informações de recebimento
- [ ] Preencher dados de qualidade, estilo e modelagem

### 6. Upload de Fotos
- [ ] Upload de foto de desenho
- [ ] Upload de foto de qualidade
- [ ] Upload de foto de estilo
- [ ] Upload de foto de amostra (com tamanho)
- [ ] Upload de foto de prova com modelo
- [ ] Visualizar fotos no relatório
- [ ] Excluir foto

### 7. Workflow de Aprovação
- [ ] Adicionar feedback de qualidade
- [ ] Adicionar feedback de estilo
- [ ] Adicionar feedback de modelagem
- [ ] Atualizar status da prova
- [ ] Liberar lacre (quando aprovada)
- [ ] Visualizar histórico de status

### 8. Exportação
- [ ] Exportar relatório em PDF
- [ ] Exportar relatório em Excel
- [ ] Verificar se dados estão corretos nos arquivos

### 9. Auditoria (Admin)
- [ ] Visualizar logs de auditoria
- [ ] Filtrar logs por usuário
- [ ] Filtrar logs por data
- [ ] Visualizar timeline de entidade
- [ ] Exportar logs em CSV

### 10. Interface e Usabilidade
- [ ] Navegação intuitiva
- [ ] Design responsivo (testar em diferentes tamanhos de tela)
- [ ] Mensagens de feedback claras
- [ ] Performance adequada
- [ ] Sem erros no console do navegador

---

## 🔧 Gerenciamento do Servidor

### Ver Status
```bash
ps aux | grep "python.*app.py"
```

### Ver Logs em Tempo Real
```bash
tail -f /home/icolas_atsuda/ProjetosWeb/prova_modelagem_app/app.log
```

### Parar Servidor
```bash
kill $(cat /home/icolas_atsuda/ProjetosWeb/prova_modelagem_app/app.pid)
```

### Reiniciar Servidor
```bash
cd /home/icolas_atsuda/ProjetosWeb/prova_modelagem_app
source .venv/bin/activate
nohup python3 app.py > app.log 2>&1 & echo $! > app.pid
```

### Verificar Porta
```bash
ss -tuln | grep ':5000'
```

---

## 🐛 Troubleshooting

### Usuários não conseguem acessar

**1. Verificar se o servidor está rodando:**
```bash
ss -tuln | grep ':5000'
```
Deve mostrar: `tcp   LISTEN 0      128           0.0.0.0:5000`

**2. Verificar IP da máquina:**
```bash
hostname -I
```

**3. Testar acesso local:**
```bash
curl http://127.0.0.1:5000
```

**4. Verificar firewall do Windows/Linux:**

Windows:
```powershell
# Liberar porta 5000
netsh advfirewall firewall add rule name="Flask App" dir=in action=allow protocol=TCP localport=5000
```

Linux (Ubuntu/WSL):
```bash
# Verificar firewall
sudo ufw status

# Liberar porta 5000 (se necessário)
sudo ufw allow 5000/tcp
```

**5. Verificar se outros computadores conseguem fazer ping:**
```bash
ping 172.28.225.112
```

### Erros no Console do Navegador

**1. Erros de CSRF Token:**
- Fazer logout e login novamente
- Limpar cookies do navegador

**2. Erros de CSP (Content Security Policy):**
- Já corrigidos na última atualização
- Recarregar página com Ctrl+F5

**3. Upload de arquivo falha:**
- Verificar tamanho (máx 10MB para fotos)
- Verificar formato (PNG, JPG, JPEG, GIF)

---

## 📊 Métricas de Homologação

### Colete os seguintes dados:

1. **Performance:**
   - Tempo de carregamento de páginas
   - Tempo de upload de fotos
   - Tempo de geração de PDF

2. **Usabilidade:**
   - Dificuldades encontradas pelos usuários
   - Sugestões de melhorias
   - Funcionalidades mais usadas

3. **Bugs:**
   - Erros encontrados
   - Passos para reproduzir
   - Screenshot do erro (se aplicável)

4. **Feedback:**
   - O que funciona bem
   - O que precisa melhorar
   - Funcionalidades adicionais desejadas

---

## 📞 Suporte Durante Homologação

**Desenvolvedor:** Sistema Flask
**Ambiente:** WSL2 Ubuntu
**Versão:** 1.0.0

**Para reportar problemas:**
1. Descrever o que estava fazendo
2. Copiar mensagem de erro (se houver)
3. Tirar screenshot da tela
4. Informar navegador e versão

---

## ✅ Próximos Passos Após Homologação

1. **Coletar Feedback:** Documentar todos os pontos levantados
2. **Corrigir Bugs:** Priorizar bugs críticos
3. **Ajustes de Usabilidade:** Implementar melhorias sugeridas
4. **Preparar Produção:** Configurar Docker/servidor dedicado
5. **Migração:** Passar do ambiente de homologação para produção
6. **Treinamento:** Treinar usuários finais
7. **Go Live:** Liberar para uso em produção

---

**Data de Deploy:** 03/12/2025
**Modo:** Desenvolvimento (Homologação)
**Duração Prevista:** 1-2 semanas de testes

**Após aprovação, será migrado para Docker com banco PostgreSQL e servidor Nginx em produção.**
