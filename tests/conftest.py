"""Configuração dos testes - fixture e setup"""
import pytest
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Adicionar o diretório pai ao PATH para importar app_v2
sys.path.insert(0, str(Path(__file__).parent.parent))

import app_v2


@pytest.fixture
def app():
    """Cria aplicação Flask para testes"""
    app_v2.app.config['TESTING'] = True
    return app_v2.app


@pytest.fixture
def client(app):
    """Cria client para testar endpoints"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Cria runner para comandos CLI"""
    return app.test_cli_runner()


@pytest.fixture(autouse=True)
def setup_test_db(tmp_path, monkeypatch):
    """
    Setup: cria DB de teste antes de cada teste
    Cleanup: remove DB de teste após cada teste
    """
    # Usar arquivo temporário para testes
    test_db_file = tmp_path / "test_dados.json"
    test_backup_dir = tmp_path / "test_backups"
    test_backup_dir.mkdir(exist_ok=True)
    
    # Monkeypatch para usar arquivo de teste
    monkeypatch.setattr(app_v2, 'DADOS_FILE', str(test_db_file))
    monkeypatch.setattr(app_v2, 'BACKUP_DIR', str(test_backup_dir))
    
    # Criar dados padrão de teste
    dados_padrao = {
        'contas': [
            {
                'id': 1,
                'bandeira': 'Bradesco',
                'tipo': 'CORRENTE',
                'saldo_manual': 1000.00,
                'criada_em': datetime.now().isoformat()
            },
            {
                'id': 2,
                'bandeira': 'Carteira',
                'tipo': 'CORRENTE',
                'saldo_manual': 500.00,
                'criada_em': datetime.now().isoformat()
            }
        ],
        'transacoes': [],
        'cartoes': [
            {
                'id': 1,
                'bandeira': 'Diners',
                'dia_vencimento': 10,
                'status': 'ATIVO',
                'criado_em': datetime.now().isoformat()
            }
        ],
        'faturas': [],
        'categorias': [
            {
                'id': 1,
                'nome': 'Alimentação',
                'tipo': 'DESPESA',
                'subcategorias': ['Restaurante', 'Supermercado']
            },
            {
                'id': 2,
                'nome': 'Salário',
                'tipo': 'RECEITA',
                'subcategorias': []
            }
        ]
    }
    
    # Salvar dados padrão
    with open(test_db_file, 'w') as f:
        json.dump(dados_padrao, f)
    
    yield test_db_file
    
    # Cleanup automático (tmp_path é removido automaticamente)


@pytest.fixture
def dados_teste(setup_test_db):
    """Carrega dados de teste"""
    return app_v2.carregar_dados()


@pytest.fixture
def backup_dir_teste(tmp_path, monkeypatch):
    """Setup do diretório de backups para testes - usa o mesmo da setup_test_db"""
    # Este fixture garante que BACKUP_DIR seja monkeypatchado
    # Usa um diretório específico no tmp_path
    backup_dir = tmp_path / "backups"
    backup_dir.mkdir()
    monkeypatch.setattr(app_v2, 'BACKUP_DIR', str(backup_dir))
    return backup_dir
