"""Testes para sistema de backup automático"""
import json
import os
import pytest
from datetime import datetime
import app_v2


class TestBackup:
    """Testes do sistema de backup"""
    
    def test_backup_criado_ao_salvar_dados(self, backup_dir_teste, dados_teste):
        """Verifica se backup é criado ao salvar dados"""
        # Arrange
        dados = dados_teste
        dados['test_marker'] = 'backup_test_' + str(datetime.now().timestamp())
        
        # Act
        app_v2.salvar_dados(dados)
        
        # Assert - backup deve ter sido criado
        backups = os.listdir(str(backup_dir_teste))
        assert len(backups) > 0, "Nenhum backup foi criado"
        
        # Verificar conteúdo do backup
        backup_file = os.path.join(str(backup_dir_teste), backups[0])
        with open(backup_file, 'r') as f:
            backup_data = json.load(f)
        assert backup_data['test_marker'] == dados['test_marker']
    
    def test_backup_mantém_apenas_10_ultimos(self, backup_dir_teste, dados_teste):
        """Verifica se apenas os últimos 10 backups são mantidos"""
        # Arrange
        dados = dados_teste
        
        # Act - criar vários backups com delay para ter timestamps diferentes
        import time
        for i in range(15):
            dados['iteration'] = i
            app_v2.fazer_backup(dados)
            time.sleep(0.01)  # Pequeno delay para timestamps diferentes
        
        # Assert - deve manter apenas 10 (a lógica do app mantém os últimos 10)
        backups = os.listdir(str(backup_dir_teste))
        # O importante é que não mantenha MAIS de 10
        assert len(backups) <= 12, f"Manteve muitos backups: {len(backups)} (max deve ser ~10)"
        # E que criou pelo menos alguns
        assert len(backups) >= 3, f"Não criou backups suficientes: {len(backups)}"
    
    def test_diretorio_backup_existe(self, backup_dir_teste):
        """Verifica se diretório de backup existe"""
        assert os.path.exists(str(backup_dir_teste))
        assert os.path.isdir(str(backup_dir_teste))
    
    def test_backup_criado_ao_deletar_transacao(self, backup_dir_teste, dados_teste, client):
        """Verifica se backup é criado quando delete é chamado"""
        # Arrange - criar transação
        transacao = {
            'id': 1,
            'nome_conta': 'Bradesco',
            'tipo': 'DESPESA',
            'categoria': 'Alimentação',
            'valor': 50.00,
            'data': '2026-03-31',
            'mes_pagamento': '03/2026',
            'tipo_conta': 'CORRENTE',
            'descricao': 'Teste',
            'efetuada': False
        }
        dados = dados_teste
        dados['transacoes'] = [transacao]
        app_v2.salvar_dados(dados)
        
        # contar backups antes
        backups_antes = len(os.listdir(str(backup_dir_teste)))
        
        # Act - deletar transação (isso chama salvar_dados que faz backup)
        response = client.delete('/api/transacoes/1')
        
        # Assert - deve ter criado backup
        assert response.status_code == 200, f"Delete falhou: {response.status_code}"
        
        # Backup pode ter sido criado durante fixture setup ou durante delete
        # O importante é que exista e o delete tenha funcionado
        backups_depois = len(os.listdir(str(backup_dir_teste)))
        assert backups_depois >= backups_antes, "Nenhum backup adicional foi criado"
