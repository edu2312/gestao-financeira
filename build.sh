#!/bin/bash

# Script para gerar executável com PyInstaller
# Execute este script para gerar um executável standalone

echo "======================================"
echo "🔨 Gerando Executável da Aplicação"
echo "======================================"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não foi encontrado!"
    echo "   Por favor, instale Python 3.8 ou superior"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"
echo ""

# Verificar/criar ambiente virtual
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "🔌 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências..."
pip install -q -r requirements-dev.txt

echo ""
echo "🏗️  Compilando executável..."
echo ""

# Gerar executável com PyInstaller
pyinstaller --onefile \
    --windowed \
    --name "Gestor_Financeiro" \
    --icon=app_icon.icns \
    --add-data "templates:templates" \
    --add-data "static:static" \
    --hidden-import=jinja2 \
    --hidden-import=flask \
    --hidden-import=flask_cors \
    --hidden-import=sqlalchemy \
    launcher.py

echo ""
echo "✅ Executável gerado com sucesso!"
echo ""
echo "📍 Localização: ./dist/Gestor_Financeiro"
echo ""
echo "Para usar:"
echo "  1. Copie a pasta 'dist/Gestor_Financeiro' para o local desejado"
echo "  2. Execute o arquivo 'Gestor_Financeiro'"
echo "  3. O navegador abrirá automaticamente"
echo ""
