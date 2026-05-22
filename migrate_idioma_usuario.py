"""
Migration: Adiciona coluna 'idioma' em usuarios (i18n).
Run once: python migrate_idioma_usuario.py
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

    cursor.execute("PRAGMA table_info(usuarios)")
    columns = [col[1] for col in cursor.fetchall()]

    if 'idioma' not in columns:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN idioma VARCHAR(5) DEFAULT 'pt'")
        conn.commit()
        print("Column 'idioma' added to usuarios table successfully.")
    else:
        print("Column 'idioma' already exists in usuarios table.")

    conn.close()


if __name__ == '__main__':
    migrate()
