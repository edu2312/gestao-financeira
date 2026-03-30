"""
Modelos de dados para sistema financeiro
"""
from datetime import datetime
from enum import Enum

class TipoTransacao(Enum):
    """Tipo de transação: crédito ou débito"""
    CREDITO = "CREDITO"
    DEBITO = "DEBITO"

class TipoConta(Enum):
    """Tipo de conta: corrente ou cartão"""
    CORRENTE = "CORRENTE"
    CARTAO = "CARTAO"

class StatusTransacao(Enum):
    """Status das transações"""
    PREVISTO = "PREVISTO"
    AGENDADO = "AGENDADO"
    PAGO = "PAGO"
    REC_PENDENTE = "REC_PENDENTE"
    RECEBIDO = "RECEBIDO"

class TipoFixoVariavel(Enum):
    """Se é despesa/receita fixa ou variável"""
    FIXO = "FIXO"
    VARIAVEL = "VARIAVEL"

class Categoria:
    """Representa uma categoria com subcategorias"""
    def __init__(self, nome: str, subcategorias: list = None):
        self.nome = nome
        self.subcategorias = subcategorias or []
    
    def adicionar_subcategoria(self, subcat: str):
        if subcat not in self.subcategorias:
            self.subcategorias.append(subcat)

class Conta:
    """Representa uma conta corrente ou cartão de crédito"""
    def __init__(self, id: str, bandeira: str, tipo: TipoConta, saldo_manual: float = 0):
        self.id = id
        self.bandeira = bandeira  # Ex: "Bradesco", "Nubank", "Visa"
        self.tipo = tipo
        self.saldo_manual = saldo_manual
        self.data_atualizacao = datetime.now()

class Transacao:
    """Representa uma transação financeira"""
    def __init__(self):
        self.data_transacao = None          # Quando foi efetivada
        self.data_vencimento = None         # Quando vence/paga
        self.mes_pagto = None               # Mês de pagamento
        self.tipo_transacao = None          # CREDITO ou DEBITO
        self.tipo_conta = None              # CORRENTE ou CARTAO
        self.bandeira = None                # Nome da conta/cartão
        self.valor = 0.0
        self.parcela = None                 # "ROT", "1/2", "3/10"
        self.estabelecimento = None         # Onde foi gasto
        self.status = None                  # PREVISTO, AGENDADO, PAGO, etc
        self.categoria = None
        self.subcategoria = None
        self.tipo_fixo_variavel = None      # FIXO ou VARIAVEL
        self.descricao = ""
        self.id = None                      # UUID
        self.data_criacao = datetime.now()

class Saldo:
    """Representa o saldo de uma conta"""
    def __init__(self, conta_id: str, tipo: str):
        self.conta_id = conta_id
        self.tipo = tipo  # "MANUAL" ou "AUTOMATICO"
        self.saldo = 0.0
        self.saldo_anterior = 0.0
        self.data_atualizacao = datetime.now()
        self.historico = []  # Lista de mudanças de saldo

class Ciclo:
    """Representa um ciclo financeiro (começa no penúltimo dia do mês)"""
    def __init__(self, mes: int, ano: int):
        self.mes = mes
        self.ano = ano
        self.data_inicio = None
        self.data_fim = None
        self.total_receita_prevista = 0.0
        self.total_despesa_prevista = 0.0
        self.saldo_previsto = 0.0
