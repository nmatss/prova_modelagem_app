import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, jsonify
from werkzeug.datastructures import MultiDict
from werkzeug.utils import secure_filename
# from xhtml2pdf import pisa  # Comentado temporariamente - instalar: pip install xhtml2pdf
from flask_login import LoginManager, login_required, current_user
from auth import auth_bp, get_user_by_id
from admin import admin_bp
from db import init_app as init_db
from models import db, Relatorio, Referencia, Prova, Foto
from config import Config
from utils import save_file
from error_handlers import register_error_handlers
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

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'info'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

# Registrar Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

# Registrar error handlers
register_error_handlers(app)


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
    relatorios = Relatorio.query.order_by(desc(Relatorio.created_at)).all()
    relatorios_com_status = []
    
    for relatorio in relatorios:
        relatorio_dict = {c.name: getattr(relatorio, c.name) for c in relatorio.__table__.columns}
        
        # Obter última prova de qualquer referência deste relatório
        ultima_prova = Prova.query.join(Referencia).filter(Referencia.relatorio_id == relatorio.id).order_by(desc(Prova.numero_prova)).first()
        
        relatorio_dict['status_atual'] = ultima_prova.status if ultima_prova else 'Novo'
        relatorios_com_status.append(relatorio_dict)

    return render_template('dashboard.html', relatorios=relatorios_com_status)

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

@app.route('/relatorio/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_relatorio(id):
    relatorio = Relatorio.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # 1. Atualiza as informações gerais do relatório
            relatorio.colecao = request.form.get('colecao')
            relatorio.descricao_geral = request.form.get('descricao_geral')
            
            # 2. Itera sobre todos os tipos possíveis
            for tipo in ['baby', 'kids', 'teen', 'adulto']:
                ref_numero = request.form.get(f'ref_{tipo}')
                if not ref_numero:
                    continue

                # Verifica se já existe uma referência deste tipo
                ref_existente = Referencia.query.filter_by(relatorio_id=id, tipo=tipo).first()

                if ref_existente:
                    # --- ATUALIZAÇÃO ---
                    ref_existente.numero_ref = ref_numero
                    ref_existente.origem = request.form.get(f'origem_{tipo}')
                    ref_existente.fornecedor = request.form.get(f'fornecedor_{tipo}')
                    ref_existente.materia_prima = request.form.get(f'materia_prima_{tipo}')
                    ref_existente.composicao = request.form.get(f'composicao_{tipo}')
                    ref_existente.gramatura = request.form.get(f'gramatura_{tipo}')
                    ref_existente.aviamentos = request.form.get(f'aviamentos_{tipo}')
                    
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
                            prova.time_estilo = request.form.get(f'time_estilo_{prova_id}')
                            prova.comentarios_estilo = request.form.get(f'comentarios_estilo_{prova_id}')
                            prova.data_lacre = request.form.get(f'data_lacre_{prova_id}')
                            prova.numero_lacre = request.form.get(f'numero_lacre_{prova_id}')
                            prova.info_adicionais = request.form.get(f'info_adicionais_{prova_id}')
                            
                            # Adicionar fotos
                            campos_fotos = ['desenho', 'qualidade', 'estilo']
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
                        tipo=tipo,
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
                        time_estilo=request.form.get(f'time_estilo_{tipo}'),
                        comentarios_estilo=request.form.get(f'comentarios_estilo_{tipo}'),
                        data_lacre=request.form.get(f'data_lacre_{tipo}'),
                        numero_lacre=request.form.get(f'numero_lacre_{tipo}'),
                        info_adicionais=request.form.get(f'info_adicionais_{tipo}')
                    )
                    db.session.add(nova_prova)
                    db.session.flush()
                    
                    campos_fotos = ['desenho', 'qualidade', 'estilo']
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
        referencias_por_tipo[ref.tipo] = ref_dict

    return render_template('editar_relatorio.html', relatorio=relatorio, referencias_por_tipo=referencias_por_tipo)


@app.route('/prova/atualizar_status', methods=['POST'])
@login_required
def atualizar_status_prova():
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
            
            novo_relatorio = Relatorio(
                descricao_geral=request.form.get('descricao_geral'),
                colecao=request.form.get('colecao'),
                ppt_path=ppt_filename
            )
            db.session.add(novo_relatorio)
            db.session.flush()
            
            for tipo in ['baby', 'kids', 'teen', 'adulto']:
                if request.form.get(f'ref_{tipo}'):
                    nova_ref = Referencia(
                        relatorio_id=novo_relatorio.id,
                        tipo=tipo,
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
                        time_estilo=request.form.get(f'time_estilo_{tipo}'),
                        comentarios_estilo=request.form.get(f'comentarios_estilo_{tipo}'),
                        data_lacre=request.form.get(f'data_lacre_{tipo}'),
                        numero_lacre=request.form.get(f'numero_lacre_{tipo}'),
                        info_adicionais=request.form.get(f'info_adicionais_{tipo}')
                    )
                    db.session.add(nova_prova)
                    db.session.flush()
                    
                    campos_fotos = ['desenho', 'qualidade', 'estilo']
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

@app.route('/referencia/<int:referencia_id>/nova_prova', methods=['GET', 'POST'])
@login_required
def adicionar_nova_prova(referencia_id):
    referencia = Referencia.query.get_or_404(referencia_id)

    if request.method == 'POST':
        try:
            novo_numero_prova = request.form.get('numero_prova')
            tipo = referencia.tipo

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
                comentarios_qualidade=request.form.get(f'comentarios_qualidade_{tipo}'),
                time_estilo=request.form.get(f'time_estilo_{tipo}'),
                comentarios_estilo=request.form.get(f'comentarios_estilo_{tipo}'),
                data_lacre=request.form.get(f'data_lacre_{tipo}'),
                numero_lacre=request.form.get(f'numero_lacre_{tipo}'),
                info_adicionais=request.form.get(f'info_adicionais_{tipo}')
            )
            db.session.add(nova_prova)
            db.session.flush()
            
            campos_fotos = ['desenho', 'qualidade', 'estilo']
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


if __name__ == '__main__':
    # Este bloco é usado apenas para desenvolvimento local
    # Em produção, use Gunicorn: gunicorn -c gunicorn_config.py wsgi:app
    app.run(
        debug=app.config.get('DEBUG', False),
        host=os.getenv('HOST', '127.0.0.1'),
        port=int(os.getenv('PORT', 5000))
    )
