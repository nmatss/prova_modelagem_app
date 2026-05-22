"""
Migration: Cria tabela 'manuais' para o módulo de Manuais/Documentos.
Run once: python migrate_manuais.py
"""
import sqlite3
import os
from config import Config


def migrate():
    db_uri = Config.SQLALCHEMY_DATABASE_URI
    if db_uri.startswith('sqlite:////'):
        db_path = db_uri[len('sqlite:///'):]
    elif db_uri.startswith('sqlite:///'):
        db_path = os.path.join(Config.basedir, db_uri[len('sqlite:///'):])
    else:
        print(f"Unsupported database URI: {db_uri}")
        return

    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}. It will be created when the app starts.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='manuais'
    """)
    if cursor.fetchone():
        print("Table 'manuais' already exists.")
        conn.close()
        return

    cursor.execute("""
        CREATE TABLE manuais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo VARCHAR(200) NOT NULL,
            descricao TEXT,
            categoria VARCHAR(100),
            file_path VARCHAR(500) NOT NULL,
            file_size INTEGER,
            uploaded_by INTEGER REFERENCES usuarios(id),
            downloads INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME
        )
    """)
    cursor.execute("CREATE INDEX idx_manuais_categoria ON manuais(categoria)")
    conn.commit()
    print("Table 'manuais' created successfully.")
    conn.close()


if __name__ == '__main__':
    migrate()
