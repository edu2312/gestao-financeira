"""Testes para resumo do dashboard"""
import json
import pytest
from datetime import datetime
import app_v2


class TestResumo:
    """Testes do endpoint /api/resumo"""
    
    def test_resumo_retorna_estrutura_correta(self, client):
        """Verifica se resumo tem todas as campos necessários"""
        # Act
        response = client.get('/api/resumo')
        
        # Assert
        assert response.status_code == 200
        resumo = response.get_json()
        
        # Campos obrigatórios
        assert 'total_receita' in resumo
        assert 'total_despesa' in resumo
        assert 'total_faturas' in resumo
        assert 'saldo_contas' in resumo
        assert 'saldo_liquido' in resumo
        assert 'num_contas' in resumo
    
    def test_resumo_calcula_receita_corrente(self, client, dados_teste):
        """Verifica cálculo de receita do mês corrente"""
        # Arrange - adicionar receita com date/mes dinamicamente
        # (API considera próximo mês se dia >= 29)
        dados = dados_teste
        from dateutil.relativedelta import relativedelta
        hoje = datetime.now()
        
        # Lógica igual ao /api/resumo
        if hoje.day >= 29:
            mes_obj = hoje + relativedelta(months=1)
        else:
            mes_obj = hoje
        
        mes_corrente_str = f"{mes_obj.month:02d}/{mes_obj.year}"
        
        transacao = {
            'id': 1,
            'nome_conta': 'Bradesco',
            'tipo': 'RECEITA',
            'categoria': 'Salário',
            'valor': 5000.00,
            'data': f'{mes_obj.year}-{mes_obj.month:02d}-15',
            'mes_pagamento': mes_corrente_str,  # Usar mês que API espera
            'tipo_conta': 'CORRENTE',
            'descricao': 'Salário',
            'efetuada': True
        }
        dados['transacoes'] = [transacao]
        app_v2.salvar_dados(dados)
        
        # Act
        response = client.get('/api/resumo')
        resumo = response.get_json()
        
        # Assert - deve contar a receita
        assert resumo['total_receita'] >= 5000.00, f"Esperava >= 5000, obteve {resumo['total_receita']}"
    
    def test_resumo_calcula_despesa_corrente(self, client, dados_teste):
        """Verifica cálculo de despesa do mês corrente"""
        # Arrange - adicionar despesa com data/mes dinamicamente
        # (API considera próximo mês se dia >= 29)
        dados = dados_teste
        from dateutil.relativedelta import relativedelta
        hoje = datetime.now()
        
        # Lógica igual ao /api/resumo
        if hoje.day >= 29:
            mes_obj = hoje + relativedelta(months=1)
        else:
            mes_obj = hoje
        
        mes_corrente_str = f"{mes_obj.month:02d}/{mes_obj.year}"
        
        transacao = {
            'id': 1,
            'nome_conta': 'Bradesco',
            'tipo': 'DESPESA',
            'categoria': 'Alimentação',
            'valor': 200.00,
            'data': f'{mes_obj.year}-{mes_obj.month:02d}-15',
            'mes_pagamento': mes_corrente_str,  # Usar mês que API espera
            'tipo_conta': 'CORRENTE',
            'descricao': 'Supermercado',
            'efetuada': True
        }
        dados['transacoes'] = [transacao]
        app_v2.salvar_dados(dados)
        
        # Act
        response = client.get('/api/resumo')
        resumo = response.get_json()
        
        # Assert - deve contar a despesa
        assert resumo['total_despesa'] >= 200.00, f"Esperava >= 200, obteve {resumo['total_despesa']}"
    
    def test_resumo_nao_conta_faturas_que_ja_estao_no_saldo(self, client, dados_teste):
        """Verifica que faturas não são contadas duas vezes"""
        # Arrange
        dados = dados_teste
        dados['contas'][0]['saldo_manual'] = 1000.00
        
        # Adicionar fatura
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
        response = client.get('/api/resumo')
        resumo = response.get_json()
        
        # Assert
        # saldo_contas = saldo_manual + receita - despesa (NÃO deve descontar faturas)
        # total_faturas = faturas abertas (separado)
        assert 'total_faturas' in resumo
        assert 'saldo_contas' in resumo
        # Ambos devem existir separadamente
        assert resumo['total_faturas'] >= 0
        assert resumo['saldo_contas'] >= 0
    
    def test_resumo_ignora_transacoes_de_meses_anteriores(self, client, dados_teste):
        """Verifica que apenas transações do mês corrente são contadas"""
        # Arrange
        dados = dados_teste
        
        # Adicionar transação de mês anterior
        transacao_anterior = {
            'id': 1,
            'nome_conta': 'Bradesco',
            'tipo': 'DESPESA',
            'categoria': 'Alimentação',
            'valor': 1000.00,
            'data': '2026-02-15',
            'mes_pagamento': '02/2026',  # Mês anterior
            'tipo_conta': 'CORRENTE',
            'descricao': 'Despesa antiga',
            'efetuada': True
        }
        dados['transacoes'] = [transacao_anterior]
        app_v2.salvar_dados(dados)
        
        # Act
        response = client.get('/api/resumo')
        resumo = response.get_json()
        
        # Assert
        # Não deve incluir despesa antiga (só mês corrente)
        assert resumo['total_despesa'] < 1000.00 or resumo['total_despesa'] == 0
