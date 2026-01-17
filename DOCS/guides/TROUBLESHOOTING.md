# 🔧 Troubleshooting Guide

Guia de resolução de problemas comuns do Sistema de Gestão de Provas de Modelagem.

---

## 📑 Índice

- [Aplicação Não Inicia](#aplicação-não-inicia)
- [Erros de Banco de Dados](#erros-de-banco-de-dados)
- [Problemas com Uploads](#problemas-com-uploads)
- [Erros de Autenticação](#erros-de-autenticação)
- [Performance Lenta](#performance-lenta)
- [Erros no Docker](#erros-no-docker)
- [Problemas com Gráficos](#problemas-com-gráficos)
- [Erros de Exportação (PDF/Excel)](#erros-de-exportação-pdfexcel)

---

## 🚫 Aplicação Não Inicia

### Problema: `ModuleNotFoundError`

```
ModuleNotFoundError: No module named 'flask'
```

**Causa:** Dependências não instaladas

**Solução:**
```bash
# Ativar ambiente virtual
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
```

---

### Problema: `Port 5000 already in use`

```
OSError: [Errno 98] Address already in use
```

**Causa:** Porta 5000 já está sendo usada

**Solução 1: Matar processo na porta**
```bash
# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Solução 2: Usar outra porta**
```bash
export FLASK_RUN_PORT=5001
python app.py
```

---

### Problema: `SECRET_KEY not configured`

```
RuntimeError: The session is unavailable because no secret key was set.
```

**Causa:** SECRET_KEY não definida no `.env`

**Solução:**
```bash
# Gerar nova SECRET_KEY
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" >> .env

# Ou editar .env manualmente
nano .env
# Adicionar: SECRET_KEY=sua_chave_secreta_aqui
```

---

## 🗄️ Erros de Banco de Dados

### Problema: `No such table: user`

```
sqlalchemy.exc.OperationalError: no such table: user
```

**Causa:** Banco de dados não inicializado

**Solução:**
```bash
# Python shell
python3 -c "from app import app, db; app.app_context().push(); db.create_all()"

# Ou via Flask shell
flask shell
>>> db.create_all()
>>> exit()
```

---

### Problema: Conexão PostgreSQL recusada

```
psycopg2.OperationalError: could not connect to server: Connection refused
```

**Causa:** PostgreSQL não está rodando ou configuração errada

**Solução 1: Verificar se PostgreSQL está rodando**
```bash
# Docker
docker ps | grep postgres

# Se não estiver rodando
docker compose up -d db

# Sistema (Ubuntu/Debian)
sudo systemctl status postgresql
sudo systemctl start postgresql
```

**Solução 2: Verificar DATABASE_URL**
```bash
# Editar .env
nano .env

# Formato correto
DATABASE_URL=postgresql://usuario:senha@host:5432/nome_banco
```

**Solução 3: Testar conexão manualmente**
```bash
psql -h localhost -U postgres -d prova_modelagem
```

---

### Problema: `InvalidTextRepresentation` (erro de tipo)

```
sqlalchemy.exc.DataError: (psycopg2.errors.InvalidTextRepresentation)
```

**Causa:** Tipo de dado incompatível (ex: string em campo integer)

**Solução:**
```python
# Verificar validação de dados antes de salvar
# Em vez de:
prova.numero_prova = request.form.get('numero_prova')

# Fazer:
try:
    prova.numero_prova = int(request.form.get('numero_prova'))
except (ValueError, TypeError):
    flash('Número de prova deve ser um número inteiro', 'error')
    return redirect(...)
```

---

### Problema: Migração falhou

```
alembic.util.exc.CommandError: Target database is not up to date.
```

**Causa:** Banco de dados desatualizado em relação às migrations

**Solução:**
```bash
# Verificar status
flask db current

# Ver histórico
flask db history

# Aplicar migrations pendentes
flask db upgrade

# Se falhar, reverter e tentar novamente
flask db downgrade
flask db upgrade
```

---

## 📷 Problemas com Uploads

### Problema: `413 Request Entity Too Large`

**Causa:** Arquivo maior que o limite permitido

**Solução:**
```python
# Aumentar limite em config.py ou .env
MAX_CONTENT_LENGTH=52428800  # 50MB (em bytes)

# Para Nginx (se usar)
# /etc/nginx/nginx.conf
client_max_body_size 50M;

# Reiniciar Nginx
sudo systemctl restart nginx
```

---

### Problema: Upload falha silenciosamente

**Causa:** Diretório de upload não tem permissões de escrita

**Solução:**
```bash
# Verificar permissões
ls -la uploads/

# Corrigir permissões
chmod 755 uploads/
chown -R $USER:$USER uploads/

# Para Docker
docker exec -it prova_modelagem_app chmod 755 /app/uploads
```

---

### Problema: Extensão de arquivo não permitida

```
Tipo de arquivo não permitido
```

**Causa:** Extensão não está na lista de permitidas

**Solução:**
```python
# config.py ou app.py
ALLOWED_EXTENSIONS = {
    'png', 'jpg', 'jpeg', 'gif', 'webp',  # Imagens
    'pdf', 'doc', 'docx',                  # Documentos
    'ppt', 'pptx',                         # Apresentações
    'xls', 'xlsx'                          # Planilhas
}

# Adicionar nova extensão
ALLOWED_EXTENSIONS.add('svg')
```

---

### Problema: Caminho de arquivo quebrado

```
FileNotFoundError: [Errno 2] No such file or directory
```

**Causa:** Caminho relativo/absoluto incorreto

**Solução:**
```python
# Sempre usar caminhos absolutos
import os
from werkzeug.utils import secure_filename

# Correto
filename = secure_filename(file.filename)
filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
file.save(filepath)

# Armazenar caminho relativo no banco
db_path = os.path.join('uploads', filename)
```

---

## 🔐 Erros de Autenticação

### Problema: Login loop infinito

**Causa:** Sessão não está sendo criada corretamente

**Solução:**
```python
# Verificar SECRET_KEY no .env
# Verificar se Flask-Login está configurado corretamente

# app.py
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

---

### Problema: `Unauthorized` mesmo após login

```
401 Unauthorized
```

**Causa:** Decorador `@login_required` sem configuração correta

**Solução:**
```python
# Verificar se está importando do lugar correto
from flask_login import login_required, current_user

# Verificar ordem dos decorators
@app.route('/dashboard')
@login_required  # DEVE vir DEPOIS do @app.route
def dashboard():
    pass
```

---

### Problema: Senha não aceita

**Causa:** Validação de senha muito restritiva ou hash incorreto

**Solução:**
```python
# Verificar hash
from werkzeug.security import check_password_hash

user = User.query.filter_by(username='admin').first()
password_ok = check_password_hash(user.password_hash, 'senha_digitada')
print(f"Senha correta: {password_ok}")

# Resetar senha de admin
user = User.query.filter_by(username='admin').first()
user.password_hash = generate_password_hash('nova_senha')
db.session.commit()
```

---

### Problema: Reset de senha não funciona

**Causa:** Token expirado ou inválido

**Solução:**
```python
# Verificar validade do token
from itsdangerous import URLSafeTimedSerializer

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
try:
    email = serializer.loads(token, salt='password-reset', max_age=3600)
    print(f"Token válido para: {email}")
except:
    print("Token inválido ou expirado")
```

---

## 🐌 Performance Lenta

### Problema: Dashboard demora para carregar

**Causa:** Queries N+1 ou falta de índices

**Solução:**
```python
# Usar eager loading
from sqlalchemy.orm import joinedload

relatorios = Relatorio.query\
    .options(
        joinedload(Relatorio.provas),
        joinedload(Relatorio.referencias)
    )\
    .filter_by(user_id=current_user.id)\
    .all()

# Adicionar índices
class Relatorio(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    status = db.Column(db.String(20), index=True)
    created_at = db.Column(db.DateTime, index=True)
```

---

### Problema: Página de analytics trava

**Causa:** Chart.js carregando muitos dados

**Solução:**
```python
# Limitar dados retornados
from sqlalchemy import func
from datetime import datetime, timedelta

# Últimos 90 dias apenas
data_limite = datetime.utcnow() - timedelta(days=90)

stats = db.session.query(
    func.date(Relatorio.created_at).label('data'),
    func.count(Relatorio.id).label('total')
)\
.filter(Relatorio.created_at >= data_limite)\
.group_by(func.date(Relatorio.created_at))\
.all()
```

---

### Problema: Banco de dados cresce muito

**Causa:** Logs de auditoria sem limpeza

**Solução:**
```bash
# Limpar logs antigos (manualmente)
python3 << 'EOF'
from app import app, db
from models import AuditLog
from datetime import datetime, timedelta

app.app_context().push()

# Deletar logs com mais de 1 ano
data_limite = datetime.utcnow() - timedelta(days=365)
AuditLog.query.filter(AuditLog.timestamp < data_limite).delete()
db.session.commit()
print("Logs antigos deletados")
EOF

# Criar job cron para automatizar
# crontab -e
# 0 2 1 * * /opt/prova_app/scripts/cleanup_logs.sh
```

---

## 🐳 Erros no Docker

### Problema: Container não inicia

```
Error: Container exited with code 1
```

**Causa:** Erro na aplicação ou configuração errada

**Solução:**
```bash
# Ver logs completos
docker compose logs web

# Rodar container interativamente para debug
docker compose run --rm web bash

# Dentro do container
python app.py
# Ver erro específico
```

---

### Problema: `database "prova_modelagem" does not exist`

**Causa:** Banco não foi criado

**Solução:**
```bash
# Acessar container do PostgreSQL
docker compose exec db psql -U postgres

# Criar banco
CREATE DATABASE prova_modelagem;
\q

# Reiniciar aplicação
docker compose restart web
```

---

### Problema: Volume não persiste dados

**Causa:** Volume não foi criado corretamente

**Solução:**
```bash
# Verificar volumes
docker volume ls

# Recriar volumes
docker compose down -v
docker compose up -d

# ATENÇÃO: -v deleta volumes, fazer backup antes!
```

---

### Problema: Health check sempre unhealthy

**Causa:** Endpoint /health não responde ou demora muito

**Solução:**
```python
# Verificar endpoint /health
curl http://localhost:5000/health

# Aumentar timeout no docker-compose.yml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
  interval: 30s
  timeout: 10s  # Aumentar de 5s para 10s
  retries: 5
```

---

## 📊 Problemas com Gráficos

### Problema: Gráficos não aparecem

**Causa:** Chart.js não carregou ou erro de dados

**Solução 1: Verificar console do navegador**
```
F12 → Console → Ver erros JavaScript
```

**Solução 2: Verificar se Chart.js está carregando**
```html
<!-- Verificar em templates/base.html -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>

<!-- Ou local -->
<script src="{{ url_for('static', filename='js/chart.min.js') }}"></script>
```

**Solução 3: Validar formato de dados**
```javascript
// analytics.html ou app.js
console.log('Dados do gráfico:', chartData);

// Formato esperado
const chartData = {
    labels: ['Jan', 'Feb', 'Mar'],
    datasets: [{
        label: 'Relatórios',
        data: [12, 19, 3]
    }]
};
```

---

### Problema: Gráfico mostra "undefined"

**Causa:** Dados não estão no formato correto ou valores nulos

**Solução:**
```python
# Backend - garantir que não há valores None
stats = {
    'labels': [item.mes or 'Sem data' for item in data],
    'values': [item.total or 0 for item in data]
}
return jsonify(stats)
```

```javascript
// Frontend - validar dados antes de criar gráfico
if (chartData && chartData.labels && chartData.labels.length > 0) {
    createChart(chartData);
} else {
    console.error('Dados inválidos para gráfico');
}
```

---

## 📄 Erros de Exportação (PDF/Excel)

### Problema: PDF não gera ou fica vazio

**Causa:** WeasyPrint não instalado ou erro de CSS

**Solução:**
```bash
# Instalar WeasyPrint e dependências
pip install WeasyPrint

# Ubuntu/Debian - instalar dependências do sistema
sudo apt-get install -y \
    python3-cffi \
    python3-brotli \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libffi-dev

# Verificar instalação
python3 -c "import weasyprint; print(weasyprint.__version__)"
```

**Debug de CSS no PDF:**
```python
# app.py - rota de PDF
from weasyprint import HTML

html_string = render_template('relatorio_pdf.html', relatorio=relatorio)
pdf = HTML(string=html_string).write_pdf()

# Para debug, salvar HTML temporário
with open('/tmp/debug.html', 'w') as f:
    f.write(html_string)
```

---

### Problema: Excel não exporta todos os dados

**Causa:** Limite de linhas ou colunas ultrapassado

**Solução:**
```python
# excel_export.py
import openpyxl
from openpyxl.utils import get_column_letter

# Verificar limites
print(f"Total de linhas: {len(data)}")  # Max: 1,048,576
print(f"Total de colunas: {len(headers)}")  # Max: 16,384

# Paginar se necessário
ROWS_PER_SHEET = 50000

for i in range(0, len(data), ROWS_PER_SHEET):
    sheet = wb.create_sheet(f"Página {i//ROWS_PER_SHEET + 1}")
    chunk = data[i:i+ROWS_PER_SHEET]
    # ... adicionar dados
```

---

### Problema: Caracteres especiais aparecem errados

**Causa:** Encoding incorreto

**Solução:**
```python
# Sempre usar UTF-8
import io

output = io.BytesIO()
wb.save(output)
output.seek(0)

return send_file(
    output,
    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    as_attachment=True,
    download_name='relatorio.xlsx'
)
```

---

## 🛠️ Ferramentas de Debug

### Logs da Aplicação

```bash
# Desenvolvimento
export FLASK_DEBUG=True
python app.py

# Produção (Gunicorn)
tail -f /app/logs/gunicorn.error.log
tail -f /app/logs/gunicorn.access.log

# Docker
docker compose logs -f web
docker compose logs -f --tail=100 web
```

---

### Flask Shell

```bash
flask shell

# Testar queries
>>> from models import User, Relatorio
>>> User.query.all()
>>> Relatorio.query.count()

# Testar funções
>>> from utils import allowed_file
>>> allowed_file('test.png')
True
```

---

### SQL Debug

```python
# app.py - Habilitar SQL logging
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Agora todas as queries serão printadas no console
```

---

### Python Debugger

```python
# Adicionar breakpoint
import pdb; pdb.set_trace()

# Ou (Python 3.7+)
breakpoint()

# Comandos úteis no debugger
# n - next line
# s - step into
# c - continue
# p variable - print variable
# l - list code around current line
# q - quit
```

---

## 📞 Quando Pedir Ajuda

Se após seguir este guia o problema persistir:

1. **Coletar informações:**
   - Logs completos da aplicação
   - Mensagem de erro exata
   - Passos para reproduzir o problema
   - Versões (Python, Flask, PostgreSQL, etc.)

2. **Verificar documentação:**
   - [DOCS/INDEX.md](../INDEX.md)
   - [DOCS/guides/MAINTENANCE.md](MAINTENANCE.md)

3. **Contatar suporte:**
   - Email: nicolas.matsuda@grupounico.com
   - Incluir todas as informações coletadas acima

---

## 🔗 Links Úteis

- **Documentação Flask:** https://flask.palletsprojects.com/
- **SQLAlchemy:** https://docs.sqlalchemy.org/
- **PostgreSQL:** https://www.postgresql.org/docs/
- **Docker:** https://docs.docker.com/
- **Chart.js:** https://www.chartjs.org/docs/

---

**[⬅ Voltar ao Índice](../INDEX.md)**
