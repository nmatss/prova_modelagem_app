/**
 * Checklist Dinâmico — carrega itens dos ChecklistTemplate ativos por categoria
 * e renderiza checkboxes adicionais no formulário de prova.
 *
 * Uso no template: insira um container vazio com data-attributes:
 *   <div class="checklist-dinamico"
 *        data-categoria="qualidade"
 *        data-prova-id="{{ prova.id }}"
 *        data-tipo="{{ tipo }}">
 *   </div>
 *
 * - data-categoria: qualidade | estilo | modelagem
 * - data-prova-id: id da prova (existente). Se omitido, considera nova prova.
 * - data-tipo: nome usado no prefixo dos inputs (ex: 'baby', 'kids', 'adulto')
 *
 * O input gerado tem name="checklist_dinamico_<categoria>_<prova_id_ou_tipo>[]".
 * O backend deve ler esse list e fazer upsert/delete em ChecklistResposta.
 */
(function() {
    'use strict';

    const CATEGORIA_LABELS = {
        'qualidade': 'Qualidade',
        'estilo': 'Estilo',
        'modelagem': 'Modelagem',
    };

    async function fetchTemplate(categoria) {
        try {
            const res = await fetch(`/admin/checklists/api/template/${categoria}`, {
                credentials: 'same-origin',
            });
            if (!res.ok) return null;
            return await res.json();
        } catch (e) {
            console.warn('Falha ao carregar template', categoria, e);
            return null;
        }
    }

    async function fetchRespostas(provaId, categoria) {
        if (!provaId) return { itens_marcados: [], observacoes: {} };
        try {
            const res = await fetch(`/admin/checklists/api/respostas/${provaId}/${categoria}`, {
                credentials: 'same-origin',
            });
            if (!res.ok) return { itens_marcados: [], observacoes: {} };
            return await res.json();
        } catch (e) {
            console.warn('Falha ao carregar respostas', provaId, categoria, e);
            return { itens_marcados: [], observacoes: {} };
        }
    }

    function renderItens(container, categoria, itens, marcados, observacoes, provaIdOrTipo) {
        if (!itens || itens.length === 0) {
            container.innerHTML = '';
            return;
        }

        const inputName = `checklist_dinamico_${categoria}_${provaIdOrTipo}[]`;
        const idPrefix = `chkdin_${categoria}_${provaIdOrTipo}`;
        const marcadosSet = new Set(marcados || []);

        const html = `
            <div class="card border-info border-opacity-25 mb-3" style="background: #f8f9ff;">
                <div class="card-body py-2 px-3">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <small class="fw-semibold text-info">
                            <i class="bi bi-stars me-1"></i>Itens configurados pelo admin (${CATEGORIA_LABELS[categoria] || categoria})
                        </small>
                        <a href="/admin/checklists/" class="small text-muted" target="_blank">
                            <i class="bi bi-gear"></i> Editar template
                        </a>
                    </div>
                    <div class="row g-2">
                        ${itens.map((item, idx) => {
                            const id = `${idPrefix}_${idx}`;
                            const checked = marcadosSet.has(item) ? 'checked' : '';
                            const obs = (observacoes && observacoes[item]) || '';
                            return `
                                <div class="col-md-4">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox"
                                               name="${inputName}" value="${escapeHtml(item)}"
                                               id="${id}" ${checked}>
                                        <label class="form-check-label small" for="${id}" title="${escapeHtml(item)}">
                                            ${escapeHtml(item)}
                                        </label>
                                        ${obs ? `<div class="small text-muted ms-4" style="font-style: italic;">${escapeHtml(obs)}</div>` : ''}
                                    </div>
                                </div>
                            `;
                        }).join('')}
                    </div>
                </div>
            </div>
        `;
        container.innerHTML = html;
    }

    function escapeHtml(s) {
        if (s == null) return '';
        return String(s)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    async function initContainer(container) {
        const categoria = container.dataset.categoria;
        const provaId = container.dataset.provaId || null;
        const tipo = container.dataset.tipo || 'novo';
        if (!categoria) return;

        const provaIdOrTipo = provaId || tipo;

        const [template, respostas] = await Promise.all([
            fetchTemplate(categoria),
            fetchRespostas(provaId, categoria),
        ]);

        if (!template || !template.itens || template.itens.length === 0) {
            container.innerHTML = '';
            return;
        }

        renderItens(
            container, categoria, template.itens,
            respostas.itens_marcados, respostas.observacoes,
            provaIdOrTipo
        );
    }

    function initAll() {
        document.querySelectorAll('.checklist-dinamico').forEach(initContainer);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAll);
    } else {
        initAll();
    }
})();
