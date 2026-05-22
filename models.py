from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

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
    is_admin = db.Column(db.Boolean, default=False)
    idioma = db.Column(db.String(5), default='pt')  # i18n preferência do usuário  # Mantido por compatibilidade
    is_active = db.Column(db.Boolean, default=True)
    ultimo_acesso = db.Column(db.DateTime)
    senha_temporaria = db.Column(db.Boolean, default=False)  # Indica se precisa trocar senha
    reset_token = db.Column(db.String(100))  # Token para reset de senha
    reset_token_expires = db.Column(db.DateTime)  # Expiração do token
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
    linha = db.Column(db.String(50))  # Linha de produto: PRAIA, ACESSÓRIO, LINGERIE, MEIAS, HOMEWEAR
    imagem_produto = db.Column(db.String(500))  # Imagem do produto
    ficha_tecnica = db.Column(db.String(500))  # Ficha técnica do produto
    status_geral = db.Column(db.String(50), default='Em Andamento')
    data_limite = db.Column(db.String(20))  # F2: Prazo/deadline
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
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'))  # F4: FK para Fornecedor
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
    checklist_qualidade = db.Column(db.Text)  # Itens selecionados separados por vírgula
    comentarios_qualidade = db.Column(db.Text)
    obs_qualidade = db.Column(db.Text)

    # Estilo
    time_estilo = db.Column(db.String(200))
    checklist_estilo = db.Column(db.Text)  # Itens selecionados separados por vírgula
    comentarios_estilo = db.Column(db.Text)
    obs_estilo = db.Column(db.Text)

    # Modelagem
    time_modelagem = db.Column(db.String(200))
    checklist_modelagem = db.Column(db.Text)  # Itens selecionados separados por vírgula
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

# =============================================================================
# F4: GESTÃO DE FORNECEDORES
# =============================================================================

class Fornecedor(db.Model):
    __tablename__ = 'fornecedores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    contato = db.Column(db.String(200))
    email = db.Column(db.String(255))
    telefone = db.Column(db.String(50))
    endereco = db.Column(db.String(500))
    pais = db.Column(db.String(100))
    cnpj = db.Column(db.String(20), unique=True)
    avaliacao = db.Column(db.Integer, default=0)  # 0-5
    observacoes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relacionamento
    referencias = db.relationship('Referencia', backref='fornecedor_obj', lazy=True)

# =============================================================================
# F3: CHECKLIST DINÂMICO
# =============================================================================

class ChecklistTemplate(db.Model):
    __tablename__ = 'checklist_templates'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)  # qualidade, estilo, modelagem
    itens = db.Column(db.Text)  # JSON array of items
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relacionamento
    respostas = db.relationship('ChecklistResposta', backref='template', lazy=True)

    def get_itens(self):
        if self.itens:
            try:
                return json.loads(self.itens)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    def set_itens(self, itens_list):
        self.itens = json.dumps(itens_list, ensure_ascii=False)


class ChecklistResposta(db.Model):
    __tablename__ = 'checklist_respostas'

    id = db.Column(db.Integer, primary_key=True)
    prova_id = db.Column(db.Integer, db.ForeignKey('provas.id'), nullable=False, index=True)
    template_id = db.Column(db.Integer, db.ForeignKey('checklist_templates.id'), nullable=False)
    item = db.Column(db.String(200), nullable=False)
    conforme = db.Column(db.Boolean, default=False)
    observacao = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento reverso para Prova (acesso via prova.respostas)
    prova = db.relationship('ProvaModelagem', backref=db.backref('respostas', lazy=True, cascade='all, delete-orphan'))

# =============================================================================
# F8: VERSIONAMENTO DE ARQUIVOS
# =============================================================================

class ArquivoVersao(db.Model):
    __tablename__ = 'arquivo_versoes'

    id = db.Column(db.Integer, primary_key=True)
    entidade_tipo = db.Column(db.String(50), nullable=False)  # relatorio, prova
    entidade_id = db.Column(db.Integer, nullable=False)
    campo = db.Column(db.String(100), nullable=False)  # ppt_path, imagem_produto, etc
    file_path = db.Column(db.String(500), nullable=False)
    versao = db.Column(db.Integer, default=1)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# =============================================================================
# F9: DASHBOARD PERSONALIZADO
# =============================================================================

class PreferenciaUsuario(db.Model):
    __tablename__ = 'preferencias_usuarios'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, unique=True)
    widget_config = db.Column(db.Text)  # JSON config
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def get_config(self):
        if self.widget_config:
            try:
                return json.loads(self.widget_config)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}

    def set_config(self, config_dict):
        self.widget_config = json.dumps(config_dict, ensure_ascii=False)

# =============================================================================
# SISTEMA DE AUDITORIA
# =============================================================================

class AuditLog(db.Model):
    """
    Tabela de auditoria para rastreamento de ações no sistema
    Registra todas as ações importantes realizadas pelos usuários
    """
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, index=True)
    usuario_nome = db.Column(db.String(255))  # Nome do usuário (cache para performance)
    acao = db.Column(db.String(50), nullable=False, index=True)  # criar, editar, excluir, login, etc
    entidade_tipo = db.Column(db.String(50))  # relatorio, prova, referencia, usuario, etc
    entidade_id = db.Column(db.Integer)  # ID da entidade afetada
    entidade_descricao = db.Column(db.String(500))  # Descrição da entidade (para histórico)
    detalhes = db.Column(db.Text)  # JSON com detalhes adicionais da ação
    ip_address = db.Column(db.String(50))  # IP do usuário
    user_agent = db.Column(db.String(500))  # Navegador/dispositivo
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Relacionamento
    usuario = db.relationship('Usuario', backref='audit_logs', lazy=True)

    def __repr__(self):
        return f'<AuditLog {self.usuario_nome} {self.acao} {self.entidade_tipo}#{self.entidade_id}>'


# =============================================================================
# IMPORT JOBS (round-trip Excel: upload → revisar → confirmar)
# =============================================================================

class ImportJob(db.Model):
    """Job de importação Excel com fluxo em 3 etapas (validar antes de commitar)."""
    __tablename__ = 'import_jobs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    arquivo_original = db.Column(db.String(500))  # nome original do arquivo enviado
    arquivo_temp_path = db.Column(db.String(500))  # caminho do arquivo temporário
    status = db.Column(db.String(20), default='pending')  # pending, validated, committed, cancelled
    parsed_data = db.Column(db.Text)  # JSON com linhas parseadas
    erros = db.Column(db.Text)  # JSON [{sheet, linha, mensagem}]
    summary = db.Column(db.Text)  # JSON com contadores de criar/atualizar
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship('Usuario')

    def get_parsed(self):
        if self.parsed_data:
            try:
                return json.loads(self.parsed_data)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}

    def set_parsed(self, data):
        self.parsed_data = json.dumps(data, default=str, ensure_ascii=False)

    def get_erros(self):
        if self.erros:
            try:
                return json.loads(self.erros)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    def set_erros(self, lista):
        self.erros = json.dumps(lista, ensure_ascii=False)

    def get_summary(self):
        if self.summary:
            try:
                return json.loads(self.summary)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}

    def set_summary(self, d):
        self.summary = json.dumps(d, ensure_ascii=False)


# =============================================================================
# LINKS PÚBLICOS (compartilhamento read-only com fornecedor)
# =============================================================================

class LinkPublico(db.Model):
    """Link público (token-based) para compartilhar um relatório em modo view-only."""
    __tablename__ = 'links_publicos'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True, nullable=False, index=True)
    relatorio_id = db.Column(db.Integer, db.ForeignKey('relatorios.id'), nullable=False, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    titulo_personalizado = db.Column(db.String(200))
    expires_at = db.Column(db.DateTime, nullable=True)
    permite_download_pdf = db.Column(db.Boolean, default=True)
    permite_download_fotos = db.Column(db.Boolean, default=True)
    visualizacoes = db.Column(db.Integer, default=0)
    ultimo_acesso = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    relatorio = db.relationship('Relatorio')
    criador = db.relationship('Usuario')

    def esta_expirado(self):
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at

    def esta_valido(self):
        return self.is_active and not self.esta_expirado()


# =============================================================================
# MANUAIS / DOCUMENTOS ESTÁTICOS
# =============================================================================

class Manual(db.Model):
    """Documentos/manuais anexáveis pelo setor (procedimentos, guias, normas)."""
    __tablename__ = 'manuais'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    categoria = db.Column(db.String(100), index=True)  # Estilo, Modelagem, Qualidade, Procedimentos, Outros
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)  # bytes
    uploaded_by = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    downloads = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    uploader = db.relationship('Usuario')

    def file_size_legivel(self):
        """Formata o tamanho do arquivo para exibição (KB / MB)."""
        if not self.file_size:
            return '—'
        if self.file_size < 1024:
            return f'{self.file_size} B'
        if self.file_size < 1024 * 1024:
            return f'{self.file_size / 1024:.1f} KB'
        return f'{self.file_size / (1024 * 1024):.1f} MB'


# Manter compatibilidade com código antigo (aliases)
# REMOVER após atualizar todo o código
User = Usuario
Prova = ProvaModelagem
Foto = FotoProva
