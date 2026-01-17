"""
Configuração do Gunicorn para produção
"""
import os
import multiprocessing

# Bind
bind = f"{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', '8000')}"

# Workers - Otimizado para SQLite e recursos limitados
workers = int(os.getenv('WORKERS', 2))  # 2 workers para SQLite (evitar lock contention)
worker_class = 'sync'
worker_connections = 100  # Reduzido para melhor performance com SQLite
timeout = 60  # Reduzido de 120 para 60 segundos
keepalive = 2  # Reduzido para liberar conexões mais rápido

# Logging
accesslog = '/app/logs/access.log'
errorlog = '/app/logs/error.log'
loglevel = os.getenv('LOG_LEVEL', 'info').lower()
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'provas_app'

# Server mechanics
daemon = False
pidfile = None
umask = 0o007
user = None
group = None
tmp_upload_dir = None

# SSL (se necessário)
# keyfile = '/path/to/keyfile'
# certfile = '/path/to/certfile'

# Server hooks
def on_starting(server):
    """Executado quando o servidor inicia"""
    print("Iniciando servidor Gunicorn...")

def on_reload(server):
    """Executado quando o servidor recarrega"""
    print("Recarregando servidor Gunicorn...")

def when_ready(server):
    """Executado quando o servidor está pronto"""
    print(f"Servidor pronto! Escutando em {bind}")

def on_exit(server):
    """Executado quando o servidor encerra"""
    print("Encerrando servidor Gunicorn...")
