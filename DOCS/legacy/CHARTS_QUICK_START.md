# Gráficos Analytics - Quick Start Guide

## Decisão: Chart.js v4.4.0 (64KB) ✅

**Por que Chart.js?**
- Leve e rápido
- Simples de usar
- 100% responsivo
- Todos os gráficos necessários

---

## 🚀 Uso Rápido

### 1. HTML - Adicionar Canvas

```html
<div class="chart-card">
    <h5><i class="bi bi-pie-chart-fill"></i> Meu Gráfico</h5>
    <div class="chart-container">
        <canvas id="meuGrafico"></canvas>
    </div>
</div>
```

### 2. JavaScript - Criar Gráfico

```javascript
// Opção A: Dados mockados (para testes)
const data = MockData.statusDistribution;
ChartConfig.createStatusChart('meuGrafico', data, 'doughnut');

// Opção B: Dados da API (produção)
fetch('/api/analytics/charts')
    .then(res => res.json())
    .then(result => {
        ChartConfig.createStatusChart('meuGrafico', result.data.statusChart);
    });
```

---

## 📊 Tipos de Gráficos

### 1. Doughnut/Pie - Status
```javascript
ChartConfig.createStatusChart('canvasId', {
    labels: ['Aprovada', 'Reprovada', 'Em Andamento', 'Comitê'],
    values: [45, 12, 18, 8]
}, 'doughnut');
```

### 2. Bar Horizontal - Fornecedores
```javascript
ChartConfig.createSuppliersChart('canvasId', {
    suppliers: ['Fornecedor A', 'Fornecedor B', 'Fornecedor C'],
    counts: [25, 20, 18]
});
```

### 3. Area Chart - Timeline
```javascript
ChartConfig.createTimelineChart('canvasId', {
    months: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
    counts: [5, 8, 12, 15, 18, 22]
});
```

### 4. Bar Vertical - Categorias
```javascript
ChartConfig.createCategoryChart('canvasId', {
    categories: ['baby', 'kids', 'teen', 'adulto'],
    counts: [35, 48, 28, 42]
});
```

### 5. Sparkline - Mini Gráfico
```javascript
ChartConfig.createSparkline('canvasId', [10, 12, 15, 18, 20, 22], '#22C55E');
```

### 6. Mixed - Barras + Linha
```javascript
ChartConfig.createMixedChart('canvasId', {
    labels: ['Jan', 'Fev', 'Mar'],
    totalProvas: [20, 25, 30],
    taxaAprovacao: [75, 80, 85]
});
```

---

## 🔄 Loading States

### Mostrar Loading
```javascript
ChartConfig.showChartLoader('containerId');
```

### Mostrar Erro
```javascript
ChartConfig.showChartError('containerId', 'Mensagem de erro');
```

### Destruir Gráfico
```javascript
ChartConfig.destroyChart('canvasId');
```

---

## 🎨 Classes CSS Disponíveis

### Containers
- `.chart-container` - Altura 300px
- `.chart-container-sm` - Altura 200px
- `.chart-container-lg` - Altura 400px

### Cards
- `.chart-card` - Card com shadow e hover
- `.chart-header` - Cabeçalho do gráfico
- `.chart-actions` - Botões de ação

### Loading
- `.chart-skeleton` - Skeleton loader
- `.chart-loading` - Loading spinner
- `.chart-error` - Estado de erro

---

## 🌐 API Endpoint

**URL:** `GET /api/analytics/charts`

**Parâmetros (opcionais):**
- `?status=Aprovada`
- `?categoria=baby`
- `?colecao=Verão2024`
- `?fornecedor=FornecedorA`

**Resposta:**
```json
{
  "success": true,
  "data": {
    "statusChart": { ... },
    "suppliersChart": { ... },
    "timelineChart": { ... },
    "categoryChart": { ... },
    "sparklines": { ... },
    "mixedChart": { ... },
    "colecoesChart": { ... }
  }
}
```

---

## 📦 Arquivos Criados

```
static/js/
  ├── charts-config.js    # Funções dos gráficos
  └── mock-data.js        # Dados de exemplo

templates/
  └── analytics_charts.html  # Template com exemplos

app.py
  └── /api/analytics/charts  # Endpoint API

static/css/
  └── custom.css          # Estilos dos gráficos (já adicionado)

templates/
  └── base.html           # CDN Chart.js (já adicionado)
```

---

## ✅ Checklist de Integração

- [x] CDN Chart.js adicionado no base.html
- [x] charts-config.js incluído globalmente
- [x] mock-data.js incluído globalmente
- [x] Endpoint API `/api/analytics/charts` criado
- [x] Estilos CSS adicionados
- [x] Template de exemplo criado

---

## 🔍 Exemplo Completo

```html
<!-- HTML -->
<div class="chart-card">
    <div class="chart-header">
        <h5><i class="bi bi-pie-chart-fill"></i> Status das Provas</h5>
        <button onclick="recarregar()">🔄</button>
    </div>
    <div class="chart-container" id="statusContainer">
        <canvas id="statusChart"></canvas>
    </div>
</div>

<!-- JavaScript -->
<script>
async function carregarGrafico() {
    // Mostrar loading
    ChartConfig.showChartLoader('statusContainer');

    try {
        // Buscar dados
        const res = await fetch('/api/analytics/charts');
        const data = await res.json();

        // Recriar canvas
        document.getElementById('statusContainer').innerHTML =
            '<canvas id="statusChart"></canvas>';

        // Criar gráfico
        ChartConfig.createStatusChart(
            'statusChart',
            data.data.statusChart,
            'doughnut'
        );
    } catch (error) {
        // Mostrar erro
        ChartConfig.showChartError('statusContainer', 'Erro ao carregar');
    }
}

function recarregar() {
    ChartConfig.destroyChart('statusChart');
    carregarGrafico();
}

// Carregar ao iniciar
carregarGrafico();
</script>
```

---

## 📱 Responsividade

Todos os gráficos são 100% responsivos:
- ✅ Desktop: altura padrão
- ✅ Tablet: altura reduzida
- ✅ Mobile: altura otimizada
- ✅ Touch-friendly
- ✅ Orientação adaptável

---

## 🎯 Cores do Sistema

```javascript
ChartConfig.COLORS = {
    primary: '#E600AA',    // Pink Puket
    secondary: '#8b5cf6',  // Purple
    success: '#22C55E',    // Green
    danger: '#EF4444',     // Red
    warning: '#F59E0B',    // Orange
    info: '#3B82F6',       // Blue
    gray: '#9CA3AF'
}
```

---

## 🛠️ Troubleshooting

### Gráfico não aparece
1. Verificar se canvas existe: `document.getElementById('canvasId')`
2. Verificar console do navegador
3. Verificar se Chart.js foi carregado: `typeof Chart`
4. Verificar se dados estão corretos

### Erro ao carregar API
1. Verificar endpoint: `/api/analytics/charts`
2. Verificar autenticação (@login_required)
3. Ver logs do Flask
4. Testar no Postman/curl

### Gráfico não é responsivo
1. Verificar `maintainAspectRatio: false`
2. Verificar container tem altura definida
3. Adicionar classe `.chart-container`

---

## 📚 Links Úteis

- **Chart.js Docs:** https://www.chartjs.org/docs/
- **Chart.js Examples:** https://www.chartjs.org/samples/
- **CDN:** https://cdn.jsdelivr.net/npm/chart.js@4.4.0/

---

**Implementado por:** Claude AI
**Data:** 16/01/2025
**Status:** ✅ Completo e funcional
