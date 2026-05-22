"""
Blueprint de Checklist Templates
Rotas para gerenciamento de templates de checklist dinâmico
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, ChecklistTemplate, ChecklistResposta
from admin import admin_required
from datetime import datetime
import json

checklist_bp = Blueprint('checklist', __name__)

# Categorias válidas para templates
CATEGORIAS_VALIDAS = ['qualidade', 'estilo', 'modelagem']

CATEGORIAS_DISPLAY = {
    'qualidade': 'Qualidade',
    'estilo': 'Estilo',
    'modelagem': 'Modelagem'
}

CATEGORIAS_CORES = {
    'qualidade': 'success',
    'estilo': 'info',
    'modelagem': 'warning'
}

CATEGORIAS_ICONES = {
    'qualidade': 'bi-check2-square',
    'estilo': 'bi-palette',
    'modelagem': 'bi-rulers'
}


@checklist_bp.route('/')
@login_required
@admin_required
def index():
    """Lista todos os templates de checklist (ativos e inativos)"""
    templates = ChecklistTemplate.query.order_by(
        ChecklistTemplate.categoria,
        ChecklistTemplate.is_active.desc(),
        ChecklistTemplate.created_at.desc()
    ).all()

    # Contar respostas vinculadas a cada template
    respostas_count = {}
    for t in templates:
        respostas_count[t.id] = ChecklistResposta.query.filter_by(template_id=t.id).count()

    return render_template('admin/checklists.html',
                           templates=templates,
                           respostas_count=respostas_count,
                           categorias_display=CATEGORIAS_DISPLAY,
                           categorias_cores=CATEGORIAS_CORES,
                           categorias_icones=CATEGORIAS_ICONES)


@checklist_bp.route('/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo():
    """Cria um novo template de checklist"""
    if request.method == 'POST':
        try:
            nome = request.form.get('nome', '').strip()
            categoria = request.form.get('categoria', '').strip().lower()
            itens_raw = request.form.get('itens', '').strip()

            # Validacoes
            if not nome:
                flash("O nome do template e obrigatorio.", "error")
                return render_template('admin/checklist_form.html',
                                       template=None,
                                       categorias=CATEGORIAS_VALIDAS,
                                       categorias_display=CATEGORIAS_DISPLAY,
                                       form_data=request.form)

            if categoria not in CATEGORIAS_VALIDAS:
                flash("Categoria invalida. Escolha entre: qualidade, estilo ou modelagem.", "error")
                return render_template('admin/checklist_form.html',
                                       template=None,
                                       categorias=CATEGORIAS_VALIDAS,
                                       categorias_display=CATEGORIAS_DISPLAY,
                                       form_data=request.form)

            if not itens_raw:
                flash("Informe pelo menos um item para o checklist.", "error")
                return render_template('admin/checklist_form.html',
                                       template=None,
                                       categorias=CATEGORIAS_VALIDAS,
                                       categorias_display=CATEGORIAS_DISPLAY,
                                       form_data=request.form)

            # Tentar interpretar como JSON primeiro, senao como lista separada por virgula
            itens_list = _parse_itens(itens_raw)

            if not itens_list:
                flash("Nenhum item valido encontrado. Separe os itens por virgula ou insira um JSON.", "error")
                return render_template('admin/checklist_form.html',
                                       template=None,
                                       categorias=CATEGORIAS_VALIDAS,
                                       categorias_display=CATEGORIAS_DISPLAY,
                                       form_data=request.form)

            # Criar template
            template = ChecklistTemplate(
                nome=nome,
                categoria=categoria,
                is_active=True
            )
            template.set_itens(itens_list)

            db.session.add(template)
            db.session.commit()

            flash(f"Template '{nome}' criado com sucesso com {len(itens_list)} itens!", "success")
            return redirect(url_for('checklist.index'))

        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao criar template: {e}", "error")
            return render_template('admin/checklist_form.html',
                                   template=None,
                                   categorias=CATEGORIAS_VALIDAS,
                                   categorias_display=CATEGORIAS_DISPLAY,
                                   form_data=request.form)

    return render_template('admin/checklist_form.html',
                           template=None,
                           categorias=CATEGORIAS_VALIDAS,
                           categorias_display=CATEGORIAS_DISPLAY,
                           form_data=None)


@checklist_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar(id):
    """Edita um template de checklist existente"""
    template = ChecklistTemplate.query.get_or_404(id)

    if request.method == 'POST':
        try:
            nome = request.form.get('nome', '').strip()
            categoria = request.form.get('categoria', '').strip().lower()
            itens_raw = request.form.get('itens', '').strip()

            # Validacoes
            if not nome:
                flash("O nome do template e obrigatorio.", "error")
                return render_template('admin/checklist_form.html',
                                       template=template,
                                       categorias=CATEGORIAS_VALIDAS,
                                       categorias_display=CATEGORIAS_DISPLAY,
                                       form_data=request.form)

            if categoria not in CATEGORIAS_VALIDAS:
                flash("Categoria invalida. Escolha entre: qualidade, estilo ou modelagem.", "error")
                return render_template('admin/checklist_form.html',
                                       template=template,
                                       categorias=CATEGORIAS_VALIDAS,
                                       categorias_display=CATEGORIAS_DISPLAY,
                                       form_data=request.form)

            if not itens_raw:
                flash("Informe pelo menos um item para o checklist.", "error")
                return render_template('admin/checklist_form.html',
                                       template=template,
                                       categorias=CATEGORIAS_VALIDAS,
                                       categorias_display=CATEGORIAS_DISPLAY,
                                       form_data=request.form)

            # Tentar interpretar como JSON primeiro, senao como lista separada por virgula
            itens_list = _parse_itens(itens_raw)

            if not itens_list:
                flash("Nenhum item valido encontrado. Separe os itens por virgula ou insira um JSON.", "error")
                return render_template('admin/checklist_form.html',
                                       template=template,
                                       categorias=CATEGORIAS_VALIDAS,
                                       categorias_display=CATEGORIAS_DISPLAY,
                                       form_data=request.form)

            # Atualizar template
            template.nome = nome
            template.categoria = categoria
            template.set_itens(itens_list)
            template.updated_at = datetime.utcnow()

            db.session.commit()

            flash(f"Template '{nome}' atualizado com sucesso com {len(itens_list)} itens!", "success")
            return redirect(url_for('checklist.index'))

        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar template: {e}", "error")
            return render_template('admin/checklist_form.html',
                                   template=template,
                                   categorias=CATEGORIAS_VALIDAS,
                                   categorias_display=CATEGORIAS_DISPLAY,
                                   form_data=request.form)

    return render_template('admin/checklist_form.html',
                           template=template,
                           categorias=CATEGORIAS_VALIDAS,
                           categorias_display=CATEGORIAS_DISPLAY,
                           form_data=None)


@checklist_bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
@admin_required
def excluir(id):
    """Soft delete - desativa o template de checklist"""
    template = ChecklistTemplate.query.get_or_404(id)

    try:
        template.is_active = False
        template.updated_at = datetime.utcnow()
        db.session.commit()
        flash(f"Template '{template.nome}' desativado com sucesso.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao desativar template: {e}", "error")

    return redirect(url_for('checklist.index'))


@checklist_bp.route('/<int:id>/reativar', methods=['POST'])
@login_required
@admin_required
def reativar(id):
    """Reativa um template de checklist desativado"""
    template = ChecklistTemplate.query.get_or_404(id)

    try:
        template.is_active = True
        template.updated_at = datetime.utcnow()
        db.session.commit()
        flash(f"Template '{template.nome}' reativado com sucesso.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao reativar template: {e}", "error")

    return redirect(url_for('checklist.index'))


@checklist_bp.route('/api/respostas/<int:prova_id>/<categoria>')
@login_required
def api_respostas_prova(prova_id, categoria):
    """Retorna as ChecklistResposta marcadas para um prova/categoria.
    Usado pelo frontend para pré-marcar itens dinâmicos ao abrir o editar."""
    categoria = categoria.strip().lower()
    if categoria not in CATEGORIAS_VALIDAS:
        return jsonify({'itens_marcados': [], 'observacoes': {}}), 400

    respostas = (
        ChecklistResposta.query
        .join(ChecklistTemplate, ChecklistResposta.template_id == ChecklistTemplate.id)
        .filter(
            ChecklistResposta.prova_id == prova_id,
            ChecklistTemplate.categoria == categoria,
        )
        .all()
    )
    return jsonify({
        'itens_marcados': [r.item for r in respostas if r.conforme],
        'observacoes': {r.item: r.observacao for r in respostas if r.observacao},
    })


@checklist_bp.route('/api/template/<categoria>')
@login_required
def api_template_por_categoria(categoria):
    """
    Retorna JSON com os itens do template ativo para a categoria informada.
    Usado pelo frontend para carregar dinamicamente os itens do checklist.
    """
    categoria = categoria.strip().lower()

    if categoria not in CATEGORIAS_VALIDAS:
        return jsonify({'error': 'Categoria invalida', 'itens': []}), 400

    template = ChecklistTemplate.query.filter_by(
        categoria=categoria,
        is_active=True
    ).order_by(ChecklistTemplate.updated_at.desc(), ChecklistTemplate.id.desc()).first()

    if not template:
        return jsonify({
            'template_id': None,
            'nome': None,
            'categoria': categoria,
            'itens': []
        })

    return jsonify({
        'template_id': template.id,
        'nome': template.nome,
        'categoria': template.categoria,
        'itens': template.get_itens()
    })


def _parse_itens(itens_raw):
    """
    Interpreta a string de itens como JSON array ou lista separada por virgula.
    Retorna uma lista de strings limpas (sem vazios).
    """
    itens_list = []

    # Tentar como JSON primeiro
    try:
        parsed = json.loads(itens_raw)
        if isinstance(parsed, list):
            itens_list = [str(item).strip() for item in parsed if str(item).strip()]
            return itens_list
    except (json.JSONDecodeError, TypeError):
        pass

    # Tentar como lista separada por virgula
    itens_list = [item.strip() for item in itens_raw.split(',') if item.strip()]

    return itens_list
