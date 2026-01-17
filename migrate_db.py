"""
Script de Migração do Banco de Dados
Adiciona novos campos para sistema de reset de senha

Execute este script antes de atualizar a aplicação em produção:
python migrate_db.py
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Adiciona novos campos ao banco de dados SQLite"""

    # Caminho do banco de dados (tentar vários locais possíveis)
    possible_paths = [
        os.path.join('data', 'provas.db'),
        os.path.join('instance', 'provas.db'),
        os.path.join('instance', 'database.db'),
    ]

    db_path = None
    for path in possible_paths:
        if os.path.exists(path):
            db_path = path
            break

    if not db_path:
        print(f"❌ Banco de dados não encontrado nos seguintes locais:")
        for path in possible_paths:
            print(f"   - {path}")
        print()
        print("   Execute a aplicação primeiro para criar o banco de dados.")
        return False

    print(f"🔧 Iniciando migração do banco de dados...")
    print(f"   Arquivo: {db_path}")
    print(f"   Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    try:
        # Backup do banco de dados
        backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup criado: {backup_path}")
        print()

        # Conectar ao banco de dados
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar se as colunas já existem
        cursor.execute("PRAGMA table_info(usuarios)")
        colunas = [col[1] for col in cursor.fetchall()]

        alteracoes = []

        # Adicionar coluna reset_token se não existir
        if 'reset_token' not in colunas:
            cursor.execute("""
                ALTER TABLE usuarios
                ADD COLUMN reset_token VARCHAR(100)
            """)
            alteracoes.append("reset_token (VARCHAR(100))")
            print("✅ Coluna 'reset_token' adicionada")
        else:
            print("ℹ️  Coluna 'reset_token' já existe")

        # Adicionar coluna reset_token_expires se não existir
        if 'reset_token_expires' not in colunas:
            cursor.execute("""
                ALTER TABLE usuarios
                ADD COLUMN reset_token_expires DATETIME
            """)
            alteracoes.append("reset_token_expires (DATETIME)")
            print("✅ Coluna 'reset_token_expires' adicionada")
        else:
            print("ℹ️  Coluna 'reset_token_expires' já existe")

        # Commit das alterações
        conn.commit()

        print()
        if alteracoes:
            print(f"✅ Migração concluída com sucesso!")
            print(f"   Total de colunas adicionadas: {len(alteracoes)}")
            for alt in alteracoes:
                print(f"   - {alt}")
        else:
            print("ℹ️  Nenhuma alteração necessária. Banco de dados já está atualizado.")

        # Verificar integridade do banco
        cursor.execute("PRAGMA integrity_check")
        resultado = cursor.fetchone()
        if resultado[0] == 'ok':
            print()
            print("✅ Verificação de integridade: OK")
        else:
            print()
            print(f"⚠️  Verificação de integridade: {resultado[0]}")

        conn.close()
        return True

    except Exception as e:
        print()
        print(f"❌ Erro durante a migração: {e}")
        print(f"   O backup está disponível em: {backup_path}")
        print(f"   Você pode restaurá-lo manualmente se necessário.")
        return False

def verify_migration():
    """Verifica se a migração foi aplicada corretamente"""
    # Tentar encontrar o banco de dados
    possible_paths = [
        os.path.join('data', 'provas.db'),
        os.path.join('instance', 'provas.db'),
        os.path.join('instance', 'database.db'),
    ]

    db_path = None
    for path in possible_paths:
        if os.path.exists(path):
            db_path = path
            break

    if not db_path:
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(usuarios)")
    colunas = [col[1] for col in cursor.fetchall()]

    conn.close()

    return 'reset_token' in colunas and 'reset_token_expires' in colunas

if __name__ == '__main__':
    print("=" * 70)
    print("   MIGRAÇÃO DO BANCO DE DADOS - SISTEMA DE RESET DE SENHA")
    print("=" * 70)
    print()

    sucesso = migrate_database()

    print()
    print("=" * 70)

    if sucesso:
        # Verificar migração
        if verify_migration():
            print("✅ MIGRAÇÃO CONCLUÍDA E VERIFICADA COM SUCESSO!")
            print()
            print("   Próximos passos:")
            print("   1. Reinicie a aplicação")
            print("   2. Teste a funcionalidade de reset de senha")
            print("   3. Se tudo funcionar, você pode remover os backups antigos")
        else:
            print("⚠️  MIGRAÇÃO INCOMPLETA")
            print("   Verifique os erros acima e tente novamente")
    else:
        print("❌ MIGRAÇÃO FALHOU")
        print("   Verifique os erros acima e corrija antes de continuar")

    print("=" * 70)
