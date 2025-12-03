-- Script de inicialização do banco de dados PostgreSQL
-- Execute este script para criar o banco de dados e usuário

-- Criar banco de dados
CREATE DATABASE provas_db
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'pt_BR.UTF-8'
    LC_CTYPE = 'pt_BR.UTF-8'
    TEMPLATE = template0;

-- Conectar ao banco de dados
\c provas_db

-- Criar usuário (altere a senha!)
CREATE USER provas_user WITH PASSWORD 'senha_segura_aqui';

-- Conceder privilégios
GRANT ALL PRIVILEGES ON DATABASE provas_db TO provas_user;
GRANT ALL ON SCHEMA public TO provas_user;

-- Após executar este script, atualize o DATABASE_URL no .env.production:
-- DATABASE_URL=postgresql://provas_user:senha_segura_aqui@localhost:5432/provas_db
