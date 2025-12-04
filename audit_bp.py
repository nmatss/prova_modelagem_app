"""
Blueprint de Auditoria
Rotas para visualização e exportação de logs
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, jsonify
from flask_login import login_required, current_user
from models import db, AuditLog, Usuario
from admin import admin_required
from audit_helpers import get_acao_display, get_categoria_display, get_severidade_badge
from sqlalchemy import desc, func, or_
from datetime import datetime, timedelta
import csv
import io

audit_bp = Blueprint('audit', __name__, url_prefix='/admin/audit')

@audit_bp.route('/')
@login_required
@admin_required
def index():
    """Dashboard principal de auditoria"""
    page = request.args.get('page', 1, type=int)
    per_page = 50

    # Filtros
    usuario_id = request.args.get('usuario_id', type=int)
    categoria = request.args.get('categoria')
    acao = request.args.get('acao')
    severidade = request.args.get('severidade')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    busca = request.args.get('busca', '')

    # Query base
    query = AuditLog.query

    # Aplicar filtros
    if usuario_id:
        query = query.filter_by(usuario_id=usuario_id)

    if categoria:
        query = query.filter_by(categoria=categoria)

    if acao:
        query = query.filter_by(acao=acao)

    if severidade:
        query = query.filter_by(severidade=severidade)

    if data_inicio:
        try:
            data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d')
            query = query.filter(AuditLog.created_at >= data_inicio_obj)
        except ValueError:
            pass

    if data_fim:
        try:
            data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d')
            # Adicionar 1 dia para incluir todo o dia
            data_fim_obj = data_fim_obj + timedelta(days=1)
            query = query.filter(AuditLog.created_at < data_fim_obj)
        except ValueError:
            pass

    if busca:
        query = query.filter(
            or_(
                AuditLog.descricao.ilike(f'%{busca}%'),
                AuditLog.usuario_nome.ilike(f'%{busca}%'),
                AuditLog.entidade.ilike(f'%{busca}%')
            )
        )

    # Ordenar por data (mais recentes primeiro)
    query = query.order_by(desc(AuditLog.created_at))

    # Paginar
    logs = query.paginate(page=page, per_page=per_page, error_out=False)

    # Estatísticas rápidas
    total_logs = AuditLog.query.count()
    logs_hoje = AuditLog.query.filter(
        AuditLog.created_at >= datetime.now().replace(hour=0, minute=0, second=0)
    ).count()
    logs_semana = AuditLog.query.filter(
        AuditLog.created_at >= datetime.now() - timedelta(days=7)
    ).count()

    # Usuários mais ativos (últimos 7 dias)
    usuarios_ativos = db.session.query(
        AuditLog.usuario_id,
        AuditLog.usuario_nome,
        func.count(AuditLog.id).label('total')
    ).filter(
        AuditLog.created_at >= datetime.now() - timedelta(days=7)
    ).group_by(AuditLog.usuario_id, AuditLog.usuario_nome).order_by(desc('total')).limit(5).all()

    # Ações mais comuns (últimos 7 dias)
    acoes_comuns = db.session.query(
        AuditLog.acao,
        func.count(AuditLog.id).label('total')
    ).filter(
        AuditLog.created_at >= datetime.now() - timedelta(days=7)
    ).group_by(AuditLog.acao).order_by(desc('total')).limit(5).all()

    # Categorias
    categorias_stats = db.session.query(
        AuditLog.categoria,
        func.count(AuditLog.id).label('total')
    ).group_by(AuditLog.categoria).all()

    # Lista de usuários para filtro
    usuarios = Usuario.query.filter_by(is_active=True).order_by(Usuario.username).all()

    # Listas de opções para filtros
    categorias_opcoes = ['AUTENTICACAO', 'USUARIOS', 'RELATORIOS', 'PROVAS', 'APROVACOES', 'ARQUIVOS', 'SISTEMA', 'EXPORTACOES']
    acoes_opcoes = ['LOGIN', 'LOGOUT', 'CREATE', 'UPDATE', 'DELETE', 'APPROVE', 'REJECT', 'PASSWORD_RESET', 'ROLE_CHANGE']
    severidades_opcoes = ['INFO', 'WARNING', 'CRITICAL']

    return render_template('audit/index.html',
                         logs=logs,
                         total_logs=total_logs,
                         logs_hoje=logs_hoje,
                         logs_semana=logs_semana,
                         usuarios_ativos=usuarios_ativos,
                         acoes_comuns=acoes_comuns,
                         categorias_stats=categorias_stats,
                         usuarios=usuarios,
                         categorias_opcoes=categorias_opcoes,
                         acoes_opcoes=acoes_opcoes,
                         severidades_opcoes=severidades_opcoes,
                         get_acao_display=get_acao_display,
                         get_categoria_display=get_categoria_display,
                         get_severidade_badge=get_severidade_badge,
                         # Manter filtros aplicados
                         filtro_usuario_id=usuario_id,
                         filtro_categoria=categoria,
                         filtro_acao=acao,
                         filtro_severidade=severidade,
                         filtro_data_inicio=data_inicio,
                         filtro_data_fim=data_fim,
                         filtro_busca=busca)

@audit_bp.route('/detalhes/<int:log_id>')
@login_required
@admin_required
def detalhes(log_id):
    """Visualiza detalhes completos de um log"""
    log = AuditLog.query.get_or_404(log_id)

    # Converter JSON de volta para dict para exibição
    import json
    dados_antes = None
    dados_depois = None

    if log.dados_antes:
        try:
            dados_antes = json.loads(log.dados_antes)
        except Exception:
            dados_antes = log.dados_antes

    if log.dados_depois:
        try:
            dados_depois = json.loads(log.dados_depois)
        except Exception:
            dados_depois = log.dados_depois

    return render_template('audit/detalhes.html',
                         log=log,
                         dados_antes=dados_antes,
                         dados_depois=dados_depois,
                         get_acao_display=get_acao_display,
                         get_categoria_display=get_categoria_display,
                         get_severidade_badge=get_severidade_badge)

@audit_bp.route('/timeline/<string:entidade>/<int:entidade_id>')
@login_required
@admin_required
def timeline(entidade, entidade_id):
    """Timeline de atividades de uma entidade específica"""
    logs = AuditLog.query.filter_by(
        entidade=entidade,
        entidade_id=entidade_id
    ).order_by(desc(AuditLog.created_at)).all()

    return render_template('audit/timeline.html',
                         logs=logs,
                         entidade=entidade,
                         entidade_id=entidade_id,
                         get_acao_display=get_acao_display,
                         get_categoria_display=get_categoria_display,
                         get_severidade_badge=get_severidade_badge)

@audit_bp.route('/usuario/<int:usuario_id>')
@login_required
@admin_required
def por_usuario(usuario_id):
    """Visualiza todas as atividades de um usuário específico"""
    usuario = Usuario.query.get_or_404(usuario_id)
    page = request.args.get('page', 1, type=int)
    per_page = 50

    logs = AuditLog.query.filter_by(usuario_id=usuario_id).order_by(
        desc(AuditLog.created_at)
    ).paginate(page=page, per_page=per_page, error_out=False)

    # Estatísticas do usuário
    total_acoes = AuditLog.query.filter_by(usuario_id=usuario_id).count()
    ultima_atividade = AuditLog.query.filter_by(usuario_id=usuario_id).order_by(
        desc(AuditLog.created_at)
    ).first()

    acoes_por_categoria = db.session.query(
        AuditLog.categoria,
        func.count(AuditLog.id).label('total')
    ).filter_by(usuario_id=usuario_id).group_by(AuditLog.categoria).all()

    return render_template('audit/por_usuario.html',
                         usuario=usuario,
                         logs=logs,
                         total_acoes=total_acoes,
                         ultima_atividade=ultima_atividade,
                         acoes_por_categoria=acoes_por_categoria,
                         get_acao_display=get_acao_display,
                         get_categoria_display=get_categoria_display,
                         get_severidade_badge=get_severidade_badge)

@audit_bp.route('/exportar/csv')
@login_required
@admin_required
def exportar_csv():
    """Exporta logs em formato CSV"""
    # Aplicar os mesmos filtros da visualização
    usuario_id = request.args.get('usuario_id', type=int)
    categoria = request.args.get('categoria')
    acao = request.args.get('acao')
    severidade = request.args.get('severidade')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    busca = request.args.get('busca', '')

    query = AuditLog.query

    if usuario_id:
        query = query.filter_by(usuario_id=usuario_id)
    if categoria:
        query = query.filter_by(categoria=categoria)
    if acao:
        query = query.filter_by(acao=acao)
    if severidade:
        query = query.filter_by(severidade=severidade)
    if data_inicio:
        try:
            data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d')
            query = query.filter(AuditLog.created_at >= data_inicio_obj)
        except ValueError:
            pass
    if data_fim:
        try:
            data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(AuditLog.created_at < data_fim_obj)
        except ValueError:
            pass
    if busca:
        query = query.filter(
            or_(
                AuditLog.descricao.ilike(f'%{busca}%'),
                AuditLog.usuario_nome.ilike(f'%{busca}%')
            )
        )

    logs = query.order_by(desc(AuditLog.created_at)).limit(10000).all()

    # Criar CSV
    output = io.StringIO()
    writer = csv.writer(output)

    # Cabeçalho
    writer.writerow([
        'ID',
        'Data/Hora',
        'Usuário',
        'Ação',
        'Entidade',
        'Entidade ID',
        'Categoria',
        'Severidade',
        'Descrição',
        'IP Address'
    ])

    # Dados
    for log in logs:
        writer.writerow([
            log.id,
            log.created_at.strftime('%d/%m/%Y %H:%M:%S'),
            log.usuario_nome,
            get_acao_display(log.acao),
            log.entidade,
            log.entidade_id or '',
            get_categoria_display(log.categoria),
            log.severidade,
            log.descricao,
            log.ip_address or ''
        ])

    # Preparar resposta
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = f'attachment; filename=audit_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

    return response

@audit_bp.route('/estatisticas')
@login_required
@admin_required
def estatisticas():
    """Página de estatísticas detalhadas"""
    # Estatísticas gerais
    total_logs = AuditLog.query.count()

    # Logs por período
    hoje = datetime.now().replace(hour=0, minute=0, second=0)
    logs_hoje = AuditLog.query.filter(AuditLog.created_at >= hoje).count()
    logs_semana = AuditLog.query.filter(AuditLog.created_at >= hoje - timedelta(days=7)).count()
    logs_mes = AuditLog.query.filter(AuditLog.created_at >= hoje - timedelta(days=30)).count()

    # Por categoria
    logs_por_categoria = db.session.query(
        AuditLog.categoria,
        func.count(AuditLog.id).label('total')
    ).group_by(AuditLog.categoria).order_by(desc('total')).all()

    # Por ação
    logs_por_acao = db.session.query(
        AuditLog.acao,
        func.count(AuditLog.id).label('total')
    ).group_by(AuditLog.acao).order_by(desc('total')).limit(10).all()

    # Por severidade
    logs_por_severidade = db.session.query(
        AuditLog.severidade,
        func.count(AuditLog.id).label('total')
    ).group_by(AuditLog.severidade).all()

    # Usuários mais ativos (todos os tempos)
    usuarios_mais_ativos = db.session.query(
        AuditLog.usuario_id,
        AuditLog.usuario_nome,
        func.count(AuditLog.id).label('total')
    ).group_by(AuditLog.usuario_id, AuditLog.usuario_nome).order_by(desc('total')).limit(10).all()

    # Atividade por dia (últimos 30 dias)
    atividade_diaria = db.session.query(
        func.date(AuditLog.created_at).label('dia'),
        func.count(AuditLog.id).label('total')
    ).filter(
        AuditLog.created_at >= hoje - timedelta(days=30)
    ).group_by('dia').order_by('dia').all()

    return render_template('audit/estatisticas.html',
                         total_logs=total_logs,
                         logs_hoje=logs_hoje,
                         logs_semana=logs_semana,
                         logs_mes=logs_mes,
                         logs_por_categoria=logs_por_categoria,
                         logs_por_acao=logs_por_acao,
                         logs_por_severidade=logs_por_severidade,
                         usuarios_mais_ativos=usuarios_mais_ativos,
                         atividade_diaria=atividade_diaria,
                         get_acao_display=get_acao_display,
                         get_categoria_display=get_categoria_display)
