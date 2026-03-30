@echo off
REM Script para gerar executável com PyInstaller no Windows

echo ======================================
echo Gerando Executável da Aplicação
echo ======================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python não foi encontrado!
    echo Por favor, instale Python 3.8 ou superior
    pause
    exit /b 1
)

echo Python encontrado: 
python --version
echo.

REM Criar ambiente virtual se não existir
if not exist "venv" (
    echo Criando ambiente virtual...
    python -m venv venv
)

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instalar dependências
echo Instalando dependências...
pip install -q -r requirements-dev.txt

echo.
echo Compilando executável...
echo.

REM Gerar executável com PyInstaller
pyinstaller --onefile ^
    --windowed ^
    --name "Gestor_Financeiro" ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --hidden-import=jinja2 ^
    --hidden-import=flask ^
    --hidden-import=flask_cors ^
    --hidden-import=sqlalchemy ^
    launcher.py

echo.
echo Executável gerado com sucesso!
echo.
echo Localização: .\dist\Gestor_Financeiro.exe
echo.
echo Para usar:
echo   1. Copie o arquivo 'dist\Gestor_Financeiro.exe' para o local desejado
echo   2. Execute o arquivo
echo   3. O navegador abrirá automaticamente
echo.
pause
