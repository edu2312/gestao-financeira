#!/bin/bash
# Script para rodar testes e validar mudanças antes de commitar

set -e  # Parar se algo falhar

echo "=========================================="
echo "🧪 RODANDO TESTES AUTOMATIZADOS"
echo "=========================================="

# Verificar se pytest está instalado
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest não está instalado"
    echo "   Execute: pip install -r requirements-test.txt"
    exit 1
fi

echo ""
echo "📦 Instalando dependências de teste..."
pip install -q -r requirements-test.txt

echo ""
echo "🔍 Executando testes..."
pytest tests/ -v --tb=short --cov=app_v2 --cov-report=term-missing

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ TODOS OS TESTES PASSARAM!"
    echo "=========================================="
    exit 0
else
    echo ""
    echo "=========================================="
    echo "❌ TESTES FALHARAM!"
    echo "=========================================="
    echo "Por favor, corrija os erros antes de continuar"
    exit 1
fi
