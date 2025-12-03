import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
env_file = os.getenv('ENV_FILE', '.env')
load_dotenv(env_file)

class Config:
    """Configuração base da aplicação"""

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///instance/provas.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }

    # Upload
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    PDF_FOLDER = os.path.join(os.getcwd(), 'relatorios_pdf')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB default

    # Extensões permitidas
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'png,jpg,jpeg,gif,pdf,xlsx,xls,ppt,pptx').split(','))

    # Extensões de imagem
    IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Extensões de documento
    DOCUMENT_EXTENSIONS = {'pdf', 'xlsx', 'xls', 'ppt', 'pptx'}

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', None)

    @staticmethod
    def init_app(app):
        """Inicializa configurações no app Flask"""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.PDF_FOLDER, exist_ok=True)

        # Criar diretório de logs se necessário
        if Config.LOG_FILE:
            log_dir = os.path.dirname(Config.LOG_FILE)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)


class DevelopmentConfig(Config):
    """Configuração de desenvolvimento"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/provas.db'


class ProductionConfig(Config):
    """Configuração de produção"""
    DEBUG = False

    @staticmethod
    def init_app(app):
        Config.init_app(app)

        # Validar configurações críticas
        if Config.SECRET_KEY == 'fallback-secret-key-change-in-production':
            raise ValueError('SECRET_KEY deve ser configurada em produção!')

        if not os.getenv('DATABASE_URL'):
            raise ValueError('DATABASE_URL deve ser configurada em produção!')


# Mapeamento de configurações
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def get_file_extension(filename):
    """Retorna a extensão do arquivo"""
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return None

def is_image(filename):
    """Verifica se o arquivo é uma imagem"""
    ext = get_file_extension(filename)
    return ext in Config.IMAGE_EXTENSIONS

def is_document(filename):
    """Verifica se o arquivo é um documento"""
    ext = get_file_extension(filename)
    return ext in Config.DOCUMENT_EXTENSIONS
