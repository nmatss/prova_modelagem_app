/**
 * JAVASCRIPT PARA GERENCIAMENTO DE TABS E UX
 * Sistema de Prova de Modelagem
 * Data: 2026-01-16
 */

// =====================================================
// 1. TAB MANAGEMENT - Persist active tab in URL
// =====================================================
(function() {
    'use strict';

    // Restore active tab from URL hash
    const hash = window.location.hash;
    if (hash) {
        const tabTrigger = document.querySelector(`button[data-bs-target="${hash}"]`);
        if (tabTrigger) {
            const tab = new bootstrap.Tab(tabTrigger);
            tab.show();
        }
    }

    // Save active tab to URL hash when changed
    const tabButtons = document.querySelectorAll('button[data-bs-toggle="tab"]');
    tabButtons.forEach(button => {
        button.addEventListener('shown.bs.tab', function(event) {
            const target = event.target.getAttribute('data-bs-target');
            history.replaceState(null, null, target);
        });
    });

    // Smooth scroll to top when changing tabs
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    });
})();

// =====================================================
// 2. STATUS MODAL - Preenche campos do modal
// =====================================================
(function() {
    'use strict';

    const statusModal = document.getElementById('statusModal');
    if (statusModal) {
        statusModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const provaId = button.getAttribute('data-prova-id');
            const novoStatus = button.getAttribute('data-novo-status');

            document.getElementById('modalProvaId').value = provaId;
            document.getElementById('modalNovoStatus').value = novoStatus;

            // Atualizar título do modal baseado no status
            const modalTitle = statusModal.querySelector('.modal-title');
            const statusText = novoStatus === 'Aprovada' ? 'Aprovar' :
                             novoStatus === 'Reprovada' ? 'Reprovar' :
                             'Enviar para Comitê';
            modalTitle.innerHTML = `<i class="bi bi-pencil-square me-2"></i>${statusText} Prova`;

            // Mudar cor do botão de submit
            const submitBtn = statusModal.querySelector('button[type="submit"]');
            submitBtn.className = `btn btn-${novoStatus === 'Aprovada' ? 'success' :
                                           novoStatus === 'Reprovada' ? 'danger' :
                                           'warning'}`;
        });
    }
})();

// =====================================================
// 3. DELETE MODAL - Solução com AJAX e timeout
// =====================================================
(function() {
    'use strict';

    const deleteModal = document.getElementById('deleteModal');
    const deleteForm = deleteModal?.querySelector('form');
    let isDeleting = false;

    if (deleteForm) {
        deleteForm.addEventListener('submit', function(e) {
            e.preventDefault();

            if (isDeleting) return;
            isDeleting = true;

            const submitBtn = deleteForm.querySelector('button[type="submit"]');
            const originalBtnHtml = submitBtn.innerHTML;
            const actionUrl = deleteForm.getAttribute('action');

            // Mostra spinner
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Excluindo...';
            submitBtn.disabled = true;

            // Timeout de 30 segundos
            const controller = new AbortController();
            const timeoutId = setTimeout(() => {
                controller.abort();
            }, 30000);

            fetch(actionUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin',
                signal: controller.signal
            })
            .then(response => {
                clearTimeout(timeoutId);

                if (response.redirected) {
                    window.location.href = response.url;
                    return;
                }

                if (!response.ok) {
                    throw new Error('Erro ' + response.status + ': ' + response.statusText);
                }

                window.location.href = '/';
            })
            .catch(error => {
                clearTimeout(timeoutId);
                isDeleting = false;

                submitBtn.innerHTML = originalBtnHtml;
                submitBtn.disabled = false;

                let errorMsg = 'Erro ao excluir o relatório.';

                if (error.name === 'AbortError') {
                    errorMsg = 'A operação excedeu o tempo limite (30s). Verifique sua conexão e tente novamente.';
                } else if (error.message) {
                    errorMsg = error.message;
                }

                // Remove erro anterior
                const existingError = deleteModal.querySelector('.delete-error-msg');
                if (existingError) existingError.remove();

                // Mostra erro
                const errorDiv = document.createElement('div');
                errorDiv.className = 'delete-error-msg alert alert-danger mt-3 mb-0';
                errorDiv.innerHTML = '<i class="bi bi-exclamation-triangle me-2"></i>' + errorMsg;

                const modalBody = deleteModal.querySelector('.modal-body');
                if (modalBody) modalBody.appendChild(errorDiv);
            });
        });
    }

    // Reset ao fechar modal
    if (deleteModal) {
        deleteModal.addEventListener('hidden.bs.modal', function() {
            isDeleting = false;

            const submitBtn = deleteForm?.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="bi bi-trash"></i> Sim, Excluir Relatório';
                submitBtn.disabled = false;
            }

            const existingError = deleteModal.querySelector('.delete-error-msg');
            if (existingError) existingError.remove();
        });
    }
})();

// =====================================================
// 4. IMAGE LIGHTBOX (OPCIONAL - NÃO IMPLEMENTADO)
// =====================================================
/*
(function() {
    'use strict';

    // Adicionar lightbox para imagens clicáveis
    const images = document.querySelectorAll('.img-thumbnail');
    images.forEach(img => {
        img.style.cursor = 'pointer';
        img.addEventListener('click', function() {
            const lightbox = document.createElement('div');
            lightbox.className = 'lightbox-overlay';
            lightbox.innerHTML = `
                <div class="lightbox-content">
                    <img src="${this.src}" alt="Imagem ampliada">
                    <button class="lightbox-close">&times;</button>
                </div>
            `;
            document.body.appendChild(lightbox);

            // Fechar ao clicar no X ou fora da imagem
            lightbox.addEventListener('click', function(e) {
                if (e.target === lightbox || e.target.classList.contains('lightbox-close')) {
                    lightbox.remove();
                }
            });
        });
    });
})();
*/

// =====================================================
// 5. KEYBOARD NAVIGATION (ACESSIBILIDADE)
// =====================================================
(function() {
    'use strict';

    // Navegação por teclado nas tabs
    const tabButtons = document.querySelectorAll('button[data-bs-toggle="tab"]');

    tabButtons.forEach((button, index) => {
        button.addEventListener('keydown', function(e) {
            let targetIndex;

            // Arrow Right - próxima tab
            if (e.key === 'ArrowRight') {
                e.preventDefault();
                targetIndex = (index + 1) % tabButtons.length;
            }
            // Arrow Left - tab anterior
            else if (e.key === 'ArrowLeft') {
                e.preventDefault();
                targetIndex = (index - 1 + tabButtons.length) % tabButtons.length;
            }
            // Home - primeira tab
            else if (e.key === 'Home') {
                e.preventDefault();
                targetIndex = 0;
            }
            // End - última tab
            else if (e.key === 'End') {
                e.preventDefault();
                targetIndex = tabButtons.length - 1;
            }

            if (targetIndex !== undefined) {
                tabButtons[targetIndex].focus();
                tabButtons[targetIndex].click();
            }
        });
    });
})();

// =====================================================
// 6. LAZY LOADING DE IMAGENS (OPCIONAL)
// =====================================================
/*
(function() {
    'use strict';

    // Lazy load para imagens
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('img-lazy');
                    observer.unobserve(img);
                }
            });
        });

        const images = document.querySelectorAll('img[data-src]');
        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback para navegadores antigos
        const images = document.querySelectorAll('img[data-src]');
        images.forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('img-lazy');
        });
    }
})();
*/

// =====================================================
// 7. AUTO-SAVE FORM (OPCIONAL - NÃO IMPLEMENTADO)
// =====================================================
/*
(function() {
    'use strict';

    // Auto-save de formulários
    const forms = document.querySelectorAll('form[data-autosave]');

    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');

        inputs.forEach(input => {
            input.addEventListener('change', function() {
                const formData = new FormData(form);
                const data = Object.fromEntries(formData);

                // Salvar no localStorage
                localStorage.setItem(`form-${form.id}`, JSON.stringify(data));

                // Mostrar feedback visual
                const saveIndicator = document.createElement('small');
                saveIndicator.className = 'text-success';
                saveIndicator.textContent = '✓ Salvo';
                input.parentElement.appendChild(saveIndicator);

                setTimeout(() => saveIndicator.remove(), 2000);
            });
        });

        // Restaurar dados ao carregar
        const savedData = localStorage.getItem(`form-${form.id}`);
        if (savedData) {
            const data = JSON.parse(savedData);
            Object.keys(data).forEach(key => {
                const input = form.elements[key];
                if (input) input.value = data[key];
            });
        }
    });
})();
*/

// =====================================================
// 8. CONFIRMATION PROMPTS
// =====================================================
(function() {
    'use strict';

    // Adicionar confirmação para ações destrutivas
    const destructiveActions = document.querySelectorAll('[data-confirm]');

    destructiveActions.forEach(element => {
        element.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm');
            if (!confirm(message)) {
                e.preventDefault();
                e.stopPropagation();
            }
        });
    });
})();

// =====================================================
// 9. TOOLTIP INITIALIZATION
// =====================================================
(function() {
    'use strict';

    // Inicializar tooltips do Bootstrap
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl =>
        new bootstrap.Tooltip(tooltipTriggerEl)
    );
})();

// =====================================================
// 10. FORM VALIDATION
// =====================================================
(function() {
    'use strict';

    // Custom validation para formulários
    const forms = document.querySelectorAll('.needs-validation');

    Array.from(forms).forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();

                // Scroll para o primeiro campo inválido
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }

            form.classList.add('was-validated');
        }, false);
    });
})();

// =====================================================
// 11. SEARCH/FILTER (OPCIONAL - NÃO IMPLEMENTADO)
// =====================================================
/*
(function() {
    'use strict';

    // Busca inline nas tabs
    const searchInput = document.querySelector('[data-search]');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const items = document.querySelectorAll('[data-searchable]');

            items.forEach(item => {
                const text = item.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
})();
*/

// =====================================================
// 12. PRINT FUNCTIONALITY
// =====================================================
(function() {
    'use strict';

    // Botão de impressão customizado
    const printButtons = document.querySelectorAll('[data-print]');

    printButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Mostrar todas as tabs antes de imprimir
            const tabPanes = document.querySelectorAll('.tab-pane');
            tabPanes.forEach(pane => {
                pane.classList.add('show', 'active');
            });

            window.print();

            // Restaurar estado após impressão
            setTimeout(() => {
                tabPanes.forEach((pane, index) => {
                    if (index !== 0) {
                        pane.classList.remove('show', 'active');
                    }
                });
            }, 100);
        });
    });
})();

// =====================================================
// 13. NOTIFICATION SYSTEM (OPCIONAL)
// =====================================================
/*
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} notification-toast`;
    notification.innerHTML = `
        <i class="bi bi-${type === 'success' ? 'check-circle' :
                         type === 'danger' ? 'exclamation-triangle' :
                         'info-circle'} me-2"></i>
        ${message}
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('show');
    }, 10);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, duration);
}
*/

// =====================================================
// 14. COPY TO CLIPBOARD
// =====================================================
(function() {
    'use strict';

    // Copiar texto para clipboard
    const copyButtons = document.querySelectorAll('[data-copy]');

    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const text = this.getAttribute('data-copy');

            navigator.clipboard.writeText(text).then(() => {
                // Feedback visual
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="bi bi-check"></i> Copiado!';

                setTimeout(() => {
                    this.innerHTML = originalText;
                }, 2000);
            });
        });
    });
})();

// =====================================================
// 15. ANALYTICS/TRACKING (OPCIONAL)
// =====================================================
/*
(function() {
    'use strict';

    // Track tab changes
    const tabButtons = document.querySelectorAll('button[data-bs-toggle="tab"]');
    tabButtons.forEach(button => {
        button.addEventListener('shown.bs.tab', function(event) {
            const tabName = event.target.textContent.trim();

            // Google Analytics
            if (typeof gtag !== 'undefined') {
                gtag('event', 'tab_change', {
                    'tab_name': tabName
                });
            }

            // Custom analytics
            console.log('Tab changed to:', tabName);
        });
    });
})();
*/

// =====================================================
// 16. PERFORMANCE MONITORING
// =====================================================
(function() {
    'use strict';

    // Monitor performance de carregamento
    window.addEventListener('load', function() {
        if (window.performance && window.performance.timing) {
            const timing = window.performance.timing;
            const loadTime = timing.loadEventEnd - timing.navigationStart;

            console.log(`Página carregada em ${loadTime}ms`);

            // Enviar métricas se necessário
            if (loadTime > 3000) {
                console.warn('Página demorou mais de 3 segundos para carregar');
            }
        }
    });
})();

// =====================================================
// 17. ERROR HANDLING
// =====================================================
window.addEventListener('error', function(event) {
    console.error('JavaScript Error:', event.error);

    // Enviar erro para sistema de logging se necessário
    // sendErrorToServer(event.error);
});

// =====================================================
// 18. UTILITY FUNCTIONS
// =====================================================
const Utils = {
    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Throttle function
    throttle: function(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },

    // Format date
    formatDate: function(date) {
        return new Date(date).toLocaleDateString('pt-BR');
    },

    // Sanitize HTML
    sanitizeHTML: function(str) {
        const temp = document.createElement('div');
        temp.textContent = str;
        return temp.innerHTML;
    }
};

// =====================================================
// FIM DO ARQUIVO
// =====================================================

console.log('✓ JavaScript carregado com sucesso - Sistema de Prova de Modelagem');
