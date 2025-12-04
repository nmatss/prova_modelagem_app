#!/bin/bash
# Backup automatizado para Docker - Sistema Puket

set -e

# Configurações
BACKUP_DIR="/opt/prova_app/backups"
DATE=$(date +%Y%m%d_%H%M%S)
KEEP_DAYS=7

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🔄 Iniciando backup...${NC}"

# Criar diretório de backup
mkdir -p "$BACKUP_DIR"

# Backup do banco de dados
echo -e "${YELLOW}📦 Backup do banco de dados...${NC}"
docker compose exec -T db pg_dump -U prova_user prova_modelagem_db | gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

# Backup dos uploads
echo -e "${YELLOW}📷 Backup dos uploads...${NC}"
tar -czf "$BACKUP_DIR/uploads_$DATE.tar.gz" -C /opt/prova_app uploads/

# Backup do .env
echo -e "${YELLOW}⚙️  Backup das configurações...${NC}"
cp /opt/prova_app/.env "$BACKUP_DIR/env_$DATE"

# Tamanho dos backups
DB_SIZE=$(du -h "$BACKUP_DIR/db_$DATE.sql.gz" | cut -f1)
UPLOADS_SIZE=$(du -h "$BACKUP_DIR/uploads_$DATE.tar.gz" | cut -f1)

echo -e "${GREEN}✅ Backup concluído!${NC}"
echo "   📊 Banco: $DB_SIZE"
echo "   📷 Uploads: $UPLOADS_SIZE"
echo "   📁 Local: $BACKUP_DIR"

# Limpar backups antigos
echo -e "${YELLOW}🗑️  Removendo backups com mais de $KEEP_DAYS dias...${NC}"
find "$BACKUP_DIR" -name "*.gz" -mtime +$KEEP_DAYS -delete
find "$BACKUP_DIR" -name "env_*" -mtime +$KEEP_DAYS -delete

echo -e "${GREEN}✅ Limpeza concluída!${NC}"

# Listar backups disponíveis
echo ""
echo "Backups disponíveis:"
ls -lh "$BACKUP_DIR" | grep -E "db_|uploads_" | tail -5
