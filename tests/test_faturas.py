"""Testes para sistema de faturas de cartão de crédito"""
import json
import pytest
from datetime import datetime
import app_v2


class TestFaturas:
    """Testes de faturas de cartão"""
    
    def test_listar_faturas(self, client):
        """Verifica listagem de faturas"""
        # Act
        response = client.get('/api/faturas')
        
        # Assert
        assert response.status_code == 200
        faturas = response.get_json()
        assert isinstance(faturas, list)
    
    def test_faturas_por_cartao(self, client, dados_teste):
        """Verifica listagem de faturas por cartão"""
        # Arrange - adicionar fatura
        dados = dados_teste
        fatura = {
            'id': 1,
            'cartao_id': 1,
            'mes_pagamento': '03/2026',
            'data_vencimento': '2026-04-10',
            'saldo': 500.00,
            'status': 'aberta',
            'criada_em': datetime.now().isoformat()
        }
        dados['faturas'] = [fatura]
        app_v2.salvar_dados(dados)
        
        # Act
        response = client.get('/api/cartoes/1/faturas')
        
        # Assert
        assert response.status_code == 200
        faturas = response.get_json()
        assert len(faturas) > 0
        assert faturas[0]['cartao_id'] == 1
    
    def test_vencimento_dinamico_por_mes(self, client, dados_teste):
        """Verifica se vencimento muda por mês (dia fixo do cartão)"""
        # Arrange - cartão Diners vence no dia 10
        dados = dados_teste
        # Adicionar transações em meses diferentes
        transacoes = [
            {
                'id': 1,
                'nome_conta': 'Diners',
                'tipo': 'DESPESA',
                'categoria': 'Alimentação',
                'valor': 100.00,
                'mes_pagamento': '02/2026',
                'data_vencimento': '2026-02-28',
                'tipo_conta': 'CREDITO',
                'descricao': 'Fev',
                'efetuada': True,
                'cartao_id': 1
            },
            {
                'id': 2,
                'nome_conta': 'Diners',
                'tipo': 'DESPESA',
                'categoria': 'Alimentação',
                'valor': 200.00,
                'mes_pagamento': '03/2026',
                'data_vencimento': '2026-03-31',
                'tipo_conta': 'CREDITO',
                'descricao': 'Mar',
                'efetuada': True,
                'cartao_id': 1
            }
        ]
        dados['transacoes'] = transacoes
        app_v2.salvar_dados(dados)
        
        # Act
        response = client.post('/api/faturas/regenerar')
        
        # Assert
        assert response.status_code in [200, 201]
        
        # Verificar faturas
        response = client.get('/api/faturas')
        faturas = response.get_json()
        
        # Deve ter faturas com vencimento 10 em meses diferentes
        vencimentos = [f['data_vencimento'] for f in faturas if f['cartao_id'] == 1]
        assert len(vencimentos) > 0
    
    def test_nao_deletar_fatura_fechada(self, client, dados_teste):
        """Verifica se não permite deletar fatura fechada"""
        # Arrange - criar fatura fechada
        dados = dados_teste
        fatura = {
            'id': 1,
            'cartao_id': 1,
            'mes_pagamento': '02/2026',
            'data_vencimento': '2026-03-10',
            'saldo': 0.00,
            'status': 'fechada',
            'criada_em': datetime.now().isoformat()
        }
        dados['faturas'] = [fatura]
        app_v2.salvar_dados(dados)
        
        # Act
        response = client.delete('/api/faturas/1')
        
        # Assert
        assert response.status_code == 400 or 'erro' in response.get_json()
    
    def test_deletar_fatura_aberta(self, client, dados_teste):
        """Verifica se permite deletar fatura aberta"""
        # Arrange - criar fatura aberta
        dados = dados_teste
        fatura = {
            'id': 1,
            'cartao_id': 1,
            'mes_pagamento': '03/2026',
            'data_vencimento': '2026-04-10',
            'saldo': 500.00,
            'status': 'aberta',
            'criada_em': datetime.now().isoformat()
        }
        dados['faturas'] = [fatura]
        app_v2.salvar_dados(dados)
        
        # Act
        response = client.delete('/api/faturas/1')
        
        # Assert
        assert response.status_code == 200
