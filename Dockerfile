# ==================================
# Dockerfile de Produção
# Sistema de Provas Puket
# Flask + PostgreSQL + Gunicorn
# ==================================

# ====================================
# Stage 1: Builder
# ====================================
FROM python:3.11-slim as builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependências de build
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --user --no-warn-script-location \
    -r requirements.txt \
    gunicorn \
    psycopg2-binary \
    weasyprint

# ====================================
# Stage 2: Runtime
# ====================================
FROM python:3.11-slim

LABEL maintainer="Puket - Nicolas Matsuda"
LABEL description="Sistema de Provas de Modelagem - Produção"
LABEL version="2.0.0"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production \
    DEBUG=False \
    PORT=8000

# Instalar dependências de runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi7 \
    shared-mime-info \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/uploads /app/logs /app/backups && \
    chown -R appuser:appuser /app

WORKDIR /app

# Copiar dependências do builder
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copiar código da aplicação
COPY --chown=appuser:appuser . .

# Criar diretórios e ajustar permissões
RUN chown -R appuser:appuser /app && \
    chmod +x /app/entrypoint.sh

# Mudar para usuário não-root
USER appuser

# Adicionar .local/bin ao PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Expor porta
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Entrypoint e comando
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]
