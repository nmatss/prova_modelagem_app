"""
Script para migrar dados do SQLite para PostgreSQL
Execute após configurar o PostgreSQL e antes de iniciar a aplicação em produção
"""
import os
from dotenv import load_dotenv

# Carregar ambiente de produção
load_dotenv('.env.production')

from app import app, db
from models import User, Relatorio, Referencia, Prova, Foto

def migrate_data():
    """
    Migra dados do SQLite para PostgreSQL
    """
    print("Iniciando migração de dados...")

    with app.app_context():
        # Criar todas as tabelas no novo banco
        print("Criando tabelas no PostgreSQL...")
        db.create_all()
        print("Tabelas criadas com sucesso!")

        print("\nPara migrar dados do SQLite:")
        print("1. Faça backup do banco SQLite atual")
        print("2. Use ferramentas como pgloader ou scripts customizados")
        print("3. Ou recrie os dados manualmente")

        # Verificar se há usuários
        user_count = User.query.count()
        if user_count == 0:
            print("\nNenhum usuário encontrado. Você precisará criar usuários administrativos.")
            print("Execute: python3 create_test_user.py")
        else:
            print(f"\n{user_count} usuário(s) encontrado(s)")

if __name__ == '__main__':
    migrate_data()
