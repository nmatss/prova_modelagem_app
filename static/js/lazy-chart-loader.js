/**
 * Lazy Chart.js Loader
 *
 * Carrega Chart.js dinamicamente apenas quando necessário,
 * reduzindo o tamanho do bundle inicial e melhorando performance.
 *
 * Uso:
 *   loadChartJS().then(() => {
 *     // Chart.js está disponível
 *     new Chart(ctx, config);
 *   });
 */

(function(window) {
    'use strict';

    /**
     * Carrega Chart.js dinamicamente se ainda não estiver carregado
     * @returns {Promise} Resolve quando Chart.js estiver pronto
     */
    function loadChartJS() {
        // Se Chart.js já estiver carregado, resolver imediatamente
        if (window.Chart) {
            console.log('✅ Chart.js already loaded');
            return Promise.resolve();
        }

        console.log('📊 Loading Chart.js...');

        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js';
            script.async = true;

            script.onload = () => {
                console.log('✅ Chart.js loaded successfully');
                resolve();
            };

            script.onerror = () => {
                console.error('❌ Failed to load Chart.js');
                reject(new Error('Failed to load Chart.js'));
            };

            document.head.appendChild(script);
        });
    }

    // Exportar para uso global
    window.loadChartJS = loadChartJS;

})(window);
