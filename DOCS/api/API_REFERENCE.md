# 🔌 API Reference

Documentação completa de todos os endpoints HTTP do Sistema de Gestão de Provas de Modelagem.

---

## 📑 Índice

- [Autenticação](#autenticação)
- [Relatórios](#relatórios)
- [Provas](#provas)
- [Fotos](#fotos)
- [Feedbacks](#feedbacks)
- [Referências](#referências)
- [Administração](#administração)
- [Auditoria](#auditoria)
- [Analytics](#analytics)
- [Exportação](#exportação)

---

## 🔐 Autenticação

Todos os endpoints (exceto login/registro) requerem autenticação via Flask-Login (sessão).

### POST /login

Fazer login no sistema.

**Requisição:**
```http
POST /login
Content-Type: application/x-www-form-urlencoded

username=admin&password=senha123
```

**Parâmetros:**
- `username` (string, obrigatório): Nome de usuário
- `password` (string, obrigatório): Senha

**Resposta (sucesso):**
```http
HTTP/1.1 302 Found
Location: /dashboard
Set-Cookie: session=...
```

**Resposta (erro):**
```http
HTTP/1.1 200 OK

Flash message: "Credenciais inválidas"
```

---

### GET /logout

Fazer logout do sistema.

**Requisição:**
```http
GET /logout
```

**Resposta:**
```http
HTTP/1.1 302 Found
Location: /login
```

---

### POST /esqueci-senha

Solicitar reset de senha por email.

**Requisição:**
```http
POST /esqueci-senha
Content-Type: application/x-www-form-urlencoded

email=usuario@exemplo.com
```

**Parâmetros:**
- `email` (string, obrigatório): Email cadastrado

**Resposta (sucesso):**
```http
HTTP/1.1 302 Found
Location: /login

Flash message: "Email de recuperação enviado"
```

---

### POST /reset-senha/<token>

Resetar senha com token válido.

**Requisição:**
```http
POST /reset-senha/eyJhbGciOiJI...
Content-Type: application/x-www-form-urlencoded

nova_senha=NovaSenha123!&confirmar_senha=NovaSenha123!
```

**Parâmetros:**
- `nova_senha` (string, obrigatório): Nova senha (mín. 8 caracteres)
- `confirmar_senha` (string, obrigatório): Confirmação de senha

**Resposta (sucesso):**
```http
HTTP/1.1 302 Found
Location: /login

Flash message: "Senha alterada com sucesso"
```

**Resposta (token inválido):**
```http
HTTP/1.1 302 Found
Location: /login

Flash message: "Link inválido ou expirado"
```

---

## 📊 Relatórios

### GET /dashboard

Listar todos os relatórios do usuário.

**Requisição:**
```http
GET /dashboard
```

**Query Parameters (opcionais):**
- `status` (string): Filtrar por status (Em Andamento, Aprovada, Reprovada, Comitê)
- `categoria` (string): Filtrar por categoria (Baby, Kids, Teen, Adulto)
- `search` (string): Buscar por coleção/fornecedor

**Resposta:**
```http
HTTP/1.1 200 OK
Content-Type: text/html

[HTML da página com lista de relatórios]
```

---

### GET /novo-relatorio

Exibir formulário de novo relatório.

**Requisição:**
```http
GET /novo-relatorio
```

**Resposta:**
```http
HTTP/1.1 200 OK
Content-Type: text/html

[Formulário HTML]
```

---

### POST /novo-relatorio

Criar novo relatório.

**Requisição:**
```http
POST /novo-relatorio
Content-Type: multipart/form-data

colecao=Primavera 2026
temporada=Primavera/Verão
categoria=Kids
fornecedor=Fornecedor ABC
apresentacao_ppt=file.pptx
ficha_tecnica=file.pdf
```

**Parâmetros:**
- `colecao` (string, obrigatório): Nome da coleção
- `temporada` (string, obrigatório): Temporada
- `categoria` (string, obrigatório): Baby|Kids|Teen|Adulto
- `fornecedor` (string, opcional): Nome do fornecedor
- `apresentacao_ppt` (file, opcional): Arquivo PPT/PPTX
- `ficha_tecnica` (file, opcional): Arquivo PDF/DOCX

**Resposta (sucesso):**
```http
HTTP/1.1 302 Found
Location: /detalhes-relatorio/123

Flash message: "Relatório criado com sucesso!"
```

**Resposta (validação falhou):**
```http
HTTP/1.1 200 OK

Flash message: "Erro: [mensagem de erro]"
[Formulário HTML com dados preenchidos]
```

---

### GET /detalhes-relatorio/<id>

Ver detalhes completos de um relatório.

**Requisição:**
```http
GET /detalhes-relatorio/123
```

**Parâmetros URL:**
- `id` (integer): ID do relatório

**Resposta (sucesso):**
```http
HTTP/1.1 200 OK
Content-Type: text/html

[HTML com detalhes do relatório, provas, fotos, feedbacks]
```

**Resposta (não encontrado):**
```http
HTTP/1.1 404 Not Found

[Página de erro 404]
```

**Resposta (sem permissão):**
```http
HTTP/1.1 403 Forbidden

[Página de erro 403]
```

---

### GET /editar-relatorio/<id>

Exibir formulário de edição.

**Requisição:**
```http
GET /editar-relatorio/123
```

**Resposta:**
```http
HTTP/1.1 200 OK

[Formulário HTML preenchido com dados atuais]
```

---

### POST /editar-relatorio/<id>

Atualizar relatório existente.

**Requisição:**
```http
POST /editar-relatorio/123
Content-Type: multipart/form-data

colecao=Primavera 2026 Atualizada
status=Aprovada
```

**Parâmetros:**
- Mesmos do POST /novo-relatorio
- `status` (string, opcional): Novo status

**Resposta (sucesso):**
```http
HTTP/1.1 302 Found
Location: /detalhes-relatorio/123

Flash message: "Relatório atualizado com sucesso!"
```

---

### POST /deletar-relatorio/<id>

Deletar relatório (e todas as provas/fotos/feedbacks associados).

**Requisição:**
```http
POST /deletar-relatorio/123
```

**Resposta (sucesso):**
```http
HTTP/1.1 302 Found
Location: /dashboard

Flash message: "Relatório deletado com sucesso"
```

**Resposta (sem permissão):**
```http
HTTP/1.1 403 Forbidden

Flash message: "Você não tem permissão para deletar este relatório"
```

---

## 🎨 Provas

### POST /adicionar-prova/<relatorio_id>

Adicionar nova prova a um relatório.

**Requisição:**
```http
POST /adicionar-prova/123
Content-Type: application/x-www-form-urlencoded

numero_prova=2&fornecedor=ABC&composicao=100% Cotton&gramatura=180g
```

**Parâmetros:**
- `numero_prova` (integer, obrigatório): Número da prova (1, 2, 3...)
- `fornecedor` (string, opcional): Fornecedor da prova
- `composicao` (string, opcional): Composição do tecido
- `gramatura` (string, opcional): Gramatura do tecido
- `motivo_alteracao` (string, opcional): Por que foi feita nova prova

**Resposta (sucesso):**
```http
HTTP/1.1 302 Found
Location: /detalhes-relatorio/123#provas

Flash message: "Prova adicionada com sucesso!"
```

**Resposta (prova duplicada):**
```http
HTTP/1.1 400 Bad Request

Flash message: "Já existe uma prova com este número"
```

---

### POST /editar-prova/<prova_id>

Editar informações de uma prova.

**Requisição:**
```http
POST /editar-prova/456
Content-Type: application/x-www-form-urlencoded

status=Aprovada&composicao=98% Cotton, 2% Elastano
```

**Parâmetros:**
- `status` (string): Em Andamento|Aprovada|Reprovada|Comitê
- `fornecedor` (string)
- `composicao` (string)
- `gramatura` (string)
- `motivo_alteracao` (string)

**Resposta (sucesso):**
```http
HTTP/1.1 302 Found
Location: /detalhes-relatorio/123#provas

Flash message: "Prova atualizada!"
```

---

### POST /deletar-prova/<prova_id>

Deletar uma prova (e todas as fotos/feedbacks associados).

**Requisição:**
```http
POST /deletar-prova/456
```

**Resposta (sucesso):**
```http
HTTP/1.1 302 Found

Flash message: "Prova deletada com sucesso"
```

---

## 📷 Fotos

### POST /upload-foto/<prova_id>

Fazer upload de fotos para uma prova.

**Requisição:**
```http
POST /upload-foto/456
Content-Type: multipart/form-data

tipo_foto=prova_na_modelo
tamanho=M
fotos[]=file1.jpg
fotos[]=file2.jpg
```

**Parâmetros:**
- `tipo_foto` (string, obrigatório): desenho|amostra|prova_na_modelo|qualidade|estilo|modelagem
- `tamanho` (string, opcional): P|M|G|GG|XG|2|4|6|8|10|12|14|16
- `fotos[]` (files, obrigatório): Array de arquivos de imagem (JPG, PNG, GIF, WebP)

**Resposta (sucesso):**
```http
HTTP/1.1 302 Found
Location: /detalhes-relatorio/123#fotos

Flash message: "2 fotos enviadas com sucesso!"
```

**Resposta (tipo de arquivo inválido):**
```http
HTTP/1.1 400 Bad Request

Flash message: "Tipo de arquivo não permitido: file.exe"
```

**Resposta (arquivo muito grande):**
```http
HTTP/1.1 413 Request Entity Too Large

Flash message: "Arquivo muito grande. Máximo: 16MB"
```

---

### POST /deletar-foto/<foto_id>

Deletar uma foto.

**Requisição:**
```http
POST /deletar-foto/789
```

**Resposta (sucesso):**
```http
HTTP/1.1 302 Found

Flash message: "Foto deletada com sucesso"
```

---

### GET /uploads/<filename>

Servir arquivo de upload (protegido por autenticação).

**Requisição:**
```http
GET /uploads/relatorio_123/prova_456/foto_789.jpg
```

**Resposta (sucesso):**
```http
HTTP/1.1 200 OK
Content-Type: image/jpeg

[Dados binários da imagem]
```

**Resposta (não encontrado):**
```http
HTTP/1.1 404 Not Found
```

---

## 💬 Feedbacks

### POST /adicionar-feedback-qualidade/<prova_id>

Adicionar feedback de qualidade.

**Requisição:**
```http
POST /adicionar-feedback-qualidade/456
Content-Type: application/x-www-form-urlencoded

checklist_costura=on
checklist_acabamento=on
checklist_botoes=on
comentarios=Costura perfeita
aprovado=on
```

**Parâmetros:**
- `checklist_costura` (boolean): on/off
- `checklist_acabamento` (boolean): on/off
- `checklist_botoes` (boolean): on/off
- `checklist_ziper` (boolean): on/off
- `checklist_elastico` (boolean): on/off
- `checklist_etiquetas` (boolean): on/off
- `comentarios` (text, opcional)
- `observacoes` (text, opcional)
- `aprovado` (boolean): on/off

**Resposta (sucesso):**
```http
HTTP/1.1 302 Found
Location: /detalhes-relatorio/123#feedbacks

Flash message: "Feedback de qualidade adicionado!"
```

---

### POST /adicionar-feedback-estilo/<prova_id>

Adicionar feedback de estilo.

**Requisição:**
```http
POST /adicionar-feedback-estilo/456
Content-Type: application/x-www-form-urlencoded

checklist_cores=on
checklist_estampas=on
sugestoes=Mudar cor do botão
aprovado=off
```

**Parâmetros:**
- `checklist_cores` (boolean)
- `checklist_estampas` (boolean)
- `checklist_aviamentos` (boolean)
- `checklist_bordados` (boolean)
- `sugestoes` (text, opcional)
- `observacoes` (text, opcional)
- `aprovado` (boolean)

**Resposta:** Mesma do feedback de qualidade

---

### POST /adicionar-feedback-modelagem/<prova_id>

Adicionar feedback de modelagem.

**Requisição:**
```http
POST /adicionar-feedback-modelagem/456
Content-Type: application/x-www-form-urlencoded

checklist_medidas=on
checklist_caimento=on
ajustes=Ajustar manga em 2cm
aprovado=off
```

**Parâmetros:**
- `checklist_medidas` (boolean)
- `checklist_caimento` (boolean)
- `checklist_proporcoes` (boolean)
- `ajustes` (text, opcional)
- `observacoes` (text, opcional)
- `aprovado` (boolean)

**Resposta:** Mesma do feedback de qualidade

---

### POST /editar-feedback-<tipo>/<feedback_id>

Editar feedback existente (qualidade, estilo ou modelagem).

**Requisição:**
```http
POST /editar-feedback-qualidade/111
Content-Type: application/x-www-form-urlencoded

comentarios=Atualizado: costura ok
aprovado=on
```

**Parâmetros:** Mesmos do POST adicionar-feedback correspondente

**Resposta (sucesso):**
```http
HTTP/1.1 302 Found

Flash message: "Feedback atualizado!"
```

---

### POST /deletar-feedback-<tipo>/<feedback_id>

Deletar feedback.

**Requisição:**
```http
POST /deletar-feedback-qualidade/111
```

**Resposta (sucesso):**
```http
HTTP/1.1 302 Found

Flash message: "Feedback deletado"
```

---

## 🖼️ Referências

### POST /adicionar-referencia/<relatorio_id>

Adicionar referência/inspiração.

**Requisição:**
```http
POST /adicionar-referencia/123
Content-Type: multipart/form-data

nome=Pinterest - Vestido Floral
imagem=ref1.jpg
```

**Parâmetros:**
- `nome` (string, obrigatório): Nome/descrição da referência
- `imagem` (file, obrigatório): Arquivo de imagem

**Resposta (sucesso):**
```http
HTTP/1.1 302 Found
Location: /detalhes-relatorio/123#referencias

Flash message: "Referência adicionada!"
```

---

### POST /deletar-referencia/<ref_id>

Deletar referência.

**Requisição:**
```http
POST /deletar-referencia/999
```

**Resposta (sucesso):**
```http
HTTP/1.1 302 Found

Flash message: "Referência deletada"
```

---

## 👨‍💼 Administração

**Requer role: `admin`**

### GET /admin/dashboard

Dashboard administrativo.

**Requisição:**
```http
GET /admin/dashboard
```

**Resposta:**
```http
HTTP/1.1 200 OK

[HTML com estatísticas do sistema]
```

---

### GET /admin/usuarios

Listar todos os usuários.

**Requisição:**
```http
GET /admin/usuarios
```

**Resposta:**
```http
HTTP/1.1 200 OK

[HTML com tabela de usuários]
```

---

### POST /admin/criar-usuario

Criar novo usuário.

**Requisição:**
```http
POST /admin/criar-usuario
Content-Type: application/x-www-form-urlencoded

username=joao
email=joao@exemplo.com
password=Senha123!
role=gestor
```

**Parâmetros:**
- `username` (string, obrigatório): Username único
- `email` (string, obrigatório): Email único
- `password` (string, obrigatório): Senha (mín. 8 caracteres)
- `role` (string, obrigatório): admin|gestor|usuario

**Resposta (sucesso):**
```http
HTTP/1.1 302 Found
Location: /admin/usuarios

Flash message: "Usuário criado com sucesso!"
```

---

### POST /admin/editar-usuario/<user_id>

Editar usuário existente.

**Requisição:**
```http
POST /admin/editar-usuario/5
Content-Type: application/x-www-form-urlencoded

email=joao.novo@exemplo.com
role=admin
```

**Parâmetros:**
- `email` (string)
- `role` (string)
- `password` (string, opcional): Nova senha (se fornecida)

**Resposta (sucesso):**
```http
HTTP/1.1 302 Found
Location: /admin/usuarios

Flash message: "Usuário atualizado!"
```

---

### POST /admin/deletar-usuario/<user_id>

Deletar usuário (não pode deletar a si mesmo).

**Requisição:**
```http
POST /admin/deletar-usuario/5
```

**Resposta (sucesso):**
```http
HTTP/1.1 302 Found
Location: /admin/usuarios

Flash message: "Usuário deletado"
```

**Resposta (tentando deletar a si mesmo):**
```http
HTTP/1.1 400 Bad Request

Flash message: "Você não pode deletar sua própria conta"
```

---

### POST /admin/alterar-senha

Admin altera sua própria senha.

**Requisição:**
```http
POST /admin/alterar-senha
Content-Type: application/x-www-form-urlencoded

senha_atual=SenhaAtual123
nova_senha=NovaSenha456!
confirmar_senha=NovaSenha456!
```

**Parâmetros:**
- `senha_atual` (string, obrigatório)
- `nova_senha` (string, obrigatório)
- `confirmar_senha` (string, obrigatório)

**Resposta (sucesso):**
```http
HTTP/1.1 302 Found
Location: /admin/dashboard

Flash message: "Senha alterada com sucesso!"
```

---

## 📜 Auditoria

### GET /auditoria

Ver logs de auditoria do sistema.

**Requisição:**
```http
GET /auditoria?acao=CREATE&tabela=relatorio&page=2
```

**Query Parameters (opcionais):**
- `acao` (string): Filtrar por ação (CREATE, UPDATE, DELETE, LOGIN, etc.)
- `tabela` (string): Filtrar por tabela
- `user_id` (integer): Filtrar por usuário
- `page` (integer): Página (paginação de 100 itens por página)

**Resposta:**
```http
HTTP/1.1 200 OK

[HTML com tabela de logs paginada]
```

---

### GET /auditoria/detalhes/<log_id>

Ver detalhes de um log específico.

**Requisição:**
```http
GET /auditoria/detalhes/12345
```

**Resposta:**
```http
HTTP/1.1 200 OK

[HTML com diff de dados antigos vs novos em JSON]
```

---

### GET /auditoria/por-usuario/<user_id>

Ver todos os logs de um usuário específico.

**Requisição:**
```http
GET /auditoria/por-usuario/3
```

**Resposta:**
```http
HTTP/1.1 200 OK

[HTML com logs do usuário]
```

---

### GET /auditoria/estatisticas

Estatísticas de auditoria.

**Requisição:**
```http
GET /auditoria/estatisticas?periodo=30d
```

**Query Parameters:**
- `periodo` (string): 7d|30d|90d|1y|all

**Resposta:**
```http
HTTP/1.1 200 OK

[HTML com gráficos de ações por tipo, usuário mais ativo, etc.]
```

---

## 📊 Analytics

### GET /analytics

Dashboard de analytics.

**Requisição:**
```http
GET /analytics
```

**Resposta:**
```http
HTTP/1.1 200 OK

[HTML com gráficos Chart.js de KPIs]
```

---

### GET /api/analytics/status-distribution

API JSON para distribuição de status.

**Requisição:**
```http
GET /api/analytics/status-distribution
```

**Resposta:**
```json
{
    "labels": ["Em Andamento", "Aprovada", "Reprovada", "Comitê"],
    "data": [45, 120, 8, 15]
}
```

---

### GET /api/analytics/timeline

API JSON para timeline de criação.

**Requisição:**
```http
GET /api/analytics/timeline?periodo=30d
```

**Query Parameters:**
- `periodo` (string): 7d|30d|90d|1y

**Resposta:**
```json
{
    "labels": ["2026-01-01", "2026-01-02", ...],
    "datasets": [{
        "label": "Relatórios Criados",
        "data": [3, 5, 2, 8, ...]
    }]
}
```

---

### GET /api/analytics/top-fornecedores

API JSON para fornecedores mais usados.

**Requisição:**
```http
GET /api/analytics/top-fornecedores?limit=10
```

**Query Parameters:**
- `limit` (integer): Quantidade de fornecedores (padrão: 10)

**Resposta:**
```json
{
    "labels": ["Fornecedor A", "Fornecedor B", ...],
    "data": [45, 32, 28, ...]
}
```

---

## 📤 Exportação

### GET /exportar-excel

Exportar relatórios para Excel.

**Requisição:**
```http
GET /exportar-excel?status=Aprovada&categoria=Kids
```

**Query Parameters (opcionais):**
- `status` (string): Filtrar por status
- `categoria` (string): Filtrar por categoria
- `fornecedor` (string): Filtrar por fornecedor
- `data_inicio` (date): Filtrar por data (formato: YYYY-MM-DD)
- `data_fim` (date): Filtrar por data

**Resposta:**
```http
HTTP/1.1 200 OK
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename="relatorios_2026-01-16.xlsx"

[Dados binários do arquivo Excel]
```

---

### GET /exportar-pdf/<relatorio_id>

Exportar relatório específico para PDF.

**Requisição:**
```http
GET /exportar-pdf/123
```

**Resposta:**
```http
HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Disposition: inline; filename="relatorio_123.pdf"

[Dados binários do PDF]
```

---

## 🔒 Códigos de Status HTTP

| Código | Descrição |
|--------|-----------|
| **200** | OK - Requisição bem-sucedida |
| **302** | Found - Redirect (após POST bem-sucedido) |
| **400** | Bad Request - Dados inválidos |
| **401** | Unauthorized - Não autenticado |
| **403** | Forbidden - Sem permissão |
| **404** | Not Found - Recurso não encontrado |
| **413** | Payload Too Large - Arquivo muito grande |
| **429** | Too Many Requests - Rate limit excedido |
| **500** | Internal Server Error - Erro do servidor |

---

## 🔐 Autenticação e Autorização

### Sessões

- **Tipo:** Flask-Login (session cookies)
- **Duração:** Permanente (até logout ou expiração)
- **Cookie:** `session` (HTTPOnly, Secure em HTTPS)

### Roles e Permissões

| Role | Permissões |
|------|------------|
| **admin** | Tudo + painel administrativo + gerenciar usuários |
| **gestor** | Criar/editar/deletar relatórios próprios + todos feedbacks |
| **usuario** | Visualizar relatórios + adicionar feedbacks |

### Verificação de Permissões

```python
# Exemplo de verificação no backend
from functools import wraps
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    # ...
```

---

## 🚦 Rate Limiting

Proteção contra abuso de requisições:

| Endpoint | Limite |
|----------|--------|
| `/login` | 5 requisições/minuto por IP |
| `/novo-relatorio` | 10 requisições/minuto por usuário |
| `/upload-foto` | 20 uploads/minuto por usuário |
| Outros | 100 requisições/minuto por usuário |

**Resposta quando limite excedido:**
```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60

Flash message: "Muitas requisições. Aguarde 60 segundos."
```

---

## 📝 Validações

### Campos Obrigatórios

Campos marcados como `obrigatório` retornam erro 400 se não fornecidos.

### Tamanhos de Arquivo

| Tipo | Tamanho Máximo |
|------|----------------|
| Imagens (JPG, PNG, GIF, WebP) | 16 MB |
| Documentos (PDF, DOCX) | 25 MB |
| Apresentações (PPT, PPTX) | 50 MB |

### Formatos Aceitos

**Imagens:** `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
**Documentos:** `.pdf`, `.doc`, `.docx`
**Apresentações:** `.ppt`, `.pptx`
**Planilhas:** `.xls`, `.xlsx`

---

## 🛠️ Exemplos de Uso

### Criar Relatório Completo (cURL)

```bash
curl -X POST http://localhost:5000/novo-relatorio \
  -H "Cookie: session=..." \
  -F "colecao=Verão 2026" \
  -F "temporada=Primavera/Verão" \
  -F "categoria=Kids" \
  -F "fornecedor=ABC Textil" \
  -F "apresentacao_ppt=@apresentacao.pptx" \
  -F "ficha_tecnica=@ficha.pdf"
```

### Adicionar Prova e Fotos (JavaScript)

```javascript
// 1. Adicionar prova
const formData = new FormData();
formData.append('numero_prova', '1');
formData.append('fornecedor', 'XYZ');
formData.append('composicao', '100% Cotton');
formData.append('gramatura', '180g');

fetch('/adicionar-prova/123', {
    method: 'POST',
    body: formData
}).then(response => {
    // Prova criada, pegar ID da resposta
    const provaId = 456; // Extrair do HTML de resposta

    // 2. Upload de fotos
    const fotoFormData = new FormData();
    fotoFormData.append('tipo_foto', 'prova_na_modelo');
    fotoFormData.append('tamanho', 'M');
    fotoFormData.append('fotos[]', fileInput.files[0]);
    fotoFormData.append('fotos[]', fileInput.files[1]);

    return fetch(`/upload-foto/${provaId}`, {
        method: 'POST',
        body: fotoFormData
    });
});
```

### Buscar Analytics (Fetch API)

```javascript
// Obter distribuição de status
fetch('/api/analytics/status-distribution')
    .then(res => res.json())
    .then(data => {
        console.log('Labels:', data.labels);
        console.log('Valores:', data.data);

        // Criar gráfico com Chart.js
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.data
                }]
            }
        });
    });
```

---

## 🔗 Links Relacionados

- **[Backend Architecture](../architecture/BACKEND.md)**
- **[Frontend Architecture](../architecture/FRONTEND.md)**
- **[Database Schema](../architecture/DATABASE.md)**
- **[Troubleshooting](../guides/TROUBLESHOOTING.md)**

---

**[⬅ Voltar ao Índice](../INDEX.md)**
