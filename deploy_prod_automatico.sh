#!/bin/bash
# ==============================================================================
# SCRIPT DE DEPLOY DE PRODUÇÃO (AUTOMÁTICO)
# Copie e cole estes comandos no terminal do servidor (192.168.168.124)
# ==============================================================================

echo "🚀 Iniciando Deploy em Produção..."

# 1. Acessar diretório do projeto
# Ajuste o caminho se necessário (ex: /opt/prova_modelagem_app)
cd /home/nicolas/prova_modelagem_app || { echo "❌ Diretório não encontrado"; exit 1; }

# 2. Configurar Git com Token para não pedir senha
# Defina a variável GITHUB_TOKEN antes de executar ou substitua abaixo
# Exemplo: export GITHUB_TOKEN="seu_token_aqui"
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  Variável GITHUB_TOKEN não definida. Configure antes de executar:"
    echo "   export GITHUB_TOKEN='seu_token_pessoal'"
    exit 1
fi
git remote set-url origin https://${GITHUB_TOKEN}@github.com/nmatss/prova_modelagem_app.git

# 3. Backup de Segurança do Banco de Dados (CRÍTICO)
echo "📦 Criando backup de segurança do banco de dados..."
# Verifica onde está o banco (local ou bind mount)
if [ -f "data/provas.db" ]; then
    cp data/provas.db "data/provas.db.pre_deploy_$(date +%Y%m%d_%H%M%S)"
    echo "✅ Backup criado com sucesso."
else
    echo "⚠️  Alerta: Banco de dados principal não encontrado em ./data/provas.db"
    if [ -f "/opt/prova_modelagem_app/data/provas.db" ]; then
         echo "ℹ️  Banco parece estar em /opt/prova_modelagem_app/data/. Backup manual recomendado se não for link simbólico."
    fi
fi

# 4. Atualizar código do GitHub
echo "⬇️  Baixando atualizações do GitHub..."
git pull origin main

# Verifica se houve erro no git pull
if [ $? -ne 0 ]; then
    echo "❌ Erro ao atualizar código. Verifique se há conflitos locais."
    exit 1
fi

# 5. Reconstruir e Reiniciar Aplicação
# -f docker-compose.sqlite.yml: Garante uso da configuração SQLite (porta 5000)
# up -d: Sobe em background
# --build: Reconstrói a imagem com as novas dependências
echo "🔄 Atualizando containers Docker..."
docker compose -f docker-compose.sqlite.yml up -d --build

# 6. Verificação Final
echo "✅ Deploy finalizado! Verificando status..."
docker compose -f docker-compose.sqlite.yml ps

echo "📜 Últimos 20 logs da aplicação:"
docker compose -f docker-compose.sqlite.yml logs --tail=20 app

echo "=============================================================================="
echo "🎉 DEPLOY CONCLUÍDO! Sistema atualizado na porta 5000."
echo "=============================================================================="
