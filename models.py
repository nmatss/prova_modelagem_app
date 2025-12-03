from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Relatorio(db.Model):
    __tablename__ = 'relatorios'
    id = db.Column(db.Integer, primary_key=True)
    descricao_geral = db.Column(db.String(200), unique=True, nullable=False)
    colecao = db.Column(db.String(100))
    ppt_path = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento
    referencias = db.relationship('Referencia', backref='relatorio', lazy=True, cascade="all, delete-orphan")

class Referencia(db.Model):
    __tablename__ = 'referencias'
    id = db.Column(db.Integer, primary_key=True)
    relatorio_id = db.Column(db.Integer, db.ForeignKey('relatorios.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False) # baby, kids, teen, adulto
    numero_ref = db.Column(db.String(100))
    origem = db.Column(db.String(100))
    fornecedor = db.Column(db.String(100))
    materia_prima = db.Column(db.String(100))
    composicao = db.Column(db.String(100))
    gramatura = db.Column(db.String(100))
    aviamentos = db.Column(db.String(200))

    # Relacionamento
    provas = db.relationship('Prova', backref='referencia', lazy=True, cascade="all, delete-orphan")

class Prova(db.Model):
    __tablename__ = 'provas'
    id = db.Column(db.Integer, primary_key=True)
    referencia_id = db.Column(db.Integer, db.ForeignKey('referencias.id'), nullable=False)
    numero_prova = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='Em Andamento')
    motivo_ultima_alteracao = db.Column(db.String(200))
    tabela_medidas_path = db.Column(db.String(200))
    
    data_recebimento = db.Column(db.String(50))
    tamanhos_recebidos = db.Column(db.String(100))
    info_medidas = db.Column(db.Text)
    data_prova = db.Column(db.String(50))
    
    time_qualidade = db.Column(db.String(50))
    comentarios_qualidade = db.Column(db.Text)
    obs_qualidade = db.Column(db.Text)
    
    time_estilo = db.Column(db.String(50))
    comentarios_estilo = db.Column(db.Text)
    obs_estilo = db.Column(db.Text)
    
    time_modelagem = db.Column(db.String(50))
    comentarios_modelagem = db.Column(db.Text)
    obs_modelagem = db.Column(db.Text)
    
    data_lacre = db.Column(db.String(50))
    numero_lacre = db.Column(db.String(50))
    info_adicionais = db.Column(db.Text)

    # Relacionamento
    fotos = db.relationship('Foto', backref='prova', lazy=True, cascade="all, delete-orphan")

class Foto(db.Model):
    __tablename__ = 'fotos'
    id = db.Column(db.Integer, primary_key=True)
    prova_id = db.Column(db.Integer, db.ForeignKey('provas.id'), nullable=False)
    contexto = db.Column(db.String(50), nullable=False) # desenho, qualidade, estilo, amostra, prova_modelo
    tamanho = db.Column(db.String(20)) # Para amostra/prova_modelo
    file_path = db.Column(db.String(200), nullable=False)
