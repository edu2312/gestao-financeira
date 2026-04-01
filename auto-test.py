#!/usr/bin/env python3
"""
🤖 ASSISTENTE AUTOMÁTICO DE TESTES
Script que roda ANTES de qualquer mudança no código

Este script:
1. ✅ Verifica se código atual passa nos testes
2. ✅ Se passar: mudança é segura, prossegue
3. ❌ Se falhar: halts antes de fazer coisas erradas
"""

import subprocess
import sys
import os
from datetime import datetime

def run_command(cmd, verbose=False):
    """Executa comando e retorna resultado"""
    try:
        if verbose:
            print(f"  $ {cmd}")
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=60
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "TIMEOUT"
    except Exception as e:
        return False, "", str(e)

def main():
    print("\n" + "="*70)
    print("🧪 VALIDAÇÃO PRÉ-ALTERAÇÃO")
    print("="*70)
    print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Step 1: Verificar se pytest existe
    print("📦 Verificando dependências...")
    success, _, _ = run_command("python3 -m pytest --version")
    if not success:
        print("❌ pytest não instalado!")
        print("   pip3 install pytest pytest-cov pytest-flask pytest-mock")
        return False
    print("   ✅ pytest encontrado")
    print()
    
    # Step 2: Rodar testes
    print("🧪 Executando testa...")
    print()
    
    success, stdout, stderr = run_command(
        "python3 -m pytest tests/ -q --tb=short",
        verbose=False
    )
    
    # Parse output
    lines = stdout.split('\n') if stdout else []
    for line in lines:
        if 'passed' in line or 'failed' in line or 'error' in line:
            print(f"   {line}")
    
    print()
    
    if success:
        print("="*70)
        print("✅ VALIDAÇÃO PASSOU - SEGURO PARA FAZER MUDANÇAS")
        print("="*70)
        print()
        print("   Próximas passos:")
        print("   1. Faça suas alterações")
        print("   2. Rode testes novamente: ./auto-test.py")
        print("   3. Se passar: pode commitar com confiança!")
        print()
        return True
    else:
        print("="*70)
        print("❌ VALIDAÇÃO FALHOU - PARE AQUI!")
        print("="*70)
        print()
        print("   Testes falharam. Não faça mudanças ainda.")
        print()
        print("   Opções:")
        print("   1. Revert do código (git checkout)")
        print("   2. Conserte os testes/ código")
        print("   3. Rode novamente: ./auto-test.py")
        print()
        
        if stdout:
            print("   DETALHES:")
            print(stdout)
        if stderr:
            print("   ERROS:")
            print(stderr)
        
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
