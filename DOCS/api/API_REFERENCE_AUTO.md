# 🔌 API Reference (Auto-Generated)

**Versão:** 2.1
**Última Atualização:** 16/01/2026 21:25
**Gerado Automaticamente:** Sim

---

## 📑 Índice

- [Autenticação](#autenticação)
- [Dashboard e Relatórios](#dashboard-e-relatórios)
- [Referências e Provas](#referências-e-provas)
- [Analytics](#analytics)
- [Exportação](#exportação)
- [Administração](#administração)
- [Auditoria](#auditoria)
- [Arquivos Estáticos](#arquivos-estáticos)

---

## 🔐 Autenticação

### GET, POST /alterar-senha

**Função:** `alterar_senha`

**Descrição:**
Permite ao usuário alterar sua própria senha

**Exemplo de Requisição:**
```http
GET /alterar-senha HTTP/1.1
Host: localhost:5000
```

---

### GET, POST /esqueci-senha

**Função:** `esqueci_senha`

**Descrição:**
Gera token de reset de senha

**Exemplo de Requisição:**
```http
GET /esqueci-senha HTTP/1.1
Host: localhost:5000
```

---

### GET, POST /login

**Função:** `login`

**Exemplo de Requisição:**
```http
GET /login HTTP/1.1
Host: localhost:5000
```

---

### GET /logout

**Função:** `logout`

**Exemplo de Requisição:**
```http
GET /logout HTTP/1.1
Host: localhost:5000
```

---

### GET, POST /reset-senha/<token>

**Função:** `reset_senha`

**Descrição:**
Reset de senha usando token

**Parâmetros da URL:**
- `token` (string)

**Exemplo de Requisição:**
```http
GET /reset-senha/<token} HTTP/1.1
Host: localhost:5000
```

---

## 📊 Dashboard e Relatórios

### GET /

**Função:** `dashboard`

**Exemplo de Requisição:**
```http
GET / HTTP/1.1
Host: localhost:5000
```

---

### GET /analytics

**Função:** `analytics`

**Descrição:**
Página de relatórios e analytics com filtros

**Exemplo de Requisição:**
```http
GET /analytics HTTP/1.1
Host: localhost:5000
```

---

### GET /analytics/exportar

**Função:** `analytics_exportar`

**Descrição:**
Exporta dados filtrados para Excel

**Exemplo de Requisição:**
```http
GET /analytics/exportar HTTP/1.1
Host: localhost:5000
```

---

### GET /api/analytics/charts

**Função:** `api_analytics_charts`

**Descrição:**
Endpoint API para fornecer dados dos gráficos
Retorna JSON com todos os dados necessários para visualizações

**Exemplo de Requisição:**
```http
GET /api/analytics/charts HTTP/1.1
Host: localhost:5000
```

---

### GET /exportar/excel

**Função:** `exportar_relatorios_excel`

**Descrição:**
Exporta todos os relatórios para Excel

**Exemplo de Requisição:**
```http
GET /exportar/excel HTTP/1.1
Host: localhost:5000
```

---

### GET /favicon.ico

**Função:** `favicon`

**Descrição:**
Serve favicon from static folder

**Exemplo de Requisição:**
```http
GET /favicon.ico HTTP/1.1
Host: localhost:5000
```

---

### GET, POST /importar/excel

**Função:** `importar_relatorios_excel`

**Descrição:**
Importa relatórios de um arquivo Excel

**Exemplo de Requisição:**
```http
GET /importar/excel HTTP/1.1
Host: localhost:5000
```

---

### GET /logs

**Função:** `logs`

**Descrição:**
Página de visualização de logs de auditoria - Apenas para administradores

**Exemplo de Requisição:**
```http
GET /logs HTTP/1.1
Host: localhost:5000
```

---

### GET, POST /novo

**Função:** `novo_relatorio`

**Exemplo de Requisição:**
```http
GET /novo HTTP/1.1
Host: localhost:5000
```

---

### POST /prova/atualizar_status

**Função:** `atualizar_status`

**Exemplo de Requisição:**
```http
POST /prova/atualizar_status HTTP/1.1
Host: localhost:5000
Content-Type: application/x-www-form-urlencoded

# Parâmetros do formulário aqui
```

---

### GET, POST /referencia/<int:referencia_id>/nova_prova

**Função:** `adicionar_nova_prova`

**Parâmetros da URL:**
- `referencia_id` (int)

**Exemplo de Requisição:**
```http
GET /referencia/{referencia_id}/nova_prova HTTP/1.1
Host: localhost:5000
```

---

### GET /relatorio/<int:id>

**Função:** `detalhes_relatorio`

**Parâmetros da URL:**
- `id` (int)

**Exemplo de Requisição:**
```http
GET /relatorio/{id} HTTP/1.1
Host: localhost:5000
```

---

### GET, POST /relatorio/<int:id>/editar

**Função:** `editar_relatorio`

**Parâmetros da URL:**
- `id` (int)

**Exemplo de Requisição:**
```http
GET /relatorio/{id}/editar HTTP/1.1
Host: localhost:5000
```

---

### GET /relatorio/<int:id>/excel

**Função:** `exportar_relatorio_excel`

**Descrição:**
Exporta detalhes de um relatório específico para Excel

**Parâmetros da URL:**
- `id` (int)

**Exemplo de Requisição:**
```http
GET /relatorio/{id}/excel HTTP/1.1
Host: localhost:5000
```

---

### POST /relatorio/<int:id>/excluir

**Função:** `excluir_relatorio`

**Descrição:**
Exclui um relatório e todos os seus arquivos associados

**Parâmetros da URL:**
- `id` (int)

**Exemplo de Requisição:**
```http
POST /relatorio/{id}/excluir HTTP/1.1
Host: localhost:5000
Content-Type: application/x-www-form-urlencoded

# Parâmetros do formulário aqui
```

---

### GET /relatorio/<int:id>/pdf

**Função:** `relatorio_pdf`

**Descrição:**
Gera e retorna o PDF do relatório

**Parâmetros da URL:**
- `id` (int)

**Exemplo de Requisição:**
```http
GET /relatorio/{id}/pdf HTTP/1.1
Host: localhost:5000
```

---

### GET /uploads/<path:filename>

**Função:** `serve_upload`

**Parâmetros da URL:**
- `filename` (path)

**Exemplo de Requisição:**
```http
GET /uploads/{filename} HTTP/1.1
Host: localhost:5000
```

---

## 👨‍💼 Administração

### GET /admin/

**Função:** `dashboard`

**Exemplo de Requisição:**
```http
GET /admin/ HTTP/1.1
Host: localhost:5000
```

---

### GET, POST /admin/change-my-password

**Função:** `change_my_password`

**Descrição:**
Permite ao admin alterar sua própria senha

**Exemplo de Requisição:**
```http
GET /admin/change-my-password HTTP/1.1
Host: localhost:5000
```

---

### GET /admin/users

**Função:** `users`

**Descrição:**
Lista todos os usuários do sistema

**Exemplo de Requisição:**
```http
GET /admin/users HTTP/1.1
Host: localhost:5000
```

---

### GET, POST /admin/users/create

**Função:** `create_user`

**Descrição:**
Cria um novo usuário com senha gerada

**Exemplo de Requisição:**
```http
GET /admin/users/create HTTP/1.1
Host: localhost:5000
```

---

### POST /admin/users/delete/<int:user_id>

**Função:** `delete_user`

**Descrição:**
Desativa um usuário (soft delete)

**Parâmetros da URL:**
- `user_id` (int)

**Exemplo de Requisição:**
```http
POST /admin/users/delete/{user_id} HTTP/1.1
Host: localhost:5000
Content-Type: application/x-www-form-urlencoded

# Parâmetros do formulário aqui
```

---

### GET, POST /admin/users/edit/<int:user_id>

**Função:** `edit_user`

**Descrição:**
Edita um usuário existente

**Parâmetros da URL:**
- `user_id` (int)

**Exemplo de Requisição:**
```http
GET /admin/users/edit/{user_id} HTTP/1.1
Host: localhost:5000
```

---

### POST /admin/users/reset_password/<int:user_id>

**Função:** `reset_password`

**Descrição:**
Redefine a senha de um usuário (gera senha aleatória) - mantido para compatibilidade

**Parâmetros da URL:**
- `user_id` (int)

**Exemplo de Requisição:**
```http
POST /admin/users/reset_password/{user_id} HTTP/1.1
Host: localhost:5000
Content-Type: application/x-www-form-urlencoded

# Parâmetros do formulário aqui
```

---

### POST /admin/users/set_password/<int:user_id>

**Função:** `set_password`

**Descrição:**
Define uma nova senha para um usuário (digitada pelo admin)

**Parâmetros da URL:**
- `user_id` (int)

**Exemplo de Requisição:**
```http
POST /admin/users/set_password/{user_id} HTTP/1.1
Host: localhost:5000
Content-Type: application/x-www-form-urlencoded

# Parâmetros do formulário aqui
```

---

### POST /admin/users/toggle_active/<int:user_id>

**Função:** `toggle_active`

**Descrição:**
Ativa/desativa um usuário

**Parâmetros da URL:**
- `user_id` (int)

**Exemplo de Requisição:**
```http
POST /admin/users/toggle_active/{user_id} HTTP/1.1
Host: localhost:5000
Content-Type: application/x-www-form-urlencoded

# Parâmetros do formulário aqui
```

---

## 📝 Notas Importantes

### Estrutura de Dados

**Hierarquia das Entidades:**
```
Relatorio (relatórios)
  └── Referencia (referencias)
      └── ProvaModelagem (provas)
          └── FotoProva (fotos)
```

### Feedbacks

⚠️ **IMPORTANTE:** Feedbacks (Qualidade, Estilo, Modelagem) são **COLUNAS** na tabela `provas`, não entidades separadas.

Para atualizar feedbacks, use:
- `POST /relatorio/<int:id>/editar` - Edita o relatório e suas provas
- `POST /prova/atualizar_status` - Atualiza status e feedbacks de uma prova específica

Campos de feedback na tabela `provas`:
```python
# Qualidade
time_qualidade: str
checklist_qualidade: str  # CSV
comentarios_qualidade: str
obs_qualidade: str

# Estilo
time_estilo: str
checklist_estilo: str  # CSV
comentarios_estilo: str
obs_estilo: str

# Modelagem
time_modelagem: str
checklist_modelagem: str  # CSV
comentarios_modelagem: str
obs_modelagem: str
```

### Sistema de Auditoria

⚠️ **STATUS:** O blueprint de auditoria existe no código mas está **DESABILITADO** em `app.py`.

Para habilitar:
```python
# app.py - descomentar:
from audit_bp import audit_bp
app.register_blueprint(audit_bp, url_prefix='/auditoria')
```

Rotas disponíveis quando habilitado:
- `GET /auditoria/` - Lista de logs
- `GET /auditoria/detalhes/<int:log_id>` - Detalhes de um log
- `GET /auditoria/timeline/<string:entidade>/<int:entidade_id>` - Timeline de uma entidade
- `GET /auditoria/usuario/<int:usuario_id>` - Logs de um usuário
- `GET /auditoria/exportar/csv` - Exportar logs para CSV
- `GET /auditoria/estatisticas` - Estatísticas de auditoria

---

## 📞 Suporte

**Desenvolvedor:** Nicolas Matsuda
**Email:** nicolas.matsuda@grupounico.com
**Projeto:** Sistema de Gestão de Provas de Modelagem - Puket

---

**[⬅ Voltar ao Índice](../INDEX.md)**
