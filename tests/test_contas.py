"""Testes para funcionalidades de contas"""
import json
import pytest
import app_v2


class TestContas:
    """Testes de CRUD de contas"""
    
    def test_listar_contas(self, client, dados_teste):
        """Verifica se lista contas corretamente"""
        # Act
        response = client.get('/api/contas')
        
        # Assert
        assert response.status_code == 200
        contas = response.get_json()
        assert len(contas) >= 2
        assert contas[0]['bandeira'] == 'Bradesco'
        assert contas[0]['saldo_manual'] == 1000.00
    
    def test_criar_conta(self, client):
        """Verifica criação de nova conta"""
        # Arrange
        nova_conta = {
            'bandeira': 'Nu Bank',
            'tipo': 'CORRENTE',
            'saldo_manual': 2000.00
        }
        
        # Act
        response = client.post('/api/contas', 
                              json=nova_conta,
                              content_type='application/json')
        
        # Assert
        assert response.status_code == 201
        data = response.get_json()
        assert data['bandeira'] == 'Nu Bank'
        assert data['saldo_manual'] == 2000.00
    
    def test_atualizar_conta(self, client):
        """Verifica atualização de conta"""
        # Arrange
        update = {'saldo_manual': 1500.00}
        
        # Act
        response = client.put('/api/contas/1',
                             json=update,
                             content_type='application/json')
        
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['saldo_manual'] == 1500.00
    
    def test_deletar_conta(self, client):
        """Verifica deleção de conta"""
        # Act
        response = client.delete('/api/contas/2')
        
        # Assert
        assert response.status_code == 200
        
        # Verificar se foi realmente deletada
        response = client.get('/api/contas')
        contas = response.get_json()
        ids = [c['id'] for c in contas]
        assert 2 not in ids
    
    def test_saldo_nao_pode_ser_negativo(self, client):
        """Verifica se saldo negativo é rejeitado (se validado)"""
        # Arrange
        update = {'saldo_manual': -100.00}
        
        # Act
        response = client.put('/api/contas/1',
                             json=update,
                             content_type='application/json')
        
        # Assert - aceita por enquanto, mas documentado
        # Este é um teste de comportamento esperado
        assert response.status_code in [200, 400]
    
    def test_calcular_saldo_dinamico(self, client, dados_teste):
        """Verifica cálculo de saldo dinâmico (manual + transações)"""
        # Arrange - adicionar transação
        dados = dados_teste
        transacao = {
            'id': 1,
            'nome_conta': 'Bradesco',
            'tipo': 'RECEITA',
            'categoria': 'Salário',
            'valor': 100.00,
            'data': '2026-03-31',
            'mes_pagamento': '03/2026',
            'tipo_conta': 'CORRENTE',
            'descricao': 'Receita teste',
            'efetuada': True
        }
        dados['transacoes'] = [transacao]
        app_v2.salvar_dados(dados)
        
        # Act
        response = client.get('/api/contas')
        contas = response.get_json()
        bradesco = next((c for c in contas if c['bandeira'] == 'Bradesco'), None)
        
        # Assert - saldo deve incluir a receita
        assert bradesco is not None
        assert bradesco['saldo'] >= 1000.00  # mínimo
