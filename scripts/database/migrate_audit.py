#!/usr/bin/env python3
"""
Script de migração para Auditoria
Cria a tabela audit_logs
"""
import sqlite3
import os

DB_PATH = '/home/icolas_atsuda/ProjetosWeb/prova_modelagem_app/instance/provas.db'

def migrate_audit():
    """Cria a tabela de auditoria"""
    print("=" * 60)
    print("MIGRAÇÃO - SISTEMA DE AUDITORIA")
    print("=" * 60)

    if not os.path.exists(DB_PATH):
        print(f"❌ Banco de dados não encontrado em: {DB_PATH}")
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Verificar se a tabela já existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='audit_logs'")
        if cursor.fetchone():
            print("\n⚠️  Tabela 'audit_logs' já existe!")
            resposta = input("Deseja recriar a tabela? (s/N): ")
            if resposta.lower() != 's':
                print("✅ Migração cancelada.")
                return True

            # Drop table
            print("🔄 Removendo tabela existente...")
            cursor.execute("DROP TABLE audit_logs")
            print("   ✅ Tabela removida")

        # Criar tabela audit_logs
        print("\n🔄 Criando tabela 'audit_logs'...")
        cursor.execute("""
            CREATE TABLE audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                usuario_nome VARCHAR(150),
                acao VARCHAR(50) NOT NULL,
                entidade VARCHAR(50) NOT NULL,
                entidade_id INTEGER,
                descricao TEXT,
                dados_antes TEXT,
                dados_depois TEXT,
                ip_address VARCHAR(45),
                user_agent VARCHAR(500),
                metodo_http VARCHAR(10),
                url VARCHAR(500),
                categoria VARCHAR(50),
                severidade VARCHAR(20),
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)
        print("   ✅ Tabela 'audit_logs' criada")

        # Criar índices para melhorar performance
        print("\n🔄 Criando índices...")
        cursor.execute("CREATE INDEX idx_audit_usuario ON audit_logs(usuario_id)")
        print("   ✅ Índice 'idx_audit_usuario' criado")

        cursor.execute("CREATE INDEX idx_audit_acao ON audit_logs(acao)")
        print("   ✅ Índice 'idx_audit_acao' criado")

        cursor.execute("CREATE INDEX idx_audit_entidade ON audit_logs(entidade)")
        print("   ✅ Índice 'idx_audit_entidade' criado")

        cursor.execute("CREATE INDEX idx_audit_entidade_id ON audit_logs(entidade_id)")
        print("   ✅ Índice 'idx_audit_entidade_id' criado")

        cursor.execute("CREATE INDEX idx_audit_categoria ON audit_logs(categoria)")
        print("   ✅ Índice 'idx_audit_categoria' criado")

        cursor.execute("CREATE INDEX idx_audit_created_at ON audit_logs(created_at)")
        print("   ✅ Índice 'idx_audit_created_at' criado")

        conn.commit()
        print("\n✅ Migração concluída com sucesso!")

        # Verificar estrutura
        print("\n📋 Estrutura da tabela:")
        cursor.execute("PRAGMA table_info(audit_logs)")
        columns = cursor.fetchall()
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")

        return True

    except Exception as e:
        print(f"\n❌ Erro na migração: {e}")
        conn.rollback()
        return False

    finally:
        conn.close()

if __name__ == '__main__':
    print("\n")

    if migrate_audit():
        print("\n" + "=" * 60)
        print("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        print("\n📝 Próximos passos:")
        print("   1. Reinicie a aplicação")
        print("   2. Faça login como admin")
        print("   3. Acesse o menu Auditoria")
        print("   4. Os logs começarão a ser registrados automaticamente")
        print()
    else:
        print("\n❌ Processo interrompido devido a erros.")
        exit(1)
