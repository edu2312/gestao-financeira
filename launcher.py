#!/usr/bin/env python3
"""
Launcher para a Aplicação de Gestão Financeira
Inicia o servidor Flask e abre o navegador automaticamente
"""

import os
import sys
import time
import webbrowser
import subprocess
import threading
from pathlib import Path

def get_app_path():
    """Obtém o diretório da aplicação"""
    if getattr(sys, 'frozen', False):
        # Executando como executável
        return Path(sys.executable).parent
    else:
        # Executando como script Python
        return Path(__file__).parent

def start_server():
    """Inicia o servidor Flask"""
    app_path = get_app_path()
    os.chdir(app_path)
    
    # Importar Flask após mudar diretório
    sys.path.insert(0, str(app_path))
    from app_v2 import app
    
    print("🚀 Iniciando servidor...")
    app.run(host='127.0.0.1', port=3333, debug=False, use_reloader=False)

def open_browser():
    """Abre o navegador após aguardar o servidor iniciar"""
    time.sleep(2)  # Aguardar servidor iniciar
    
    print("🌐 Abrindo navegador...")
    webbrowser.open('http://127.0.0.1:3333')

def main():
    """Função principal"""
    print("=" * 60)
    print("  💰 Aplicação de Gestão Financeira")
    print("=" * 60)
    print()
    print("📍 Iniciando aplicação...")
    print("   Servidor: http://127.0.0.1:3333")
    print()
    print("⏳ Por favor, aguarde enquanto o aplicativo inicia...")
    print()
    
    # Iniciar servidor em thread separada
    server_thread = threading.Thread(target=start_server, daemon=False)
    server_thread.start()
    
    # Abrir navegador em thread separada
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Manter a aplicação rodando
    server_thread.join()

if __name__ == '__main__':
    main()
