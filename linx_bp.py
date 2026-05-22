"""Blueprint Linx — endpoints REST + UI de seleção múltipla de produtos.

Resolve dois pedidos da reunião 04/05/2026:
- Item 6: Integração com Linx (db_puket em db01.grupounico.com)
- Item 1: Anexar múltiplos produtos de uma vez (via batch import do ERP)

Toda escrita é local (Fornecedor / Referencia / ProvaModelagem do Prova App).
O db_puket é estritamente read-only.
"""
from __future__ import annotations

import logging
from typing import Optional

from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

import linx_client
from models import db, Relatorio, Referencia, ProvaModelagem, Fornecedor

linx_bp = Blueprint('linx', __name__)
logger = logging.getLogger(__name__)

# Limite anti-abuso (e anti-acidente) no batch de import. Não tem motivo
# legítimo de criar >100 referências a partir de uma única tela.
ANEXAR_BATCH_MAX = 100


def _require_enabled():
    if not linx_client.is_enabled():
        abort(503, description='Integração Linx desabilitada. Configure LINX_DB_* no .env.')


def _audit(acao: str, entidade_tipo: str | None = None,
           entidade_id: int | None = None, entidade_descricao: str | None = None,
           detalhes: object = None) -> None:
    """Registra ação no audit log. Lazy import para evitar circular import com app."""
    try:
        from app import registrar_log  # noqa: PLC0415  (intencional: late binding)
        registrar_log(
            acao=acao,
            entidade_tipo=entidade_tipo,
            entidade_id=entidade_id,
            entidade_descricao=entidade_descricao,
            detalhes=detalhes,
        )
    except Exception as exc:  # noqa: BLE001
        # Audit nunca derruba o fluxo principal; só loga e segue.
        logger.warning('Falha ao registrar audit log Linx: %s', exc)


# ---------------------------------------------------------------------------
# Status / healthcheck
# ---------------------------------------------------------------------------

@linx_bp.route('/')
@login_required
def index():
    """Painel administrativo: status do ERP + atalhos."""
    status = linx_client.ping()
    colecoes = linx_client.listar_colecoes(limit=30) if status.get('ok') else []
    return render_template('linx_index.html', status=status, colecoes=colecoes)


@linx_bp.route('/status')
@login_required
def status():
    return jsonify(linx_client.ping())


@linx_bp.route('/cache/limpar', methods=['POST'])
@login_required
def limpar_cache():
    linx_client.cache_clear()
    flash('Cache do ERP limpo.', 'success')
    return redirect(url_for('linx.index'))


# ---------------------------------------------------------------------------
# Autocomplete JSON
# ---------------------------------------------------------------------------

@linx_bp.route('/api/fornecedores')
@login_required
def api_fornecedores():
    q = request.args.get('q', '').strip()
    limit = min(request.args.get('limit', 10, type=int), 50)
    return jsonify(linx_client.buscar_fornecedores(q, limit=limit))


@linx_bp.route('/api/fornecedores/<codigo>')
@login_required
def api_fornecedor(codigo):
    forn = linx_client.obter_fornecedor(codigo)
    if not forn:
        return jsonify({'error': 'não encontrado'}), 404
    return jsonify(forn)


@linx_bp.route('/api/produtos')
@login_required
def api_produtos():
    q = request.args.get('q', '').strip()
    colecao = request.args.get('colecao') or None
    limit = min(request.args.get('limit', 20, type=int), 100)
    return jsonify(linx_client.buscar_produtos(q, limit=limit, colecao=colecao))


@linx_bp.route('/api/produtos/<codigo>')
@login_required
def api_produto(codigo):
    prod = linx_client.obter_produto(codigo)
    if not prod:
        return jsonify({'error': 'não encontrado'}), 404
    return jsonify(prod)


@linx_bp.route('/api/colecoes')
@login_required
def api_colecoes():
    return jsonify(linx_client.listar_colecoes())


# ---------------------------------------------------------------------------
# Importar fornecedor único (a partir do botão "Buscar no ERP")
# ---------------------------------------------------------------------------

@linx_bp.route('/importar-fornecedor', methods=['POST'])
@login_required
def importar_fornecedor():
    _require_enabled()
    codigo = (request.form.get('codigo') or '').strip()
    if not codigo:
        flash('Código do fornecedor é obrigatório.', 'danger')
        return redirect(url_for('fornecedor.index'))

    forn_linx = linx_client.obter_fornecedor(codigo)
    if not forn_linx:
        flash(f'Fornecedor {codigo} não encontrado no ERP.', 'warning')
        return redirect(url_for('fornecedor.index'))

    forn_local, criado = _resolver_ou_criar_fornecedor_local(forn_linx)
    if forn_local is None:
        flash('Falha ao importar fornecedor (erro de integridade).', 'danger')
        return redirect(url_for('fornecedor.index'))

    if criado:
        _audit(
            acao='IMPORT_LINX',
            entidade_tipo='Fornecedor',
            entidade_id=forn_local.id,
            entidade_descricao=forn_local.nome,
            detalhes={'origem': 'linx', 'codigo_erp': forn_linx['codigo']},
        )
        flash(f'Fornecedor "{forn_local.nome}" importado do ERP.', 'success')
    else:
        flash(f'Fornecedor "{forn_local.nome}" já existia localmente — vinculado.', 'info')
    return redirect(url_for('fornecedor.detalhes', id=forn_local.id))


def _resolver_ou_criar_fornecedor_local(forn_linx: dict) -> tuple[Optional[Fornecedor], bool]:
    """Encontra ou cria um Fornecedor local a partir de um dict vindo do ERP.

    Retorna (fornecedor, criado_agora). `criado_agora=False` significa que
    já existia. Faz rollback em caso de IntegrityError (concorrência) e
    tenta lookup uma segunda vez para retornar o registro vencedor.
    """
    cnpj = forn_linx.get('cnpj') or None
    nome = forn_linx['nome']

    existente = None
    if cnpj:
        existente = Fornecedor.query.filter_by(cnpj=cnpj, is_active=True).first()
    if not existente:
        existente = Fornecedor.query.filter_by(nome=nome, is_active=True).first()
    if existente:
        return existente, False

    novo = Fornecedor(
        nome=nome,
        cnpj=cnpj,
        observacoes=(
            f"Importado do ERP (cod {forn_linx['codigo']}"
            f"{', tipo ' + forn_linx['tipo'] if forn_linx.get('tipo') else ''}"
            f"{', facção' if forn_linx.get('beneficiador') else ''})."
        ),
    )
    try:
        db.session.add(novo)
        db.session.flush()
        return novo, True
    except IntegrityError:
        db.session.rollback()
        # Outro request criou em paralelo — buscar de novo
        if cnpj:
            existente = Fornecedor.query.filter_by(cnpj=cnpj, is_active=True).first()
        if not existente:
            existente = Fornecedor.query.filter_by(nome=nome, is_active=True).first()
        return existente, False
    except SQLAlchemyError as exc:
        logger.error('Erro ao criar Fornecedor (Linx import): %s', exc)
        db.session.rollback()
        return None, False


# ---------------------------------------------------------------------------
# Anexar múltiplos produtos do ERP a um relatório (item 1 da reunião)
# ---------------------------------------------------------------------------

@linx_bp.route('/anexar-produtos/<int:relatorio_id>', methods=['GET'])
@login_required
def anexar_produtos(relatorio_id):
    """Tela de busca + seleção múltipla."""
    _require_enabled()
    relatorio = Relatorio.query.get_or_404(relatorio_id)
    q = request.args.get('q', '').strip()
    colecao = request.args.get('colecao') or None
    produtos = linx_client.buscar_produtos(q, limit=50, colecao=colecao) if q else []
    colecoes = linx_client.listar_colecoes(limit=50)
    return render_template(
        'linx_anexar_produtos.html',
        relatorio=relatorio,
        produtos=produtos,
        q=q,
        colecao_atual=colecao,
        colecoes=colecoes,
    )


@linx_bp.route('/anexar-produtos/<int:relatorio_id>', methods=['POST'])
@login_required
def anexar_produtos_post(relatorio_id):
    """Cria N Referencia + ProvaModelagem inicial a partir dos códigos selecionados.

    Limites de robustez:
    - Máximo de ANEXAR_BATCH_MAX códigos por chamada (defesa anti-abuso)
    - Toda a operação em uma única transação: se algo crítico falhar, rollback
      e nada fica importado pela metade
    - Audit log com sumário ao final
    """
    _require_enabled()
    relatorio = Relatorio.query.get_or_404(relatorio_id)
    codigos = request.form.getlist('codigo')
    if not codigos:
        flash('Nenhum produto selecionado.', 'warning')
        return redirect(url_for('linx.anexar_produtos', relatorio_id=relatorio_id))

    # Dedup + limpeza
    codigos = [c.strip() for c in codigos if c and c.strip()]
    codigos = list(dict.fromkeys(codigos))  # preserva ordem, remove duplicatas

    if len(codigos) > ANEXAR_BATCH_MAX:
        flash(
            f'Limite de {ANEXAR_BATCH_MAX} produtos por importação. Você selecionou {len(codigos)}.',
            'danger',
        )
        return redirect(url_for('linx.anexar_produtos', relatorio_id=relatorio_id))

    criados = 0
    duplicados = 0
    nao_encontrados = 0
    fornecedores_cache: dict[str, Optional[int]] = {}

    try:
        for codigo in codigos:
            ja_existe = Referencia.query.filter_by(
                relatorio_id=relatorio.id,
                numero_ref=codigo,
                is_active=True,
            ).first()
            if ja_existe:
                duplicados += 1
                continue

            prod = linx_client.obter_produto(codigo)
            if not prod:
                nao_encontrados += 1
                continue

            # Resolver fornecedor local (com cache por código ERP nesta requisição)
            fornecedor_id = None
            cod_forn = prod.get('fornecedor_codigo')
            if cod_forn:
                if cod_forn not in fornecedores_cache:
                    forn_linx = linx_client.obter_fornecedor(cod_forn)
                    if forn_linx:
                        forn_local, _ = _resolver_ou_criar_fornecedor_local(forn_linx)
                        fornecedores_cache[cod_forn] = forn_local.id if forn_local else None
                    else:
                        fornecedores_cache[cod_forn] = None
                fornecedor_id = fornecedores_cache[cod_forn]

            ref = Referencia(
                relatorio_id=relatorio.id,
                tipo_categoria=prod.get('categoria_sugerida') or 'adulto',
                numero_ref=prod['codigo'],
                codigo_referencia=prod.get('refer_fabricante') or prod['codigo'],
                fornecedor_id=fornecedor_id,
                origem='ERP Linx',
                gramatura=f"{prod['peso']:.3f}" if prod.get('peso') else None,
                observacoes=(
                    f"Importado do ERP em lote. "
                    f"Descrição ERP: {prod.get('descricao') or '—'}. "
                    f"Coleção: {prod.get('colecao') or '—'}. "
                    f"Linha: {prod.get('linha') or '—'}."
                ),
            )
            db.session.add(ref)
            db.session.flush()

            db.session.add(ProvaModelagem(
                referencia_id=ref.id,
                numero_prova=1,
                status='Em Andamento',
            ))
            criados += 1

        db.session.commit()
    except SQLAlchemyError as exc:
        db.session.rollback()
        logger.error('Falha no batch Linx anexar_produtos (relatorio %s): %s', relatorio_id, exc)
        flash('Erro ao anexar produtos: a operação foi revertida.', 'danger')
        return redirect(url_for('linx.anexar_produtos', relatorio_id=relatorio_id))

    _audit(
        acao='IMPORT_LINX_BATCH',
        entidade_tipo='Relatorio',
        entidade_id=relatorio.id,
        entidade_descricao=relatorio.codigo or relatorio.descricao_geral,
        detalhes={
            'origem': 'linx',
            'solicitados': len(codigos),
            'criados': criados,
            'duplicados': duplicados,
            'nao_encontrados': nao_encontrados,
        },
    )

    msg_partes = [f'{criados} produto(s) anexado(s)']
    if duplicados:
        msg_partes.append(f'{duplicados} já existia(m)')
    if nao_encontrados:
        msg_partes.append(f'{nao_encontrados} não encontrado(s) no ERP')
    flash('. '.join(msg_partes) + '.', 'success' if criados else 'warning')
    return redirect(url_for('detalhes_relatorio', id=relatorio.id))
