"""
Módulo de Segurança
Implementa proteções de segurança para a aplicação
"""
import re
import os
import secrets
from flask import request, abort, session
from functools import wraps
from datetime import datetime, timedelta
import hashlib

# ============================================================================
# GERAÇÃO DE SECRET KEY SEGURA
# ============================================================================

def generate_secret_key():
    """Gera uma SECRET_KEY criptograficamente segura"""
    return secrets.token_hex(32)  # 64 caracteres hexadecimais

def save_secret_key_to_env():
    """Salva a SECRET_KEY no arquivo .env"""
    env_path = '.env'
    secret_key = generate_secret_key()

    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            lines = f.readlines()

        with open(env_path, 'w') as f:
            found = False
            for line in lines:
                if line.startswith('SECRET_KEY='):
                    f.write(f'SECRET_KEY={secret_key}\n')
                    found = True
                else:
                    f.write(line)

            if not found:
                f.write(f'\nSECRET_KEY={secret_key}\n')
    else:
        with open(env_path, 'w') as f:
            f.write(f'SECRET_KEY={secret_key}\n')

    return secret_key


# ============================================================================
# VALIDAÇÃO DE INPUTS
# ============================================================================

class InputValidator:
    """Validador de inputs para prevenir XSS e injection attacks"""

    # Padrões perigosos
    DANGEROUS_PATTERNS = [
        r'<script[^>]*>.*?</script>',  # Scripts
        r'javascript:',                  # JavaScript URI
        r'on\w+\s*=',                   # Event handlers
        r'<iframe',                      # Iframes
        r'<object',                      # Objects
        r'<embed',                       # Embeds
        r'eval\(',                       # Eval
        r'expression\(',                 # CSS expressions
    ]

    @staticmethod
    def sanitize_string(value, max_length=None):
        """Sanitiza uma string removendo caracteres perigosos"""
        if not value or not isinstance(value, str):
            return value

        # Remover tags HTML
        value = re.sub(r'<[^>]+>', '', value)

        # Verificar padrões perigosos
        for pattern in InputValidator.DANGEROUS_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                return ''  # Retorna vazio se encontrar padrão perigoso

        # Limitar tamanho
        if max_length and len(value) > max_length:
            value = value[:max_length]

        return value.strip()

    @staticmethod
    def sanitize_filename(filename):
        """Sanitiza nome de arquivo"""
        if not filename:
            return ''

        # Remove path traversal
        filename = os.path.basename(filename)

        # Remove caracteres perigosos
        filename = re.sub(r'[^\w\s\-\.]', '', filename)

        # Remove múltiplos pontos
        while '..' in filename:
            filename = filename.replace('..', '.')

        return filename

    @staticmethod
    def validate_email(email):
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_username(username):
        """Valida username (apenas alfanuméricos e _-)"""
        if not username or len(username) < 3 or len(username) > 50:
            return False
        pattern = r'^[a-zA-Z0-9_-]+$'
        return re.match(pattern, username) is not None


# ============================================================================
# RATE LIMITING MANUAL
# ============================================================================

class RateLimiter:
    """Rate limiter simples baseado em memória"""

    def __init__(self):
        self.requests = {}  # {ip: [(timestamp, endpoint), ...]}
        self.cleanup_interval = 300  # 5 minutos
        self.last_cleanup = datetime.now()

    def cleanup(self):
        """Remove entradas antigas"""
        now = datetime.now()
        if (now - self.last_cleanup).seconds > self.cleanup_interval:
            cutoff = now - timedelta(minutes=10)
            for ip in list(self.requests.keys()):
                self.requests[ip] = [
                    (ts, ep) for ts, ep in self.requests[ip]
                    if ts > cutoff
                ]
                if not self.requests[ip]:
                    del self.requests[ip]
            self.last_cleanup = now

    def check_rate_limit(self, ip, endpoint, max_requests=60, window=60):
        """
        Verifica se IP excedeu limite de requisições

        Args:
            ip: IP do cliente
            endpoint: Endpoint sendo acessado
            max_requests: Número máximo de requisições
            window: Janela de tempo em segundos

        Returns:
            bool: True se permitido, False se bloqueado
        """
        self.cleanup()

        now = datetime.now()
        cutoff = now - timedelta(seconds=window)

        if ip not in self.requests:
            self.requests[ip] = []

        # Filtrar requisições dentro da janela
        recent = [
            (ts, ep) for ts, ep in self.requests[ip]
            if ts > cutoff and ep == endpoint
        ]

        if len(recent) >= max_requests:
            return False

        # Adicionar requisição atual
        self.requests[ip].append((now, endpoint))
        return True

# Instância global
rate_limiter = RateLimiter()


def rate_limit(max_requests=60, window=60):
    """
    Decorator para aplicar rate limiting

    Usage:
        @rate_limit(max_requests=10, window=60)
        def my_route():
            ...
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            ip = request.remote_addr
            endpoint = request.endpoint

            if not rate_limiter.check_rate_limit(ip, endpoint, max_requests, window):
                abort(429, description="Muitas requisições. Tente novamente em alguns segundos.")

            return f(*args, **kwargs)
        return wrapped
    return decorator


# ============================================================================
# PROTEÇÃO CSRF
# ============================================================================

def generate_csrf_token():
    """Gera um token CSRF"""
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(32)
    return session['_csrf_token']

def validate_csrf_token(token):
    """Valida o token CSRF"""
    if '_csrf_token' not in session:
        return False
    return secrets.compare_digest(session['_csrf_token'], token)

def csrf_protect(f):
    """Decorator para proteção CSRF"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
            if not token or not validate_csrf_token(token):
                abort(403, description="Token CSRF inválido ou ausente")
        return f(*args, **kwargs)
    return wrapped


# ============================================================================
# HEADERS DE SEGURANÇA
# ============================================================================

class SecurityHeaders:
    """Adiciona headers de segurança às respostas"""

    @staticmethod
    def add_security_headers(response):
        """Adiciona headers de segurança"""

        # Prevenir clickjacking
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'

        # Prevenir MIME sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'

        # XSS Protection
        response.headers['X-XSS-Protection'] = '1; mode=block'

        # Referrer Policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # Content Security Policy
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
            "font-src 'self' https: data:; "
            "img-src 'self' data: https:; "
            "connect-src 'self' https://cdn.jsdelivr.net; "
            "frame-ancestors 'self'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )

        # Strict Transport Security (HTTPS)
        # Descomente se usar HTTPS
        # response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

        # Permissions Policy
        response.headers['Permissions-Policy'] = (
            "geolocation=(), "
            "microphone=(), "
            "camera=(), "
            "payment=(), "
            "usb=(), "
            "magnetometer=(), "
            "gyroscope=(), "
            "speaker=()"
        )

        return response


# ============================================================================
# VALIDAÇÃO DE UPLOADS
# ============================================================================

class FileUploadValidator:
    """Validador de uploads de arquivos"""

    # Extensões permitidas
    ALLOWED_EXTENSIONS = {
        'images': {'png', 'jpg', 'jpeg', 'gif'},
        'documents': {'pdf', 'xlsx', 'xls', 'ppt', 'pptx', 'doc', 'docx'}
    }

    # Magic numbers para validação de tipo
    MAGIC_NUMBERS = {
        'png': b'\x89PNG\r\n\x1a\n',
        'jpg': b'\xff\xd8\xff',
        'jpeg': b'\xff\xd8\xff',
        'gif': b'GIF8',
        'pdf': b'%PDF',
    }

    # Tamanho máximo por tipo (em bytes)
    MAX_SIZES = {
        'images': 10 * 1024 * 1024,      # 10MB
        'documents': 50 * 1024 * 1024,   # 50MB
    }

    @staticmethod
    def validate_extension(filename, allowed_types=['images', 'documents']):
        """Valida extensão do arquivo"""
        if not filename or '.' not in filename:
            return False

        ext = filename.rsplit('.', 1)[1].lower()

        for file_type in allowed_types:
            if ext in FileUploadValidator.ALLOWED_EXTENSIONS.get(file_type, set()):
                return True

        return False

    @staticmethod
    def validate_file_type(file_content, filename):
        """Valida o tipo real do arquivo pelos magic numbers"""
        if not file_content:
            return False

        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else None
        if not ext:
            return False

        # Obter magic number esperado
        expected_magic = FileUploadValidator.MAGIC_NUMBERS.get(ext)
        if not expected_magic:
            return True  # Se não há magic number definido, confiar na extensão

        # Verificar magic number
        return file_content.startswith(expected_magic)

    @staticmethod
    def validate_file_size(file_size, file_type='images'):
        """Valida tamanho do arquivo"""
        max_size = FileUploadValidator.MAX_SIZES.get(file_type, 10 * 1024 * 1024)
        return file_size <= max_size


# ============================================================================
# SENHA SEGURA
# ============================================================================

class PasswordValidator:
    """Validador de senhas"""

    MIN_LENGTH = 8

    @staticmethod
    def validate_password_strength(password):
        """
        Valida força da senha

        Returns:
            (bool, str): (válido, mensagem)
        """
        if len(password) < PasswordValidator.MIN_LENGTH:
            return False, f"Senha deve ter no mínimo {PasswordValidator.MIN_LENGTH} caracteres"

        if not re.search(r'[a-z]', password):
            return False, "Senha deve conter pelo menos uma letra minúscula"

        if not re.search(r'[A-Z]', password):
            return False, "Senha deve conter pelo menos uma letra maiúscula"

        if not re.search(r'[0-9]', password):
            return False, "Senha deve conter pelo menos um número"

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Senha deve conter pelo menos um caractere especial"

        return True, "Senha forte"


# ============================================================================
# INICIALIZAÇÃO
# ============================================================================

def init_security(app):
    """Inicializa configurações de segurança"""

    # Adicionar headers de segurança a todas as respostas
    @app.after_request
    def add_security_headers(response):
        return SecurityHeaders.add_security_headers(response)

    # Disponibilizar CSRF token no contexto
    @app.context_processor
    def csrf_token():
        return dict(csrf_token=generate_csrf_token)

    # Configurar sessões seguras
    app.config['SESSION_COOKIE_SECURE'] = False  # True em produção com HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=12)

    # Gerar SECRET_KEY se não existir
    if app.config.get('SECRET_KEY') == 'fallback-secret-key-change-in-production':
        print("⚠️  WARNING: Using fallback SECRET_KEY. Generating new one...")
        new_key = save_secret_key_to_env()
        app.config['SECRET_KEY'] = new_key
        print(f"✅ New SECRET_KEY generated and saved to .env")

    return app
