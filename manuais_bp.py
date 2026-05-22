"""
Blueprint de Manuais / Documentos estáticos.

Permite ao setor anexar manuais (procedimentos, guias, normas) categorizados,
visíveis a todos usuários logados. Upload/edição restritos a administradores.
"""
import os
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash,
    send_from_directory, current_app, abort,
)
from flask_login import login_required, current_user
from sqlalchemy import desc

from models import db, Manual
from utils import save_file, delete_file
from admin import admin_required


manuais_bp = Blueprint('manuais', __name__)


CATEGORIAS = ['Estilo', 'Modelagem', 'Qualidade', 'Procedimentos', 'Outros']


@manuais_bp.route('/')
@login_required
def index():
    """Lista manuais ativos agrupados por categoria, com busca opcional."""
    q = request.args.get('q', '').strip()
    categoria_filtro = request.args.get('categoria', '').strip()

    query = Manual.query.filter_by(is_active=True)

    if q:
        like = f'%{q}%'
        query = query.filter(db.or_(
            Manual.titulo.ilike(like),
            Manual.descricao.ilike(like),
        ))

    if categoria_filtro:
        query = query.filter_by(categoria=categoria_filtro)

    manuais = query.order_by(Manual.categoria, desc(Manual.created_at)).all()

    # Agrupar por categoria
    agrupado = {}
    for m in manuais:
        cat = m.categoria or 'Outros'
        agrupado.setdefault(cat, []).append(m)

    return render_template(
        'manuais.html',
        manuais_por_categoria=agrupado,
        categorias=CATEGORIAS,
        q=q,
        categoria_filtro=categoria_filtro,
        total=len(manuais),
    )


@manuais_bp.route('/novo', methods=['GET', 'POST'])
@admin_required
def novo():
    """Upload de novo manual (apenas admin)."""
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        if not titulo:
            flash('O título do manual é obrigatório.', 'danger')
            return render_template('manual_form.html', manual=None, categorias=CATEGORIAS)

        arquivo = request.files.get('arquivo')
        if not arquivo or arquivo.filename == '':
            flash('Selecione um arquivo para o manual.', 'danger')
            return render_template('manual_form.html', manual=None, categorias=CATEGORIAS)

        filename = save_file(arquivo)
        if not filename:
            # save_file já emite flash com motivo
            return render_template('manual_form.html', manual=None, categorias=CATEGORIAS)

        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        try:
            file_size = os.path.getsize(filepath)
        except OSError:
            file_size = None

        manual = Manual(
            titulo=titulo,
            descricao=request.form.get('descricao', '').strip() or None,
            categoria=request.form.get('categoria', '').strip() or 'Outros',
            file_path=filename,
            file_size=file_size,
            uploaded_by=current_user.id,
        )
        db.session.add(manual)
        db.session.commit()

        _registrar_log('criar', manual, f'Manual criado: {titulo}')

        flash(f'Manual "{titulo}" enviado com sucesso.', 'success')
        return redirect(url_for('manuais.detalhes', id=manual.id))

    return render_template('manual_form.html', manual=None, categorias=CATEGORIAS)


@manuais_bp.route('/<int:id>')
@login_required
def detalhes(id):
    """Detalhes de um manual."""
    manual = Manual.query.filter_by(id=id, is_active=True).first_or_404()
    return render_template('manual_detalhes.html', manual=manual)


@manuais_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def editar(id):
    """Editar metadados do manual (não substitui o arquivo)."""
    manual = Manual.query.filter_by(id=id, is_active=True).first_or_404()

    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        if not titulo:
            flash('O título do manual é obrigatório.', 'danger')
            return render_template('manual_form.html', manual=manual, categorias=CATEGORIAS)

        manual.titulo = titulo
        manual.descricao = request.form.get('descricao', '').strip() or None
        manual.categoria = request.form.get('categoria', '').strip() or 'Outros'

        # Substituição opcional do arquivo
        arquivo = request.files.get('arquivo')
        if arquivo and arquivo.filename:
            novo_filename = save_file(arquivo)
            if novo_filename:
                arquivo_antigo = manual.file_path
                manual.file_path = novo_filename
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], novo_filename)
                try:
                    manual.file_size = os.path.getsize(filepath)
                except OSError:
                    pass
                # Remove o arquivo antigo do disco
                if arquivo_antigo:
                    delete_file(arquivo_antigo)

        db.session.commit()
        _registrar_log('editar', manual, f'Manual atualizado: {manual.titulo}')

        flash('Manual atualizado com sucesso.', 'success')
        return redirect(url_for('manuais.detalhes', id=manual.id))

    return render_template('manual_form.html', manual=manual, categorias=CATEGORIAS)


@manuais_bp.route('/<int:id>/download')
@login_required
def download(id):
    """Faz download do arquivo do manual e incrementa contador."""
    manual = Manual.query.filter_by(id=id, is_active=True).first_or_404()

    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], manual.file_path)
    if not os.path.exists(filepath):
        flash('Arquivo do manual não encontrado no disco.', 'danger')
        abort(404)

    manual.downloads = (manual.downloads or 0) + 1
    db.session.commit()

    _registrar_log('download', manual, f'Manual baixado: {manual.titulo}')

    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        manual.file_path,
        as_attachment=True,
        download_name=_nome_amigavel(manual),
    )


@manuais_bp.route('/<int:id>/excluir', methods=['POST'])
@admin_required
def excluir(id):
    """Soft delete do manual."""
    manual = Manual.query.filter_by(id=id, is_active=True).first_or_404()
    manual.is_active = False
    db.session.commit()

    _registrar_log('excluir', manual, f'Manual excluído: {manual.titulo}')

    flash(f'Manual "{manual.titulo}" excluído.', 'success')
    return redirect(url_for('manuais.index'))


def _nome_amigavel(manual):
    """Constroi um nome amigável para download preservando a extensão."""
    _, ext = os.path.splitext(manual.file_path)
    titulo_safe = ''.join(c if c.isalnum() or c in ' -_' else '_' for c in manual.titulo).strip() or 'manual'
    return f'{titulo_safe}{ext}'


def _registrar_log(acao, manual, descricao):
    """Wrapper para registrar no AuditLog reutilizando o helper do app.py."""
    try:
        from app import registrar_log
        registrar_log(
            acao=acao,
            entidade_tipo='manual',
            entidade_id=manual.id,
            entidade_descricao=descricao,
        )
    except Exception:
        # Audit log é best-effort; não bloqueia a ação
        pass
