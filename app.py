import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, jsonify, make_response
from flask_compress import Compress
from weasyprint import HTML, CSS
from werkzeug.datastructures import MultiDict
from werkzeug.utils import secure_filename
# from xhtml2pdf import pisa  # Comentado temporariamente - instalar: pip install xhtml2pdf
from flask_login import LoginManager, login_required, current_user
from auth import auth_bp, get_user_by_id
from admin import admin_bp
from audit_bp import audit_bp  # ✅ Habilitado - AuditLog existe no banco (models.py)
from db import init_app as init_db
from models import db, Relatorio, Referencia, Prova, Foto, AuditLog
from config import Config
from utils import save_file
from excel_export import export_relatorios_to_excel, export_detalhes_to_excel
from error_handlers import register_error_handlers
from security import init_security, SecurityHeaders
from sqlalchemy import desc

# Configurar logging será feito após criar o app
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Carregar configurações do config.py
app.config.from_object(Config)
Config.init_app(app)

# Configurar logging para produção
if not app.debug:
    # Log para arquivo
    if Config.LOG_FILE:
        file_handler = RotatingFileHandler(
            Config.LOG_FILE,
            maxBytes=10485760,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(getattr(logging, Config.LOG_LEVEL.upper()))
        app.logger.addHandler(file_handler)

    # Log para console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(getattr(logging, Config.LOG_LEVEL.upper()))
    stream_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    app.logger.addHandler(stream_handler)

    app.logger.setLevel(getattr(logging, Config.LOG_LEVEL.upper()))
    app.logger.info('Aplicação de Provas iniciada em modo produção')
else:
    # Desenvolvimento - log simples
    logging.basicConfig(level=logging.INFO)
    app.logger.info('Aplicação de Provas iniciada em modo desenvolvimento')

# Inicializar database
init_db(app)

# Inicializar segurança
init_security(app)

# ========================================
# COMPRESSÃO GZIP/BROTLI
# ========================================
# Configurar compressão de respostas HTTP
compress = Compress()
compress.init_app(app)

# Configurações de compressão
app.config['COMPRESS_MIMETYPES'] = [
    'text/html',
    'text/css',
    'text/xml',
    'text/plain',
    'text/javascript',
    'application/json',
    'application/javascript',
    'application/xml',
    'application/xhtml+xml',
    'application/rss+xml',
    'application/atom+xml',
    'image/svg+xml'
]
app.config['COMPRESS_LEVEL'] = 6  # 1-9, padrão 6
app.config['COMPRESS_MIN_SIZE'] = 500  # Comprimir apenas arquivos > 500 bytes
app.config['COMPRESS_ALGORITHM'] = 'gzip'  # 'gzip' ou 'br' (brotli)

app.logger.info(f'Compressão HTTP habilitada: {app.config["COMPRESS_ALGORITHM"].upper()}')

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'info'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

# ========================================
# SISTEMA DE AUDITORIA
# ========================================

def registrar_log(acao, entidade_tipo=None, entidade_id=None, entidade_descricao=None, detalhes=None):
    """
    Registra uma ação no sistema de auditoria

    Args:
        acao: Tipo de ação (criar, editar, excluir, login, logout, etc)
        entidade_tipo: Tipo da entidade afetada (relatorio, prova, referencia, usuario, etc)
        entidade_id: ID da entidade afetada
        entidade_descricao: Descrição da entidade para histórico
        detalhes: Informações adicionais em formato texto ou JSON
    """
    try:
        import json
        from flask_login import current_user

        # Obter informações do usuário atual
        usuario_id = current_user.id if current_user.is_authenticated else None
        usuario_nome = current_user.username if current_user.is_authenticated else 'Sistema'

        # Obter IP e User Agent
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')[:500]

        # Converter detalhes para JSON se for dict
        if isinstance(detalhes, dict):
            detalhes = json.dumps(detalhes, ensure_ascii=False)

        # Criar registro de log
        log = AuditLog(
            usuario_id=usuario_id,
            usuario_nome=usuario_nome,
            acao=acao,
            entidade_tipo=entidade_tipo,
            entidade_id=entidade_id,
            entidade_descricao=entidade_descricao,
            detalhes=detalhes,
            ip_address=ip_address,
            user_agent=user_agent
        )

        db.session.add(log)
        db.session.commit()

        app.logger.info(f'Audit Log: {usuario_nome} {acao} {entidade_tipo}#{entidade_id}')

    except Exception as e:
        app.logger.error(f'Erro ao registrar log de auditoria: {str(e)}')
        db.session.rollback()

# Registrar Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(audit_bp, url_prefix='/auditoria')  # ✅ Habilitado - AuditLog existe

# Registrar error handlers
register_error_handlers(app)


# ========================================
# OTIMIZAÇÕES DE PERFORMANCE
# ========================================

@app.after_request
def optimize_response(response):
    """Otimizações de performance e segurança nas respostas"""
    from datetime import datetime, timedelta

    # 1. CACHE HEADERS - Otimização de Performance
    if request.path.startswith('/static/'):
        # Cache agressivo para assets estáticos (1 ano)
        response.cache_control.public = True
        response.cache_control.max_age = 31536000  # 1 ano
        response.cache_control.immutable = True
        response.expires = datetime.now() + timedelta(days=365)
    elif request.path.startswith('/uploads/'):
        # Cache moderado para uploads (30 dias)
        response.cache_control.public = True
        response.cache_control.max_age = 2592000  # 30 dias
    elif response.content_type and 'text/html' in response.content_type:
        # Sem cache para HTML dinâmico
        response.cache_control.no_cache = True
        response.cache_control.no_store = True
        response.cache_control.must_revalidate = True
    elif response.content_type and 'application/json' in response.content_type:
        # Cache curto para API JSON (5 minutos)
        response.cache_control.public = True
        response.cache_control.max_age = 300

    # 2. COMPRESSION HINTS
    if 'Content-Type' in response.headers:
        content_type = response.headers['Content-Type']
        compressible = ['text/', 'application/json', 'application/javascript',
                       'application/xml', 'image/svg+xml']
        if any(ct in content_type for ct in compressible):
            response.vary = 'Accept-Encoding'

    return response


def gerar_e_salvar_pdf(relatorio_id, evento="CRIADO"):
    """
    Geração de PDF desabilitada temporariamente.
    Para habilitar: pip install xhtml2pdf e descomentar import acima
    """
    print(f"PDF não gerado (xhtml2pdf não instalado) para relatório ID: {relatorio_id} (Evento: {evento})")
    return True  # Retornar True para não quebrar o fluxo

    # CÓDIGO COMENTADO - Descomente após instalar xhtml2pdf
    # print(f"Iniciando geração de PDF para o relatório ID: {relatorio_id} (Evento: {evento})")
    #
    # relatorio = Relatorio.query.get(relatorio_id)
    # if not relatorio:
    #     print(f"!!! ERRO: Relatório com ID {relatorio_id} não encontrado para gerar PDF.")
    #     return False
    #
    # # Preparar dados para o template (mantendo estrutura compatível)
    # referencias_completas = []
    # for ref in relatorio.referencias:
    #     ref_dict = {c.name: getattr(ref, c.name) for c in ref.__table__.columns}
    #
    #     provas_completas = []
    #     for prova in ref.provas:
    #         prova_dict = {c.name: getattr(prova, c.name) for c in prova.__table__.columns}
    #
    #         prova_dict['fotos'] = {}
    #         for foto in prova.fotos:
    #             contexto = foto.contexto
    #             if contexto not in prova_dict['fotos']:
    #                 prova_dict['fotos'][contexto] = []
    #             prova_dict['fotos'][contexto].append({c.name: getattr(foto, c.name) for c in foto.__table__.columns})
    #
    #         provas_completas.append(prova_dict)
    #
    #     ref_dict['provas'] = provas_completas
    #     referencias_completas.append(ref_dict)
    #
    # assunto_email = f"RELATÓRIO DE PROVA PEÇA PILOTO {evento}! {relatorio.descricao_geral} COLEÇÃO {relatorio.colecao}"
    # nome_ficheiro_pdf = f"{secure_filename(assunto_email)}.pdf"
    # caminho_ficheiro_pdf = os.path.join(app.config['PDF_FOLDER'], nome_ficheiro_pdf)
    #
    # html_renderizado = render_template('relatorio_pdf.html',
    #                                    relatorio=relatorio,
    #                                    referencias=referencias_completas)
    #
    # def link_callback(uri, rel):
    #     if uri.startswith(url_for('serve_upload', filename='')):
    #         path_relativo = uri[len(url_for('serve_upload', filename='')):]
    #         caminho_final = os.path.join(app.config['UPLOAD_FOLDER'], path_relativo)
    #         return caminho_final
    #     return uri
    #
    # try:
    #     with open(caminho_ficheiro_pdf, "w+b") as pdf_file:
    #         pisa_status = pisa.CreatePDF(
    #             html_renderizado.encode('utf-8'),
    #             dest=pdf_file,
    #             encoding='utf-8',
    #             link_callback=link_callback
    #         )
    #
    #     if not pisa_status.err:
    #         print(f"\n--- PDF Gerado: {caminho_ficheiro_pdf} ---\n")
    #         return True
    #     else:
    #         print(f"!!! ERRO AO GERAR PDF: {pisa_status.err}")
    #         return False
    # except Exception as e:
    #     print(f"!!! EXCEÇÃO AO GERAR PDF: {e}")
    #     return False

@app.route('/')
@login_required
def dashboard():
    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = 20

    # Obter relatórios paginados
    pagination = Relatorio.query.order_by(desc(Relatorio.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    relatorios = pagination.items
    relatorios_com_status = []

    for relatorio in relatorios:
        relatorio_dict = {c.name: getattr(relatorio, c.name) for c in relatorio.__table__.columns}

        # Obter última prova de qualquer referência deste relatório
        ultima_prova = Prova.query.join(Referencia).filter(Referencia.relatorio_id == relatorio.id).order_by(desc(Prova.numero_prova)).first()

        relatorio_dict['status_atual'] = ultima_prova.status if ultima_prova else 'Novo'

        # Buscar primeira foto do relatório
        # Ordem de prioridade: imagem_produto do relatório > primeira foto de qualquer prova
        primeira_foto = None

        if relatorio.imagem_produto:
            primeira_foto = relatorio.imagem_produto
        else:
            # Buscar primeira foto de qualquer prova deste relatório
            foto = Foto.query.join(Prova).join(Referencia).filter(
                Referencia.relatorio_id == relatorio.id
            ).order_by(Foto.id).first()

            if foto:
                primeira_foto = foto.file_path

        relatorio_dict['primeira_foto'] = primeira_foto

        # Buscar informações das referências
        referencias = Referencia.query.filter_by(relatorio_id=relatorio.id).all()
        relatorio_dict['total_referencias'] = len(referencias)

        # Categoria (primeira categoria encontrada)
        categorias = [r.tipo_categoria for r in referencias if r.tipo_categoria]
        relatorio_dict['categoria'] = categorias[0] if categorias else None

        # Fornecedores únicos
        fornecedores = list(set([r.fornecedor for r in referencias if r.fornecedor]))
        relatorio_dict['fornecedores'] = ', '.join(fornecedores) if fornecedores else None

        # Data de criação formatada
        if relatorio.created_at:
            relatorio_dict['data_criacao'] = relatorio.created_at.strftime('%d/%m/%Y')
        else:
            relatorio_dict['data_criacao'] = 'N/A'

        # Total de provas
        total_provas = Prova.query.join(Referencia).filter(Referencia.relatorio_id == relatorio.id).count()
        relatorio_dict['total_provas'] = total_provas

        relatorios_com_status.append(relatorio_dict)

    # ESTATÍSTICAS E INSIGHTS
    total_relatorios = Relatorio.query.count()
    total_referencias = Referencia.query.count()
    total_provas = Prova.query.count()

    # Provas por status - Valores em MAIÚSCULAS após padronização
    provas_aprovadas = Prova.query.filter_by(status='APROVADA').count()
    provas_reprovadas = Prova.query.filter_by(status='REPROVADA').count()
    provas_em_andamento = Prova.query.filter_by(status='EM ANDAMENTO').count()
    provas_comite = Prova.query.filter_by(status='COMITÊ').count()

    # Taxa de aprovação
    taxa_aprovacao = round((provas_aprovadas / total_provas * 100) if total_provas > 0 else 0, 1)

    # Referências por categoria
    refs_por_categoria = db.session.query(
        Referencia.tipo_categoria,
        db.func.count(Referencia.id)
    ).group_by(Referencia.tipo_categoria).all()

    categorias_stats = {cat: count for cat, count in refs_por_categoria}

    # Relatórios recentes (últimos 30 dias)
    from datetime import datetime, timedelta
    trinta_dias_atras = datetime.utcnow() - timedelta(days=30)
    relatorios_recentes = Relatorio.query.filter(Relatorio.created_at >= trinta_dias_atras).count()

    # Provas com retrabalho (número da prova > 1)
    provas_retrabalho = Prova.query.filter(Prova.numero_prova > 1).count()
    taxa_retrabalho = round((provas_retrabalho / total_provas * 100) if total_provas > 0 else 0, 1)

    # Insights
    insights = []

    if taxa_aprovacao >= 80:
        insights.append({
            'tipo': 'success',
            'icone': 'bi-trophy',
            'titulo': 'Excelente Performance!',
            'mensagem': f'Taxa de aprovação de {taxa_aprovacao}% - acima da meta de 80%'
        })
    elif taxa_aprovacao >= 60:
        insights.append({
            'tipo': 'warning',
            'icone': 'bi-exclamation-triangle',
            'titulo': 'Performance Moderada',
            'mensagem': f'Taxa de aprovação de {taxa_aprovacao}% - pode melhorar'
        })
    else:
        insights.append({
            'tipo': 'danger',
            'icone': 'bi-exclamation-circle',
            'titulo': 'Atenção Necessária',
            'mensagem': f'Taxa de aprovação baixa: {taxa_aprovacao}% - revisar processos'
        })

    if taxa_retrabalho > 30:
        insights.append({
            'tipo': 'warning',
            'icone': 'bi-arrow-repeat',
            'titulo': 'Alto Retrabalho',
            'mensagem': f'{taxa_retrabalho}% das provas precisaram de retrabalho'
        })

    if relatorios_recentes > 5:
        insights.append({
            'tipo': 'info',
            'icone': 'bi-calendar-check',
            'titulo': 'Alta Produtividade',
            'mensagem': f'{relatorios_recentes} relatórios criados nos últimos 30 dias'
        })

    if provas_em_andamento > 10:
        insights.append({
            'tipo': 'info',
            'icone': 'bi-hourglass-split',
            'titulo': 'Provas Pendentes',
            'mensagem': f'{provas_em_andamento} provas aguardando finalização'
        })

    # Média de provas por referência
    media_provas_por_referencia = round((total_provas / total_referencias) if total_referencias > 0 else 0, 1)

    stats = {
        'total_relatorios': total_relatorios,
        'total_referencias': total_referencias,
        'total_provas': total_provas,
        'provas_aprovadas': provas_aprovadas,
        'provas_reprovadas': provas_reprovadas,
        'provas_em_andamento': provas_em_andamento,
        'provas_comite': provas_comite,
        'taxa_aprovacao': taxa_aprovacao,
        'taxa_retrabalho': taxa_retrabalho,
        'media_provas_por_referencia': media_provas_por_referencia,
        'categorias': categorias_stats,
        'relatorios_recentes': relatorios_recentes,
        'insights': insights
    }

    return render_template('dashboard.html', relatorios=relatorios_com_status, stats=stats, pagination=pagination)

@app.route('/favicon.ico')
def favicon():
    """Serve favicon from static folder"""
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.route('/uploads/<path:filename>')
@login_required
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/relatorio/<int:id>')
@login_required
def detalhes_relatorio(id):
    relatorio = Relatorio.query.get_or_404(id)
    
    # Preparar estrutura para template
    referencias_completas = []
    for ref in relatorio.referencias:
        ref_dict = {c.name: getattr(ref, c.name) for c in ref.__table__.columns}
        
        provas_completas = []
        # Ordenar provas por número
        provas_ordenadas = sorted(ref.provas, key=lambda x: x.numero_prova)
        
        for prova in provas_ordenadas:
            prova_dict = {c.name: getattr(prova, c.name) for c in prova.__table__.columns}
            
            prova_dict['fotos'] = {}
            for foto in prova.fotos:
                contexto = foto.contexto
                if contexto not in prova_dict['fotos']:
                    prova_dict['fotos'][contexto] = []
                prova_dict['fotos'][contexto].append({c.name: getattr(foto, c.name) for c in foto.__table__.columns})
            
            provas_completas.append(prova_dict)
        
        ref_dict['provas'] = provas_completas
        referencias_completas.append(ref_dict)

    return render_template('detalhes_relatorio.html', relatorio=relatorio, referencias=referencias_completas)

@app.route('/relatorio/<int:id>/pdf')
@login_required
def relatorio_pdf(id):
    """Gera e retorna o PDF do relatório"""
    relatorio = Relatorio.query.get_or_404(id)

    # Preparar dados para o template (mesma estrutura do detalhes_relatorio)
    referencias_completas = []
    for ref in relatorio.referencias:
        ref_dict = {c.name: getattr(ref, c.name) for c in ref.__table__.columns}

        provas_completas = []
        provas_ordenadas = sorted(ref.provas, key=lambda x: x.numero_prova)

        for prova in provas_ordenadas:
            prova_dict = {c.name: getattr(prova, c.name) for c in prova.__table__.columns}

            prova_dict['fotos'] = {}
            for foto in prova.fotos:
                contexto = foto.contexto
                if contexto not in prova_dict['fotos']:
                    prova_dict['fotos'][contexto] = []
                # Adicionar caminho absoluto para WeasyPrint
                foto_dict = {c.name: getattr(foto, c.name) for c in foto.__table__.columns}
                foto_dict['caminho_absoluto'] = os.path.join(app.config['UPLOAD_FOLDER'], foto.file_path)
                prova_dict['fotos'][contexto].append(foto_dict)

            provas_completas.append(prova_dict)

        ref_dict['provas'] = provas_completas
        referencias_completas.append(ref_dict)

    # Renderizar o HTML do PDF
    from datetime import datetime
    html_string = render_template('relatorio_pdf.html',
                                   relatorio=relatorio,
                                   referencias=referencias_completas,
                                   now=datetime.now)

    # Gerar PDF usando WeasyPrint com base_url do diretório de uploads
    pdf = HTML(string=html_string, base_url=request.url_root).write_pdf()

    # Criar resposta
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=relatorio_{relatorio.id}_{secure_filename(relatorio.descricao_geral)}.pdf'

    return response

@app.route('/relatorio/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_relatorio(id):
    relatorio = Relatorio.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # 1. Atualiza as informações gerais do relatório
            relatorio.colecao = request.form.get('colecao')
            relatorio.descricao_geral = request.form.get('descricao_geral')

            # Atualiza PPT se um novo arquivo foi enviado
            ppt_file = request.files.get('ppt')
            if ppt_file and ppt_file.filename:
                # Excluir PPT antigo se existir
                if relatorio.ppt_path:
                    from utils import delete_file
                    delete_file(relatorio.ppt_path)
                # Salvar novo PPT
                ppt_filename = save_file(ppt_file)
                if ppt_filename:
                    relatorio.ppt_path = ppt_filename
            
            # 2. Itera sobre todos os tipos possíveis
            for tipo in ['baby', 'kids', 'teen', 'adulto']:
                ref_numero = request.form.get(f'ref_{tipo}')
                if not ref_numero:
                    continue

                # Verifica se já existe uma referência deste tipo
                ref_existente = Referencia.query.filter_by(relatorio_id=id, tipo_categoria=tipo).first()

                if ref_existente:
                    # --- ATUALIZAÇÃO ---
                    ref_existente.numero_ref = ref_numero
                    # Atualiza dados da referência (busca por ID específico ou por tipo)
                    ref_existente.origem = request.form.get(f'origem_ref_{ref_existente.id}') or request.form.get(f'origem_{tipo}')
                    ref_existente.fornecedor = request.form.get(f'fornecedor_ref_{ref_existente.id}') or request.form.get(f'fornecedor_{tipo}')
                    ref_existente.materia_prima = request.form.get(f'materia_prima_ref_{ref_existente.id}') or request.form.get(f'materia_prima_{tipo}')
                    ref_existente.composicao = request.form.get(f'composicao_ref_{ref_existente.id}') or request.form.get(f'composicao_{tipo}')
                    ref_existente.gramatura = request.form.get(f'gramatura_ref_{ref_existente.id}') or request.form.get(f'gramatura_{tipo}')
                    ref_existente.aviamentos = request.form.get(f'aviamentos_ref_{ref_existente.id}') or request.form.get(f'aviamentos_{tipo}')
                    
                    # Atualiza provas existentes
                    provas_existentes_ids = request.form.getlist(f'prova_id_{tipo}')
                    for prova_id in provas_existentes_ids:
                        prova = Prova.query.get(prova_id)
                        if prova:
                            prova.data_recebimento = request.form.get(f'data_recebimento_{prova_id}')
                            prova.tamanhos_recebidos = ", ".join(request.form.getlist(f'tamanhos_recebidos_{prova_id}'))
                            prova.info_medidas = request.form.get(f'info_medidas_{prova_id}')
                            prova.data_prova = request.form.get(f'data_prova_{prova_id}')
                            prova.time_qualidade = request.form.get(f'time_qualidade_{prova_id}')
                            prova.comentarios_qualidade = request.form.get(f'comentarios_qualidade_{prova_id}')
                            prova.obs_qualidade = request.form.get(f'obs_qualidade_{prova_id}')
                            prova.time_estilo = request.form.get(f'time_estilo_{prova_id}')
                            prova.comentarios_estilo = request.form.get(f'comentarios_estilo_{prova_id}')
                            prova.obs_estilo = request.form.get(f'obs_estilo_{prova_id}')
                            prova.time_modelagem = request.form.get(f'time_modelagem_{prova_id}')
                            prova.comentarios_modelagem = request.form.get(f'comentarios_modelagem_{prova_id}')
                            prova.obs_modelagem = request.form.get(f'obs_modelagem_{prova_id}')
                            prova.data_lacre = request.form.get(f'data_lacre_{prova_id}')
                            prova.numero_lacre = request.form.get(f'numero_lacre_{prova_id}')
                            prova.info_adicionais = request.form.get(f'info_adicionais_{prova_id}')
                            
                            # Adicionar fotos
                            campos_fotos = ['desenho', 'qualidade', 'estilo', 'modelagem']
                            for contexto in campos_fotos:
                                for file in request.files.getlist(f'fotos_{contexto}_{prova_id}'):
                                    filename = save_file(file)
                                    if filename:
                                        foto = Foto(prova_id=prova.id, contexto=contexto, file_path=filename)
                                        db.session.add(foto)
                            
                            for tamanho in request.form.getlist(f'tamanhos_recebidos_{prova_id}'):
                                for contexto in ['amostra', 'prova_modelo']:
                                    for file in request.files.getlist(f'fotos_{contexto}_{prova_id}_{tamanho.replace(" ", "")}'):
                                        filename = save_file(file)
                                        if filename:
                                            foto = Foto(prova_id=prova.id, contexto=contexto, tamanho=tamanho, file_path=filename)
                                            db.session.add(foto)

                else:
                    # --- CRIAÇÃO ---
                    nova_ref = Referencia(
                        relatorio_id=id,
                        tipo_categoria=tipo,
                        numero_ref=ref_numero,
                        origem=request.form.get(f'origem_{tipo}'),
                        fornecedor=request.form.get(f'fornecedor_{tipo}'),
                        materia_prima=request.form.get(f'materia_prima_{tipo}'),
                        composicao=request.form.get(f'composicao_{tipo}'),
                        gramatura=request.form.get(f'gramatura_{tipo}'),
                        aviamentos=request.form.get(f'aviamentos_{tipo}')
                    )
                    db.session.add(nova_ref)
                    db.session.flush() # Para obter o ID

                    tabela_medidas_filename = save_file(request.files.get(f'tabela_medidas_{tipo}'))

                    nova_prova = Prova(
                        referencia_id=nova_ref.id,
                        numero_prova=1,
                        tabela_medidas_path=tabela_medidas_filename,
                        data_recebimento=request.form.get(f'data_recebimento_{tipo}'),
                        tamanhos_recebidos=", ".join(request.form.getlist(f'tamanhos_recebidos_{tipo}')),
                        info_medidas=request.form.get(f'info_medidas_{tipo}'),
                        data_prova=request.form.get(f'data_prova_{tipo}'),
                        time_qualidade=request.form.get(f'time_qualidade_{tipo}'),
                        comentarios_qualidade=request.form.get(f'comentarios_qualidade_{tipo}'),
                        obs_qualidade=request.form.get(f'obs_qualidade_{tipo}'),
                        time_estilo=request.form.get(f'time_estilo_{tipo}'),
                        comentarios_estilo=request.form.get(f'comentarios_estilo_{tipo}'),
                        obs_estilo=request.form.get(f'obs_estilo_{tipo}'),
                        time_modelagem=request.form.get(f'time_modelagem_{tipo}'),
                        comentarios_modelagem=request.form.get(f'comentarios_modelagem_{tipo}'),
                        obs_modelagem=request.form.get(f'obs_modelagem_{tipo}'),
                        data_lacre=request.form.get(f'data_lacre_{tipo}'),
                        numero_lacre=request.form.get(f'numero_lacre_{tipo}'),
                        info_adicionais=request.form.get(f'info_adicionais_{tipo}')
                    )
                    db.session.add(nova_prova)
                    db.session.flush()
                    
                    campos_fotos = ['desenho', 'qualidade', 'estilo', 'modelagem']
                    for contexto in campos_fotos:
                        for file in request.files.getlist(f'fotos_{contexto}_{tipo}'):
                            filename = save_file(file)
                            if filename:
                                foto = Foto(prova_id=nova_prova.id, contexto=contexto, file_path=filename)
                                db.session.add(foto)

                    for tamanho in request.form.getlist(f'tamanhos_recebidos_{tipo}'):
                        for contexto in ['amostra', 'prova_modelo']:
                            for file in request.files.getlist(f'fotos_{contexto}_{tipo}_{tamanho.replace(" ", "")}'):
                                filename = save_file(file)
                                if filename:
                                    foto = Foto(prova_id=nova_prova.id, contexto=contexto, tamanho=tamanho, file_path=filename)
                                    db.session.add(foto)

            db.session.commit()
            flash("Relatório atualizado com sucesso!", "success")
            gerar_e_salvar_pdf(id, evento="ATUALIZADO")
            return redirect(url_for('detalhes_relatorio', id=id))

        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar o relatório: {e}", "error")
            return redirect(url_for('editar_relatorio', id=id))
    
    # GET
    referencias_por_tipo = {}
    for ref in relatorio.referencias:
        ref_dict = {c.name: getattr(ref, c.name) for c in ref.__table__.columns}
        
        provas_completas = []
        provas_ordenadas = sorted(ref.provas, key=lambda x: x.numero_prova)
        for prova in provas_ordenadas:
            prova_dict = {c.name: getattr(prova, c.name) for c in prova.__table__.columns}
            prova_dict['tamanhos_lista'] = [t.strip() for t in (prova.tamanhos_recebidos or '').split(',') if t.strip()]
            
            prova_dict['fotos'] = {}
            for foto in prova.fotos:
                contexto = foto.contexto
                if contexto not in prova_dict['fotos']:
                    prova_dict['fotos'][contexto] = []
                prova_dict['fotos'][contexto].append({c.name: getattr(foto, c.name) for c in foto.__table__.columns})
            provas_completas.append(prova_dict)
        
        ref_dict['provas'] = provas_completas
        referencias_por_tipo[ref.tipo_categoria] = ref_dict

    return render_template('editar_relatorio.html', relatorio=relatorio, referencias_por_tipo=referencias_por_tipo)


@app.route('/prova/atualizar_status', methods=['POST'])
@login_required
def atualizar_status():
    prova_id = request.form.get('prova_id')
    novo_status = request.form.get('novo_status')
    motivo = request.form.get('motivo')
    
    try:
        prova = Prova.query.get(prova_id)
        if prova:
            prova.status = novo_status
            prova.motivo_ultima_alteracao = motivo
            db.session.commit()
            
            flash(f"Status da prova atualizado para '{novo_status}' com sucesso!", "success")
            
            # Encontrar relatório para gerar PDF
            relatorio_id = prova.referencia.relatorio_id
            gerar_e_salvar_pdf(relatorio_id, evento="ATUALIZADO")
            return redirect(url_for('detalhes_relatorio', id=relatorio_id))
            
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao atualizar o status: {e}", "error")
        return redirect(url_for('dashboard'))
    
    return redirect(url_for('dashboard'))

@app.route('/novo', methods=['GET', 'POST'])
@login_required
def novo_relatorio():
    if request.method == 'POST':
        try:
            ppt_filename = save_file(request.files.get('ppt'))
            imagem_produto_filename = save_file(request.files.get('imagem_produto'))
            ficha_tecnica_filename = save_file(request.files.get('ficha_tecnica'))

            novo_relatorio = Relatorio(
                descricao_geral=request.form.get('descricao_geral'),
                colecao=request.form.get('colecao'),
                ppt_path=ppt_filename,
                imagem_produto=imagem_produto_filename,
                ficha_tecnica=ficha_tecnica_filename
            )
            db.session.add(novo_relatorio)
            db.session.flush()
            
            for tipo in ['baby', 'kids', 'teen', 'adulto']:
                if request.form.get(f'ref_{tipo}'):
                    nova_ref = Referencia(
                        relatorio_id=novo_relatorio.id,
                        tipo_categoria=tipo,
                        numero_ref=request.form.get(f'ref_{tipo}'),
                        origem=request.form.get(f'origem_{tipo}'),
                        fornecedor=request.form.get(f'fornecedor_{tipo}'),
                        materia_prima=request.form.get(f'materia_prima_{tipo}'),
                        composicao=request.form.get(f'composicao_{tipo}'),
                        gramatura=request.form.get(f'gramatura_{tipo}'),
                        aviamentos=request.form.get(f'aviamentos_{tipo}')
                    )
                    db.session.add(nova_ref)
                    db.session.flush()

                    tabela_medidas_filename = save_file(request.files.get(f'tabela_medidas_{tipo}'))

                    nova_prova = Prova(
                        referencia_id=nova_ref.id,
                        numero_prova=1,
                        tabela_medidas_path=tabela_medidas_filename,
                        data_recebimento=request.form.get(f'data_recebimento_{tipo}'),
                        tamanhos_recebidos=", ".join(request.form.getlist(f'tamanhos_recebidos_{tipo}')),
                        info_medidas=request.form.get(f'info_medidas_{tipo}'),
                        data_prova=request.form.get(f'data_prova_{tipo}'),
                        time_qualidade=request.form.get(f'time_qualidade_{tipo}'),
                        comentarios_qualidade=request.form.get(f'comentarios_qualidade_{tipo}'),
                        obs_qualidade=request.form.get(f'obs_qualidade_{tipo}'),
                        time_estilo=request.form.get(f'time_estilo_{tipo}'),
                        comentarios_estilo=request.form.get(f'comentarios_estilo_{tipo}'),
                        obs_estilo=request.form.get(f'obs_estilo_{tipo}'),
                        time_modelagem=request.form.get(f'time_modelagem_{tipo}'),
                        comentarios_modelagem=request.form.get(f'comentarios_modelagem_{tipo}'),
                        obs_modelagem=request.form.get(f'obs_modelagem_{tipo}'),
                        data_lacre=request.form.get(f'data_lacre_{tipo}'),
                        numero_lacre=request.form.get(f'numero_lacre_{tipo}'),
                        info_adicionais=request.form.get(f'info_adicionais_{tipo}')
                    )
                    db.session.add(nova_prova)
                    db.session.flush()
                    
                    campos_fotos = ['desenho', 'qualidade', 'estilo', 'modelagem']
                    for contexto in campos_fotos:
                        for file in request.files.getlist(f'fotos_{contexto}_{tipo}'):
                            filename = save_file(file)
                            if filename:
                                foto = Foto(prova_id=nova_prova.id, contexto=contexto, file_path=filename)
                                db.session.add(foto)

                    for tamanho in request.form.getlist(f'tamanhos_recebidos_{tipo}'):
                        for contexto in ['amostra', 'prova_modelo']:
                            for file in request.files.getlist(f'fotos_{contexto}_{tipo}_{tamanho.replace(" ", "")}'):
                                filename = save_file(file)
                                if filename:
                                    foto = Foto(prova_id=nova_prova.id, contexto=contexto, tamanho=tamanho, file_path=filename)
                                    db.session.add(foto)
            
            db.session.commit()
            flash("Relatório criado com sucesso!", "success")
            
            gerar_e_salvar_pdf(novo_relatorio.id, evento="CRIADO")
            
            return redirect(url_for('dashboard'))

        except Exception as e:
            db.session.rollback()
            print(f"!!! ERRO AO SALVAR NO BANCO DE DADOS: {e}")
            flash(f"Ocorreu um erro ao salvar o relatório: {e}. Por favor, verifique os campos e tente novamente.", "error")
            return render_template('novo_relatorio.html', form_data=request.form)

    return render_template('novo_relatorio.html', form_data=MultiDict())

@app.route('/relatorio/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_relatorio(id):
    """Exclui um relatório e todos os seus arquivos associados"""
    relatorio = Relatorio.query.get_or_404(id)

    try:
        # Coletar todos os arquivos para excluir
        arquivos_para_excluir = []

        # PPT do relatório
        if relatorio.ppt_path:
            arquivos_para_excluir.append(relatorio.ppt_path)

        # Arquivos de referências e provas
        for ref in relatorio.referencias:
            for prova in ref.provas:
                # Tabela de medidas
                if prova.tabela_medidas_path:
                    arquivos_para_excluir.append(prova.tabela_medidas_path)
                # Fotos
                for foto in prova.fotos:
                    if foto.file_path:
                        arquivos_para_excluir.append(foto.file_path)

        # Excluir do banco (cascade delete cuida das referências, provas e fotos)
        descricao = relatorio.descricao_geral
        colecao = relatorio.colecao
        db.session.delete(relatorio)
        db.session.commit()

        # Registrar log de auditoria
        registrar_log(
            acao='excluir',
            entidade_tipo='relatorio',
            entidade_id=id,
            entidade_descricao=f'{descricao} - {colecao}',
            detalhes=f'Excluído {len(arquivos_para_excluir)} arquivo(s) associado(s)'
        )

        # Excluir arquivos físicos
        from utils import delete_file
        for arquivo in arquivos_para_excluir:
            delete_file(arquivo)

        flash(f"Relatório '{descricao}' excluído com sucesso!", "success")
        return redirect(url_for('dashboard'))

    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir o relatório: {e}", "error")
        return redirect(url_for('detalhes_relatorio', id=id))


@app.route('/referencia/<int:referencia_id>/nova_prova', methods=['GET', 'POST'])
@login_required
def adicionar_nova_prova(referencia_id):
    referencia = Referencia.query.get_or_404(referencia_id)

    if request.method == 'POST':
        try:
            novo_numero_prova = request.form.get('numero_prova')
            tipo = referencia.tipo_categoria

            tabela_medidas_filename = save_file(request.files.get(f'tabela_medidas_{tipo}'))

            nova_prova = Prova(
                referencia_id=referencia.id,
                numero_prova=novo_numero_prova,
                tabela_medidas_path=tabela_medidas_filename,
                data_recebimento=request.form.get(f'data_recebimento_{tipo}'),
                tamanhos_recebidos=", ".join(request.form.getlist(f'tamanhos_recebidos_{tipo}')),
                info_medidas=request.form.get(f'info_medidas_{tipo}'),
                data_prova=request.form.get(f'data_prova_{tipo}'),
                time_qualidade=request.form.get(f'time_qualidade_{tipo}'),
                checklist_qualidade=", ".join(request.form.getlist(f'checklist_qualidade_{tipo}')),
                comentarios_qualidade=request.form.get(f'comentarios_qualidade_{tipo}'),
                obs_qualidade=request.form.get(f'obs_qualidade_{tipo}'),
                time_estilo=request.form.get(f'time_estilo_{tipo}'),
                checklist_estilo=", ".join(request.form.getlist(f'checklist_estilo_{tipo}')),
                comentarios_estilo=request.form.get(f'comentarios_estilo_{tipo}'),
                obs_estilo=request.form.get(f'obs_estilo_{tipo}'),
                time_modelagem=request.form.get(f'time_modelagem_{tipo}'),
                checklist_modelagem=", ".join(request.form.getlist(f'checklist_modelagem_{tipo}')),
                comentarios_modelagem=request.form.get(f'comentarios_modelagem_{tipo}'),
                obs_modelagem=request.form.get(f'obs_modelagem_{tipo}'),
                data_lacre=request.form.get(f'data_lacre_{tipo}'),
                numero_lacre=request.form.get(f'numero_lacre_{tipo}'),
                info_adicionais=request.form.get(f'info_adicionais_{tipo}')
            )
            db.session.add(nova_prova)
            db.session.flush()
            
            campos_fotos = ['desenho', 'qualidade', 'estilo', 'modelagem']
            for contexto in campos_fotos:
                for file in request.files.getlist(f'fotos_{contexto}_{tipo}'):
                    filename = save_file(file)
                    if filename:
                        foto = Foto(prova_id=nova_prova.id, contexto=contexto, file_path=filename)
                        db.session.add(foto)

            for tamanho in request.form.getlist(f'tamanhos_recebidos_{tipo}'):
                for contexto in ['amostra', 'prova_modelo']:
                    for file in request.files.getlist(f'fotos_{contexto}_{tipo}_{tamanho.replace(" ", "")}'):
                        filename = save_file(file)
                        if filename:
                            foto = Foto(prova_id=nova_prova.id, contexto=contexto, tamanho=tamanho, file_path=filename)
                            db.session.add(foto)
            
            db.session.commit()
            flash(f"{novo_numero_prova}ª prova adicionada com sucesso!", "success")

            gerar_e_salvar_pdf(referencia.relatorio_id, evento="ATUALIZADO")

            return redirect(url_for('detalhes_relatorio', id=referencia.relatorio_id))

        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao salvar a nova prova: {e}", "error")
            return redirect(url_for('detalhes_relatorio', id=referencia.relatorio_id))
    
    ultima_prova = Prova.query.filter_by(referencia_id=referencia_id).order_by(desc(Prova.numero_prova)).first()
    novo_numero_prova = ultima_prova.numero_prova + 1 if ultima_prova else 1

    return render_template('nova_prova.html', referencia=referencia, novo_numero_prova=novo_numero_prova)


@app.route('/exportar/excel')
@login_required
def exportar_relatorios_excel():
    """Exporta todos os relatórios para Excel"""
    try:
        relatorios = Relatorio.query.order_by(desc(Relatorio.created_at)).all()
        relatorios_data = []

        for relatorio in relatorios:
            # Contar referências
            num_referencias = Referencia.query.filter_by(relatorio_id=relatorio.id).count()

            # Obter status atual
            ultima_prova = Prova.query.join(Referencia).filter(
                Referencia.relatorio_id == relatorio.id
            ).order_by(desc(Prova.numero_prova)).first()

            relatorios_data.append({
                'id': relatorio.id,
                'colecao': relatorio.colecao or '',
                'descricao_geral': relatorio.descricao_geral or '',
                'num_referencias': num_referencias,
                'status_geral': ultima_prova.status if ultima_prova else 'Novo',
                'data_criacao': relatorio.created_at.strftime('%d/%m/%Y %H:%M') if relatorio.created_at else ''
            })

        filename = export_relatorios_to_excel(relatorios_data)

        flash(f'Relatórios exportados com sucesso!', 'success')
        return send_from_directory(app.config['PDF_FOLDER'], filename, as_attachment=True)

    except Exception as e:
        flash(f'Erro ao exportar relatórios: {e}', 'error')
        return redirect(url_for('dashboard'))


@app.route('/relatorio/<int:id>/excel')
@login_required
def exportar_relatorio_excel(id):
    """Exporta detalhes de um relatório específico para Excel"""
    try:
        relatorio = Relatorio.query.get_or_404(id)

        # Preparar dados do relatório
        relatorio_data = {
            'id': relatorio.id,
            'colecao': relatorio.colecao,
            'descricao_geral': relatorio.descricao_geral
        }

        # Preparar referências com provas
        referencias = []
        for ref in relatorio.referencias:
            ref_data = {
                'numero_ref': ref.numero_ref,
                'tipo': ref.tipo_categoria,
                'provas': []
            }

            for prova in ref.provas:
                ref_data['provas'].append({
                    'numero_prova': prova.numero_prova,
                    'status': prova.status,
                    'data_recebimento': prova.data_recebimento,
                    'data_prova': prova.data_prova,
                    'tamanhos_recebidos': prova.tamanhos_recebidos
                })

            referencias.append(ref_data)

        filename = export_detalhes_to_excel(relatorio_data, referencias)

        flash(f'Relatório exportado para Excel!', 'success')
        return send_from_directory(app.config['PDF_FOLDER'], filename, as_attachment=True)

    except Exception as e:
        flash(f'Erro ao exportar relatório: {e}', 'error')
        return redirect(url_for('detalhes_relatorio', id=id))


@app.route('/importar/excel', methods=['GET', 'POST'])
@login_required
def importar_relatorios_excel():
    """Importa relatórios de um arquivo Excel"""
    if request.method == 'POST':
        try:
            from openpyxl import load_workbook

            arquivo = request.files.get('arquivo_excel')
            if not arquivo or arquivo.filename == '':
                flash('Nenhum arquivo selecionado!', 'error')
                return redirect(url_for('dashboard'))

            # Verificar extensão
            if not arquivo.filename.endswith(('.xlsx', '.xls')):
                flash('Formato inválido! Use apenas arquivos Excel (.xlsx ou .xls)', 'error')
                return redirect(url_for('dashboard'))

            # Salvar temporariamente
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
                arquivo.save(temp_file.name)
                temp_path = temp_file.name

            # Carregar workbook
            wb = load_workbook(temp_path, data_only=True)

            relatorios_importados = 0
            erros = []

            # Ler aba "Informações Gerais" ou primeira aba
            if "Informações Gerais" in wb.sheetnames:
                ws = wb["Informações Gerais"]
            else:
                ws = wb.active

            # Processar dados (assumindo formato: linha 1 = header, linha 2+ = dados)
            headers = [cell.value for cell in ws[1]]

            for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
                try:
                    # Criar dicionário de dados da linha
                    dados = dict(zip(headers, row))

                    if not dados.get('Descrição'):
                        continue  # Pular linhas vazias

                    # Criar relatório
                    novo_rel = Relatorio(
                        descricao_geral=str(dados.get('Descrição', '')).upper(),
                        colecao=str(dados.get('Coleção', '')).upper() if dados.get('Coleção') else None,
                        temporada=str(dados.get('Temporada', '')).upper() if dados.get('Temporada') else None,
                        ano=int(dados.get('Ano')) if dados.get('Ano') and str(dados.get('Ano')).isdigit() else None,
                        status_geral=str(dados.get('Status Geral', 'EM ANDAMENTO')).upper()
                    )
                    db.session.add(novo_rel)
                    relatorios_importados += 1

                except Exception as e:
                    erros.append(f"Linha {row_idx}: {str(e)}")
                    continue

            db.session.commit()

            # Remover arquivo temporário
            import os
            os.unlink(temp_path)

            if relatorios_importados > 0:
                flash(f'✅ {relatorios_importados} relatório(s) importado(s) com sucesso!', 'success')

            if erros:
                flash(f'⚠️ {len(erros)} erro(s) durante importação. Verifique o formato do arquivo.', 'warning')

            return redirect(url_for('dashboard'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao importar arquivo: {str(e)}', 'error')
            return redirect(url_for('dashboard'))

    # GET - Mostrar página de upload
    return redirect(url_for('dashboard'))


# ========================================
# PÁGINA DE RELATÓRIOS E ANALYTICS
# ========================================

@app.route('/analytics')
@login_required
def analytics():
    """Página de relatórios e analytics com filtros"""
    from datetime import datetime, timedelta

    # Obter parâmetros de filtro
    filtro_status = request.args.get('status', '')
    filtro_categoria = request.args.get('categoria', '')
    filtro_colecao = request.args.get('colecao', '')
    filtro_fornecedor = request.args.get('fornecedor', '')
    filtro_referencia = request.args.get('referencia', '')
    filtro_data_inicio = request.args.get('data_inicio', '')
    filtro_data_fim = request.args.get('data_fim', '')

    # Query base de provas
    query_provas = Prova.query.join(Referencia).join(Relatorio)

    # Aplicar filtros
    if filtro_status:
        query_provas = query_provas.filter(Prova.status == filtro_status)
    if filtro_categoria:
        query_provas = query_provas.filter(Referencia.tipo_categoria == filtro_categoria)
    if filtro_colecao:
        query_provas = query_provas.filter(Relatorio.colecao == filtro_colecao)
    if filtro_fornecedor:
        query_provas = query_provas.filter(Referencia.fornecedor == filtro_fornecedor)
    if filtro_referencia:
        # Busca parcial por número de referência (case-insensitive)
        query_provas = query_provas.filter(Referencia.numero_ref.ilike(f'%{filtro_referencia}%'))

    # Filtro de data
    if filtro_data_inicio:
        try:
            data_inicio = datetime.strptime(filtro_data_inicio, '%Y-%m-%d')
            query_provas = query_provas.filter(Prova.created_at >= data_inicio)
        except:
            pass
    if filtro_data_fim:
        try:
            data_fim = datetime.strptime(filtro_data_fim, '%Y-%m-%d')
            data_fim = data_fim + timedelta(days=1)  # Incluir o dia inteiro
            query_provas = query_provas.filter(Prova.created_at < data_fim)
        except:
            pass

    # ========================================
    # ESTATÍSTICAS GERAIS (sem filtros)
    # ========================================
    total_relatorios = Relatorio.query.count()
    total_referencias = Referencia.query.count()
    total_provas = Prova.query.count()

    # Por status (sem filtros) - Valores em MAIÚSCULAS após padronização
    provas_aprovadas = Prova.query.filter_by(status='APROVADA').count()
    provas_reprovadas = Prova.query.filter_by(status='REPROVADA').count()
    provas_em_andamento = Prova.query.filter_by(status='EM ANDAMENTO').count()
    provas_comite = Prova.query.filter_by(status='COMITÊ').count()

    # Taxa de aprovação
    taxa_aprovacao = round((provas_aprovadas / total_provas * 100) if total_provas > 0 else 0, 1)
    taxa_reprovacao = round((provas_reprovadas / total_provas * 100) if total_provas > 0 else 0, 1)

    # Provas com retrabalho
    provas_retrabalho = Prova.query.filter(Prova.numero_prova > 1).count()
    taxa_retrabalho = round((provas_retrabalho / total_provas * 100) if total_provas > 0 else 0, 1)

    # ========================================
    # ESTATÍSTICAS FILTRADAS
    # ========================================
    provas_filtradas = query_provas.all()
    total_filtrado = len(provas_filtradas)

    filtrado_aprovadas = sum(1 for p in provas_filtradas if p.status == 'APROVADA')
    filtrado_reprovadas = sum(1 for p in provas_filtradas if p.status == 'REPROVADA')
    filtrado_em_andamento = sum(1 for p in provas_filtradas if p.status == 'EM ANDAMENTO')
    filtrado_comite = sum(1 for p in provas_filtradas if p.status == 'COMITÊ')

    taxa_aprovacao_filtrada = round((filtrado_aprovadas / total_filtrado * 100) if total_filtrado > 0 else 0, 1)

    # ========================================
    # DADOS PARA GRÁFICOS
    # ========================================

    # Por categoria
    categorias_stats = db.session.query(
        Referencia.tipo_categoria,
        db.func.count(Referencia.id)
    ).group_by(Referencia.tipo_categoria).all()

    # Por status
    status_stats = db.session.query(
        Prova.status,
        db.func.count(Prova.id)
    ).group_by(Prova.status).all()

    # Por fornecedor (top 10)
    fornecedores_stats = db.session.query(
        Referencia.fornecedor,
        db.func.count(Referencia.id)
    ).filter(Referencia.fornecedor.isnot(None), Referencia.fornecedor != '').group_by(
        Referencia.fornecedor
    ).order_by(db.func.count(Referencia.id).desc()).limit(10).all()

    # Por coleção
    colecoes_stats = db.session.query(
        Relatorio.colecao,
        db.func.count(Relatorio.id)
    ).filter(Relatorio.colecao.isnot(None), Relatorio.colecao != '').group_by(
        Relatorio.colecao
    ).order_by(db.func.count(Relatorio.id).desc()).all()

    # Relatórios por mês (últimos 12 meses)
    doze_meses_atras = datetime.utcnow() - timedelta(days=365)
    relatorios_por_mes = db.session.query(
        db.func.strftime('%Y-%m', Relatorio.created_at).label('mes'),
        db.func.count(Relatorio.id)
    ).filter(Relatorio.created_at >= doze_meses_atras).group_by('mes').order_by('mes').all()

    # ========================================
    # INSIGHTS INTELIGENTES
    # ========================================
    insights = []

    # Insight de aprovação
    if taxa_aprovacao >= 80:
        insights.append({
            'tipo': 'success',
            'icone': 'bi-trophy-fill',
            'titulo': 'Excelente Taxa de Aprovação',
            'mensagem': f'{taxa_aprovacao}% das provas foram aprovadas. Parabéns pela qualidade!'
        })
    elif taxa_aprovacao >= 60:
        insights.append({
            'tipo': 'warning',
            'icone': 'bi-exclamation-triangle-fill',
            'titulo': 'Taxa de Aprovação Moderada',
            'mensagem': f'{taxa_aprovacao}% de aprovação. Há espaço para melhorias no processo.'
        })
    else:
        insights.append({
            'tipo': 'danger',
            'icone': 'bi-x-circle-fill',
            'titulo': 'Atenção: Baixa Aprovação',
            'mensagem': f'Apenas {taxa_aprovacao}% aprovadas. Recomenda-se revisar fornecedores e processos.'
        })

    # Insight de retrabalho
    if taxa_retrabalho > 30:
        insights.append({
            'tipo': 'warning',
            'icone': 'bi-arrow-repeat',
            'titulo': 'Alto Índice de Retrabalho',
            'mensagem': f'{taxa_retrabalho}% das provas precisaram de mais de uma tentativa.'
        })
    elif taxa_retrabalho > 0:
        insights.append({
            'tipo': 'info',
            'icone': 'bi-arrow-repeat',
            'titulo': 'Retrabalho Controlado',
            'mensagem': f'{taxa_retrabalho}% das provas necessitaram retrabalho.'
        })

    # Insight de provas pendentes
    if provas_em_andamento > 10:
        insights.append({
            'tipo': 'info',
            'icone': 'bi-hourglass-split',
            'titulo': 'Provas Aguardando Análise',
            'mensagem': f'{provas_em_andamento} provas em andamento aguardando conclusão.'
        })

    # Insight de comitê
    if provas_comite > 0:
        insights.append({
            'tipo': 'primary',
            'icone': 'bi-people-fill',
            'titulo': 'Provas para Comitê',
            'mensagem': f'{provas_comite} provas aguardando decisão do comitê.'
        })

    # Top fornecedor
    if fornecedores_stats:
        top_fornecedor = fornecedores_stats[0]
        insights.append({
            'tipo': 'secondary',
            'icone': 'bi-building',
            'titulo': 'Fornecedor mais Ativo',
            'mensagem': f'"{top_fornecedor[0]}" com {top_fornecedor[1]} referências.'
        })

    # ========================================
    # OPÇÕES PARA FILTROS (dropdowns)
    # ========================================
    opcoes_status = ['EM ANDAMENTO', 'APROVADA', 'REPROVADA', 'COMITÊ']
    opcoes_categorias = ['BABY', 'KIDS', 'TEEN', 'ADULTO']

    # Coleções únicas
    opcoes_colecoes = [c[0] for c in db.session.query(Relatorio.colecao).filter(
        Relatorio.colecao.isnot(None), Relatorio.colecao != ''
    ).distinct().order_by(Relatorio.colecao).all()]

    # Fornecedores únicos
    opcoes_fornecedores = [f[0] for f in db.session.query(Referencia.fornecedor).filter(
        Referencia.fornecedor.isnot(None), Referencia.fornecedor != ''
    ).distinct().order_by(Referencia.fornecedor).all()]

    # ========================================
    # TABELA DE DADOS FILTRADOS
    # ========================================
    dados_tabela = []
    for prova in provas_filtradas:
        ref = prova.referencia
        rel = ref.relatorio
        dados_tabela.append({
            'relatorio_id': rel.id,
            'colecao': rel.colecao or '-',
            'descricao': rel.descricao_geral or '-',
            'referencia': ref.numero_ref or '-',
            'categoria': ref.tipo_categoria,
            'fornecedor': ref.fornecedor or '-',
            'numero_prova': prova.numero_prova,
            'status': prova.status,
            'data_prova': prova.data_prova or '-'
        })

    return render_template('analytics.html',
        # Estatísticas gerais
        total_relatorios=total_relatorios,
        total_referencias=total_referencias,
        total_provas=total_provas,
        provas_aprovadas=provas_aprovadas,
        provas_reprovadas=provas_reprovadas,
        provas_em_andamento=provas_em_andamento,
        provas_comite=provas_comite,
        taxa_aprovacao=taxa_aprovacao,
        taxa_reprovacao=taxa_reprovacao,
        taxa_retrabalho=taxa_retrabalho,

        # Estatísticas filtradas
        total_filtrado=total_filtrado,
        filtrado_aprovadas=filtrado_aprovadas,
        filtrado_reprovadas=filtrado_reprovadas,
        filtrado_em_andamento=filtrado_em_andamento,
        filtrado_comite=filtrado_comite,
        taxa_aprovacao_filtrada=taxa_aprovacao_filtrada,

        # Dados para gráficos
        categorias_stats=dict(categorias_stats),
        status_stats=dict(status_stats),
        fornecedores_stats=fornecedores_stats,
        colecoes_stats=colecoes_stats,
        relatorios_por_mes=relatorios_por_mes,

        # Insights
        insights=insights,

        # Opções para filtros
        opcoes_status=opcoes_status,
        opcoes_categorias=opcoes_categorias,
        opcoes_colecoes=opcoes_colecoes,
        opcoes_fornecedores=opcoes_fornecedores,

        # Filtros ativos
        filtro_status=filtro_status,
        filtro_categoria=filtro_categoria,
        filtro_colecao=filtro_colecao,
        filtro_fornecedor=filtro_fornecedor,
        filtro_referencia=filtro_referencia,
        filtro_data_inicio=filtro_data_inicio,
        filtro_data_fim=filtro_data_fim,

        # Dados da tabela
        dados_tabela=dados_tabela
    )


@app.route('/api/analytics/charts')
@login_required
def api_analytics_charts():
    """
    Endpoint API para fornecer dados dos gráficos
    Retorna JSON com todos os dados necessários para visualizações
    """
    from datetime import datetime, timedelta

    try:
        # Obter parâmetros de filtro (opcional)
        filtro_status = request.args.get('status', '')
        filtro_categoria = request.args.get('categoria', '')
        filtro_colecao = request.args.get('colecao', '')
        filtro_fornecedor = request.args.get('fornecedor', '')

        # Query base
        query_provas = Prova.query.join(Referencia).join(Relatorio)

        # Aplicar filtros se fornecidos
        if filtro_status:
            query_provas = query_provas.filter(Prova.status == filtro_status)
        if filtro_categoria:
            query_provas = query_provas.filter(Referencia.tipo_categoria == filtro_categoria)
        if filtro_colecao:
            query_provas = query_provas.filter(Relatorio.colecao == filtro_colecao)
        if filtro_fornecedor:
            query_provas = query_provas.filter(Referencia.fornecedor == filtro_fornecedor)

        # ========================================
        # 1. DISTRIBUIÇÃO POR STATUS (Pie/Doughnut)
        # ========================================
        status_stats = db.session.query(
            Prova.status,
            db.func.count(Prova.id)
        ).group_by(Prova.status).all()

        status_chart = {
            'labels': [status for status, _ in status_stats],
            'values': [count for _, count in status_stats]
        }

        # ========================================
        # 2. TOP 10 FORNECEDORES (Bar Horizontal)
        # ========================================
        fornecedores_stats = db.session.query(
            Referencia.fornecedor,
            db.func.count(Referencia.id)
        ).filter(
            Referencia.fornecedor.isnot(None),
            Referencia.fornecedor != ''
        ).group_by(
            Referencia.fornecedor
        ).order_by(
            db.func.count(Referencia.id).desc()
        ).limit(10).all()

        suppliers_chart = {
            'suppliers': [forn for forn, _ in fornecedores_stats],
            'counts': [count for _, count in fornecedores_stats]
        }

        # ========================================
        # 3. TIMELINE - RELATÓRIOS POR MÊS (Area Chart)
        # ========================================
        doze_meses_atras = datetime.utcnow() - timedelta(days=365)
        relatorios_por_mes = db.session.query(
            db.func.strftime('%Y-%m', Relatorio.created_at).label('mes'),
            db.func.count(Relatorio.id)
        ).filter(
            Relatorio.created_at >= doze_meses_atras
        ).group_by('mes').order_by('mes').all()

        # Formatar meses para display (Jan, Fev, Mar...)
        meses_map = {
            '01': 'Jan', '02': 'Fev', '03': 'Mar', '04': 'Abr',
            '05': 'Mai', '06': 'Jun', '07': 'Jul', '08': 'Ago',
            '09': 'Set', '10': 'Out', '11': 'Nov', '12': 'Dez'
        }

        timeline_chart = {
            'months': [meses_map.get(mes.split('-')[1], mes) if mes else '' for mes, _ in relatorios_por_mes],
            'counts': [count for _, count in relatorios_por_mes]
        }

        # ========================================
        # 4. DISTRIBUIÇÃO POR CATEGORIA (Bar Vertical)
        # ========================================
        categorias_stats = db.session.query(
            Referencia.tipo_categoria,
            db.func.count(Referencia.id)
        ).group_by(Referencia.tipo_categoria).all()

        category_chart = {
            'categories': [cat for cat, _ in categorias_stats],
            'counts': [count for _, count in categorias_stats]
        }

        # ========================================
        # 5. SPARKLINES - TENDÊNCIAS DOS ÚLTIMOS 12 MESES
        # ========================================
        sparklines = {}

        # Relatórios por mês (últimos 12)
        rel_sparkline = []
        for i in range(11, -1, -1):
            mes_inicio = datetime.utcnow() - timedelta(days=30*i)
            mes_fim = datetime.utcnow() - timedelta(days=30*(i-1)) if i > 0 else datetime.utcnow()
            count = Relatorio.query.filter(
                Relatorio.created_at >= mes_inicio,
                Relatorio.created_at < mes_fim
            ).count()
            rel_sparkline.append(count)
        sparklines['relatorios'] = rel_sparkline

        # Taxa de aprovação por mês (últimos 12)
        taxa_sparkline = []
        for i in range(11, -1, -1):
            mes_inicio = datetime.utcnow() - timedelta(days=30*i)
            mes_fim = datetime.utcnow() - timedelta(days=30*(i-1)) if i > 0 else datetime.utcnow()
            total = Prova.query.filter(
                Prova.created_at >= mes_inicio,
                Prova.created_at < mes_fim
            ).count()
            aprovadas = Prova.query.filter(
                Prova.created_at >= mes_inicio,
                Prova.created_at < mes_fim,
                Prova.status == 'APROVADA'
            ).count()
            taxa = round((aprovadas / total * 100) if total > 0 else 0, 1)
            taxa_sparkline.append(taxa)
        sparklines['aprovacao'] = taxa_sparkline

        # ========================================
        # 6. GRÁFICO MISTO - PROVAS E TAXA DE APROVAÇÃO POR MÊS
        # ========================================
        mixed_data = {
            'labels': [],
            'totalProvas': [],
            'taxaAprovacao': []
        }

        for i in range(5, -1, -1):
            mes_inicio = datetime.utcnow() - timedelta(days=30*i)
            mes_fim = datetime.utcnow() - timedelta(days=30*(i-1)) if i > 0 else datetime.utcnow()

            # Total de provas
            total = Prova.query.filter(
                Prova.created_at >= mes_inicio,
                Prova.created_at < mes_fim
            ).count()

            # Provas aprovadas
            aprovadas = Prova.query.filter(
                Prova.created_at >= mes_inicio,
                Prova.created_at < mes_fim,
                Prova.status == 'APROVADA'
            ).count()

            # Taxa
            taxa = round((aprovadas / total * 100) if total > 0 else 0, 1)

            # Label do mês
            mes_label = meses_map.get(mes_inicio.strftime('%m'), mes_inicio.strftime('%b'))

            mixed_data['labels'].append(mes_label)
            mixed_data['totalProvas'].append(total)
            mixed_data['taxaAprovacao'].append(taxa)

        # ========================================
        # 7. COLEÇÕES
        # ========================================
        colecoes_stats = db.session.query(
            Relatorio.colecao,
            db.func.count(Relatorio.id)
        ).filter(
            Relatorio.colecao.isnot(None),
            Relatorio.colecao != ''
        ).group_by(
            Relatorio.colecao
        ).order_by(
            db.func.count(Relatorio.id).desc()
        ).limit(8).all()

        colecoes_chart = {
            'labels': [col for col, _ in colecoes_stats],
            'counts': [count for _, count in colecoes_stats]
        }

        # ========================================
        # RETORNAR JSON
        # ========================================
        return jsonify({
            'success': True,
            'data': {
                'statusChart': status_chart,
                'suppliersChart': suppliers_chart,
                'timelineChart': timeline_chart,
                'categoryChart': category_chart,
                'sparklines': sparklines,
                'mixedChart': mixed_data,
                'colecoesChart': colecoes_chart
            }
        })

    except Exception as e:
        app.logger.error(f"Erro ao gerar dados dos gráficos: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/analytics/exportar')
@login_required
def analytics_exportar():
    """Exporta dados filtrados para Excel"""
    from datetime import datetime, timedelta
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    # Obter parâmetros de filtro
    filtro_status = request.args.get('status', '')
    filtro_categoria = request.args.get('categoria', '')
    filtro_colecao = request.args.get('colecao', '')
    filtro_fornecedor = request.args.get('fornecedor', '')
    filtro_referencia = request.args.get('referencia', '')
    filtro_data_inicio = request.args.get('data_inicio', '')
    filtro_data_fim = request.args.get('data_fim', '')

    # Query base
    query_provas = Prova.query.join(Referencia).join(Relatorio)

    # Aplicar filtros
    if filtro_status:
        query_provas = query_provas.filter(Prova.status == filtro_status)
    if filtro_categoria:
        query_provas = query_provas.filter(Referencia.tipo_categoria == filtro_categoria)
    if filtro_colecao:
        query_provas = query_provas.filter(Relatorio.colecao == filtro_colecao)
    if filtro_fornecedor:
        query_provas = query_provas.filter(Referencia.fornecedor == filtro_fornecedor)
    if filtro_referencia:
        # Busca parcial por número de referência (case-insensitive)
        query_provas = query_provas.filter(Referencia.numero_ref.ilike(f'%{filtro_referencia}%'))
    if filtro_data_inicio:
        try:
            data_inicio = datetime.strptime(filtro_data_inicio, '%Y-%m-%d')
            query_provas = query_provas.filter(Prova.created_at >= data_inicio)
        except:
            pass
    if filtro_data_fim:
        try:
            data_fim = datetime.strptime(filtro_data_fim, '%Y-%m-%d')
            data_fim = data_fim + timedelta(days=1)
            query_provas = query_provas.filter(Prova.created_at < data_fim)
        except:
            pass

    provas = query_provas.order_by(Relatorio.colecao, Referencia.tipo_categoria, Prova.numero_prova).all()

    # Criar workbook
    wb = Workbook()

    # ========================================
    # ABA 1: RESUMO
    # ========================================
    ws_resumo = wb.active
    ws_resumo.title = "Resumo"

    header_font = Font(bold=True, color="FFFFFF", size=11)
    header_fill = PatternFill(start_color="e6007e", end_color="e6007e", fill_type="solid")
    subheader_fill = PatternFill(start_color="f8bbd9", end_color="f8bbd9", fill_type="solid")
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # Título
    ws_resumo['A1'] = "RELATÓRIO DE ANALYTICS - PROVAS DE MODELAGEM"
    ws_resumo['A1'].font = Font(bold=True, size=14, color="e6007e")
    ws_resumo.merge_cells('A1:D1')

    ws_resumo['A2'] = f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    ws_resumo['A2'].font = Font(italic=True, size=10)

    # Filtros aplicados
    ws_resumo['A4'] = "Filtros Aplicados:"
    ws_resumo['A4'].font = Font(bold=True)

    row = 5
    if filtro_status:
        ws_resumo[f'A{row}'] = f"Status: {filtro_status}"
        row += 1
    if filtro_categoria:
        ws_resumo[f'A{row}'] = f"Categoria: {filtro_categoria}"
        row += 1
    if filtro_colecao:
        ws_resumo[f'A{row}'] = f"Coleção: {filtro_colecao}"
        row += 1
    if filtro_fornecedor:
        ws_resumo[f'A{row}'] = f"Fornecedor: {filtro_fornecedor}"
        row += 1
    if filtro_data_inicio or filtro_data_fim:
        periodo = f"Período: {filtro_data_inicio or 'início'} até {filtro_data_fim or 'hoje'}"
        ws_resumo[f'A{row}'] = periodo
        row += 1

    if row == 5:
        ws_resumo[f'A{row}'] = "Nenhum filtro aplicado (dados completos)"
        row += 1

    # Estatísticas
    row += 1
    ws_resumo[f'A{row}'] = "Estatísticas"
    ws_resumo[f'A{row}'].font = Font(bold=True, size=12)

    row += 1
    total = len(provas)
    aprovadas = sum(1 for p in provas if p.status == 'APROVADA')
    reprovadas = sum(1 for p in provas if p.status == 'REPROVADA')
    em_andamento = sum(1 for p in provas if p.status == 'EM ANDAMENTO')
    comite = sum(1 for p in provas if p.status == 'COMITÊ')

    stats = [
        ("Total de Provas", total),
        ("Aprovadas", aprovadas),
        ("Reprovadas", reprovadas),
        ("Em Andamento", em_andamento),
        ("Comitê", comite),
        ("Taxa de Aprovação", f"{round(aprovadas/total*100, 1) if total > 0 else 0}%")
    ]

    for stat_name, stat_value in stats:
        ws_resumo[f'A{row}'] = stat_name
        ws_resumo[f'B{row}'] = stat_value
        row += 1

    # ========================================
    # ABA 2: DADOS DETALHADOS
    # ========================================
    ws_dados = wb.create_sheet("Dados Detalhados")

    headers = ["ID Relatório", "Coleção", "Descrição", "Referência", "Categoria",
               "Fornecedor", "Nº Prova", "Status", "Data Prova", "Data Recebimento",
               "Tamanhos", "Time Qualidade", "Time Estilo", "Time Modelagem"]

    for col_num, header in enumerate(headers, 1):
        cell = ws_dados.cell(row=1, column=col_num)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border

    for row_num, prova in enumerate(provas, 2):
        ref = prova.referencia
        rel = ref.relatorio

        data = [
            rel.id,
            rel.colecao or '',
            rel.descricao_geral or '',
            ref.numero_ref or '',
            ref.tipo_categoria,
            ref.fornecedor or '',
            prova.numero_prova,
            prova.status,
            prova.data_prova or '',
            prova.data_recebimento or '',
            prova.tamanhos_recebidos or '',
            prova.time_qualidade or '',
            prova.time_estilo or '',
            prova.time_modelagem or ''
        ]

        for col_num, value in enumerate(data, 1):
            cell = ws_dados.cell(row=row_num, column=col_num)
            cell.value = value
            cell.border = border

            # Colorir por status
            if col_num == 8:  # Status
                if value == 'APROVADA':
                    cell.fill = PatternFill(start_color="c6efce", end_color="c6efce", fill_type="solid")
                elif value == 'REPROVADA':
                    cell.fill = PatternFill(start_color="ffc7ce", end_color="ffc7ce", fill_type="solid")
                elif value == 'COMITÊ':
                    cell.fill = PatternFill(start_color="ffeb9c", end_color="ffeb9c", fill_type="solid")

    # Ajustar larguras
    for ws in [ws_resumo, ws_dados]:
        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            for cell in column:
                try:
                    if cell.value and len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            ws.column_dimensions[column_letter].width = min(max_length + 2, 50)

    # Salvar
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"analytics_export_{timestamp}.xlsx"
    filepath = os.path.join(app.config['PDF_FOLDER'], filename)
    wb.save(filepath)

    return send_from_directory(app.config['PDF_FOLDER'], filename, as_attachment=True)


# ========================================
# LOGS DE AUDITORIA (Admin Only)
# ========================================

@app.route('/logs')
@login_required
def logs():
    """Página de visualização de logs de auditoria - Apenas para administradores"""
    # Verificar se usuário é admin
    if not current_user.is_admin and current_user.role != 'admin':
        flash('Acesso negado. Apenas administradores podem visualizar logs.', 'danger')
        return redirect(url_for('dashboard'))

    # Parâmetros de paginação e filtro
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    filtro_acao = request.args.get('acao', '')
    filtro_usuario = request.args.get('usuario', '')
    filtro_entidade = request.args.get('entidade', '')

    # Query base
    query = AuditLog.query

    # Aplicar filtros
    if filtro_acao:
        query = query.filter(AuditLog.acao == filtro_acao)
    if filtro_usuario:
        query = query.filter(AuditLog.usuario_nome.ilike(f'%{filtro_usuario}%'))
    if filtro_entidade:
        query = query.filter(AuditLog.entidade_tipo == filtro_entidade)

    # Ordenar por data (mais recente primeiro)
    query = query.order_by(desc(AuditLog.created_at))

    # Paginar resultados
    logs_paginados = query.paginate(page=page, per_page=per_page, error_out=False)

    # Estatísticas
    total_logs = AuditLog.query.count()
    acoes_unicos = db.session.query(AuditLog.acao, db.func.count(AuditLog.id)).group_by(AuditLog.acao).all()
    usuarios_ativos = db.session.query(AuditLog.usuario_nome, db.func.count(AuditLog.id)).group_by(AuditLog.usuario_nome).order_by(desc(db.func.count(AuditLog.id))).limit(10).all()

    return render_template('logs.html',
                         logs=logs_paginados.items,
                         pagination=logs_paginados,
                         total_logs=total_logs,
                         acoes_unicos=acoes_unicos,
                         usuarios_ativos=usuarios_ativos,
                         filtro_acao=filtro_acao,
                         filtro_usuario=filtro_usuario,
                         filtro_entidade=filtro_entidade)


# ========================================
# Comandos CLI para manutenção
# ========================================

@app.cli.command('reset-all-passwords')
def reset_all_passwords():
    """Reseta as senhas de todos os usuários para uma senha padrão temporária."""
    from models import User
    from werkzeug.security import generate_password_hash

    HASH_METHOD = 'pbkdf2:sha256'
    senha_padrao = 'mudar123'

    users = User.query.all()
    print(f"Resetando senhas de {len(users)} usuários...")

    for user in users:
        user.password_hash = generate_password_hash(senha_padrao, method=HASH_METHOD)
        user.senha_temporaria = True
        print(f"  - {user.username}: senha resetada")

    db.session.commit()
    print(f"\nTodas as senhas foram resetadas para: {senha_padrao}")
    print("Os usuários deverão trocar a senha no primeiro acesso.")


@app.cli.command('create-admin')
def create_admin():
    """Cria um usuário administrador padrão."""
    from models import User
    from werkzeug.security import generate_password_hash

    HASH_METHOD = 'pbkdf2:sha256'
    username = 'admin'
    senha = 'admin123'

    # Verificar se já existe
    if User.query.filter_by(username=username).first():
        print(f"Usuário '{username}' já existe.")
        return

    admin = User(
        username=username,
        email='admin@sistema.local',
        nome_completo='Administrador',
        password_hash=generate_password_hash(senha, method=HASH_METHOD),
        role='admin',
        is_admin=True,
        is_active=True,
        senha_temporaria=True
    )

    db.session.add(admin)
    db.session.commit()

    print(f"Usuário administrador criado!")
    print(f"  Username: {username}")
    print(f"  Senha: {senha}")
    print("  ** Troque a senha após o primeiro login! **")


if __name__ == '__main__':
    # Este bloco é usado apenas para desenvolvimento local
    # Em produção, use Gunicorn: gunicorn -c gunicorn_config.py wsgi:app
    app.run(
        debug=app.config.get('DEBUG', False),
        host=os.getenv('HOST', '127.0.0.1'),
        port=int(os.getenv('PORT', 5000))
    )
