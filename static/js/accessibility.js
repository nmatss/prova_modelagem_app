// ========================================
// WCAG 2.1 AA ACCESSIBILITY JAVASCRIPT
// Sistema de Acessibilidade Completo
// ========================================

(function() {
    'use strict';

    // ========================================
    // 1. KEYBOARD NAVIGATION DETECTION
    // ========================================

    // Detecta se usuário está usando teclado ou mouse
    let isUsingKeyboard = false;

    document.addEventListener('keydown', function(e) {
        // Tab key indica navegação por teclado
        if (e.key === 'Tab') {
            isUsingKeyboard = true;
            document.body.classList.add('using-keyboard');
            document.body.classList.remove('using-mouse');
        }
    });

    document.addEventListener('mousedown', function() {
        isUsingKeyboard = false;
        document.body.classList.add('using-mouse');
        document.body.classList.remove('using-keyboard');
    });

    // ========================================
    // 2. SKIP TO MAIN CONTENT
    // ========================================

    function createSkipLink() {
        // Verifica se já existe
        if (document.querySelector('.skip-to-main')) return;

        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.className = 'skip-to-main';
        skipLink.textContent = 'Pular para conteúdo principal';

        skipLink.addEventListener('click', function(e) {
            e.preventDefault();
            const mainContent = document.getElementById('main-content') ||
                              document.querySelector('main') ||
                              document.querySelector('.content-wrapper');

            if (mainContent) {
                mainContent.setAttribute('tabindex', '-1');
                mainContent.focus();
                mainContent.removeAttribute('tabindex');
            }
        });

        document.body.insertBefore(skipLink, document.body.firstChild);
    }

    // ========================================
    // 3. LIVE REGION ANNOUNCER
    // ========================================

    let announcerContainer;

    function createAnnouncer() {
        if (document.querySelector('.sr-announcements')) return;

        announcerContainer = document.createElement('div');
        announcerContainer.className = 'sr-announcements';
        announcerContainer.setAttribute('aria-live', 'polite');
        announcerContainer.setAttribute('aria-atomic', 'true');
        announcerContainer.setAttribute('role', 'status');
        document.body.appendChild(announcerContainer);
    }

    function announce(message, priority = 'polite') {
        if (!announcerContainer) {
            createAnnouncer();
        }

        announcerContainer.setAttribute('aria-live', priority);
        announcerContainer.textContent = '';

        setTimeout(() => {
            announcerContainer.textContent = message;
        }, 100);

        // Limpa após 5 segundos
        setTimeout(() => {
            announcerContainer.textContent = '';
        }, 5000);
    }

    // Expor função globalmente
    window.announceToScreenReader = announce;

    // ========================================
    // 4. MODAL ACCESSIBILITY (WCAG 2.4.3)
    // ========================================

    function trapFocus(element) {
        const focusableElements = element.querySelectorAll(
            'a[href]:not([tabindex="-1"]), button:not([tabindex="-1"]):not([disabled]), textarea:not([tabindex="-1"]):not([disabled]), input:not([tabindex="-1"]):not([type="hidden"]):not([disabled]), select:not([tabindex="-1"]):not([disabled]), [tabindex]:not([tabindex="-1"])'
        );

        const firstFocusable = focusableElements[0];
        const lastFocusable = focusableElements[focusableElements.length - 1];

        // Função para handle do Tab
        const handleTabKey = function(e) {
            if (e.key !== 'Tab') return;

            if (e.shiftKey) {
                // Shift + Tab
                if (document.activeElement === firstFocusable) {
                    e.preventDefault();
                    lastFocusable.focus();
                }
            } else {
                // Tab
                if (document.activeElement === lastFocusable) {
                    e.preventDefault();
                    firstFocusable.focus();
                }
            }
        };

        // Função para handle do Escape
        const handleEscapeKey = function(e) {
            if (e.key === 'Escape') {
                closeModal(element);
            }
        };

        element.addEventListener('keydown', handleTabKey);
        element.addEventListener('keydown', handleEscapeKey);

        // Foca no primeiro elemento
        if (firstFocusable) {
            setTimeout(() => firstFocusable.focus(), 100);
        }

        // Retorna função de cleanup
        return function cleanup() {
            element.removeEventListener('keydown', handleTabKey);
            element.removeEventListener('keydown', handleEscapeKey);
        };
    }

    function closeModal(modalElement) {
        const modal = bootstrap.Modal.getInstance(modalElement);
        if (modal) {
            modal.hide();
        }
    }

    // Aplica trap focus quando modal abre
    document.addEventListener('shown.bs.modal', function(e) {
        const modal = e.target;

        // Adiciona aria-modal
        modal.setAttribute('aria-modal', 'true');

        // Adiciona role se não existir
        if (!modal.getAttribute('role')) {
            modal.setAttribute('role', 'dialog');
        }

        // Anuncia abertura do modal
        const modalTitle = modal.querySelector('.modal-title');
        if (modalTitle) {
            announce('Modal aberto: ' + modalTitle.textContent);
        }

        // Trap focus
        const cleanup = trapFocus(modal);

        // Cleanup quando modal fechar
        modal.addEventListener('hidden.bs.modal', cleanup, { once: true });
    });

    // Anuncia fechamento do modal
    document.addEventListener('hidden.bs.modal', function() {
        announce('Modal fechado');
    });

    // ========================================
    // 5. FORM VALIDATION & ARIA LABELS
    // ========================================

    function enhanceFormAccessibility() {
        // Adiciona aria-required em campos obrigatórios
        document.querySelectorAll('[required]').forEach(field => {
            field.setAttribute('aria-required', 'true');

            // Adiciona aria-invalid inicialmente como false
            if (!field.hasAttribute('aria-invalid')) {
                field.setAttribute('aria-invalid', 'false');
            }

            // Cria container de erro se não existir
            let errorContainer = document.getElementById(field.id + '-error');
            if (!errorContainer && field.id) {
                errorContainer = document.createElement('span');
                errorContainer.id = field.id + '-error';
                errorContainer.className = 'error-message';
                errorContainer.setAttribute('role', 'alert');
                errorContainer.setAttribute('aria-live', 'polite');
                field.parentElement.appendChild(errorContainer);

                field.setAttribute('aria-describedby', errorContainer.id);
            }

            // Validação em tempo real
            field.addEventListener('invalid', function(e) {
                e.preventDefault();
                this.setAttribute('aria-invalid', 'true');

                const errorContainer = document.getElementById(this.id + '-error');
                if (errorContainer) {
                    errorContainer.textContent = this.validationMessage;
                }

                announce('Erro no campo ' + (this.labels[0]?.textContent || this.name) + ': ' + this.validationMessage, 'assertive');
            });

            field.addEventListener('input', function() {
                if (this.validity.valid) {
                    this.setAttribute('aria-invalid', 'false');

                    const errorContainer = document.getElementById(this.id + '-error');
                    if (errorContainer) {
                        errorContainer.textContent = '';
                    }
                }
            });
        });

        // Associa labels com inputs
        document.querySelectorAll('input, select, textarea').forEach(field => {
            if (field.id && !field.labels?.length && !field.getAttribute('aria-label')) {
                const label = document.querySelector(`label[for="${field.id}"]`);
                if (!label) {
                    console.warn('Campo sem label:', field);
                }
            }
        });
    }

    // ========================================
    // 6. LOADING STATE ANNOUNCEMENTS
    // ========================================

    function announceLoadingState() {
        const loadingObserver = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1) {
                        // Loading overlay
                        if (node.id === 'loadingOverlay' || node.classList?.contains('loading')) {
                            announce('Carregando conteúdo, por favor aguarde', 'assertive');
                        }

                        // Spinner
                        if (node.classList?.contains('spinner-border')) {
                            const parent = node.closest('[aria-label], [aria-labelledby]');
                            if (!parent) {
                                announce('Carregando', 'polite');
                            }
                        }
                    }
                });
            });
        });

        loadingObserver.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // ========================================
    // 7. DYNAMIC CONTENT ANNOUNCEMENTS
    // ========================================

    function announceFilterChanges() {
        // Anuncia mudanças em filtros
        const filterCheckboxes = document.querySelectorAll('.filter-pill-premium input[type="checkbox"]');

        filterCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                const label = this.parentElement.textContent.trim();
                const action = this.checked ? 'selecionado' : 'desmarcado';
                announce(`Filtro ${label} ${action}`, 'polite');
            });
        });

        // Anuncia mudanças na contagem de resultados
        const countElement = document.getElementById('reportsCount');
        if (countElement) {
            const countObserver = new MutationObserver(() => {
                const count = countElement.textContent;
                announce(`${count} encontrados`, 'polite');
            });

            countObserver.observe(countElement, {
                childList: true,
                characterData: true,
                subtree: true
            });
        }
    }

    // ========================================
    // 8. SEARCH ANNOUNCEMENTS
    // ========================================

    function announceSearchResults() {
        const searchInput = document.getElementById('searchInput');
        if (!searchInput) return;

        let searchTimeout;

        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);

            searchTimeout = setTimeout(() => {
                const resultsCount = document.querySelectorAll('.report-card:not([style*="display: none"])').length;
                announce(`${resultsCount} resultados encontrados para "${this.value}"`, 'polite');
            }, 1000);
        });
    }

    // ========================================
    // 9. TOAST/ALERT ANNOUNCEMENTS
    // ========================================

    function announceAlerts() {
        const alertObserver = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1 && node.classList?.contains('alert')) {
                        const message = node.textContent.trim();
                        const priority = node.classList.contains('alert-danger') ||
                                       node.classList.contains('alert-error') ? 'assertive' : 'polite';
                        announce(message, priority);
                    }
                });
            });
        });

        alertObserver.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // ========================================
    // 10. KEYBOARD SHORTCUTS
    // ========================================

    const shortcuts = {
        'ctrl+/': 'Mostrar atalhos de teclado',
        '/': 'Focar na busca',
        'ctrl+n': 'Novo relatório',
        'esc': 'Fechar modal/diálogo',
        'ctrl+s': 'Salvar formulário'
    };

    function setupKeyboardShortcuts() {
        document.addEventListener('keydown', function(e) {
            // Ctrl/Cmd + / = Mostrar atalhos
            if ((e.ctrlKey || e.metaKey) && e.key === '/') {
                e.preventDefault();
                showShortcutsHelp();
            }

            // / = Focar busca
            if (e.key === '/' && !e.ctrlKey && !e.metaKey) {
                const searchInput = document.getElementById('searchInput');
                if (searchInput && document.activeElement !== searchInput) {
                    e.preventDefault();
                    searchInput.focus();
                    announce('Campo de busca focado', 'polite');
                }
            }

            // Ctrl/Cmd + N = Novo relatório
            if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
                e.preventDefault();
                const newReportBtn = document.querySelector('.btn-new-report, a[href*="novo_relatorio"]');
                if (newReportBtn) {
                    window.location.href = newReportBtn.href;
                }
            }
        });
    }

    function showShortcutsHelp() {
        let helpDialog = document.getElementById('keyboard-shortcuts-help');

        if (!helpDialog) {
            helpDialog = document.createElement('div');
            helpDialog.id = 'keyboard-shortcuts-help';
            helpDialog.className = 'modal fade';
            helpDialog.setAttribute('tabindex', '-1');
            helpDialog.setAttribute('role', 'dialog');
            helpDialog.setAttribute('aria-labelledby', 'shortcutsTitle');
            helpDialog.setAttribute('aria-modal', 'true');

            helpDialog.innerHTML = `
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="shortcutsTitle">
                                <i class="bi bi-keyboard me-2"></i>
                                Atalhos de Teclado
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
                        </div>
                        <div class="modal-body">
                            <table class="table">
                                <caption class="sr-only">Lista de atalhos de teclado disponíveis</caption>
                                <thead>
                                    <tr>
                                        <th scope="col">Atalho</th>
                                        <th scope="col">Ação</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${Object.entries(shortcuts).map(([key, description]) => `
                                        <tr>
                                            <td><kbd>${key}</kbd></td>
                                            <td>${description}</td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                        </div>
                    </div>
                </div>
            `;

            document.body.appendChild(helpDialog);
        }

        const modal = new bootstrap.Modal(helpDialog);
        modal.show();
    }

    // ========================================
    // 11. IMAGE ALT TEXT VALIDATION
    // ========================================

    function validateImageAccessibility() {
        document.querySelectorAll('img').forEach(img => {
            if (!img.hasAttribute('alt')) {
                console.warn('Imagem sem atributo alt:', img);
                img.setAttribute('alt', '');
                img.setAttribute('role', 'presentation');
            }

            // Adiciona loading lazy se não existir
            if (!img.hasAttribute('loading') && img.src) {
                img.setAttribute('loading', 'lazy');
            }
        });
    }

    // ========================================
    // 12. BUTTON ACCESSIBILITY
    // ========================================

    function enhanceButtonAccessibility() {
        // Botões apenas com ícone precisam de aria-label
        document.querySelectorAll('button:not([aria-label])').forEach(btn => {
            const hasText = btn.textContent.trim().length > 0;
            const hasIcon = btn.querySelector('i, svg');

            if (hasIcon && !hasText && !btn.getAttribute('aria-label')) {
                console.warn('Botão apenas com ícone sem aria-label:', btn);

                // Tenta inferir do ícone
                const icon = btn.querySelector('i');
                if (icon) {
                    const iconClasses = Array.from(icon.classList);
                    const iconName = iconClasses.find(c => c.startsWith('bi-'));
                    if (iconName) {
                        btn.setAttribute('aria-label', iconName.replace('bi-', '').replace(/-/g, ' '));
                    }
                }
            }

            // Marca ícones como decorativos
            const icons = btn.querySelectorAll('i, svg');
            icons.forEach(icon => {
                if (!icon.getAttribute('aria-hidden')) {
                    icon.setAttribute('aria-hidden', 'true');
                }
            });
        });
    }

    // ========================================
    // 13. HEADING HIERARCHY VALIDATION
    // ========================================

    function validateHeadingHierarchy() {
        const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'));
        let lastLevel = 0;

        headings.forEach(heading => {
            const level = parseInt(heading.tagName[1]);

            if (lastLevel > 0 && level > lastLevel + 1) {
                console.warn(`Hierarquia de heading incorreta: saltou de h${lastLevel} para h${level}`, heading);
            }

            lastLevel = level;
        });
    }

    // ========================================
    // 14. ARIA LIVE REGIONS FOR DYNAMIC CONTENT
    // ========================================

    function setupLiveRegions() {
        // Marca regiões dinâmicas
        const dynamicRegions = document.querySelectorAll('.reports-grid, #reportsCount, .no-results');

        dynamicRegions.forEach(region => {
            if (!region.getAttribute('aria-live')) {
                region.setAttribute('aria-live', 'polite');
            }
            if (!region.getAttribute('aria-atomic')) {
                region.setAttribute('aria-atomic', 'false');
            }
        });
    }

    // ========================================
    // 15. TABLE ACCESSIBILITY
    // ========================================

    function enhanceTableAccessibility() {
        document.querySelectorAll('table').forEach(table => {
            // Adiciona caption se não existir
            if (!table.querySelector('caption')) {
                const caption = document.createElement('caption');
                caption.className = 'sr-only';
                caption.textContent = 'Tabela de dados';
                table.insertBefore(caption, table.firstChild);
            }

            // Adiciona scope em headers
            table.querySelectorAll('th').forEach(th => {
                if (!th.getAttribute('scope')) {
                    // Detecta se é header de coluna ou linha
                    const isInThead = th.closest('thead') !== null;
                    th.setAttribute('scope', isInThead ? 'col' : 'row');
                }
            });
        });
    }

    // ========================================
    // 16. LANDMARK ROLES
    // ========================================

    function ensureLandmarkRoles() {
        // Main content
        const mainContent = document.querySelector('main, .content-wrapper, .main-wrapper');
        if (mainContent && !mainContent.getAttribute('role')) {
            mainContent.setAttribute('role', 'main');
            mainContent.id = mainContent.id || 'main-content';
        }

        // Navigation
        document.querySelectorAll('nav').forEach(nav => {
            if (!nav.getAttribute('aria-label') && !nav.getAttribute('aria-labelledby')) {
                nav.setAttribute('aria-label', 'Navegação');
            }
        });

        // Footer
        const footer = document.querySelector('footer');
        if (footer && !footer.getAttribute('role')) {
            footer.setAttribute('role', 'contentinfo');
        }
    }

    // ========================================
    // 17. FOCUS MANAGEMENT
    // ========================================

    function manageFocus() {
        // Foca no conteúdo principal após navegação
        window.addEventListener('load', () => {
            const mainContent = document.querySelector('#main-content, main, .content-wrapper');
            if (mainContent && window.location.hash === '') {
                // Não foca automaticamente para não atrapalhar, mas permite skip link funcionar
                mainContent.setAttribute('tabindex', '-1');
            }
        });

        // Gerencia focus após ações
        document.addEventListener('click', (e) => {
            // Após deletar item, foca no próximo ou no botão de adicionar
            if (e.target.closest('.btn-delete-report, .btn-excluir')) {
                setTimeout(() => {
                    const firstCard = document.querySelector('.report-card');
                    const newBtn = document.querySelector('.btn-new-report');

                    if (firstCard) {
                        firstCard.querySelector('a, button')?.focus();
                    } else if (newBtn) {
                        newBtn.focus();
                    }
                }, 100);
            }
        });
    }

    // ========================================
    // 18. CONTRAST CHECKER (Development)
    // ========================================

    function checkContrast() {
        if (window.location.hostname !== 'localhost' && !window.location.hostname.includes('127.0.0.1')) {
            return; // Só roda em desenvolvimento
        }

        console.group('🎨 Accessibility Contrast Checker');

        const elements = document.querySelectorAll('body, body *:not(script):not(style)');
        let issues = 0;

        elements.forEach(el => {
            const style = window.getComputedStyle(el);
            const color = style.color;
            const bg = style.backgroundColor;

            if (color && bg && bg !== 'rgba(0, 0, 0, 0)') {
                const contrast = getContrastRatio(color, bg);
                const fontSize = parseFloat(style.fontSize);
                const isBold = parseInt(style.fontWeight) >= 700;

                const isLargeText = fontSize >= 18 || (fontSize >= 14 && isBold);
                const minContrast = isLargeText ? 3 : 4.5;

                if (contrast < minContrast) {
                    console.warn(`Baixo contraste (${contrast.toFixed(2)}:1):`, el);
                    issues++;
                }
            }
        });

        console.log(`${issues} problemas de contraste encontrados`);
        console.groupEnd();
    }

    function getContrastRatio(color1, color2) {
        const l1 = getLuminance(color1);
        const l2 = getLuminance(color2);
        return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
    }

    function getLuminance(color) {
        const rgb = color.match(/\d+/g).map(Number);
        const [r, g, b] = rgb.map(val => {
            val = val / 255;
            return val <= 0.03928 ? val / 12.92 : Math.pow((val + 0.055) / 1.055, 2.4);
        });
        return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    }

    // ========================================
    // 19. INITIALIZATION
    // ========================================

    function init() {
        console.group('♿ Accessibility Features Loading...');

        // createSkipLink(); // Desabilitado conforme solicitado
        createAnnouncer();
        enhanceFormAccessibility();
        announceLoadingState();
        announceFilterChanges();
        announceSearchResults();
        announceAlerts();
        setupKeyboardShortcuts();
        validateImageAccessibility();
        enhanceButtonAccessibility();
        validateHeadingHierarchy();
        setupLiveRegions();
        enhanceTableAccessibility();
        ensureLandmarkRoles();
        manageFocus();

        // Desenvolvimento apenas
        if (window.location.hostname === 'localhost' || window.location.hostname.includes('127.0.0.1')) {
            checkContrast();
        }

        console.log('✅ Accessibility features loaded successfully!');
        console.groupEnd();

        // Anuncia que a página está pronta
        announce('Página carregada e pronta para uso', 'polite');
    }

    // Inicializa quando DOM estiver pronto
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // ========================================
    // 20. EXPOR API PÚBLICA
    // ========================================

    window.Accessibility = {
        announce: announce,
        showShortcuts: showShortcutsHelp,
        trapFocus: trapFocus,
        checkContrast: checkContrast
    };

})();

console.log('🎯 Accessibility.js loaded - Sistema WCAG 2.1 AA ativado');
