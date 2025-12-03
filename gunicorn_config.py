"""
Configuração do Gunicorn para produção
"""
import os
import multiprocessing

# Bind
bind = f"{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', '8000')}"

# Workers
workers = int(os.getenv('WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = '/var/log/provas_app/access.log'
errorlog = '/var/log/provas_app/error.log'
loglevel = os.getenv('LOG_LEVEL', 'info').lower()
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'provas_app'

# Server mechanics
daemon = False
pidfile = '/var/run/provas_app/gunicorn.pid'
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
