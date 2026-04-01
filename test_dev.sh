#!/bin/bash
# Script rápido para rodar apenas testes de backup
pytest tests/test_backup.py -v

#!/bin/bash
# Script para rodar testes específicos com relatório detalhado

echo "=========================================="
echo "🧪 MODO DESENVOLVIMENTO - TESTES DETALHADOS"
echo "=========================================="
echo ""

if [ "$1" = "backup" ]; then
    echo "🔒 Testando BACKUP..."
    pytest tests/test_backup.py -v --tb=long
elif [ "$1" = "contas" ]; then
    echo "💼 Testando CONTAS..."
    pytest tests/test_contas.py -v --tb=long
elif [ "$1" = "faturas" ]; then
    echo "📄 Testando FATURAS..."
    pytest tests/test_faturas.py -v --tb=long
elif [ "$1" = "resumo" ]; then
    echo "📊 Testando RESUMO..."
    pytest tests/test_resumo.py -v --tb=long
else
    echo "📊 Executando todos os testes com relatório HTML..."
    pytest tests/ -v --tb=short --html=coverage/report.html --self-contained-html
    echo "Relatório: coverage/report.html"
fi
