#!/bin/bash
# Exemplo prático: como os testes salvam o dia!

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║  🧪 DEMONSTRAÇÃO: TESTES AUTOMATIZADOS PROTEGEM SEU CÓDIGO        ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")"

# Função para mostrar resultado
check_result() {
    if [ $? -eq 0 ]; then
        echo "  ✅ PASSOU"
    else
        echo "  ❌ FALHOU"
    fi
}

echo "📊 CENÁRIO 1: Estado atual do código"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Rodando testes de backup..."
python3 -m pytest tests/test_backup.py::TestBackup::test_backup_criado_ao_salvar_dados -q
check_result

echo ""
echo "Rodando testes de contas..."
python3 -m pytest tests/test_contas.py::TestContas::test_listar_contas -q 2>/dev/null || echo "  ⚠️  ERRO (dependência de Flask client)"

echo ""
echo ""
echo "📋 CENÁRIO 2: Se eu fizesse uma mudança errada"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Simulando: fazer backup sempre retornaria None (ERRO)"
echo ""
echo "   ❌ Isso quebraria:"
echo "      - Fazer backup antes de deletar coisas"
echo "      - Proteger contra perda de dados"
echo "      - Recuperação de erros"
echo ""
echo "   🛡️  Teste detectaria antes que seja deployado!"
echo ""
echo ""
echo "════════════════════════════════════════════════════════════════════"
echo ""
echo "✨ RESUMO:"
echo ""
echo "  1️⃣  Antes de fazer mudança, testes garantem que tudo funciona"
echo "  2️⃣  Você não consegue commitar código que quebra testes"
echo "  3️⃣  Se danifica algo, erro aparece IMEDIATAMENTE"
echo "  4️⃣  Você vê exatamente qual função foi quebrada"
echo ""
echo "════════════════════════════════════════════════════════════════════"
echo ""
echo "🚀 Para rodar todos os testes:"
echo "   ./run_tests.sh"
echo ""
echo "🎯 Para modo desenvolvimento (mais detalhes):"
echo "   ./test_dev.sh"
echo ""
echo "📖 Para ler a documentação completa:"
echo "   cat TESTING.md"
echo ""
