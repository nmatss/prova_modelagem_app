#!/usr/bin/env python3
"""
Script de migração do banco de dados
Adiciona novos campos sem importar o app
"""
import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = '/home/icolas_atsuda/ProjetosWeb/prova_modelagem_app/instance/provas.db'

def migrate_database():
    """Adiciona novos campos ao banco de dados"""
    print("=" * 60)
    print("MIGRAÇÃO DO BANCO DE DADOS")
    print("=" * 60)

    if not os.path.exists(DB_PATH):
        print(f"❌ Banco de dados não encontrado em: {DB_PATH}")
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Verificar quais colunas existem
        cursor.execute("PRAGMA table_info(usuarios)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"\n📋 Colunas atuais: {', '.join(columns)}")

        # Adicionar coluna 'role' se não existir
        if 'role' not in columns:
            print("\n🔄 Adicionando coluna 'role'...")
            cursor.execute("ALTER TABLE usuarios ADD COLUMN role VARCHAR(50) DEFAULT 'usuario'")
            print("   ✅ Coluna 'role' adicionada")
        else:
            print("\n   ℹ️ Coluna 'role' já existe")

        # Adicionar coluna 'senha_temporaria' se não existir
        if 'senha_temporaria' not in columns:
            print("🔄 Adicionando coluna 'senha_temporaria'...")
            cursor.execute("ALTER TABLE usuarios ADD COLUMN senha_temporaria BOOLEAN DEFAULT 0")
            print("   ✅ Coluna 'senha_temporaria' adicionada")
        else:
            print("   ℹ️ Coluna 'senha_temporaria' já existe")

        # Atualizar role dos usuários admin existentes
        print("\n🔄 Atualizando roles dos usuários admin...")
        cursor.execute("UPDATE usuarios SET role = 'admin' WHERE is_admin = 1")
        print(f"   ✅ {cursor.rowcount} usuários admin atualizados")

        # Atualizar role dos usuários não-admin
        cursor.execute("UPDATE usuarios SET role = 'usuario' WHERE is_admin = 0 OR is_admin IS NULL")
        print(f"   ✅ {cursor.rowcount} usuários normais atualizados")

        conn.commit()
        print("\n✅ Migração concluída com sucesso!")

        return True

    except Exception as e:
        print(f"\n❌ Erro na migração: {e}")
        conn.rollback()
        return False

    finally:
        conn.close()

def update_admin_password():
    """Atualiza a senha do usuário admin.

    Requer variável de ambiente `ADMIN_RESET_PASSWORD` definida.
    A senha NUNCA é impressa em log/stdout.
    """
    print("\n" + "=" * 60)
    print("ATUALIZAÇÃO DA SENHA DO ADMIN")
    print("=" * 60)

    nova_senha = os.getenv("ADMIN_RESET_PASSWORD")
    if not nova_senha:
        print("\n❌ Variável ADMIN_RESET_PASSWORD não definida.")
        print("   Defina antes de rodar:")
        print("     export ADMIN_RESET_PASSWORD='sua-nova-senha-forte'")
        print("   Ou via secrets/admin.env e re-execute.")
        return False
    if len(nova_senha) < 8:
        print("\n❌ ADMIN_RESET_PASSWORD muito curta (mínimo 8 caracteres).")
        return False

    senha_hash = generate_password_hash(nova_senha)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Verificar se admin existe
        cursor.execute("SELECT id, username, email FROM usuarios WHERE username = 'admin'")
        admin = cursor.fetchone()

        if not admin:
            print("\n❌ Usuário 'admin' não encontrado!")
            print("🔄 Criando usuário admin...")

            cursor.execute("""
                INSERT INTO usuarios (username, email, nome_completo, password_hash, role, is_admin, is_active, senha_temporaria)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, ('admin', 'admin@puket.com', 'Administrador do Sistema', senha_hash, 'admin', 1, 1, 0))

            conn.commit()
            print("✅ Usuário admin criado com sucesso!")
            print(f"   Username: admin")
            print(f"   Senha: (definida via ADMIN_RESET_PASSWORD — {len(nova_senha)} caracteres)")
            print(f"   Email: admin@puket.com")
            return True

        # Atualizar senha do admin
        print(f"\n🔄 Atualizando senha do admin (ID: {admin[0]}, Username: {admin[1]})...")

        cursor.execute("""
            UPDATE usuarios
            SET password_hash = ?, role = 'admin', is_admin = 1, senha_temporaria = 0
            WHERE username = 'admin'
        """, (senha_hash,))

        conn.commit()

        print("✅ Senha do admin atualizada com sucesso!")
        print(f"   Username: {admin[1]}")
        print(f"   Nova senha: (definida via ADMIN_RESET_PASSWORD — {len(nova_senha)} caracteres)")
        print(f"   Email: {admin[2] or 'N/A'}")

        return True

    except Exception as e:
        print(f"\n❌ Erro ao atualizar senha: {e}")
        conn.rollback()
        return False

    finally:
        conn.close()

if __name__ == '__main__':
    print("\n")

    # Executar migração
    if migrate_database():
        # Atualizar senha do admin
        update_admin_password()

        print("\n" + "=" * 60)
        print("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        print("\n📝 Próximos passos:")
        print("   1. Reinicie a aplicação")
        print("   2. Faça login com:")
        print("      Username: admin")
        print("      Senha: (a que você definiu em ADMIN_RESET_PASSWORD)")
        print("   3. Acesse /admin/users para gerenciar usuários")
        print()
    else:
        print("\n❌ Processo interrompido devido a erros.")
        exit(1)
