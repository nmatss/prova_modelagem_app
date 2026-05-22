"""
Migration: Cria tabela 'links_publicos' para compartilhamento read-only de relatórios.
Run once: python migrate_links_publicos.py
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
        SELECT name FROM sqlite_master WHERE type='table' AND name='links_publicos'
    """)
    if cursor.fetchone():
        print("Table 'links_publicos' already exists.")
        conn.close()
        return

    cursor.execute("""
        CREATE TABLE links_publicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token VARCHAR(64) NOT NULL UNIQUE,
            relatorio_id INTEGER NOT NULL REFERENCES relatorios(id),
            created_by INTEGER REFERENCES usuarios(id),
            titulo_personalizado VARCHAR(200),
            expires_at DATETIME,
            permite_download_pdf BOOLEAN DEFAULT 1,
            permite_download_fotos BOOLEAN DEFAULT 1,
            visualizacoes INTEGER DEFAULT 0,
            ultimo_acesso DATETIME,
            is_active BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("CREATE INDEX idx_links_token ON links_publicos(token)")
    cursor.execute("CREATE INDEX idx_links_relatorio ON links_publicos(relatorio_id)")
    conn.commit()
    print("Table 'links_publicos' created successfully.")
    conn.close()


if __name__ == '__main__':
    migrate()
