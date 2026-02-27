/**
 * WIZARD MULTI-STEP - JAVASCRIPT
 * Sistema de Prova de Modelagem
 * Navegação, validação e auto-save
 */

class ReportWizard {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 3;
        this.formData = this.loadFromStorage() || {};

        this.init();
    }

    init() {
        this.setupElements();
        this.setupEventListeners();
        this.updateProgress();
        this.restoreFormData();
        this.setupAutoSave();
    }

    setupElements() {
        this.form = document.getElementById('wizardForm');
        this.prevBtn = document.getElementById('prevBtn');
        this.nextBtn = document.getElementById('nextBtn');
        this.submitBtn = document.getElementById('submitBtn');
        this.progressLine = document.querySelector('.wizard-progress-line');
        this.stepIndicators = document.querySelectorAll('.wizard-step');
        this.stepContents = document.querySelectorAll('.wizard-step-content');
    }

    setupEventListeners() {
        // Botões de navegação
        this.prevBtn?.addEventListener('click', () => this.previousStep());
        this.nextBtn?.addEventListener('click', () => this.nextStep());

        // Clique nos indicadores de step
        this.stepIndicators.forEach((step, index) => {
            step.addEventListener('click', () => {
                const stepNumber = index + 1;
                if (stepNumber < this.currentStep || step.classList.contains('completed')) {
                    this.goToStep(stepNumber);
                }
            });
        });

        // Preview de imagem
        const imagemProdutoInput = document.getElementById('imagem_produto');
        if (imagemProdutoInput) {
            imagemProdutoInput.addEventListener('change', (e) => this.previewImage(e));
        }

        // File upload displays
        this.setupFileDisplays();

        // Form submit
        this.form?.addEventListener('submit', (e) => this.handleSubmit(e));

        // Auto-save em mudanças de input
        this.form?.addEventListener('input', () => {
            this.saveToStorage();
        });
    }

    setupFileDisplays() {
        const fileInputs = this.form?.querySelectorAll('input[type="file"]');
        fileInputs?.forEach(input => {
            input.addEventListener('change', (e) => {
                const files = e.target.files;
                const displayId = `${input.id}_display`;
                let display = document.getElementById(displayId);

                if (!display) {
                    display = document.createElement('div');
                    display.id = displayId;
                    display.className = 'file-name-display';
                    input.parentElement.appendChild(display);
                }

                if (files.length > 0) {
                    const fileNames = Array.from(files).map(f => f.name).join(', ');
                    display.textContent = `📎 ${fileNames}`;
                    display.classList.add('show');
                } else {
                    display.classList.remove('show');
                }
            });
        });
    }

    previewImage(event) {
        const file = event.target.files[0];
        const previewContainer = document.getElementById('image_preview_container');

        if (!previewContainer) {
            const container = document.createElement('div');
            container.id = 'image_preview_container';
            container.className = 'image-preview-container';
            event.target.parentElement.appendChild(container);
        }

        const container = document.getElementById('image_preview_container');

        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                container.innerHTML = `
                    <img src="${e.target.result}" alt="Preview" class="image-preview">
                `;
            };
            reader.readAsDataURL(file);
        } else {
            container.innerHTML = '';
        }
    }

    nextStep() {
        if (this.validateCurrentStep()) {
            this.markStepAsCompleted(this.currentStep);
            this.saveToStorage();

            if (this.currentStep < this.totalSteps) {
                this.currentStep++;
                this.updateProgress();
            }
        }
    }

    previousStep() {
        if (this.currentStep > 1) {
            this.currentStep--;
            this.updateProgress();
        }
    }

    goToStep(stepNumber) {
        if (stepNumber >= 1 && stepNumber <= this.totalSteps) {
            this.currentStep = stepNumber;
            this.updateProgress();
        }
    }

    updateProgress() {
        // Atualizar indicadores de step
        this.stepIndicators.forEach((step, index) => {
            const stepNumber = index + 1;
            step.classList.remove('active');

            if (stepNumber === this.currentStep) {
                step.classList.add('active');
            }
        });

        // Atualizar conteúdo dos steps
        this.stepContents.forEach((content, index) => {
            content.classList.remove('active');
            if (index + 1 === this.currentStep) {
                content.classList.add('active');
            }
        });

        // Atualizar barra de progresso
        const progress = ((this.currentStep - 1) / (this.totalSteps - 1)) * 100;
        if (this.progressLine) {
            this.progressLine.style.width = `${progress}%`;
        }

        // Atualizar botões
        this.updateButtons();

        // Popular revisão ao chegar no último step
        if (this.currentStep === this.totalSteps) {
            this.populateReview();
        }
    }

    updateButtons() {
        // Botão Anterior
        if (this.prevBtn) {
            this.prevBtn.disabled = this.currentStep === 1;
            this.prevBtn.style.visibility = this.currentStep === 1 ? 'hidden' : 'visible';
        }

        // Botões Próximo e Finalizar
        if (this.currentStep === this.totalSteps) {
            if (this.nextBtn) this.nextBtn.style.display = 'none';
            if (this.submitBtn) this.submitBtn.style.display = 'inline-flex';
        } else {
            if (this.nextBtn) this.nextBtn.style.display = 'inline-flex';
            if (this.submitBtn) this.submitBtn.style.display = 'none';
        }
    }

    markStepAsCompleted(stepNumber) {
        const stepIndicator = this.stepIndicators[stepNumber - 1];
        if (stepIndicator && !stepIndicator.classList.contains('completed')) {
            stepIndicator.classList.add('completed');
        }
    }

    validateCurrentStep() {
        let isValid = true;
        const currentContent = this.stepContents[this.currentStep - 1];

        // Remover mensagens de validação anteriores
        this.clearValidationMessages();

        switch(this.currentStep) {
            case 1: // Info + Categoria + Referência
                isValid = this.validateStep1(currentContent);
                if (isValid) isValid = this.validateCategory();
                if (isValid) isValid = this.validateReference();
                break;
            case 2: // Prova de Modelagem
                isValid = true; // Optional
                break;
            case 3: // Revisão
                isValid = true;
                this.populateReview();
                break;
        }

        return isValid;
    }

    validateStep1(content) {
        const colecao = content.querySelector('#colecao');
        const descricao = content.querySelector('#descricao_geral');

        if (!colecao?.value.trim()) {
            this.showValidationMessage(colecao, 'Por favor, informe a coleção');
            return false;
        }

        if (!descricao?.value.trim()) {
            this.showValidationMessage(descricao, 'Por favor, informe a descrição geral');
            return false;
        }

        return true;
    }

    validateCategory() {
        const categoryCheckboxes = document.querySelectorAll('input[name="tipo_produto"]');
        const isSelected = Array.from(categoryCheckboxes).some(cb => cb.checked);

        if (!isSelected) {
            this.showValidationMessage(
                categoryCheckboxes[0].closest('.category-selection'),
                'Por favor, selecione pelo menos uma categoria'
            );
            return false;
        }

        return true;
    }

    validateReference() {
        const selectedCategories = document.querySelectorAll('input[name="tipo_produto"]:checked');
        if (selectedCategories.length === 0) return false;

        for (const cat of selectedCategories) {
            const tipo = cat.value;
            const refInput = document.getElementById(`ref_${tipo}`);

            if (!refInput?.value.trim()) {
                this.showValidationMessage(refInput, `Por favor, informe a referência ${tipo}`);
                return false;
            }
        }

        return true;
    }

    showValidationMessage(element, message) {
        if (!element) return;

        let msgDiv = element.parentElement.querySelector('.validation-message');

        if (!msgDiv) {
            msgDiv = document.createElement('div');
            msgDiv.className = 'validation-message';
            element.parentElement.appendChild(msgDiv);
        }

        msgDiv.innerHTML = `<i class="bi bi-exclamation-circle-fill"></i> ${message}`;
        msgDiv.classList.add('show');

        // Scroll para o elemento
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        element.focus();
    }

    clearValidationMessages() {
        const messages = this.form?.querySelectorAll('.validation-message.show');
        messages?.forEach(msg => msg.classList.remove('show'));
    }

    populateReview() {
        // Informações Gerais
        this.setReviewValue('review_colecao', document.getElementById('colecao')?.value);
        this.setReviewValue('review_descricao', document.getElementById('descricao_geral')?.value);

        // Linha
        const linha = document.getElementById('linha')?.value;
        this.setReviewValue('review_linha', linha || 'Não informado');

        const pptFile = document.getElementById('ppt')?.files[0];
        this.setReviewValue('review_ppt', pptFile ? pptFile.name : 'Não enviado');

        const imagemFile = document.getElementById('imagem_produto')?.files[0];
        this.setReviewValue('review_imagem', imagemFile ? imagemFile.name : 'Não enviado');

        const fichaFile = document.getElementById('ficha_tecnica')?.files[0];
        this.setReviewValue('review_ficha', fichaFile ? fichaFile.name : 'Não enviado');

        // Categorias (múltipla seleção)
        const categorias = document.querySelectorAll('input[name="tipo_produto"]:checked');
        const categoriasNomes = Array.from(categorias).map(cb => cb.value.toUpperCase());
        this.setReviewValue('review_categoria', categoriasNomes.length > 0 ? categoriasNomes.join(', ') : 'Não selecionado');

        // Dados por categoria - agregar de todas as selecionadas
        const refs = [], origens = [], fornecedores = [], materias = [], composicoes = [], gramaturas = [], aviamentosList = [];
        const datasReceb = [], datasProva = [], tamanhosList = [];
        let totalFotos = 0;
        const qualResps = [], qualItems = [], qualComents = [], qualObsList = [];
        const estResps = [], estItems = [], estComents = [], estObsList = [];
        const modResps = [], modItems = [], modComents = [], modObsList = [];
        const datasLacre = [], numerosLacre = [], infosAdicionais = [];

        categorias.forEach(cat => {
            const tipo = cat.value;
            const label = tipo.toUpperCase();

            const ref = document.getElementById(`ref_${tipo}`)?.value;
            if (ref) refs.push(`[${label}] ${ref}`);

            const origem = document.querySelector(`select[name="origem_${tipo}"]`)?.value;
            if (origem) origens.push(`[${label}] ${origem}`);

            const fornecedor = document.querySelector(`input[name="fornecedor_${tipo}"]`)?.value;
            if (fornecedor) fornecedores.push(`[${label}] ${fornecedor}`);

            const materiaPrima = document.querySelector(`input[name="materia_prima_${tipo}"]`)?.value;
            if (materiaPrima) materias.push(`[${label}] ${materiaPrima}`);

            const composicao = document.querySelector(`input[name="composicao_${tipo}"]`)?.value;
            if (composicao) composicoes.push(`[${label}] ${composicao}`);

            const gramatura = document.querySelector(`input[name="gramatura_${tipo}"]`)?.value;
            if (gramatura) gramaturas.push(`[${label}] ${gramatura}`);

            const aviamentos = document.querySelector(`input[name="aviamentos_${tipo}"]`)?.value;
            if (aviamentos) aviamentosList.push(`[${label}] ${aviamentos}`);

            const dataReceb = document.querySelector(`input[name="data_recebimento_${tipo}"]`)?.value;
            if (dataReceb) datasReceb.push(`[${label}] ${dataReceb}`);

            const dataProva = document.querySelector(`input[name="data_prova_${tipo}"]`)?.value;
            if (dataProva) datasProva.push(`[${label}] ${dataProva}`);

            const tamanhos = Array.from(document.querySelectorAll(`input[name="tamanhos_recebidos_${tipo}"]:checked`)).map(cb => cb.value);
            if (tamanhos.length > 0) tamanhosList.push(`[${label}] ${tamanhos.join(', ')}`);

            const fileInputs = document.querySelectorAll(`#prova_section_${tipo} input[type="file"]`);
            fileInputs.forEach(input => { totalFotos += input.files.length; });

            const qr = document.querySelector(`input[name="time_qualidade_${tipo}"]`)?.value;
            if (qr) qualResps.push(`[${label}] ${qr}`);
            const qc = Array.from(document.querySelectorAll(`input[name="checklist_qualidade_${tipo}"]:checked`)).map(cb => cb.value.replace(/_/g, ' ').toLowerCase());
            if (qc.length) qualItems.push(`[${label}] ${qc.join(', ')}`);
            const qcom = document.querySelector(`textarea[name="comentarios_qualidade_${tipo}"]`)?.value;
            if (qcom) qualComents.push(`[${label}] ${qcom}`);
            const qobs = document.querySelector(`textarea[name="obs_qualidade_${tipo}"]`)?.value;
            if (qobs) qualObsList.push(`[${label}] ${qobs}`);

            const er = document.querySelector(`input[name="time_estilo_${tipo}"]`)?.value;
            if (er) estResps.push(`[${label}] ${er}`);
            const ec = Array.from(document.querySelectorAll(`input[name="checklist_estilo_${tipo}"]:checked`)).map(cb => cb.value.replace(/_/g, ' ').toLowerCase());
            if (ec.length) estItems.push(`[${label}] ${ec.join(', ')}`);
            const ecom = document.querySelector(`textarea[name="comentarios_estilo_${tipo}"]`)?.value;
            if (ecom) estComents.push(`[${label}] ${ecom}`);
            const eobs = document.querySelector(`textarea[name="obs_estilo_${tipo}"]`)?.value;
            if (eobs) estObsList.push(`[${label}] ${eobs}`);

            const mr = document.querySelector(`input[name="time_modelagem_${tipo}"]`)?.value;
            if (mr) modResps.push(`[${label}] ${mr}`);
            const mc = Array.from(document.querySelectorAll(`input[name="checklist_modelagem_${tipo}"]:checked`)).map(cb => cb.value.replace(/_/g, ' ').toLowerCase());
            if (mc.length) modItems.push(`[${label}] ${mc.join(', ')}`);
            const mcom = document.querySelector(`textarea[name="comentarios_modelagem_${tipo}"]`)?.value;
            if (mcom) modComents.push(`[${label}] ${mcom}`);
            const mobs = document.querySelector(`textarea[name="obs_modelagem_${tipo}"]`)?.value;
            if (mobs) modObsList.push(`[${label}] ${mobs}`);

            const dl = document.querySelector(`input[name="data_lacre_${tipo}"]`)?.value;
            if (dl) datasLacre.push(`[${label}] ${dl}`);
            const nl = document.querySelector(`input[name="numero_lacre_${tipo}"]`)?.value;
            if (nl) numerosLacre.push(`[${label}] ${nl}`);
            const ia = document.querySelector(`textarea[name="info_adicionais_${tipo}"]`)?.value;
            if (ia) infosAdicionais.push(`[${label}] ${ia}`);
        });

        this.setReviewValue('review_referencia', refs.join(' | ') || 'Não informado');
        this.setReviewValue('review_origem', origens.join(' | ') || 'Não informado');
        this.setReviewValue('review_fornecedor', fornecedores.join(' | ') || 'Não informado');
        this.setReviewValue('review_materia_prima', materias.join(' | ') || 'Não informado');
        this.setReviewValue('review_composicao', composicoes.join(' | ') || 'Não informado');
        this.setReviewValue('review_gramatura', gramaturas.join(' | ') || 'Não informado');
        this.setReviewValue('review_aviamentos', aviamentosList.join(' | ') || 'Não informado');
        this.setReviewValue('review_data_recebimento', datasReceb.join(' | ') || 'Não informado');
        this.setReviewValue('review_data_prova', datasProva.join(' | ') || 'Não informado');
        this.setReviewValue('review_tamanhos', tamanhosList.join(' | ') || 'Nenhum selecionado');
        this.setReviewValue('review_fotos_count', totalFotos > 0 ? `${totalFotos} arquivo(s)` : 'Nenhum');
        this.setReviewValue('review_qualidade_resp', qualResps.join(' | ') || 'Não informado');
        this.setReviewValue('review_qualidade', qualItems.join(' | ') || 'Sem itens');
        this.setReviewValue('review_qualidade_comentarios', qualComents.join(' | ') || 'Sem comentários');
        this.setReviewValue('review_qualidade_obs', qualObsList.join(' | ') || 'Sem observações');
        this.setReviewValue('review_estilo_resp', estResps.join(' | ') || 'Não informado');
        this.setReviewValue('review_estilo', estItems.join(' | ') || 'Sem itens');
        this.setReviewValue('review_estilo_comentarios', estComents.join(' | ') || 'Sem comentários');
        this.setReviewValue('review_estilo_obs', estObsList.join(' | ') || 'Sem observações');
        this.setReviewValue('review_modelagem_resp', modResps.join(' | ') || 'Não informado');
        this.setReviewValue('review_modelagem', modItems.join(' | ') || 'Sem itens');
        this.setReviewValue('review_modelagem_comentarios', modComents.join(' | ') || 'Sem comentários');
        this.setReviewValue('review_modelagem_obs', modObsList.join(' | ') || 'Sem observações');
        this.setReviewValue('review_data_lacre', datasLacre.join(' | ') || 'Não informado');
        this.setReviewValue('review_numero_lacre', numerosLacre.join(' | ') || 'Não informado');
        this.setReviewValue('review_info_adicionais', infosAdicionais.join(' | ') || 'Não informado');

        // Preview da imagem se existir
        const imagemPreview = document.getElementById('image_preview_container');
        const reviewImageContainer = document.getElementById('review_image_preview');
        if (imagemPreview && reviewImageContainer) {
            reviewImageContainer.innerHTML = imagemPreview.innerHTML;
        }
    }

    setReviewValue(elementId, value) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = value || 'Não informado';
        }
    }

    saveToStorage() {
        if (!this.form) return;

        const formData = new FormData(this.form);
        const data = {};

        // Salvar apenas valores de texto (não arquivos)
        for (let [key, value] of formData.entries()) {
            if (typeof value === 'string') {
                data[key] = value;
            }
        }

        data.currentStep = this.currentStep;
        data.timestamp = new Date().toISOString();

        try {
            localStorage.setItem('wizard_draft', JSON.stringify(data));
            this.showDraftIndicator();
        } catch (e) {
            console.warn('Não foi possível salvar o rascunho:', e);
        }
    }

    loadFromStorage() {
        try {
            const stored = localStorage.getItem('wizard_draft');
            if (stored) {
                const data = JSON.parse(stored);

                // Verificar se o rascunho não é muito antigo (24 horas)
                const timestamp = new Date(data.timestamp);
                const now = new Date();
                const hoursDiff = (now - timestamp) / (1000 * 60 * 60);

                if (hoursDiff < 24) {
                    return data;
                } else {
                    localStorage.removeItem('wizard_draft');
                }
            }
        } catch (e) {
            console.warn('Não foi possível carregar o rascunho:', e);
        }
        return null;
    }

    restoreFormData() {
        if (!this.formData || Object.keys(this.formData).length === 0) return;

        // Restaurar valores dos campos
        for (let [key, value] of Object.entries(this.formData)) {
            if (key === 'currentStep' || key === 'timestamp') continue;

            const input = this.form?.querySelector(`[name="${key}"]`);
            if (input) {
                if (input.type === 'radio' || input.type === 'checkbox') {
                    if (input.value === value) {
                        input.checked = true;
                    }
                } else {
                    input.value = value;
                }
            }
        }

        // Restaurar step atual
        if (this.formData.currentStep) {
            this.currentStep = this.formData.currentStep;
            this.updateProgress();
        }

        console.log('Rascunho restaurado');
    }

    showDraftIndicator() {
        const indicator = document.getElementById('draft_indicator');
        if (indicator) {
            indicator.classList.add('show');
            setTimeout(() => {
                indicator.classList.remove('show');
            }, 2000);
        }
    }

    clearStorage() {
        try {
            localStorage.removeItem('wizard_draft');
        } catch (e) {
            console.warn('Não foi possível limpar o rascunho:', e);
        }
    }

    setupAutoSave() {
        // Auto-save a cada 30 segundos
        setInterval(() => {
            if (this.form) {
                this.saveToStorage();
            }
        }, 30000);
    }

    handleSubmit(event) {
        // Não prevenir o submit - deixar o form enviar normalmente
        // Limpar o storage após submit
        this.clearStorage();

        // Mostrar loading
        const submitBtn = this.submitBtn;
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span> Salvando...';
        }
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    const wizardForm = document.getElementById('wizardForm');
    if (wizardForm) {
        window.reportWizard = new ReportWizard();
        console.log('Wizard inicializado com sucesso');
    }
});

// Função auxiliar para mostrar/esconder seções de referência (mantida do código original)
function setupReferenceListener(type) {
    const inputField = document.getElementById(`ref_${type}`);
    const detailsSection = document.getElementById(`detalhes_${type}`);

    if (!inputField || !detailsSection) return;

    const checkVisibility = () => {
        const refValue = inputField.value;
        if (refValue.trim() !== '') {
            detailsSection.style.display = 'block';
        } else {
            detailsSection.style.display = 'none';
        }
    };

    inputField.addEventListener('keyup', checkVisibility);
    inputField.addEventListener('input', checkVisibility);
    inputField.addEventListener('change', checkVisibility);
    checkVisibility();
}

// Função para criar campos de upload dinâmicos (mantida do código original)
function createUploadField(contexto, type, size, labelText) {
    const safeSize = size.replace(/\s+/g, '');
    const fieldId = `dynamic_${contexto}_${type}_${safeSize}`;

    const wrapper = document.createElement('div');
    wrapper.className = 'mb-2';
    wrapper.id = fieldId;

    const label = document.createElement('label');
    label.className = 'form-label small';
    label.textContent = `${labelText} (Tamanho: ${size})`;

    const input = document.createElement('input');
    input.type = 'file';
    input.className = 'form-control form-control-sm';
    input.name = `fotos_${contexto}_${type}_${safeSize}`;
    input.multiple = true;

    wrapper.appendChild(label);
    wrapper.appendChild(input);
    return wrapper;
}

function handleSizeChange(event) {
    const checkbox = event.target;
    const size = checkbox.value;
    const checkboxGroup = checkbox.closest('.checkbox-group');
    if (!checkboxGroup) return;

    const type = checkboxGroup.getAttribute('data-type');
    const amostraPlaceholder = document.getElementById(`placeholder_fotos_amostra_${type}`);
    const provaPlaceholder = document.getElementById(`placeholder_fotos_prova_modelo_${type}`);

    if (!amostraPlaceholder || !provaPlaceholder) return;

    const safeSize = size.replace(/\s+/g, '');
    const fieldIdAmostra = `dynamic_amostra_${type}_${safeSize}`;
    const fieldIdProva = `dynamic_prova_modelo_${type}_${safeSize}`;

    if (checkbox.checked) {
        if (!document.getElementById(fieldIdAmostra)) {
            const amostraField = createUploadField('amostra', type, size, 'Fotos da amostra');
            amostraPlaceholder.appendChild(amostraField);
        }
        if (!document.getElementById(fieldIdProva)) {
            const provaField = createUploadField('prova_modelo', type, size, 'Fotos da prova, peça na modelo');
            provaPlaceholder.appendChild(provaField);
        }
    } else {
        const amostraField = document.getElementById(fieldIdAmostra);
        if (amostraField) amostraField.remove();
        const provaField = document.getElementById(fieldIdProva);
        if (provaField) provaField.remove();
    }
}

// Converter inputs de texto para MAIÚSCULO automaticamente
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('input[type="text"], textarea').forEach(input => {
        if (!input.classList.contains('no-uppercase')) {
            input.addEventListener('input', function(e) {
                const start = this.selectionStart;
                const end = this.selectionEnd;
                this.value = this.value.toUpperCase();
                this.setSelectionRange(start, end);
            });
        }
    });
});
