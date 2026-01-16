// ========================================
// PROVA MODELAGEM - UX ENHANCEMENTS
// Versão 2.0 - Correção definitiva de modais
// ========================================

(function() {
    'use strict';

    // ========================================
    // LOADING OVERLAY - COMPLETAMENTE ISOLADO DOS MODAIS
    // ========================================

    var loadingOverlay = null;
    var isModalOpen = false;

    function createLoadingOverlay() {
        if (loadingOverlay) return loadingOverlay;

        var overlay = document.createElement('div');
        overlay.id = 'loadingOverlay';
        overlay.className = 'loading-overlay-hidden';
        overlay.innerHTML = '<div class="spinner-container">' +
            '<div class="spinner-border text-light" role="status">' +
            '<span class="visually-hidden">Carregando...</span>' +
            '</div>' +
            '<p class="mt-3 fw-bold">Processando...</p>' +
            '</div>';
        document.body.appendChild(overlay);
        loadingOverlay = overlay;
        return overlay;
    }

    function showLoading() {
        // NUNCA mostrar loading se modal estiver aberto
        if (isModalOpen) return;
        if (document.querySelector('.modal.show')) return;
        if (document.body.classList.contains('modal-open')) return;

        var overlay = createLoadingOverlay();
        overlay.className = 'loading-overlay-visible';
    }

    function hideLoading() {
        if (loadingOverlay) {
            loadingOverlay.className = 'loading-overlay-hidden';
        }
        // Também remover qualquer overlay existente por ID
        var existingOverlay = document.getElementById('loadingOverlay');
        if (existingOverlay) {
            existingOverlay.className = 'loading-overlay-hidden';
            existingOverlay.style.cssText = 'display:none!important;pointer-events:none!important;visibility:hidden!important;opacity:0!important;z-index:-9999!important;';
        }
    }

    function forceHideAllOverlays() {
        // Força esconder TUDO que possa estar bloqueando
        var overlays = document.querySelectorAll('#loadingOverlay, .loading-overlay-visible, [class*="loading"], [class*="overlay"]:not(.modal-backdrop)');
        overlays.forEach(function(el) {
            if (!el.classList.contains('modal') && !el.classList.contains('modal-backdrop') && !el.closest('.modal')) {
                el.style.cssText = 'display:none!important;pointer-events:none!important;visibility:hidden!important;opacity:0!important;z-index:-9999!important;';
            }
        });
    }

    // ========================================
    // EVENTOS DE MODAL - PRIORIDADE MÁXIMA
    // ========================================

    // Quando QUALQUER modal começar a abrir
    document.addEventListener('show.bs.modal', function(e) {
        isModalOpen = true;
        hideLoading();
        forceHideAllOverlays();
    }, true); // Capture phase para pegar primeiro

    // Quando modal estiver completamente aberto
    document.addEventListener('shown.bs.modal', function(e) {
        isModalOpen = true;
        hideLoading();
        forceHideAllOverlays();

        // Garantir que o modal está interativo
        var modal = e.target;
        if (modal) {
            modal.style.pointerEvents = 'auto';
            var content = modal.querySelector('.modal-content');
            if (content) {
                content.style.pointerEvents = 'auto';
            }
            // Focar no primeiro elemento interativo
            var firstInput = modal.querySelector('input:not([type="hidden"]), button:not([data-bs-dismiss]), textarea, select');
            if (firstInput) {
                setTimeout(function() { firstInput.focus(); }, 100);
            }
        }
    }, true);

    // Quando modal fechar
    document.addEventListener('hidden.bs.modal', function(e) {
        // Verificar se ainda há algum modal aberto
        setTimeout(function() {
            isModalOpen = document.querySelector('.modal.show') !== null;
        }, 100);
    }, true);

    // ========================================
    // INICIALIZAÇÃO
    // ========================================

    document.addEventListener('DOMContentLoaded', function() {

        // Esconder loading quando página carrega
        hideLoading();
        forceHideAllOverlays();

        // ========================================
        // FORM SUBMIT - Mostrar loading APENAS para forms fora de modais
        // ========================================

        document.querySelectorAll('form').forEach(function(form) {
            form.addEventListener('submit', function(e) {
                // NUNCA mostrar loading para forms dentro de modais
                if (form.closest('.modal')) {
                    return; // Deixa o form submeter normalmente
                }
                // NUNCA mostrar loading em páginas de admin
                if (window.location.pathname.indexOf('/admin') !== -1) {
                    return;
                }
                // Só mostrar loading se form for válido
                if (form.checkValidity()) {
                    showLoading();
                }
            });
        });

        // ========================================
        // VALIDAÇÃO DE FORMULÁRIOS
        // ========================================

        document.querySelectorAll('[required]').forEach(function(field) {
            var label = field.previousElementSibling;
            if (label && label.tagName === 'LABEL' && label.innerHTML.indexOf('*') === -1) {
                label.innerHTML += ' <span class="text-danger">*</span>';
            }
        });

        document.querySelectorAll('.form-control, .form-select').forEach(function(field) {
            field.addEventListener('blur', function() {
                if (this.hasAttribute('required') && !this.value.trim()) {
                    this.classList.add('is-invalid');
                } else {
                    this.classList.remove('is-invalid');
                    if (this.value.trim()) {
                        this.classList.add('is-valid');
                    }
                }
            });

            field.addEventListener('input', function() {
                if (this.classList.contains('is-invalid') && this.value.trim()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                }
            });
        });

        // ========================================
        // AUTO-DISMISS ALERTS
        // ========================================

        document.querySelectorAll('.alert:not(.alert-permanent)').forEach(function(alert) {
            setTimeout(function() {
                if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                    var bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                }
            }, 5000);
        });

        // ========================================
        // TOOLTIPS
        // ========================================

        if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
            var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.forEach(function(tooltipTriggerEl) {
                new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }

        // ========================================
        // SCROLL TO TOP BUTTON
        // ========================================

        var scrollTopBtn = document.createElement('button');
        scrollTopBtn.innerHTML = '<i class="bi bi-arrow-up"></i>';
        scrollTopBtn.className = 'btn btn-primary position-fixed rounded-circle scroll-top-btn';
        scrollTopBtn.style.cssText = 'bottom:20px;right:20px;width:50px;height:50px;display:none;z-index:1000;';
        scrollTopBtn.setAttribute('title', 'Voltar ao topo');
        scrollTopBtn.setAttribute('type', 'button');

        scrollTopBtn.addEventListener('click', function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        document.body.appendChild(scrollTopBtn);

        window.addEventListener('scroll', function() {
            scrollTopBtn.style.display = window.pageYOffset > 300 ? 'block' : 'none';
        });

        // ========================================
        // KEYBOARD SHORTCUTS
        // ========================================

        document.addEventListener('keydown', function(e) {
            // Ctrl/Cmd + S para salvar
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                // Só se não houver modal aberto
                if (!document.querySelector('.modal.show')) {
                    e.preventDefault();
                    var form = document.querySelector('form:not(.modal form)');
                    if (form) {
                        var submitBtn = form.querySelector('[type="submit"]');
                        if (submitBtn && !submitBtn.disabled) {
                            submitBtn.click();
                        }
                    }
                }
            }
        });

        // ========================================
        // IMAGE PREVIEW
        // ========================================

        document.querySelectorAll('input[type="file"][accept*="image"]').forEach(function(input) {
            input.addEventListener('change', function(e) {
                var files = Array.from(e.target.files);
                if (files.length === 0) return;

                var oldPreview = this.parentElement.querySelector('.file-preview');
                if (oldPreview) oldPreview.remove();

                var previewContainer = document.createElement('div');
                previewContainer.className = 'mt-2 d-flex flex-wrap gap-2 file-preview';

                files.slice(0, 5).forEach(function(file) {
                    if (file.type.startsWith('image/')) {
                        var reader = new FileReader();
                        reader.onload = function(e) {
                            var img = document.createElement('img');
                            img.src = e.target.result;
                            img.className = 'img-thumbnail';
                            img.style.cssText = 'width:80px;height:80px;object-fit:cover;';
                            previewContainer.appendChild(img);
                        };
                        reader.readAsDataURL(file);
                    }
                });

                if (files.length > 5) {
                    var moreLabel = document.createElement('div');
                    moreLabel.className = 'd-flex align-items-center justify-content-center bg-light border rounded';
                    moreLabel.style.cssText = 'width:80px;height:80px;';
                    moreLabel.innerHTML = '<small class="text-muted">+' + (files.length - 5) + '</small>';
                    previewContainer.appendChild(moreLabel);
                }

                this.parentElement.appendChild(previewContainer);
            });
        });

        // ========================================
        // FILE INPUT LABELS
        // ========================================

        document.querySelectorAll('input[type="file"]').forEach(function(input) {
            input.addEventListener('change', function(e) {
                var fileName = e.target.files.length > 0
                    ? (e.target.files.length === 1
                        ? e.target.files[0].name
                        : e.target.files.length + ' arquivos selecionados')
                    : 'Nenhum arquivo selecionado';

                var helper = this.parentElement.querySelector('.file-helper');
                if (!helper) {
                    helper = document.createElement('small');
                    helper.className = 'file-helper text-muted d-block mt-1';
                    this.parentElement.appendChild(helper);
                }
                helper.textContent = fileName;
            });
        });

        console.log('✅ UX Enhancements v2.0 loaded successfully!');
    });

    // Esconder loading quando página carregar completamente
    window.addEventListener('load', function() {
        hideLoading();
        forceHideAllOverlays();
    });

})();
