@echo off
echo --- Configurando Ambiente Local ---

REM Verifica se Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python nao encontrado! Por favor instale o Python.
    pause
    exit /b
)

REM Cria ambiente virtual se nao existir
if not exist "venv" (
    echo Criando ambiente virtual...
    python -m venv venv
)

REM Ativa ambiente virtual
call venv\Scripts\activate

REM Instala dependencias
echo Instalando dependencias...
pip install -r requirements.txt

REM Inicializa banco de dados
echo Verificando banco de dados...
python database_setup.py

REM Inicia a aplicacao
echo --- Iniciando Aplicacao ---
echo Acesse http://127.0.0.1:5000 no seu navegador
python app.py

pause
