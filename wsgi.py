"""
WSGI entry point para produção
"""
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente de produção
env_file = os.getenv('ENV_FILE', '.env.production')
load_dotenv(env_file)

from app import app

if __name__ == "__main__":
    app.run()
