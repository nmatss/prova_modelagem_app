from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    """
    Tabela de usuários do sistema
    Nomenclatura: PT-BR para domínio de negócio
    """
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    nome_completo = db.Column(db.String(255))
    role = db.Column(db.String(50), default='usuario')  # admin, gestor, usuario
    is_admin = db.Column(db.Boolean, default=False)  # Mantido por compatibilidade
    is_active = db.Column(db.Boolean, default=True)
    ultimo_acesso = db.Column(db.DateTime)
    senha_temporaria = db.Column(db.Boolean, default=False)  # Indica se precisa trocar senha
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relacionamentos (apenas os que existem no banco real)
    # relatorios_criados = db.relationship('Relatorio', backref='criador', lazy=True, foreign_keys='Relatorio.created_by')

class Relatorio(db.Model):
    """
    Tabela de relatórios de coleção
    Agrupa referências por coleção/temporada
    """
    __tablename__ = 'relatorios'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, index=True)  # REL-2025-001
    descricao_geral = db.Column(db.String(500), nullable=False)
    colecao = db.Column(db.String(200))
    temporada = db.Column(db.String(50))  # Verão 2025, Inverno 2024
    ano = db.Column(db.Integer)
    ppt_path = db.Column(db.String(500))
    status_geral = db.Column(db.String(50), default='Em Andamento')
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relacionamentos
    referencias = db.relationship('Referencia', backref='relatorio', lazy=True, cascade="all, delete-orphan")

class Referencia(db.Model):
    """
    Tabela de referências de produtos
    Cada referência pertence a um relatório
    NOTA: Usando nomenclatura do banco de dados atual
    """
    __tablename__ = 'referencias'

    id = db.Column(db.Integer, primary_key=True)
    relatorio_id = db.Column(db.Integer, db.ForeignKey('relatorios.id'), nullable=False, index=True)
    codigo_referencia = db.Column(db.String(100))  # Código único da referência
    tipo_categoria = db.Column(db.String(50), nullable=False)  # baby, kids, teen, adulto
    numero_ref = db.Column(db.String(100))
    origem = db.Column(db.String(100))
    fornecedor = db.Column(db.String(200))
    fornecedor_contato = db.Column(db.String(200))
    materia_prima = db.Column(db.String(200))
    composicao = db.Column(db.String(200))
    gramatura = db.Column(db.String(100))
    aviamentos = db.Column(db.String(500))
    observacoes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relacionamentos
    provas = db.relationship('ProvaModelagem', backref='referencia', lazy=True, cascade="all, delete-orphan")

class ProvaModelagem(db.Model):
    """
    Tabela de provas de modelagem
    Cada prova pertence a uma referência
    NOTA: Usando nomenclatura do banco de dados atual
    """
    __tablename__ = 'provas'

    id = db.Column(db.Integer, primary_key=True)
    referencia_id = db.Column(db.Integer, db.ForeignKey('referencias.id'), nullable=False, index=True)
    numero_prova = db.Column(db.Integer, nullable=False)

    # Status e rastreamento
    status = db.Column(db.String(50), default='Em Andamento')
    motivo_ultima_alteracao = db.Column(db.Text)

    # Tabela de medidas
    tabela_medidas_path = db.Column(db.String(500))

    # Informações de recebimento
    data_recebimento = db.Column(db.String(20))
    tamanhos_recebidos = db.Column(db.String(200))
    info_medidas = db.Column(db.Text)
    data_prova = db.Column(db.String(20))

    # Qualidade
    time_qualidade = db.Column(db.String(200))
    comentarios_qualidade = db.Column(db.Text)
    obs_qualidade = db.Column(db.Text)

    # Estilo
    time_estilo = db.Column(db.String(200))
    comentarios_estilo = db.Column(db.Text)
    obs_estilo = db.Column(db.Text)

    # Modelagem
    time_modelagem = db.Column(db.String(200))
    comentarios_modelagem = db.Column(db.Text)
    obs_modelagem = db.Column(db.Text)

    # Lacre
    data_lacre = db.Column(db.String(20))
    numero_lacre = db.Column(db.String(100))

    # Informações adicionais
    info_adicionais = db.Column(db.Text)

    # Controle
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relacionamentos
    fotos = db.relationship('FotoProva', backref='prova', lazy=True, cascade="all, delete-orphan")

class FotoProva(db.Model):
    """
    Tabela de fotos das provas
    NOTA: Usando nomenclatura do banco de dados atual
    """
    __tablename__ = 'fotos'

    id = db.Column(db.Integer, primary_key=True)
    prova_id = db.Column(db.Integer, db.ForeignKey('provas.id'), nullable=False, index=True)
    contexto = db.Column(db.String(50), nullable=False)  # desenho, qualidade, estilo, amostra, prova_modelo
    tamanho = db.Column(db.String(50))  # Para amostra/prova_modelo
    file_path = db.Column(db.String(500), nullable=False)

# Classes removidas (não existem no banco de dados real):
# - HistoricoStatus
# - ConfiguracaoSistema
# - AuditLog


# Manter compatibilidade com código antigo (aliases)
# REMOVER após atualizar todo o código
User = Usuario
Prova = ProvaModelagem
Foto = FotoProva
