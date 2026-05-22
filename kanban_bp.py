from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from sqlalchemy import desc

from models import db, Relatorio, Referencia, ProvaModelagem as Prova, FotoProva

kanban_bp = Blueprint('kanban', __name__)

# Colunas do Kanban e suas ordens
KANBAN_COLUNAS = [
    'Em Andamento',
    'Comit\u00ea',
    'Aprovado',
    'Reprovado',
]


_CONTEXTO_PRIORIDADE = ('desenho', 'amostra', 'prova_modelo', 'qualidade', 'estilo', 'modelagem')


def _foto_destaque(relatorio, prova_ids):
    """Escolhe a foto de destaque do card. Prioridade:
    1. relatorio.imagem_produto
    2. Primeira FotoProva entre as provas do relatorio (preferindo contexto 'desenho').
    Retorna o file_path relativo ou None.
    """
    if relatorio.imagem_produto:
        return relatorio.imagem_produto

    if not prova_ids:
        return None

    fotos = FotoProva.query.filter(FotoProva.prova_id.in_(prova_ids)).all()
    if not fotos:
        return None

    fotos.sort(key=lambda f: (
        _CONTEXTO_PRIORIDADE.index(f.contexto) if f.contexto in _CONTEXTO_PRIORIDADE else 99,
        f.id,
    ))
    return fotos[0].file_path


def _build_card(relatorio):
    """Monta o dict de um card do Kanban a partir de um Relatorio."""
    referencias = Referencia.query.filter_by(
        relatorio_id=relatorio.id,
        is_active=True,
    ).all()

    total_referencias = len(referencias)
    total_provas = 0
    ultima_prova_status = None
    ultima_prova_created = None
    todas_prova_ids = []

    for ref in referencias:
        provas = Prova.query.filter_by(
            referencia_id=ref.id,
            is_active=True,
        ).order_by(desc(Prova.created_at)).all()

        total_provas += len(provas)
        todas_prova_ids.extend(p.id for p in provas)

        if provas:
            candidata = provas[0]  # mais recente desta referencia
            if (
                ultima_prova_created is None
                or (candidata.created_at and candidata.created_at > ultima_prova_created)
            ):
                ultima_prova_created = candidata.created_at
                ultima_prova_status = candidata.status

    return {
        'id': relatorio.id,
        'descricao_geral': relatorio.descricao_geral,
        'colecao': relatorio.colecao,
        'status_geral': relatorio.status_geral,
        'data_limite': relatorio.data_limite,
        'total_referencias': total_referencias,
        'total_provas': total_provas,
        'ultima_prova_status': ultima_prova_status,
        'foto_destaque': _foto_destaque(relatorio, todas_prova_ids),
    }


@kanban_bp.route('/')
@login_required
def index():
    """Renderiza o quadro Kanban com os relatorios organizados por status."""
    relatorios = Relatorio.query.filter_by(is_active=True).order_by(
        desc(Relatorio.created_at)
    ).all()

    # Inicializa as colunas vazias
    columns = {col: [] for col in KANBAN_COLUNAS}

    for rel in relatorios:
        status = rel.status_geral or 'Em Andamento'
        card = _build_card(rel)

        if status in columns:
            columns[status].append(card)
        else:
            # Status desconhecido vai para "Em Andamento"
            columns['Em Andamento'].append(card)

    return render_template('kanban.html', columns=columns)


@kanban_bp.route('/mover', methods=['POST'])
@login_required
def mover():
    """Endpoint AJAX para mover um card entre colunas (atualiza status_geral)."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'error': 'JSON inv\u00e1lido'}), 400

    relatorio_id = data.get('relatorio_id')
    novo_status = data.get('novo_status')

    if not relatorio_id or not novo_status:
        return jsonify({'success': False, 'error': 'Campos obrigat\u00f3rios ausentes'}), 400

    if novo_status not in KANBAN_COLUNAS:
        return jsonify({'success': False, 'error': 'Status inv\u00e1lido'}), 400

    relatorio = Relatorio.query.get(relatorio_id)
    if not relatorio:
        return jsonify({'success': False, 'error': 'Relat\u00f3rio n\u00e3o encontrado'}), 404

    relatorio.status_geral = novo_status
    db.session.commit()

    return jsonify({'success': True})
