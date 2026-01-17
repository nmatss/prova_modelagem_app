/**
 * CHARTS-CONFIG.JS
 * Configuração global e funções para criação de gráficos usando Chart.js
 *
 * Biblioteca escolhida: Chart.js v4.4.0
 * - Leve: 64KB minificado
 * - Simples de usar e manter
 * - Suporte completo a todos os tipos de gráficos necessários
 * - Responsivo por padrão
 * - Ótima documentação
 */

// ========================================
// CONFIGURAÇÃO GLOBAL DO CHART.JS
// ========================================

// Cores do tema (seguindo paleta do sistema)
const CHART_COLORS = {
    primary: '#E600AA',      // Pink principal
    secondary: '#8b5cf6',    // Purple
    success: '#22C55E',      // Green
    danger: '#EF4444',       // Red
    warning: '#F59E0B',      // Yellow/Orange
    info: '#3B82F6',         // Blue
    gray: '#9CA3AF',         // Gray
    light: '#F3F4F6',
    dark: '#374151'
};

// Cores para status das provas
const STATUS_COLORS = {
    'Aprovada': CHART_COLORS.success,
    'Reprovada': CHART_COLORS.danger,
    'Em Andamento': CHART_COLORS.warning,
    'Comitê': CHART_COLORS.info,
    'Novo': CHART_COLORS.gray
};

// Cores para categorias
const CATEGORY_COLORS = {
    'baby': '#EC4899',     // Pink
    'kids': '#3B82F6',     // Blue
    'teen': '#10B981',     // Green
    'adulto': '#8B5CF6'    // Purple
};

// Configuração padrão global
const DEFAULT_CHART_OPTIONS = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
        mode: 'index',
        intersect: false
    },
    plugins: {
        legend: {
            display: true,
            position: 'bottom',
            labels: {
                padding: 15,
                font: {
                    family: 'Inter, sans-serif',
                    size: 11
                },
                usePointStyle: true,
                pointStyle: 'circle'
            }
        },
        tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            padding: 12,
            cornerRadius: 8,
            titleFont: {
                size: 13,
                family: 'Inter, sans-serif'
            },
            bodyFont: {
                size: 12,
                family: 'Inter, sans-serif'
            },
            displayColors: true,
            boxPadding: 6
        }
    }
};

// ========================================
// FUNÇÕES DE CRIAÇÃO DE GRÁFICOS
// ========================================

/**
 * PIE/DOUGHNUT CHART - Distribuição por Status
 * @param {string} canvasId - ID do elemento canvas
 * @param {Object} data - Dados do gráfico {labels: [], values: []}
 * @param {string} type - 'pie' ou 'doughnut'
 * @returns {Chart} Instância do gráfico
 */
function createStatusChart(canvasId, data, type = 'doughnut') {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`Canvas #${canvasId} não encontrado`);
        return null;
    }

    // Mapear cores baseado nos labels
    const backgroundColors = data.labels.map(label => STATUS_COLORS[label] || CHART_COLORS.gray);

    return new Chart(ctx, {
        type: type,
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: backgroundColors,
                borderWidth: 2,
                borderColor: '#fff',
                hoverOffset: 8
            }]
        },
        options: {
            ...DEFAULT_CHART_OPTIONS,
            cutout: type === 'doughnut' ? '65%' : '0%',
            plugins: {
                ...DEFAULT_CHART_OPTIONS.plugins,
                legend: {
                    ...DEFAULT_CHART_OPTIONS.plugins.legend,
                    position: 'right'
                },
                tooltip: {
                    ...DEFAULT_CHART_OPTIONS.plugins.tooltip,
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * BAR CHART HORIZONTAL - Top Fornecedores
 * @param {string} canvasId - ID do elemento canvas
 * @param {Object} data - Dados {suppliers: [], counts: []}
 * @returns {Chart} Instância do gráfico
 */
function createSuppliersChart(canvasId, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`Canvas #${canvasId} não encontrado`);
        return null;
    }

    // Criar gradiente
    const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 400, 0);
    gradient.addColorStop(0, CHART_COLORS.primary);
    gradient.addColorStop(1, CHART_COLORS.secondary);

    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.suppliers,
            datasets: [{
                label: 'Relatórios',
                data: data.counts,
                backgroundColor: gradient,
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            ...DEFAULT_CHART_OPTIONS,
            indexAxis: 'y', // Barras horizontais
            plugins: {
                ...DEFAULT_CHART_OPTIONS.plugins,
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        font: {
                            family: 'Inter, sans-serif'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                y: {
                    ticks: {
                        font: {
                            family: 'Inter, sans-serif',
                            size: 11
                        }
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

/**
 * AREA CHART - Tendência Temporal
 * @param {string} canvasId - ID do elemento canvas
 * @param {Object} data - Dados {months: [], counts: []}
 * @returns {Chart} Instância do gráfico
 */
function createTimelineChart(canvasId, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`Canvas #${canvasId} não encontrado`);
        return null;
    }

    // Criar gradiente de fundo
    const gradientFill = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
    gradientFill.addColorStop(0, 'rgba(230, 0, 170, 0.2)');
    gradientFill.addColorStop(1, 'rgba(230, 0, 170, 0.02)');

    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.months,
            datasets: [{
                label: 'Relatórios Criados',
                data: data.counts,
                fill: true,
                backgroundColor: gradientFill,
                borderColor: CHART_COLORS.primary,
                borderWidth: 3,
                tension: 0.4,
                pointRadius: 5,
                pointHoverRadius: 7,
                pointBackgroundColor: CHART_COLORS.primary,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointHoverBackgroundColor: CHART_COLORS.primary,
                pointHoverBorderColor: '#fff',
                pointHoverBorderWidth: 3
            }]
        },
        options: {
            ...DEFAULT_CHART_OPTIONS,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                ...DEFAULT_CHART_OPTIONS.plugins,
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        font: {
                            family: 'Inter, sans-serif'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    ticks: {
                        font: {
                            family: 'Inter, sans-serif'
                        }
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

/**
 * BAR CHART - Distribuição por Categoria
 * @param {string} canvasId - ID do elemento canvas
 * @param {Object} data - Dados {categories: [], counts: []}
 * @returns {Chart} Instância do gráfico
 */
function createCategoryChart(canvasId, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`Canvas #${canvasId} não encontrado`);
        return null;
    }

    // Mapear cores baseado nas categorias
    const backgroundColors = data.categories.map(cat => CATEGORY_COLORS[cat] || CHART_COLORS.gray);

    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.categories.map(c => c.charAt(0).toUpperCase() + c.slice(1)),
            datasets: [{
                label: 'Referências',
                data: data.counts,
                backgroundColor: backgroundColors,
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            ...DEFAULT_CHART_OPTIONS,
            plugins: {
                ...DEFAULT_CHART_OPTIONS.plugins,
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        font: {
                            family: 'Inter, sans-serif'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    ticks: {
                        font: {
                            family: 'Inter, sans-serif'
                        }
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

/**
 * SPARKLINE - Mini gráfico para KPIs
 * @param {string} canvasId - ID do elemento canvas
 * @param {Array} values - Array de valores
 * @param {string} color - Cor da linha (opcional)
 * @returns {Chart} Instância do gráfico
 */
function createSparkline(canvasId, values, color = CHART_COLORS.success) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`Canvas #${canvasId} não encontrado`);
        return null;
    }

    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array(values.length).fill(''),
            datasets: [{
                data: values,
                borderColor: color,
                borderWidth: 2,
                pointRadius: 0,
                pointHoverRadius: 3,
                fill: false,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            },
            scales: {
                x: { display: false },
                y: { display: false }
            },
            interaction: {
                mode: 'nearest',
                intersect: false
            }
        }
    });
}

/**
 * MIXED CHART - Gráfico combinado (Barras + Linha)
 * @param {string} canvasId - ID do elemento canvas
 * @param {Object} data - Dados {labels: [], dataset1: [], dataset2: []}
 * @returns {Chart} Instância do gráfico
 */
function createMixedChart(canvasId, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`Canvas #${canvasId} não encontrado`);
        return null;
    }

    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [
                {
                    type: 'bar',
                    label: 'Total Provas',
                    data: data.totalProvas,
                    backgroundColor: 'rgba(59, 130, 246, 0.5)',
                    borderColor: CHART_COLORS.info,
                    borderWidth: 2,
                    borderRadius: 6
                },
                {
                    type: 'line',
                    label: 'Taxa de Aprovação (%)',
                    data: data.taxaAprovacao,
                    borderColor: CHART_COLORS.success,
                    backgroundColor: 'rgba(34, 197, 94, 0.1)',
                    borderWidth: 3,
                    tension: 0.4,
                    yAxisID: 'y1',
                    pointRadius: 4,
                    pointHoverRadius: 6
                }
            ]
        },
        options: {
            ...DEFAULT_CHART_OPTIONS,
            scales: {
                y: {
                    type: 'linear',
                    position: 'left',
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        font: { family: 'Inter, sans-serif' }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                y1: {
                    type: 'linear',
                    position: 'right',
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        },
                        font: { family: 'Inter, sans-serif' }
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                },
                x: {
                    ticks: {
                        font: { family: 'Inter, sans-serif' }
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// ========================================
// UTILITÁRIOS
// ========================================

/**
 * Destrói um gráfico existente antes de criar um novo
 * @param {string} canvasId - ID do canvas
 */
function destroyChart(canvasId) {
    const canvas = document.getElementById(canvasId);
    if (canvas && canvas.chart) {
        canvas.chart.destroy();
    }
}

/**
 * Mostra skeleton loader enquanto carrega
 * @param {string} containerId - ID do container
 */
function showChartLoader(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="chart-skeleton">
                <div class="skeleton-bar" style="height: 60%; animation-delay: 0s;"></div>
                <div class="skeleton-bar" style="height: 80%; animation-delay: 0.1s;"></div>
                <div class="skeleton-bar" style="height: 40%; animation-delay: 0.2s;"></div>
                <div class="skeleton-bar" style="height: 90%; animation-delay: 0.3s;"></div>
                <div class="skeleton-bar" style="height: 70%; animation-delay: 0.4s;"></div>
            </div>
        `;
    }
}

/**
 * Mostra mensagem de erro no container do gráfico
 * @param {string} containerId - ID do container
 * @param {string} message - Mensagem de erro
 */
function showChartError(containerId, message = 'Erro ao carregar gráfico') {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="chart-error">
                <i class="bi bi-exclamation-triangle-fill text-warning"></i>
                <p class="mt-2 mb-0 text-muted">${message}</p>
            </div>
        `;
    }
}

/**
 * Formata números grandes (1000 -> 1K)
 * @param {number} num - Número para formatar
 * @returns {string} Número formatado
 */
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

// ========================================
// EXPORTAR PARA ESCOPO GLOBAL
// ========================================

window.ChartConfig = {
    // Constantes
    COLORS: CHART_COLORS,
    STATUS_COLORS,
    CATEGORY_COLORS,

    // Funções de criação
    createStatusChart,
    createSuppliersChart,
    createTimelineChart,
    createCategoryChart,
    createSparkline,
    createMixedChart,

    // Utilitários
    destroyChart,
    showChartLoader,
    showChartError,
    formatNumber
};

console.log('Charts Config loaded successfully');
