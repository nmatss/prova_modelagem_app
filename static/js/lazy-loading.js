/**
 * LAZY LOADING OPTIMIZATION
 * Sistema completo de carregamento tardio para imagens e componentes pesados
 */

(function() {
    'use strict';

    // ========================================
    // 1. LAZY LOADING DE IMAGENS
    // ========================================

    /**
     * Inicializa lazy loading de imagens usando Intersection Observer
     */
    function initImageLazyLoading() {
        // Verificar suporte nativo ao loading="lazy"
        if ('loading' in HTMLImageElement.prototype) {
            // Navegador suporta lazy loading nativo
            const images = document.querySelectorAll('img[data-src]');
            images.forEach(img => {
                img.src = img.dataset.src;
                if (img.dataset.srcset) {
                    img.srcset = img.dataset.srcset;
                }
                img.removeAttribute('data-src');
                img.removeAttribute('data-srcset');
            });
            console.log('✅ Native lazy loading habilitado para', images.length, 'imagens');
            return;
        }

        // Fallback: Intersection Observer
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;

                    // Carregar imagem
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }

                    if (img.dataset.srcset) {
                        img.srcset = img.dataset.srcset;
                        img.removeAttribute('data-srcset');
                    }

                    // Remover classe lazy
                    img.classList.remove('lazy-image');
                    img.classList.add('lazy-loaded');

                    // Parar de observar
                    observer.unobserve(img);
                }
            });
        }, {
            root: null,
            rootMargin: '50px', // Começar a carregar 50px antes de aparecer
            threshold: 0.01
        });

        // Observar todas as imagens lazy
        const lazyImages = document.querySelectorAll('img[data-src], img.lazy-image');
        lazyImages.forEach(img => imageObserver.observe(img));

        console.log('✅ Intersection Observer lazy loading habilitado para', lazyImages.length, 'imagens');
    }

    // ========================================
    // 2. LAZY LOADING DE BACKGROUND IMAGES
    // ========================================

    function initBackgroundLazyLoading() {
        const bgObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    const bgImage = element.dataset.bgImage;

                    if (bgImage) {
                        element.style.backgroundImage = `url('${bgImage}')`;
                        element.removeAttribute('data-bg-image');
                        element.classList.add('bg-loaded');
                    }

                    observer.unobserve(element);
                }
            });
        }, {
            rootMargin: '50px',
            threshold: 0.01
        });

        const lazyBgs = document.querySelectorAll('[data-bg-image]');
        lazyBgs.forEach(bg => bgObserver.observe(bg));

        if (lazyBgs.length > 0) {
            console.log('✅ Background lazy loading habilitado para', lazyBgs.length, 'elementos');
        }
    }

    // ========================================
    // 3. LAZY LOADING DE COMPONENTES PESADOS
    // ========================================

    /**
     * Carrega Chart.js apenas quando necessário
     */
    window.loadChartsLibrary = async function() {
        if (window.Chart) {
            return Promise.resolve(); // Já carregado
        }

        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js';
            script.onload = () => {
                console.log('✅ Chart.js carregado dinamicamente');
                resolve();
            };
            script.onerror = reject;
            document.head.appendChild(script);
        });
    };

    /**
     * Lazy loading de gráficos
     */
    function initChartLazyLoading() {
        const chartObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(async (entry) => {
                if (entry.isIntersecting) {
                    const chartContainer = entry.target;

                    // Carregar Chart.js se necessário
                    if (!window.Chart) {
                        await window.loadChartsLibrary();
                    }

                    // Disparar evento personalizado
                    chartContainer.dispatchEvent(new CustomEvent('chartVisible', {
                        bubbles: true
                    }));

                    observer.unobserve(chartContainer);
                }
            });
        }, {
            rootMargin: '100px', // Carregar antes de aparecer
            threshold: 0.1
        });

        const chartContainers = document.querySelectorAll('.chart-container, [data-chart]');
        chartContainers.forEach(container => chartObserver.observe(container));

        if (chartContainers.length > 0) {
            console.log('✅ Chart lazy loading habilitado para', chartContainers.length, 'gráficos');
        }
    }

    // ========================================
    // 4. PRELOAD DE RECURSOS CRÍTICOS
    // ========================================

    function preloadCriticalResources() {
        // Preload de imagens críticas (above the fold)
        const criticalImages = document.querySelectorAll('img[data-critical]');
        criticalImages.forEach(img => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'image';
            link.href = img.dataset.src || img.src;
            document.head.appendChild(link);
        });

        // Preconnect para CDNs
        const preconnects = [
            'https://cdn.jsdelivr.net',
            'https://fonts.googleapis.com',
            'https://fonts.gstatic.com'
        ];

        preconnects.forEach(url => {
            const link = document.createElement('link');
            link.rel = 'preconnect';
            link.href = url;
            link.crossOrigin = 'anonymous';
            document.head.appendChild(link);
        });
    }

    // ========================================
    // 5. DEBOUNCE PARA SCROLL EVENTS
    // ========================================

    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // ========================================
    // 6. LAZY LOADING DE IFRAMES (VÍDEOS, MAPAS)
    // ========================================

    function initIframeLazyLoading() {
        const iframeObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const iframe = entry.target;

                    if (iframe.dataset.src) {
                        iframe.src = iframe.dataset.src;
                        iframe.removeAttribute('data-src');
                        iframe.classList.add('iframe-loaded');
                    }

                    observer.unobserve(iframe);
                }
            });
        }, {
            rootMargin: '200px',
            threshold: 0.01
        });

        const lazyIframes = document.querySelectorAll('iframe[data-src]');
        lazyIframes.forEach(iframe => iframeObserver.observe(iframe));

        if (lazyIframes.length > 0) {
            console.log('✅ Iframe lazy loading habilitado para', lazyIframes.length, 'elementos');
        }
    }

    // ========================================
    // 7. GERENCIAMENTO DE MEMÓRIA
    // ========================================

    /**
     * Remove imagens fora da viewport para economizar memória
     * Útil para páginas muito longas
     */
    function initMemoryManagement() {
        let memoryCleanupEnabled = false;

        // Habilitar apenas se houver muitas imagens
        const totalImages = document.querySelectorAll('img').length;
        if (totalImages < 50) {
            return; // Não necessário para poucos elementos
        }

        const memoryObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                const img = entry.target;

                if (!entry.isIntersecting && memoryCleanupEnabled) {
                    // Imagem saiu da viewport
                    if (img.dataset.originalSrc) {
                        return; // Já otimizada
                    }

                    // Guardar src original
                    img.dataset.originalSrc = img.src;

                    // Substituir por placeholder pequeno
                    img.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
                } else if (entry.isIntersecting && img.dataset.originalSrc) {
                    // Imagem voltou para viewport
                    img.src = img.dataset.originalSrc;
                    delete img.dataset.originalSrc;
                }
            });
        }, {
            rootMargin: '300px', // Manter margem generosa
            threshold: 0
        });

        // Observar apenas imagens grandes
        const images = document.querySelectorAll('img:not([data-critical])');
        images.forEach(img => {
            // Observar apenas se imagem for grande (>100KB estimado)
            if (img.naturalWidth > 500 || img.naturalHeight > 500) {
                memoryObserver.observe(img);
            }
        });

        // Habilitar após 5 segundos
        setTimeout(() => {
            memoryCleanupEnabled = true;
            console.log('✅ Memory management habilitado');
        }, 5000);
    }

    // ========================================
    // INICIALIZAÇÃO
    // ========================================

    function init() {
        // Aguardar DOM estar pronto
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }

        console.log('🚀 Inicializando lazy loading...');

        // Executar otimizações
        preloadCriticalResources();
        initImageLazyLoading();
        initBackgroundLazyLoading();
        initChartLazyLoading();
        initIframeLazyLoading();

        // Memory management apenas em páginas grandes
        if (document.body.scrollHeight > window.innerHeight * 3) {
            initMemoryManagement();
        }

        console.log('✅ Lazy loading inicializado com sucesso');
    }

    // Auto-inicialização
    init();

    // Exportar funções úteis
    window.LazyLoading = {
        init,
        initImageLazyLoading,
        loadChartsLibrary
    };

})();
