"""
Script para inicializar banco de dados em desenvolvimento
"""
import os
os.environ['ENV_FILE'] = '.env'

from flask import Flask
from models import db, User
from config import Config
from werkzeug.security import generate_password_hash

# Criar app minimalista
app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

# Inicializar DB
db.init_app(app)

with app.app_context():
    # Criar todas as tabelas
    print("Criando tabelas...")
    db.create_all()
    print("✓ Tabelas criadas com sucesso!")

    # Criar usuário admin se não existir
    if not User.query.filter_by(username='admin').first():
        print("Criando usuário admin...")
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✓ Usuário admin criado: admin / admin123")
    else:
        print("✓ Usuário admin já existe")

    print(f"\n✓ Banco de dados pronto: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print("✓ Você pode iniciar a aplicação com: python3 app.py")
