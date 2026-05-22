"""
Migration: Cria tabela 'import_jobs' para o fluxo round-trip Excel.
Run once: python migrate_import_jobs.py
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
        SELECT name FROM sqlite_master WHERE type='table' AND name='import_jobs'
    """)
    if cursor.fetchone():
        print("Table 'import_jobs' already exists.")
        conn.close()
        return

    cursor.execute("""
        CREATE TABLE import_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES usuarios(id),
            arquivo_original VARCHAR(500),
            arquivo_temp_path VARCHAR(500),
            status VARCHAR(20) DEFAULT 'pending',
            parsed_data TEXT,
            erros TEXT,
            summary TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            confirmed_at DATETIME
        )
    """)
    cursor.execute("CREATE INDEX idx_import_jobs_user ON import_jobs(user_id, status)")
    conn.commit()
    print("Table 'import_jobs' created successfully.")
    conn.close()


if __name__ == '__main__':
    migrate()
