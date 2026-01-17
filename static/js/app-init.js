/**
 * ========================================
 * PROVA MODELAGEM - APP INITIALIZATION
 * Sistema de Orquestração Global
 * ========================================
 *
 * Este arquivo orquestra todos os módulos do sistema:
 * - Navigation (sidebar colapsável)
 * - Accessibility features
 * - Performance monitoring
 * - Lazy loading
 * - Global utilities
 */

(function() {
    'use strict';

    // ========================================
    // CONFIGURAÇÃO GLOBAL
    // ========================================

    const AppConfig = {
        version: '2.0.0',
        debug: false, // Debug desativado - ativar se necessário
        features: {
            sidebar: true,
            accessibility: true,
            lazyLoading: true,
            performanceMonitoring: false
        }
    };

    // ========================================
    // SIDEBAR NAVIGATION
    // ========================================

    function initSidebar() {
        const sidebar = document.getElementById('sidebar');
        const sidebarToggle = document.getElementById('sidebarToggle');
        const mobileMenuToggle = document.getElementById('mobileMenuToggle');
        const sidebarBackdrop = document.getElementById('sidebarBackdrop');
        const mainWrapper = document.querySelector('.main-wrapper');

        if (AppConfig.debug) {
            console.log('🔧 Initializing Sidebar...');
            console.log('  sidebar:', sidebar);
            console.log('  sidebarToggle:', sidebarToggle);
            console.log('  mainWrapper:', mainWrapper);
        }

        if (!sidebar) {
            console.warn('❌ Sidebar element not found!');
            return;
        }

        if (!sidebarToggle) {
            console.warn('❌ Sidebar toggle button not found!');
            return;
        }

        // Restaurar estado do localStorage
        const sidebarState = localStorage.getItem('sidebarCollapsed');
        if (sidebarState === 'true') {
            sidebar.classList.add('collapsed');
        }

        // Toggle sidebar (desktop)
        sidebarToggle.addEventListener('click', (e) => {
            e.preventDefault();
            sidebar.classList.toggle('collapsed');
            const isCollapsed = sidebar.classList.contains('collapsed');

            // Salvar estado
            localStorage.setItem('sidebarCollapsed', isCollapsed);

            if (AppConfig.debug) {
                console.log(`🔄 Sidebar toggled: ${isCollapsed ? 'collapsed' : 'expanded'}`);
            }

            // Anunciar para leitores de tela
            if (window.announceToScreenReader) {
                const msg = isCollapsed ? 'Menu recolhido' : 'Menu expandido';
                window.announceToScreenReader(msg);
            }
        });

        // Mobile menu toggle
        if (mobileMenuToggle && sidebarBackdrop) {
            mobileMenuToggle.addEventListener('click', () => {
                sidebar.classList.add('mobile-open');
                sidebarBackdrop.classList.add('active');
                document.body.style.overflow = 'hidden';
            });

            sidebarBackdrop.addEventListener('click', () => {
                sidebar.classList.remove('mobile-open');
                sidebarBackdrop.classList.remove('active');
                document.body.style.overflow = '';
            });
        }

        // Fechar sidebar mobile ao clicar em link
        const sidebarLinks = sidebar.querySelectorAll('.menu-link');
        sidebarLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 992) {
                    sidebar.classList.remove('mobile-open');
                    if (sidebarBackdrop) sidebarBackdrop.classList.remove('active');
                    document.body.style.overflow = '';
                }
            });
        });

        // Tooltips removidos - agora usando Bootstrap 5 tooltips padrão

        // Responsividade ao resize
        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                if (window.innerWidth >= 992) {
                    sidebar.classList.remove('mobile-open');
                    if (sidebarBackdrop) sidebarBackdrop.classList.remove('active');
                    document.body.style.overflow = '';
                }
            }, 250);
        });
    }

    // Tooltip helpers removidos - usando Bootstrap 5 tooltips padrão

    // ========================================
    // BOTTOM NAVIGATION (Mobile)
    // ========================================

    function initBottomNav() {
        const bottomNav = document.querySelector('.bottom-nav');
        if (!bottomNav) return;

        let lastScrollY = window.scrollY;
        let ticking = false;

        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    const currentScrollY = window.scrollY;

                    if (currentScrollY > lastScrollY && currentScrollY > 100) {
                        // Scroll down - hide
                        bottomNav.classList.add('hidden');
                    } else {
                        // Scroll up - show
                        bottomNav.classList.remove('hidden');
                    }

                    lastScrollY = currentScrollY;
                    ticking = false;
                });

                ticking = true;
            }
        });
    }

    // ========================================
    // GLOBAL UTILITIES
    // ========================================

    function initGlobalUtils() {
        // Auto-dismiss alerts
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            if (alert.classList.contains('alert-success')) {
                setTimeout(() => {
                    if (alert.querySelector('.btn-close')) {
                        alert.querySelector('.btn-close').click();
                    } else {
                        alert.style.opacity = '0';
                        setTimeout(() => alert.remove(), 300);
                    }
                }, 5000);
            }
        });

        // Função para aplicar uppercase a um input
        function applyUppercaseToInput(input) {
            // Pular se já foi processado
            if (input.dataset.uppercaseApplied) return;

            // Pular inputs que devem permanecer com case normal
            if (input.classList.contains('no-uppercase') ||
                input.type === 'password' ||
                input.type === 'email' ||
                input.type === 'url' ||
                input.type === 'search') {
                return;
            }

            // Marcar como processado
            input.dataset.uppercaseApplied = 'true';

            // Converter valor em tempo real (CSS já aplica text-transform)
            input.addEventListener('input', function() {
                const start = this.selectionStart;
                const end = this.selectionEnd;
                this.value = this.value.toUpperCase();
                this.setSelectionRange(start, end);
            });

            if (AppConfig.debug) {
                console.log('✅ Uppercase enabled for:', input.name || input.id || input.placeholder || 'unnamed input');
            }
        }

        // Aplicar uppercase a todos os inputs existentes
        const allTextInputs = document.querySelectorAll('input[type="text"], input:not([type]), textarea');
        allTextInputs.forEach(applyUppercaseToInput);

        // Garantir que inputs .no-uppercase mantenham case normal
        const normalInputs = document.querySelectorAll('.no-uppercase');
        normalInputs.forEach(input => {
            input.style.textTransform = 'none';
        });

        if (AppConfig.debug) {
            console.log(`📝 Uppercase applied to ${allTextInputs.length} inputs`);
        }

        // Observador para inputs adicionados dinamicamente
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // Element node
                        // Se o nó adicionado é um input
                        if ((node.tagName === 'INPUT' && (node.type === 'text' || !node.type)) || node.tagName === 'TEXTAREA') {
                            applyUppercaseToInput(node);
                        }
                        // Se o nó contém inputs
                        const inputs = node.querySelectorAll('input[type="text"], input:not([type]), textarea');
                        inputs.forEach(applyUppercaseToInput);
                    }
                });
            });
        });

        // Iniciar observação
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });

        // Prevent double form submission
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', function() {
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn && !submitBtn.disabled) {
                    submitBtn.disabled = true;
                    setTimeout(() => submitBtn.disabled = false, 3000);
                }
            });
        });

        // External links
        const externalLinks = document.querySelectorAll('a[href^="http"]:not([href*="' + location.hostname + '"])');
        externalLinks.forEach(link => {
            if (!link.hasAttribute('target')) {
                link.setAttribute('target', '_blank');
                link.setAttribute('rel', 'noopener noreferrer');
            }
        });

        // Smooth scroll para âncoras
        const anchorLinks = document.querySelectorAll('a[href^="#"]:not([href="#"])');
        anchorLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);

                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // ========================================
    // IMAGE LAZY LOADING FALLBACK
    // ========================================

    function initLazyLoadingFallback() {
        // Se o navegador não suporta loading="lazy", usar Intersection Observer
        if ('loading' in HTMLImageElement.prototype) {
            return; // Browser nativo suporta lazy loading
        }

        const images = document.querySelectorAll('img[loading="lazy"]');

        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                        }
                        img.classList.add('loaded');
                        observer.unobserve(img);
                    }
                });
            });

            images.forEach(img => imageObserver.observe(img));
        } else {
            // Fallback: carregar todas as imagens
            images.forEach(img => {
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                }
            });
        }
    }

    // ========================================
    // PERFORMANCE MONITORING (opcional)
    // ========================================

    function initPerformanceMonitoring() {
        if (!AppConfig.features.performanceMonitoring) return;
        if (!window.performance || !window.performance.timing) return;

        window.addEventListener('load', () => {
            setTimeout(() => {
                const perfData = window.performance.timing;
                const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
                const connectTime = perfData.responseEnd - perfData.requestStart;
                const renderTime = perfData.domComplete - perfData.domLoading;

                if (AppConfig.debug) {
                    console.group('⚡ Performance Metrics');
                    console.log(`Page Load Time: ${pageLoadTime}ms`);
                    console.log(`Connect Time: ${connectTime}ms`);
                    console.log(`Render Time: ${renderTime}ms`);
                    console.groupEnd();
                }

                // Enviar métricas para analytics (se configurado)
                // Ex: sendToAnalytics({ pageLoadTime, connectTime, renderTime });
            }, 0);
        });
    }

    // ========================================
    // ERROR HANDLING GLOBAL
    // ========================================

    function initErrorHandling() {
        // Capturar erros JavaScript globais
        window.addEventListener('error', (event) => {
            if (AppConfig.debug) {
                console.error('Global Error:', event.error);
            }

            // Não mostrar erro para usuário em produção
            if (AppConfig.debug) {
                const errorMsg = `Erro: ${event.message} em ${event.filename}:${event.lineno}`;
                console.error(errorMsg);
            }
        });

        // Capturar promises rejeitadas não tratadas
        window.addEventListener('unhandledrejection', (event) => {
            if (AppConfig.debug) {
                console.error('Unhandled Promise Rejection:', event.reason);
            }
        });
    }

    // ========================================
    // INICIALIZAÇÃO
    // ========================================

    function init() {
        if (AppConfig.debug) {
            console.log(`%c🚀 Prova Modelagem App v${AppConfig.version}`, 'color: #E6007E; font-size: 16px; font-weight: bold;');
            console.log('%cInitializing...', 'color: #64748B;');
        }

        // Inicializar módulos
        initSidebar();
        initBottomNav();
        initGlobalUtils();
        initLazyLoadingFallback();
        initPerformanceMonitoring();
        initErrorHandling();

        // Marcar app como inicializado
        document.documentElement.classList.add('app-initialized');

        if (AppConfig.debug) {
            console.log('%c✅ App initialized successfully', 'color: #10B981; font-weight: bold;');
        }
    }

    // ========================================
    // DOM READY
    // ========================================

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Expor para debug (apenas em dev)
    if (AppConfig.debug) {
        window.ProvaModelagemApp = {
            version: AppConfig.version,
            config: AppConfig
        };
    }

})();
