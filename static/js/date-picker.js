// ========================================
// DATE PICKER ENHANCEMENTS
// Sistema de validação e formatação para inputs HTML5 type="date"
// ========================================

document.addEventListener('DOMContentLoaded', function() {

    // ========================================
    // CONFIGURAÇÕES E CONSTANTES
    // ========================================

    const DATE_CONFIG = {
        locale: 'pt-BR',
        format: 'DD/MM/YYYY',
        isoFormat: 'YYYY-MM-DD',
        minDate: '1900-01-01',
        maxDate: new Date().toISOString().split('T')[0], // hoje
        futureMaxDate: '2100-12-31'
    };

    // ========================================
    // UTILITÁRIOS DE DATA
    // ========================================

    /**
     * Formata uma data ISO para o formato brasileiro
     * @param {string} isoDate - Data no formato YYYY-MM-DD
     * @returns {string} Data no formato DD/MM/YYYY
     */
    function formatDateToBR(isoDate) {
        if (!isoDate) return '';
        const [year, month, day] = isoDate.split('-');
        return `${day}/${month}/${year}`;
    }

    /**
     * Converte uma data brasileira para ISO
     * @param {string} brDate - Data no formato DD/MM/YYYY
     * @returns {string} Data no formato YYYY-MM-DD
     */
    function formatDateToISO(brDate) {
        if (!brDate) return '';
        const [day, month, year] = brDate.split('/');
        return `${year}-${month}-${day}`;
    }

    /**
     * Valida se uma data é válida
     * @param {string} dateString - Data a ser validada
     * @returns {boolean}
     */
    function isValidDate(dateString) {
        if (!dateString) return false;
        const date = new Date(dateString);
        return date instanceof Date && !isNaN(date);
    }

    /**
     * Compara duas datas
     * @param {string} date1 - Primeira data (ISO)
     * @param {string} date2 - Segunda data (ISO)
     * @returns {number} -1 se date1 < date2, 0 se iguais, 1 se date1 > date2
     */
    function compareDates(date1, date2) {
        const d1 = new Date(date1);
        const d2 = new Date(date2);
        return d1 < d2 ? -1 : d1 > d2 ? 1 : 0;
    }

    /**
     * Calcula a diferença em dias entre duas datas
     * @param {string} startDate - Data inicial (ISO)
     * @param {string} endDate - Data final (ISO)
     * @returns {number} Número de dias
     */
    function daysDifference(startDate, endDate) {
        const d1 = new Date(startDate);
        const d2 = new Date(endDate);
        const diffTime = Math.abs(d2 - d1);
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    }

    // ========================================
    // VALIDAÇÃO DE RANGE DE DATAS
    // ========================================

    /**
     * Configura validação para um par de inputs de data (início/fim)
     * @param {HTMLElement} startInput - Input de data inicial
     * @param {HTMLElement} endInput - Input de data final
     */
    function setupDateRangeValidation(startInput, endInput) {
        if (!startInput || !endInput) return;

        const validateRange = () => {
            const startDate = startInput.value;
            const endDate = endInput.value;

            // Remove mensagens de erro anteriores
            removeErrorMessage(startInput);
            removeErrorMessage(endInput);

            if (startDate && endDate) {
                if (compareDates(startDate, endDate) > 0) {
                    // Data final anterior à data inicial
                    showErrorMessage(endInput, 'A data final deve ser posterior à data inicial');
                    endInput.classList.add('is-invalid');
                    startInput.classList.add('is-invalid');
                    return false;
                } else {
                    // Válido
                    endInput.classList.remove('is-invalid');
                    startInput.classList.remove('is-invalid');
                    endInput.classList.add('is-valid');
                    startInput.classList.add('is-valid');

                    // Mostra a diferença em dias
                    const days = daysDifference(startDate, endDate);
                    showInfoMessage(endInput, `Período de ${days} dia(s)`);
                    return true;
                }
            }
            return true;
        };

        startInput.addEventListener('change', validateRange);
        endInput.addEventListener('change', validateRange);
        startInput.addEventListener('blur', validateRange);
        endInput.addEventListener('blur', validateRange);

        // Validação inicial
        validateRange();
    }

    /**
     * Mostra mensagem de erro abaixo do input
     * @param {HTMLElement} input
     * @param {string} message
     */
    function showErrorMessage(input, message) {
        removeErrorMessage(input);
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback d-block';
        errorDiv.textContent = message;
        errorDiv.setAttribute('data-error-for', input.id || input.name);
        input.parentElement.appendChild(errorDiv);
    }

    /**
     * Mostra mensagem informativa abaixo do input
     * @param {HTMLElement} input
     * @param {string} message
     */
    function showInfoMessage(input, message) {
        removeInfoMessage(input);
        const infoDiv = document.createElement('div');
        infoDiv.className = 'form-text text-success';
        infoDiv.innerHTML = `<i class="bi bi-info-circle me-1"></i>${message}`;
        infoDiv.setAttribute('data-info-for', input.id || input.name);
        input.parentElement.appendChild(infoDiv);
    }

    /**
     * Remove mensagem de erro
     * @param {HTMLElement} input
     */
    function removeErrorMessage(input) {
        const errorDiv = input.parentElement.querySelector(`[data-error-for="${input.id || input.name}"]`);
        if (errorDiv) errorDiv.remove();
    }

    /**
     * Remove mensagem informativa
     * @param {HTMLElement} input
     */
    function removeInfoMessage(input) {
        const infoDiv = input.parentElement.querySelector(`[data-info-for="${input.id || input.name}"]`);
        if (infoDiv) infoDiv.remove();
    }

    // ========================================
    // CONFIGURAÇÃO AUTOMÁTICA DE LIMITES
    // ========================================

    /**
     * Configura limites min/max para inputs de data
     * @param {HTMLElement} input
     */
    function setupDateLimits(input) {
        // Se o campo permite datas futuras (ex: data de liberação)
        const allowFuture = input.hasAttribute('data-allow-future');

        if (!input.hasAttribute('min')) {
            input.setAttribute('min', DATE_CONFIG.minDate);
        }

        if (!input.hasAttribute('max')) {
            input.setAttribute('max', allowFuture ? DATE_CONFIG.futureMaxDate : DATE_CONFIG.maxDate);
        }
    }

    // ========================================
    // DETECÇÃO AUTOMÁTICA DE DATE RANGES
    // ========================================

    /**
     * Detecta pares de inputs de data_inicio e data_fim e configura validação
     */
    function autoDetectDateRanges() {
        // Procura por inputs com nome data_inicio
        const startInputs = document.querySelectorAll('input[type="date"][name*="data_inicio"], input[type="date"][name*="data_recebimento"]');

        startInputs.forEach(startInput => {
            // Tenta encontrar o input correspondente de data_fim ou data_prova
            const baseName = startInput.name.replace('data_inicio', '').replace('data_recebimento', '');
            let endInput = document.querySelector(`input[type="date"][name*="data_fim"]${baseName ? `[name*="${baseName}"]` : ''}`);

            if (!endInput) {
                endInput = document.querySelector(`input[type="date"][name*="data_prova"]${baseName ? `[name*="${baseName}"]` : ''}`);
            }

            if (endInput) {
                setupDateRangeValidation(startInput, endInput);
            }
        });

        // Também procura por data de recebimento vs data de prova
        const recebimentoInputs = document.querySelectorAll('input[type="date"][name*="data_recebimento"]');
        recebimentoInputs.forEach(recInput => {
            const idMatch = recInput.name.match(/data_recebimento_(.+)/);
            if (idMatch) {
                const suffix = idMatch[1];
                const provaInput = document.querySelector(`input[type="date"][name="data_prova_${suffix}"]`);
                if (provaInput) {
                    setupDateRangeValidation(recInput, provaInput);
                }
            }
        });

        // Validação específica para analytics (data_inicio e data_fim sem sufixo)
        const analyticsStartInput = document.querySelector('input[type="date"][name="data_inicio"]');
        const analyticsEndInput = document.querySelector('input[type="date"][name="data_fim"]');

        if (analyticsStartInput && analyticsEndInput) {
            setupDateRangeValidation(analyticsStartInput, analyticsEndInput);
        }
    }

    // ========================================
    // MELHORIAS VISUAIS
    // ========================================

    /**
     * Adiciona ícone de calendário aos inputs de data
     * @param {HTMLElement} input
     */
    function enhanceDateInput(input) {
        // Adiciona classe para estilização
        input.classList.add('date-input-enhanced');

        // Wrapper para posicionar o ícone
        if (!input.parentElement.classList.contains('date-input-wrapper')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'date-input-wrapper position-relative';
            input.parentElement.insertBefore(wrapper, input);
            wrapper.appendChild(input);

            // Ícone de calendário
            const icon = document.createElement('i');
            icon.className = 'bi bi-calendar3 date-input-icon';
            icon.style.cssText = 'position: absolute; right: 12px; top: 50%; transform: translateY(-50%); pointer-events: none; color: #6c757d; font-size: 1.1rem;';
            wrapper.appendChild(icon);
        }

        // Placeholder melhorado
        if (!input.hasAttribute('placeholder')) {
            input.setAttribute('placeholder', 'dd/mm/aaaa');
        }

        // Configurar limites
        setupDateLimits(input);
    }

    // ========================================
    // INICIALIZAÇÃO
    // ========================================

    /**
     * Inicializa todos os date pickers na página
     */
    function initializeDatePickers() {
        // Seleciona todos os inputs type="date"
        const dateInputs = document.querySelectorAll('input[type="date"]');

        dateInputs.forEach(input => {
            enhanceDateInput(input);
        });

        // Configura validação de ranges automaticamente
        autoDetectDateRanges();

        console.log(`✅ Date Picker initialized for ${dateInputs.length} input(s)`);
    }

    // ========================================
    // COMPONENTE DATE RANGE PICKER
    // ========================================

    /**
     * Cria um componente de date range picker
     * @param {Object} options - Opções do componente
     * @returns {HTMLElement}
     */
    function createDateRangePicker(options = {}) {
        const {
            containerClass = 'date-range-picker',
            startName = 'data_inicio',
            endName = 'data_fim',
            startLabel = 'Data Início',
            endLabel = 'Data Fim',
            startValue = '',
            endValue = '',
            required = false
        } = options;

        const container = document.createElement('div');
        container.className = containerClass;
        container.innerHTML = `
            <div class="row g-3">
                <div class="col-md-6">
                    <label class="form-label">${startLabel}${required ? ' <span class="text-danger">*</span>' : ''}</label>
                    <input type="date" class="form-control" name="${startName}" value="${startValue}" ${required ? 'required' : ''}>
                </div>
                <div class="col-md-6">
                    <label class="form-label">${endLabel}${required ? ' <span class="text-danger">*</span>' : ''}</label>
                    <input type="date" class="form-control" name="${endName}" value="${endValue}" ${required ? 'required' : ''}>
                </div>
            </div>
        `;

        // Inicializar validação
        setTimeout(() => {
            const startInput = container.querySelector(`[name="${startName}"]`);
            const endInput = container.querySelector(`[name="${endName}"]`);
            enhanceDateInput(startInput);
            enhanceDateInput(endInput);
            setupDateRangeValidation(startInput, endInput);
        }, 100);

        return container;
    }

    // ========================================
    // API PÚBLICA
    // ========================================

    // Expõe funções úteis globalmente
    window.DatePickerUtils = {
        formatDateToBR,
        formatDateToISO,
        isValidDate,
        compareDates,
        daysDifference,
        setupDateRangeValidation,
        createDateRangePicker
    };

    // ========================================
    // EXECUÇÃO
    // ========================================

    initializeDatePickers();

    console.log('✅ Date Picker module loaded successfully!');
});
