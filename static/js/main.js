// Seleciona os elementos do modal uma vez para reutilização
const modal = document.getElementById('statusModal');
const modalProvaIdInput = document.getElementById('modalProvaId');
const modalNovoStatusInput = document.getElementById('modalNovoStatus');
const modalMotivoTextarea = document.getElementById('modalMotivo');

/**
 * Abre o modal para alterar o status de uma prova.
 * @param {HTMLElement} button - O botão que foi clicado.
 */
function openStatusModal(button) {
    // Pega os dados a partir dos atributos 'data-*' do botão
    const provaId = button.getAttribute('data-prova-id');
    const novoStatus = button.getAttribute('data-novo-status');

    // Define os valores dos campos escondidos no formulário do modal
    modalProvaIdInput.value = provaId;
    modalNovoStatusInput.value = novoStatus;
    
    // Limpa o campo de texto do motivo
    modalMotivoTextarea.value = '';
    
    // Mostra o modal
    modal.style.display = 'flex';
    
    // Coloca o cursor a piscar no campo do motivo
    modalMotivoTextarea.focus();
}

/**
 * Fecha o modal de alteração de status.
 */
function closeStatusModal() {
    // Esconde o modal
    modal.style.display = 'none';
}
