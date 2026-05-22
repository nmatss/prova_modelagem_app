"""
Blueprint público: rotas SEM autenticação para visualização read-only
de relatórios via token de compartilhamento.
"""
import os
import secrets
from datetime import datetime

from flask import (
    Blueprint, render_template, request, abort, send_from_directory,
    current_app, redirect, url_for, flash,
)
from flask_login import login_required, current_user

from models import db, LinkPublico, Relatorio, FotoProva


publico_bp = Blueprint('publico', __name__)


def _registrar_acesso_log(acao, link, detalhes=None):
    """Registra acesso público.

    AuditLog.usuario_id é NOT NULL no schema atual; como acessos públicos são
    anônimos por definição, não tentamos persistir em AuditLog — apenas
    emitimos via app.logger. O contador `LinkPublico.visualizacoes` já faz a
    contagem persistente. Para usuário logado (raro nessas rotas), persiste normalmente.
    """
    from flask_login import current_user
    from flask import current_app

    if not current_user.is_authenticated:
        current_app.logger.info(
            f'PublicLink {acao}: token={link.token[:8]}... rel={link.relatorio_id} {detalhes or ""}'
        )
        return

    try:
        from app import registrar_log
        registrar_log(
            acao=acao,
            entidade_tipo='link_publico',
            entidade_id=link.id,
            entidade_descricao=f'Token {link.token[:8]}... · relatório #{link.relatorio_id}',
            detalhes=detalhes,
        )
    except Exception:
        pass


def _carregar_link_valido(token):
    """Carrega o link pelo token; retorna (link, motivo_invalido_ou_None)."""
    link = LinkPublico.query.filter_by(token=token).first()
    if not link:
        return None, 'inexistente'
    if not link.is_active:
        return link, 'revogado'
    if link.esta_expirado():
        return link, 'expirado'
    return link, None


@publico_bp.route('/<string:token>')
def visualizar(token):
    """Renderiza um relatório em modo read-only para o portador do token."""
    link, motivo = _carregar_link_valido(token)
    if motivo:
        return render_template('publico/expirado.html', motivo=motivo), 410 if motivo != 'inexistente' else 404

    relatorio = Relatorio.query.get(link.relatorio_id)
    if not relatorio or not relatorio.is_active:
        return render_template('publico/expirado.html', motivo='relatorio_removido'), 410

    # Incrementa contador e atualiza último acesso
    link.visualizacoes = (link.visualizacoes or 0) + 1
    link.ultimo_acesso = datetime.utcnow()
    db.session.commit()

    _registrar_acesso_log(
        'link_publico_acesso', link,
        detalhes=f'IP={request.remote_addr} UA={(request.user_agent.string or "")[:200]}'
    )

    return render_template(
        'publico/relatorio_view.html',
        link=link,
        relatorio=relatorio,
    )


@publico_bp.route('/<string:token>/pdf')
def baixar_pdf(token):
    """Baixa o PDF do relatório (se o link permitir)."""
    link, motivo = _carregar_link_valido(token)
    if motivo:
        return render_template('publico/expirado.html', motivo=motivo), 410 if motivo != 'inexistente' else 404

    if not link.permite_download_pdf:
        return render_template('publico/expirado.html', motivo='download_pdf_bloqueado'), 403

    relatorio = Relatorio.query.get(link.relatorio_id)
    if not relatorio or not relatorio.is_active:
        return render_template('publico/expirado.html', motivo='relatorio_removido'), 410

    from app import _gerar_pdf_relatorio_response
    _registrar_acesso_log(
        'link_publico_pdf', link,
        detalhes=f'IP={request.remote_addr}'
    )
    return _gerar_pdf_relatorio_response(relatorio, inline=False)


@publico_bp.route('/<string:token>/foto/<int:foto_id>')
def baixar_foto(token, foto_id):
    """Serve uma foto individual do relatório (validando que pertence ao mesmo)."""
    link, motivo = _carregar_link_valido(token)
    if motivo:
        abort(404)

    if not link.permite_download_fotos:
        abort(403)

    foto = FotoProva.query.get(foto_id)
    if not foto:
        abort(404)

    # Validar que a foto pertence ao relatório do link
    if foto.prova_id is None:
        abort(404)
    from models import ProvaModelagem as Prova
    prova = Prova.query.get(foto.prova_id)
    if not prova or prova.referencia is None:
        abort(404)
    if prova.referencia.relatorio_id != link.relatorio_id:
        abort(404)

    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        foto.file_path,
        as_attachment=False,
    )


# ============================================================================
# Rotas admin (login obrigatório) — gerar, listar, revogar links
# ============================================================================

@publico_bp.route('/admin/relatorio/<int:id>/gerar', methods=['POST'])
@login_required
def gerar(id):
    """Cria um novo link público para um relatório."""
    relatorio = Relatorio.query.get_or_404(id)

    expires_at = None
    expira_str = request.form.get('expira_em', '').strip()
    if expira_str:
        try:
            expires_at = datetime.strptime(expira_str, '%Y-%m-%d')
        except ValueError:
            flash('Data de expiração inválida.', 'danger')
            return redirect(url_for('detalhes_relatorio', id=id))

    link = LinkPublico(
        token=secrets.token_urlsafe(48),
        relatorio_id=relatorio.id,
        created_by=current_user.id,
        titulo_personalizado=request.form.get('titulo_personalizado', '').strip() or None,
        expires_at=expires_at,
        permite_download_pdf=bool(request.form.get('permite_download_pdf')),
        permite_download_fotos=bool(request.form.get('permite_download_fotos')),
    )
    db.session.add(link)
    db.session.commit()

    _registrar_acesso_log('link_publico_criado', link)

    flash('Link público gerado com sucesso. Copie a URL na lista abaixo.', 'success')
    return redirect(url_for('detalhes_relatorio', id=id, _anchor='links-publicos'))


@publico_bp.route('/admin/link/<int:link_id>/revogar', methods=['POST'])
@login_required
def revogar(link_id):
    """Desativa um link público existente."""
    link = LinkPublico.query.get_or_404(link_id)
    relatorio_id = link.relatorio_id
    link.is_active = False
    db.session.commit()
    _registrar_acesso_log('link_publico_revogado', link)
    flash('Link revogado.', 'success')
    return redirect(url_for('detalhes_relatorio', id=relatorio_id, _anchor='links-publicos'))
