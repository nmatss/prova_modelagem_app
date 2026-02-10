"""
Migration script: Add 'linha' column to relatorios table
Run this script once to add the new column to an existing database.
Usage: python migrate_linha.py
"""
import sqlite3
import os
from config import Config

def migrate():
    # Extract database path from SQLAlchemy URI
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

    # Check if column already exists
    cursor.execute("PRAGMA table_info(relatorios)")
    columns = [col[1] for col in cursor.fetchall()]

    if 'linha' not in columns:
        cursor.execute("ALTER TABLE relatorios ADD COLUMN linha VARCHAR(50)")
        conn.commit()
        print("Column 'linha' added to relatorios table successfully.")
    else:
        print("Column 'linha' already exists in relatorios table.")

    conn.close()

if __name__ == '__main__':
    migrate()
