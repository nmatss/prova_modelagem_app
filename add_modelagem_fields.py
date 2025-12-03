import sqlite3

conn = sqlite3.connect('provas.db')
cursor = conn.cursor()

print("Adicionando campos de Modelagem à tabela provas...")

# Adicionar colunas de modelagem se não existirem
try:
    cursor.execute('ALTER TABLE provas ADD COLUMN time_modelagem TEXT')
    print("✓ Coluna 'time_modelagem' adicionada")
except sqlite3.OperationalError:
    print("- Coluna 'time_modelagem' já existe")

try:
    cursor.execute('ALTER TABLE provas ADD COLUMN comentarios_modelagem TEXT')
    print("✓ Coluna 'comentarios_modelagem' adicionada")
except sqlite3.OperationalError:
    print("- Coluna 'comentarios_modelagem' já existe")

try:
    cursor.execute('ALTER TABLE provas ADD COLUMN obs_modelagem TEXT')
    print("✓ Coluna 'obs_modelagem' adicionada")
except sqlite3.OperationalError:
    print("- Coluna 'obs_modelagem' já existe")

conn.commit()
conn.close()
print("\n✅ Migração concluída com sucesso!")
