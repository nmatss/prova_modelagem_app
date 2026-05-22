from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from sqlalchemy import desc
from models import db, Fornecedor, Referencia, ProvaModelagem as Prova

fornecedor_bp = Blueprint('fornecedor', __name__)


@fornecedor_bp.route('/')
@login_required
def index():
    """List all active fornecedores with search and pagination."""
    q = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 20

    query = Fornecedor.query.filter_by(is_active=True)

    if q:
        search = f'%{q}%'
        query = query.filter(
            db.or_(
                Fornecedor.nome.ilike(search),
                Fornecedor.cnpj.ilike(search),
                Fornecedor.email.ilike(search),
                Fornecedor.contato.ilike(search),
                Fornecedor.pais.ilike(search),
            )
        )

    query = query.order_by(Fornecedor.nome)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'fornecedores.html',
        fornecedores=pagination.items,
        pagination=pagination,
        q=q,
    )


@fornecedor_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    """Create a new fornecedor."""
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        if not nome:
            flash('O nome do fornecedor é obrigatório.', 'danger')
            return render_template('fornecedor_form.html', fornecedor=None)

        cnpj = request.form.get('cnpj', '').strip() or None
        if cnpj:
            existente = Fornecedor.query.filter_by(cnpj=cnpj, is_active=True).first()
            if existente:
                flash('Já existe um fornecedor ativo com este CNPJ.', 'danger')
                return render_template('fornecedor_form.html', fornecedor=None)

        fornecedor = Fornecedor(
            nome=nome,
            contato=request.form.get('contato', '').strip(),
            email=request.form.get('email', '').strip(),
            telefone=request.form.get('telefone', '').strip(),
            endereco=request.form.get('endereco', '').strip(),
            pais=request.form.get('pais', '').strip() or None,
            cnpj=cnpj,
            avaliacao=request.form.get('avaliacao', 0, type=int),
            observacoes=request.form.get('observacoes', '').strip(),
        )

        db.session.add(fornecedor)
        db.session.commit()
        flash(f'Fornecedor "{fornecedor.nome}" criado com sucesso.', 'success')
        return redirect(url_for('fornecedor.detalhes', id=fornecedor.id))

    return render_template('fornecedor_form.html', fornecedor=None)


@fornecedor_bp.route('/<int:id>')
@login_required
def detalhes(id):
    """Show fornecedor details with metrics."""
    fornecedor = Fornecedor.query.get_or_404(id)

    referencias = Referencia.query.filter_by(fornecedor_id=fornecedor.id).all()
    total_referencias = len(referencias)

    total_provas = 0
    provas_aprovadas = 0
    provas_reprovadas = 0
    provas_pendentes = 0

    for ref in referencias:
        provas = Prova.query.filter_by(referencia_id=ref.id).all()
        total_provas += len(provas)
        for prova in provas:
            status = getattr(prova, 'status', None)
            if status:
                status_lower = status.lower()
                if status_lower in ('aprovada', 'aprovado'):
                    provas_aprovadas += 1
                elif status_lower in ('reprovada', 'reprovado'):
                    provas_reprovadas += 1
                else:
                    provas_pendentes += 1
            else:
                provas_pendentes += 1

    taxa_aprovacao = round((provas_aprovadas / total_provas * 100) if total_provas > 0 else 0)

    return render_template(
        'fornecedor_detalhes.html',
        fornecedor=fornecedor,
        referencias=referencias,
        total_referencias=total_referencias,
        total_provas=total_provas,
        provas_aprovadas=provas_aprovadas,
        provas_reprovadas=provas_reprovadas,
        provas_pendentes=provas_pendentes,
        taxa_aprovacao=taxa_aprovacao,
    )


@fornecedor_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Edit an existing fornecedor."""
    fornecedor = Fornecedor.query.get_or_404(id)

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        if not nome:
            flash('O nome do fornecedor é obrigatório.', 'danger')
            return render_template('fornecedor_form.html', fornecedor=fornecedor)

        cnpj = request.form.get('cnpj', '').strip() or None
        if cnpj:
            existente = Fornecedor.query.filter(
                Fornecedor.cnpj == cnpj,
                Fornecedor.id != fornecedor.id,
                Fornecedor.is_active == True,
            ).first()
            if existente:
                flash('Já existe um fornecedor ativo com este CNPJ.', 'danger')
                return render_template('fornecedor_form.html', fornecedor=fornecedor)

        fornecedor.nome = nome
        fornecedor.contato = request.form.get('contato', '').strip()
        fornecedor.email = request.form.get('email', '').strip()
        fornecedor.telefone = request.form.get('telefone', '').strip()
        fornecedor.endereco = request.form.get('endereco', '').strip()
        fornecedor.pais = request.form.get('pais', '').strip() or None
        fornecedor.cnpj = cnpj
        fornecedor.avaliacao = request.form.get('avaliacao', 0, type=int)
        fornecedor.observacoes = request.form.get('observacoes', '').strip()

        db.session.commit()
        flash(f'Fornecedor "{fornecedor.nome}" atualizado com sucesso.', 'success')
        return redirect(url_for('fornecedor.detalhes', id=fornecedor.id))

    return render_template('fornecedor_form.html', fornecedor=fornecedor)


@fornecedor_bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    """Soft delete a fornecedor by setting is_active=False."""
    fornecedor = Fornecedor.query.get_or_404(id)
    fornecedor.is_active = False
    db.session.commit()
    flash(f'Fornecedor "{fornecedor.nome}" excluído com sucesso.', 'success')
    return redirect(url_for('fornecedor.index'))


@fornecedor_bp.route('/api/buscar')
@login_required
def api_buscar():
    """Autocomplete JSON endpoint. Returns list of {id, nome, cnpj}."""
    q = request.args.get('q', '').strip()
    if not q or len(q) < 2:
        return jsonify([])

    search = f'%{q}%'
    fornecedores = (
        Fornecedor.query
        .filter_by(is_active=True)
        .filter(
            db.or_(
                Fornecedor.nome.ilike(search),
                Fornecedor.cnpj.ilike(search),
            )
        )
        .order_by(Fornecedor.nome)
        .limit(10)
        .all()
    )

    results = [
        {'id': f.id, 'nome': f.nome, 'cnpj': f.cnpj or ''}
        for f in fornecedores
    ]
    return jsonify(results)
