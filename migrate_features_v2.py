"""
Migration script for Features v2:
- F2: data_limite on relatorios
- F4: fornecedores table + fornecedor_id on referencias
- F3: checklist_templates + checklist_respostas tables
- F8: arquivo_versoes table
- F9: preferencias_usuarios table
- Seed: default checklist templates

Idempotent: safe to run multiple times.
"""

import sqlite3
import shutil
import os
from datetime import datetime
import json

DB_PATH = '/tmp/provas.db'

def backup_db():
    if os.path.exists(DB_PATH):
        backup_path = DB_PATH.replace('.db', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db')
        shutil.copy2(DB_PATH, backup_path)
        print(f"Backup criado: {backup_path}")
    else:
        print("Banco de dados não encontrado, pulando backup.")

def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cursor.fetchall()]
    return column in columns

def table_exists(cursor, table):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    return cursor.fetchone() is not None

def migrate():
    backup_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # =============================================
    # F2: ALTER TABLE relatorios ADD data_limite
    # =============================================
    if not column_exists(cursor, 'relatorios', 'data_limite'):
        cursor.execute("ALTER TABLE relatorios ADD COLUMN data_limite VARCHAR(20)")
        print("+ Coluna 'data_limite' adicionada em 'relatorios'")
    else:
        print("= Coluna 'data_limite' já existe em 'relatorios'")

    # =============================================
    # F4: CREATE TABLE fornecedores
    # =============================================
    if not table_exists(cursor, 'fornecedores'):
        cursor.execute("""
            CREATE TABLE fornecedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(200) NOT NULL,
                contato VARCHAR(200),
                email VARCHAR(255),
                telefone VARCHAR(50),
                endereco VARCHAR(500),
                cnpj VARCHAR(20) UNIQUE,
                avaliacao INTEGER DEFAULT 0,
                observacoes TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME
            )
        """)
        print("+ Tabela 'fornecedores' criada")
    else:
        print("= Tabela 'fornecedores' já existe")

    # F4: ALTER TABLE referencias ADD fornecedor_id
    if not column_exists(cursor, 'referencias', 'fornecedor_id'):
        cursor.execute("ALTER TABLE referencias ADD COLUMN fornecedor_id INTEGER REFERENCES fornecedores(id)")
        print("+ Coluna 'fornecedor_id' adicionada em 'referencias'")
    else:
        print("= Coluna 'fornecedor_id' já existe em 'referencias'")

    # =============================================
    # F3: CREATE TABLE checklist_templates
    # =============================================
    if not table_exists(cursor, 'checklist_templates'):
        cursor.execute("""
            CREATE TABLE checklist_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(200) NOT NULL,
                categoria VARCHAR(50) NOT NULL,
                itens TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME
            )
        """)
        print("+ Tabela 'checklist_templates' criada")

        # Seed default templates
        templates_seed = [
            ('Checklist de Qualidade', 'qualidade', json.dumps([
                'Costura reta e uniforme',
                'Acabamento de borda',
                'Resistência do tecido',
                'Alinhamento de estampa',
                'Verificação de cores',
                'Teste de lavagem',
                'Verificação de aviamentos',
                'Conferência de etiquetas'
            ], ensure_ascii=False)),
            ('Checklist de Estilo', 'estilo', json.dumps([
                'Caimento adequado',
                'Proporções corretas',
                'Detalhes de design',
                'Harmonia visual',
                'Conformidade com croqui',
                'Acabamento estético',
                'Equilíbrio de cores',
                'Adequação ao público-alvo'
            ], ensure_ascii=False)),
            ('Checklist de Modelagem', 'modelagem', json.dumps([
                'Medidas conferidas',
                'Grade de tamanhos',
                'Encaixe de moldes',
                'Margem de costura',
                'Sentido do fio',
                'Pences e recortes',
                'Simetria das partes',
                'Conformidade com ficha técnica'
            ], ensure_ascii=False)),
        ]

        cursor.executemany(
            "INSERT INTO checklist_templates (nome, categoria, itens) VALUES (?, ?, ?)",
            templates_seed
        )
        print("+ Seed de checklist templates inserido (3 templates padrão)")
    else:
        print("= Tabela 'checklist_templates' já existe")

    # F3: CREATE TABLE checklist_respostas
    if not table_exists(cursor, 'checklist_respostas'):
        cursor.execute("""
            CREATE TABLE checklist_respostas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prova_id INTEGER NOT NULL REFERENCES provas(id),
                template_id INTEGER NOT NULL REFERENCES checklist_templates(id),
                item VARCHAR(200) NOT NULL,
                conforme BOOLEAN DEFAULT 0,
                observacao TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("+ Tabela 'checklist_respostas' criada")
    else:
        print("= Tabela 'checklist_respostas' já existe")

    # =============================================
    # F8: CREATE TABLE arquivo_versoes
    # =============================================
    if not table_exists(cursor, 'arquivo_versoes'):
        cursor.execute("""
            CREATE TABLE arquivo_versoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entidade_tipo VARCHAR(50) NOT NULL,
                entidade_id INTEGER NOT NULL,
                campo VARCHAR(100) NOT NULL,
                file_path VARCHAR(500) NOT NULL,
                versao INTEGER DEFAULT 1,
                uploaded_by INTEGER REFERENCES usuarios(id),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("+ Tabela 'arquivo_versoes' criada")
    else:
        print("= Tabela 'arquivo_versoes' já existe")

    # =============================================
    # F9: CREATE TABLE preferencias_usuarios
    # =============================================
    if not table_exists(cursor, 'preferencias_usuarios'):
        cursor.execute("""
            CREATE TABLE preferencias_usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL UNIQUE REFERENCES usuarios(id),
                widget_config TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME
            )
        """)
        print("+ Tabela 'preferencias_usuarios' criada")
    else:
        print("= Tabela 'preferencias_usuarios' já existe")

    conn.commit()
    conn.close()
    print("\nMigração concluída com sucesso!")


if __name__ == '__main__':
    migrate()
