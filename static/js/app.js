// ========================================
// PROVA MODELAGEM - UX ENHANCEMENTS
// ========================================

document.addEventListener('DOMContentLoaded', function() {

    // ========================================
    // LOADING OVERLAY
    // ========================================

    function createLoadingOverlay() {
        if (!document.getElementById('loadingOverlay')) {
            const overlay = document.createElement('div');
            overlay.id = 'loadingOverlay';
            overlay.innerHTML = `
                <div class="spinner-container">
                    <div class="spinner-border text-light" role="status">
                        <span class="visually-hidden">Carregando...</span>
                    </div>
                    <p class="mt-3 fw-bold">Processando...</p>
                </div>
            `;
            document.body.appendChild(overlay);
        }
    }

    function showLoading() {
        createLoadingOverlay();
        document.getElementById('loadingOverlay').classList.add('show');
    }

    function hideLoading() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.classList.remove('show');
        }
    }

    // Show loading on form submit
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            // Check if form is valid
            if (form.checkValidity()) {
                showLoading();
            }
        });
    });

    // Hide loading when page loads
    window.addEventListener('load', hideLoading);


    // ========================================
    // FORM VALIDATION ENHANCEMENTS
    // ========================================

    // Add visual feedback for required fields
    document.querySelectorAll('[required]').forEach(field => {
        const label = field.previousElementSibling;
        if (label && label.tagName === 'LABEL') {
            label.innerHTML += ' <span class="text-danger">*</span>';
        }
    });

    // Real-time validation feedback
    document.querySelectorAll('.form-control, .form-select').forEach(field => {
        field.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value.trim()) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });

        field.addEventListener('input', function() {
            if (this.classList.contains('is-invalid')) {
                if (this.value.trim()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                }
            }
        });
    });


    // ========================================
    // ALERTS AUTO-DISMISS
    // ========================================

    document.querySelectorAll('.alert:not(.alert-permanent)').forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });


    // ========================================
    // CONFIRM DANGEROUS ACTIONS
    // ========================================

    document.querySelectorAll('[data-confirm]').forEach(element => {
        element.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || 'Tem certeza?';
            if (!confirm(message)) {
                e.preventDefault();
                e.stopPropagation();
                return false;
            }
        });
    });


    // ========================================
    // TOOLTIPS
    // ========================================

    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });


    // ========================================
    // IMAGE PREVIEW
    // ========================================

    document.querySelectorAll('input[type="file"][accept*="image"]').forEach(input => {
        input.addEventListener('change', function(e) {
            const files = Array.from(e.target.files);

            if (files.length > 0) {
                const previewContainer = document.createElement('div');
                previewContainer.className = 'mt-2 d-flex flex-wrap gap-2';

                // Remove old preview if exists
                const oldPreview = this.parentElement.querySelector('.file-preview');
                if (oldPreview) {
                    oldPreview.remove();
                }

                previewContainer.className += ' file-preview';

                files.slice(0, 5).forEach(file => {
                    if (file.type.startsWith('image/')) {
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            const img = document.createElement('img');
                            img.src = e.target.result;
                            img.className = 'img-thumbnail';
                            img.style.width = '80px';
                            img.style.height = '80px';
                            img.style.objectFit = 'cover';
                            previewContainer.appendChild(img);
                        };
                        reader.readAsDataURL(file);
                    }
                });

                if (files.length > 5) {
                    const moreLabel = document.createElement('div');
                    moreLabel.className = 'd-flex align-items-center justify-content-center bg-light border rounded';
                    moreLabel.style.width = '80px';
                    moreLabel.style.height = '80px';
                    moreLabel.innerHTML = `<small class="text-muted">+${files.length - 5}</small>`;
                    previewContainer.appendChild(moreLabel);
                }

                this.parentElement.appendChild(previewContainer);
            }
        });
    });


    // ========================================
    // SMOOTH SCROLL TO TOP
    // ========================================

    const scrollTopBtn = document.createElement('button');
    scrollTopBtn.innerHTML = '<i class="bi bi-arrow-up"></i>';
    scrollTopBtn.className = 'btn btn-primary position-fixed bottom-0 end-0 m-4 rounded-circle';
    scrollTopBtn.style.width = '50px';
    scrollTopBtn.style.height = '50px';
    scrollTopBtn.style.display = 'none';
    scrollTopBtn.style.zIndex = '1000';
    scrollTopBtn.setAttribute('title', 'Voltar ao topo');

    scrollTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    document.body.appendChild(scrollTopBtn);

    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            scrollTopBtn.style.display = 'block';
        } else {
            scrollTopBtn.style.display = 'none';
        }
    });


    // ========================================
    // ANIMATE ON SCROLL
    // ========================================

    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card, .alert, .page-header').forEach(el => {
        observer.observe(el);
    });


    // ========================================
    // CHARACTER COUNTER FOR TEXTAREAS
    // ========================================

    document.querySelectorAll('textarea[maxlength]').forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        const counter = document.createElement('small');
        counter.className = 'text-muted d-block text-end mt-1';

        const updateCounter = () => {
            const remaining = maxLength - textarea.value.length;
            counter.textContent = `${remaining} caracteres restantes`;

            if (remaining < 20) {
                counter.classList.add('text-warning');
            } else {
                counter.classList.remove('text-warning');
            }
        };

        textarea.parentElement.appendChild(counter);
        updateCounter();

        textarea.addEventListener('input', updateCounter);
    });


    // ========================================
    // KEYBOARD SHORTCUTS
    // ========================================

    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + S to save forms
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            const form = document.querySelector('form');
            if (form) {
                const submitBtn = form.querySelector('[type="submit"]');
                if (submitBtn) {
                    submitBtn.click();
                }
            }
        }

        // Escape to close modals
        if (e.key === 'Escape') {
            const modal = bootstrap.Modal.getInstance(document.querySelector('.modal.show'));
            if (modal) {
                modal.hide();
            }
        }
    });


    // ========================================
    // COPY TO CLIPBOARD
    // ========================================

    document.querySelectorAll('[data-clipboard]').forEach(element => {
        element.style.cursor = 'pointer';
        element.addEventListener('click', function() {
            const text = this.getAttribute('data-clipboard') || this.textContent;

            navigator.clipboard.writeText(text).then(() => {
                // Show feedback
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="bi bi-check"></i> Copiado!';
                this.classList.add('text-success');

                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.classList.remove('text-success');
                }, 2000);
            });
        });
    });


    // ========================================
    // ENHANCED SEARCH
    // ========================================

    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        let searchTimeout;

        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);

            // Add loading indicator
            this.style.backgroundImage = `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236b7280'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z'%3E%3C/path%3E%3C/svg%3E"), url("data:image/svg+xml,%3Csvg class='animate-spin' xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24'%3E%3Ccircle class='opacity-25' cx='12' cy='12' r='10' stroke='currentColor' stroke-width='4'%3E%3C/circle%3E%3Cpath class='opacity-75' fill='currentColor' d='M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z'%3E%3C/path%3E%3C/svg%3E")`;

            searchTimeout = setTimeout(() => {
                // Reset icon
                this.style.backgroundImage = `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236b7280'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z'%3E%3C/path%3E%3C/svg%3E")`;
            }, 300);
        });
    }


    // ========================================
    // PREVENT DOUBLE SUBMIT
    // ========================================

    document.querySelectorAll('form').forEach(form => {
        let isSubmitting = false;

        form.addEventListener('submit', function(e) {
            if (isSubmitting) {
                e.preventDefault();
                return false;
            }

            if (this.checkValidity()) {
                isSubmitting = true;

                // Disable submit button
                const submitBtn = this.querySelector('[type="submit"]');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    const originalText = submitBtn.innerHTML;
                    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processando...';
                }
            }
        });
    });


    // ========================================
    // ENHANCED FILE INPUT LABELS
    // ========================================

    document.querySelectorAll('input[type="file"]').forEach(input => {
        input.addEventListener('change', function(e) {
            const fileName = e.target.files.length > 0
                ? e.target.files.length === 1
                    ? e.target.files[0].name
                    : `${e.target.files.length} arquivos selecionados`
                : 'Nenhum arquivo selecionado';

            // Update label or add helper text
            let helper = this.parentElement.querySelector('.file-helper');
            if (!helper) {
                helper = document.createElement('small');
                helper.className = 'file-helper text-muted d-block mt-1';
                this.parentElement.appendChild(helper);
            }
            helper.textContent = fileName;
        });
    });


    console.log('✅ UX Enhancements loaded successfully!');
});
