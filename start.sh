#!/bin/bash

# Script para instalar dependências e iniciar a aplicação

echo "🚀 Sistema de Finanças - Startup"
echo "=================================="
echo ""

# Qual sistema?
if [[ "$OSTYPE" == "darwin"* ]]; then
    PYTHON="python3"
    echo "✅ Detectado: macOS"
else
    PYTHON="python"
    echo "✅ Detectado: Windows/Linux"
fi

# Verificar se Python existe
if ! command -v $PYTHON &> /dev/null; then
    echo "❌ Python não encontrado! Instale Python 3.9+"
    exit 1
fi

echo ""
echo "📦 Instalando dependências..."
$PYTHON -m pip install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

echo "✅ Dependências instaladas"
echo ""
echo "🔥 Iniciando aplicação..."
echo "📱 Abra seu navegador em: http://localhost:5000"
echo ""
echo "Pressione Ctrl+C para parar"
echo ""

$PYTHON app.py
