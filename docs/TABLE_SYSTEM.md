# Sistema de Tabelas Modernas - Documentação

## Visão Geral

Sistema completo de tabelas com UX aprimorada, incluindo:
- ✅ Ordenação (sorting) multi-coluna
- ✅ Busca/filtragem em tempo real
- ✅ Paginação (client-side e server-side)
- ✅ Ações inline (hover)
- ✅ Responsividade mobile (card view)
- ✅ Loading states
- ✅ Empty states
- ✅ Suporte a diferentes tipos de dados (string, number, date)

## Arquivos Criados

### Frontend
- `/static/css/table.css` - Estilos completos das tabelas
- `/static/js/datatable.js` - Classe JavaScript DataTable
- `/templates/table_example.html` - Template de exemplo

### Backend
- `/api_pagination.py` - Helpers para paginação no Flask

### Tabelas Atualizadas
- `/templates/admin/users.html` - Tabela de usuários
- `/templates/audit/index.html` - Tabela de auditoria

## Como Usar

### 1. Incluir CSS e JS no Template

```html
{% block styles %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/table.css') }}">
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', filename='js/datatable.js') }}"></script>
{% endblock %}
```

### 2. Estrutura HTML Básica

```html
<div class="table-container">
  <!-- Header com busca e ações -->
  <div class="table-header">
    <div class="table-search">
      <i class="bi bi-search"></i>
      <input type="text" placeholder="Buscar..." class="table-search-input">
    </div>
    <div class="table-actions">
      <button class="btn btn-sm btn-primary">
        <i class="bi bi-plus"></i> Novo
      </button>
    </div>
  </div>

  <!-- Tabela -->
  <div class="table-responsive">
    <table class="table-modern">
      <thead>
        <tr>
          <th data-sortable="true" data-type="string">
            Nome
            <span class="sort-icon">
              <i class="bi bi-chevron-expand"></i>
            </span>
          </th>
          <th data-sortable="true" data-type="date">Data</th>
          <th class="actions-column">Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td data-label="Nome">João Silva</td>
          <td data-label="Data" data-sort-value="2025-01-16">16/01/2025</td>
          <td class="actions-cell">
            <div class="action-buttons">
              <button class="btn-action" title="Editar">
                <i class="bi bi-pencil"></i>
              </button>
              <button class="btn-action btn-action-danger" title="Excluir">
                <i class="bi bi-trash"></i>
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- Footer com paginação -->
  <div class="table-footer">
    <div class="table-info"></div>
    <nav class="pagination-nav"></nav>
    <select class="per-page-select">
      <option value="20">20 por página</option>
      <option value="50">50 por página</option>
    </select>
  </div>
</div>
```

### 3. Atributos Importantes

#### Colunas (`<th>`)
- `data-sortable="true"` - Habilita ordenação
- `data-type="string|number|date"` - Define tipo para ordenação correta
- `class="actions-column"` - Para coluna de ações (alinhamento direita)

#### Células (`<td>`)
- `data-label="Label"` - OBRIGATÓRIO para mobile (label do campo)
- `data-sort-value="value"` - Valor customizado para ordenação (opcional)
- `class="actions-cell"` - Para célula de ações

#### Badges de Status
```html
<span class="badge badge-success">Ativo</span>
<span class="badge badge-error">Erro</span>
<span class="badge badge-warning">Alerta</span>
<span class="badge badge-info">Info</span>
<span class="badge badge-secondary">Neutro</span>
```

#### Botões de Ação
```html
<div class="action-buttons">
  <button class="btn-action" title="Visualizar">
    <i class="bi bi-eye"></i>
  </button>
  <button class="btn-action btn-action-warning" title="Editar">
    <i class="bi bi-pencil"></i>
  </button>
  <button class="btn-action btn-action-danger" title="Excluir">
    <i class="bi bi-trash"></i>
  </button>
</div>
```

### 4. Inicialização Manual (Opcional)

A classe `DataTable` é auto-inicializada, mas você pode customizar:

```javascript
const table = document.querySelector('.table-modern');
const dt = new DataTable(table, {
  sortable: true,        // Habilita ordenação
  searchable: true,      // Habilita busca
  perPage: 20,           // Itens por página
  pagination: true,      // Habilita paginação
  mobileBreakpoint: 768  // Breakpoint para mobile
});

// Métodos disponíveis
dt.filter('termo de busca');  // Filtrar programaticamente
dt.goToPage(2);               // Ir para página
dt.refresh();                 // Recarregar dados
dt.destroy();                 // Destruir instância
```

## Backend (Paginação Server-Side)

### Uso Básico

```python
from api_pagination import DataTablePaginator

@app.route('/api/users')
def get_users_api():
    paginator = DataTablePaginator(
        model=User,
        base_query=User.query,
        searchable_fields=['username', 'email', 'nome_completo'],
        default_sort='id',
        default_order='desc'
    )
    return paginator.get_response()
```

### Com Filtros Customizados

```python
@app.route('/api/relatorios')
def get_relatorios_api():
    query = Relatorio.query

    # Aplicar filtros customizados
    status = request.args.get('status')
    if status:
        query = query.filter_by(status_atual=status)

    # Usar paginação simples
    items, meta = simple_pagination(query)
    return jsonify({'items': items, 'meta': meta})
```

### Com Serializer Customizado

```python
@app.route('/api/audit')
def get_audit_api():
    def serialize_log(log):
        return {
            'id': log.id,
            'timestamp': log.created_at.isoformat(),
            'user': log.usuario_nome,
            'action': log.acao
        }

    paginator = DataTablePaginator(
        model=AuditLog,
        base_query=AuditLog.query,
        searchable_fields=['descricao', 'usuario_nome'],
        default_sort='created_at',
        default_order='desc'
    )
    return paginator.get_response(serializer=serialize_log)
```

### Parâmetros da URL

A API aceita os seguintes query parameters:

- `page` (int) - Número da página (padrão: 1)
- `per_page` (int) - Itens por página (padrão: 20)
- `search` (string) - Termo de busca
- `sort` (string) - Campo para ordenar
- `order` (string) - Direção (asc/desc)

Exemplo: `/api/users?page=2&per_page=50&search=joao&sort=created_at&order=desc`

## Responsividade Mobile

Em telas menores que 768px, a tabela automaticamente se transforma em cards:

```css
/* Mobile: cada linha vira um card */
@media (max-width: 768px) {
  .table-modern thead { display: none; }
  .table-modern tbody tr { display: block; }
  .table-modern td { display: block; }
  .table-modern td::before {
    content: attr(data-label);
    font-weight: 600;
  }
}
```

**IMPORTANTE**: Sempre adicionar `data-label` em todas as células `<td>` para funcionar no mobile.

## Estados Especiais

### Empty State
```html
<tr>
  <td colspan="X" class="table-empty">
    <div class="table-empty-icon">
      <i class="bi bi-inbox"></i>
    </div>
    <h3>Nenhum resultado</h3>
    <p>Mensagem descritiva</p>
  </td>
</tr>
```

### Loading State
```html
<div class="table-loading">
  <!-- Loading spinner é gerado automaticamente via CSS -->
</div>
```

## Variáveis CSS Customizáveis

O sistema usa CSS variables que podem ser customizadas:

```css
:root {
  --primary: #ec4899;
  --error: #dc2626;
  --success: #10b981;
  --warning: #f59e0b;

  --gray-50: #fafafa;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;

  --radius-md: 8px;
  --radius-lg: 12px;

  --space-2: 8px;
  --space-4: 16px;
  --space-6: 24px;
}
```

## Exemplos Práticos

### Tabela com Badges de Status
```html
<td data-label="Status" data-sort-value="ativo">
  {% if user.is_active %}
  <span class="badge badge-success">Ativo</span>
  {% else %}
  <span class="badge badge-error">Inativo</span>
  {% endif %}
</td>
```

### Coluna com Link
```html
<td data-label="Nome">
  <a href="{{ url_for('view_user', id=user.id) }}" class="text-decoration-none">
    <strong>{{ user.name }}</strong>
  </a>
</td>
```

### Data com Sort Correto
```html
<td data-label="Data" data-sort-value="2025-01-16">
  16/01/2025
</td>
```

### Número Formatado
```html
<td data-label="Valor" data-sort-value="1250.50">
  R$ 1.250,50
</td>
```

## Performance

O sistema foi otimizado para:
- ✅ 1000+ linhas com paginação client-side
- ✅ 10000+ linhas com paginação server-side
- ✅ Debounce de 300ms na busca
- ✅ Lazy loading de imagens (via Intersection Observer)

## Acessibilidade

- ✅ Suporte a navegação por teclado
- ✅ Labels em mobile (data-label)
- ✅ Títulos descritivos (title attribute)
- ✅ Contraste de cores adequado
- ✅ Focus states visíveis

## Troubleshooting

### Tabela não ordena
- Verificar se `data-sortable="true"` está presente
- Verificar se `.sort-icon` está dentro do `<th>`
- Verificar console para erros JavaScript

### Busca não funciona
- Verificar se `.table-search-input` está presente
- Verificar se a tabela está dentro de `.table-container`
- Verificar console para erros

### Mobile não funciona
- Verificar se TODOS os `<td>` têm `data-label`
- Verificar se o CSS `table.css` foi incluído
- Testar em DevTools com responsive mode

### Ações não aparecem
- Verificar se `.action-buttons` está dentro de `.actions-cell`
- Verificar estrutura HTML completa
- Ações aparecem apenas no hover (desktop)

## Changelog

### v1.0.0 (2026-01-16)
- ✅ Sistema completo de tabelas
- ✅ Sorting multi-coluna
- ✅ Busca/filtragem
- ✅ Paginação (client/server)
- ✅ Responsividade mobile
- ✅ Backend helpers
- ✅ Documentação completa

## Suporte

Para dúvidas ou problemas:
1. Verificar esta documentação
2. Verificar `/templates/table_example.html` para exemplos
3. Verificar console do navegador para erros
4. Verificar estrutura HTML completa
