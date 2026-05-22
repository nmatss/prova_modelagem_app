"""
Migration script: Add 'pais' column to fornecedores table.
Run once: python migrate_pais_fornecedor.py
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

    cursor.execute("PRAGMA table_info(fornecedores)")
    columns = [col[1] for col in cursor.fetchall()]

    if 'pais' not in columns:
        cursor.execute("ALTER TABLE fornecedores ADD COLUMN pais VARCHAR(100)")
        conn.commit()
        print("Column 'pais' added to fornecedores table successfully.")
    else:
        print("Column 'pais' already exists in fornecedores table.")

    conn.close()


if __name__ == '__main__':
    migrate()
