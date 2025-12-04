#!/usr/bin/env python3
"""
Script de inicialização do banco de dados
Cria todas as tabelas seguindo a nomenclatura padrão definida
"""
import os
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash

# Importar app e modelos
from app import app
from models import db, Usuario, Relatorio, Referencia, ProvaModelagem, FotoProva, HistoricoStatus, ConfiguracaoSistema

def init_database():
    """Inicializa o banco de dados"""
    with app.app_context():
        print("="*60)
        print("🔧 INICIALIZAÇÃO DO BANCO DE DADOS")
        print("="*60)

        # Verificar se banco já existe
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if os.path.exists(db_path):
            print(f"\n⚠️  Banco de dados já existe: {db_path}")
            resposta = input("Deseja recriar? Isso APAGARÁ todos os dados (s/N): ")
            if resposta.lower() != 's':
                print("❌ Operação cancelada")
                sys.exit(0)

            # Fazer backup
            backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.rename(db_path, backup_path)
            print(f"✅ Backup criado: {backup_path}")

        print("\n📋 Criando tabelas...")

        # Criar todas as tabelas
        db.create_all()

        print("✅ Tabelas criadas:")
        print("   ✓ usuarios")
        print("   ✓ relatorios")
        print("   ✓ referencias")
        print("   ✓ provas_modelagem")
        print("   ✓ fotos_provas")
        print("   ✓ historico_status")
        print("   ✓ configuracoes_sistema")

        # Criar usuário admin padrão
        print("\n👤 Criando usuário administrador...")
        admin = Usuario(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            email='admin@example.com',
            nome_completo='Administrador do Sistema',
            is_admin=True,
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.session.add(admin)

        # Criar usuário teste
        user_teste = Usuario(
            username='teste',
            password_hash=generate_password_hash('teste123'),
            email='teste@example.com',
            nome_completo='Usuário de Teste',
            is_admin=False,
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.session.add(user_teste)

        print("✅ Usuários criados:")
        print("   ✓ admin (senha: admin123)")
        print("   ✓ teste (senha: teste123)")

        # Criar configurações padrão do sistema
        print("\n⚙️  Criando configurações do sistema...")

        configs = [
            {
                'chave': 'status_prova_disponiveis',
                'valor': 'Em Andamento,Aprovada,Reprovada,Cancelada,Aguardando',
                'tipo_dado': 'list',
                'descricao': 'Status disponíveis para provas de modelagem'
            },
            {
                'chave': 'categorias_produto',
                'valor': 'baby,kids,teen,adulto',
                'tipo_dado': 'list',
                'descricao': 'Categorias de produtos disponíveis'
            },
            {
                'chave': 'contextos_foto',
                'valor': 'desenho,qualidade,estilo,amostra,prova_modelo',
                'tipo_dado': 'list',
                'descricao': 'Contextos disponíveis para fotos'
            },
            {
                'chave': 'tamanhos_padrao',
                'valor': 'PP,P,M,G,GG,XG,2,4,6,8,10,12,14,16',
                'tipo_dado': 'list',
                'descricao': 'Tamanhos padrão de roupas'
            },
            {
                'chave': 'max_upload_size_mb',
                'valor': '16',
                'tipo_dado': 'int',
                'descricao': 'Tamanho máximo de upload em MB'
            },
            {
                'chave': 'versao_sistema',
                'valor': '2.0.0',
                'tipo_dado': 'string',
                'descricao': 'Versão atual do sistema'
            },
            {
                'chave': 'ultima_atualizacao',
                'valor': datetime.utcnow().isoformat(),
                'tipo_dado': 'datetime',
                'descricao': 'Data da última atualização do sistema'
            }
        ]

        for config_data in configs:
            config = ConfiguracaoSistema(**config_data)
            db.session.add(config)

        print(f"✅ {len(configs)} configurações criadas")

        # Commit de todas as mudanças
        db.session.commit()

        print("\n" + "="*60)
        print("✅ BANCO DE DADOS INICIALIZADO COM SUCESSO!")
        print("="*60)
        print("\n📊 Estatísticas:")
        print(f"   Usuários: {Usuario.query.count()}")
        print(f"   Relatórios: {Relatorio.query.count()}")
        print(f"   Referências: {Referencia.query.count()}")
        print(f"   Provas: {ProvaModelagem.query.count()}")
        print(f"   Fotos: {FotoProva.query.count()}")
        print(f"   Configurações: {ConfiguracaoSistema.query.count()}")

        print("\n🚀 Sistema pronto para uso!")
        print("\n💡 Acesse com:")
        print("   URL: http://127.0.0.1:5000")
        print("   Usuário: admin")
        print("   Senha: admin123")
        print("\n")

if __name__ == '__main__':
    init_database()
