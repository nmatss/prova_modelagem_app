# Comandos Executados na Pesquisa do Servidor

**Data:** 16/01/2026
**Servidor:** 192.168.168.124
**Objetivo:** Documentação completa do servidor de produção

---

## 1. Informações do Sistema Operacional

```bash
# Sistema e kernel
sshpass -p 'Grupo2@2254' ssh -o StrictHostKeyChecking=no nicolas@192.168.168.124 "uname -a && cat /etc/os-release"

# Resultado:
# - OS: Ubuntu 24.04.3 LTS (Noble Numbat)
# - Kernel: 6.8.0-90-generic
# - Hostname: n8n
```

---

## 2. Recursos do Servidor

```bash
# Memória
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "free -h"
# Resultado: 9.7 GB RAM, 4.0 GB Swap

# Disco
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "df -h"
# Resultado: 97 GB total, 32 GB usado (35%)

# CPU
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "nproc && lscpu"
# Resultado: 12 vCPUs, Intel Xeon E5-2650 @ 2.00GHz
```

---

## 3. Docker e Containers

```bash
# Versões
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "docker --version && docker compose version"
# Docker: 28.5.0
# Compose: v2.39.4

# Containers em execução
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "docker ps -a"
# prova_modelagem_app: Running (healthy)
# n8n-n8n-1, n8n-traefik-1, n8n-postgres-1

# Imagens
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "docker images"
# prova_modelagem_app-app: 331 MB

# Inspeção do container
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "docker inspect prova_modelagem_app"
# ID: aa81a7b1cf25
# IP: 172.21.0.2
# Status: Running (healthy)
```

---

## 4. Estrutura de Arquivos

```bash
# Diretório principal
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "ls -la /home/nicolas/prova_modelagem_app/"

# Diretório de dados
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "ls -lh /opt/prova_modelagem_app/"
```

---

## 5. Configurações

```bash
# Docker Compose
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "cat /home/nicolas/prova_modelagem_app/docker-compose.sqlite.yml"

# Variáveis de ambiente
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "cat /home/nicolas/prova_modelagem_app/.env"

# Gunicorn
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "cat /home/nicolas/prova_modelagem_app/gunicorn_config.py"

# Dockerfile
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "cat /home/nicolas/prova_modelagem_app/Dockerfile"

# Entrypoint
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "cat /home/nicolas/prova_modelagem_app/entrypoint.sh"

# Dependências
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "cat /home/nicolas/prova_modelagem_app/requirements.txt"
```

---

## 6. Volumes e Rede

```bash
# Volumes Docker
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "docker volume ls"
# prova_modelagem_app_app_data
# prova_modelagem_app_app_uploads
# prova_modelagem_app_app_logs

# Inspeção de volumes
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "docker volume inspect prova_modelagem_app_app_data prova_modelagem_app_app_uploads prova_modelagem_app_app_logs"

# Redes Docker
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "docker network ls"
# prova_modelagem_app_app_network: 172.21.0.1/16

# Configuração de rede do servidor
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "ip addr show && hostname -I"
# IP: 192.168.168.124/23
```

---

## 7. Dados e Logs

```bash
# Conteúdo dos volumes
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "ls -lh /opt/prova_modelagem_app/data/"
# provas.db (80 KB)
# Backups automáticos

sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "ls -lh /opt/prova_modelagem_app/logs/"
# access.log (3.2 MB)
# error.log (855 KB)

sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "ls -lh /opt/prova_modelagem_app/uploads/"
# Arquivos XLSX e imagens (14 MB total)

# Logs do container
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "docker logs --tail 50 prova_modelagem_app"
```

---

## 8. Monitoramento

```bash
# Status do serviço Docker
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "systemctl status docker --no-pager"

# Estatísticas do container
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "docker stats --no-stream prova_modelagem_app"
# CPU: 0.02%, RAM: 94 MB / 512 MB (18%)

# Uptime e load
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "uptime && who"
# Uptime: 4h 33min
# Load: 1.29, 1.26, 2.29
```

---

## 9. Teste de Conectividade

```bash
# Teste HTTP
sshpass -p 'Grupo2@2254' ssh nicolas@192.168.168.124 "curl -s http://localhost:5000/ | head -20"
# Aplicação respondendo (redirect para /login)
```

---

## Resumo dos Dados Coletados

### Sistema
- Ubuntu 24.04.3 LTS, Kernel 6.8.0-90
- 12 vCPUs, 9.7 GB RAM, 97 GB disco
- IP: 192.168.168.124

### Docker
- Docker 28.5.0, Compose v2.39.4
- Container: prova_modelagem_app (Running/Healthy)
- Imagem: 331 MB
- Uso: CPU 0.02%, RAM 94 MB

### Volumes
- app_data: /opt/prova_modelagem_app/data (80 KB DB + backups)
- app_uploads: /opt/prova_modelagem_app/uploads (14 MB)
- app_logs: /opt/prova_modelagem_app/logs (4 MB)

### Rede
- Container IP: 172.21.0.2
- Porta: 5000:5000
- Network: prova_modelagem_app_app_network

### Aplicação
- Flask 3.0.0 + SQLite
- Gunicorn 21.2.0 (2 workers)
- Admin: admin / Space1234

---

**Total de comandos executados:** 28
**Tempo de coleta:** ~5 minutos
**Status final:** ✅ Documentação completa gerada
