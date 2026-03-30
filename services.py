"""
Serviços e lógica de negócio
"""
from database import db, TransacaoModel, SaldoModel, ContaModel, CategoriaModel, SubcategoriaModel
from datetime import datetime, date
from calendar import monthrange

class SaldoService:
    """Serviço para cálculo e gerenciamento de saldos"""
    
    @staticmethod
    def calcular_saldo_automatico(conta_id: str, data_referencia: date = None) -> float:
        """
        Calcula saldo automático baseado nas transações
        
        Saldo Automático = Saldo Manual Inicial + Transações PAGAS/RECEBIDAS
        """
        if data_referencia is None:
            data_referencia = date.today()
        
        # Pega o saldo manual mais recente
        saldo_manual = SaldoModel.query.filter_by(
            conta_id=conta_id,
            tipo='MANUAL',
        ).order_by(SaldoModel.data_referencia.desc()).first()
        
        saldo_inicial = saldo_manual.valor if saldo_manual else 0.0
        
        # Calcula transações efetivadas até essa data
        transacoes = TransacaoModel.query.filter(
            TransacaoModel.conta_id == conta_id,
            TransacaoModel.data_transacao <= data_referencia,
            TransacaoModel.status.in_(['PAGO', 'RECEBIDO'])
        ).all()
        
        total_credito = sum(t.valor for t in transacoes if t.tipo_transacao == 'CREDITO')
        total_debito = sum(t.valor for t in transacoes if t.tipo_transacao == 'DEBITO')
        
        saldo_automatico = saldo_inicial + total_credito - total_debito
        
        return round(saldo_automatico, 2)
    
    @staticmethod
    def atualizar_saldo_manual(conta_id: str, novo_saldo: float, data_referencia: date = None):
        """Atualiza o saldo manual de uma conta"""
        if data_referencia is None:
            data_referencia = date.today()
        
        saldo = SaldoModel(
            conta_id=conta_id,
            tipo='MANUAL',
            valor=novo_saldo,
            data_referencia=data_referencia
        )
        db.session.add(saldo)
        db.session.commit()
        return saldo
    
    @staticmethod
    def salvar_saldo_automatico(conta_id: str, data_referencia: date = None):
        """Salva o saldo automático calculado"""
        if data_referencia is None:
            data_referencia = date.today()
        
        valor_automatico = SaldoService.calcular_saldo_automatico(conta_id, data_referencia)
        
        saldo = SaldoModel(
            conta_id=conta_id,
            tipo='AUTOMATICO',
            valor=valor_automatico,
            data_referencia=data_referencia
        )
        db.session.add(saldo)
        db.session.commit()
        return saldo

class TransacaoService:
    """Serviço para gerenciar transações"""
    
    @staticmethod
    def criar_transacao(dados: dict) -> TransacaoModel:
        """Cria uma nova transação"""
        transacao = TransacaoModel(
            data_transacao=datetime.strptime(dados['data_transacao'], '%Y-%m-%d').date(),
            data_vencimento=datetime.strptime(dados['data_vencimento'], '%Y-%m-%d').date() if dados.get('data_vencimento') else None,
            mes_pagto=dados.get('mes_pagto'),
            tipo_transacao=dados['tipo_transacao'],
            tipo_conta=dados['tipo_conta'],
            conta_id=dados['conta_id'],
            valor=float(dados['valor']),
            parcela=dados.get('parcela', 'ROT'),
            estabelecimento=dados.get('estabelecimento'),
            status=dados.get('status', 'PREVISTO'),
            categoria=dados.get('categoria'),
            subcategoria=dados.get('subcategoria'),
            tipo_fixo_variavel=dados.get('tipo_fixo_variavel', 'VARIAVEL'),
            descricao=dados.get('descricao', '')
        )
        db.session.add(transacao)
        db.session.commit()
        return transacao
    
    @staticmethod
    def atualizar_status_transacao(transacao_id: str, novo_status: str) -> TransacaoModel:
        """Atualiza o status de uma transação"""
        transacao = TransacaoModel.query.get(transacao_id)
        if transacao:
            transacao.status = novo_status
            transacao.data_atualizacao = datetime.now()
            db.session.commit()
        return transacao
    
    @staticmethod
    def listar_transacoes_pendentes(conta_id: str = None) -> list:
        """Lista todas as transações pendentes"""
        query = TransacaoModel.query.filter(
            TransacaoModel.status.in_(['PREVISTO', 'AGENDADO', 'REC_PENDENTE'])
        )
        if conta_id:
            query = query.filter_by(conta_id=conta_id)
        return query.all()

class CicloService:
    """Serviço para gerenciar ciclos financeiros"""
    
    @staticmethod
    def calcular_datas_ciclo(mes: int, ano: int) -> tuple:
        """
        Calcula data de início e fim do ciclo
        Ciclo começa no penúltimo dia do mês anterior
        """
        # Data do penúltimo dia do mês anterior
        if mes == 1:
            mes_anterior = 12
            ano_anterior = ano - 1
        else:
            mes_anterior = mes - 1
            ano_anterior = ano
        
        # Penúltimo dia do mês anterior
        _, dias_mes = monthrange(ano_anterior, mes_anterior)
        data_inicio = date(ano_anterior, mes_anterior, dias_mes - 1)
        
        # Último dia do mês atual
        _, dias_mes_atual = monthrange(ano, mes)
        data_fim = date(ano, mes, dias_mes_atual)
        
        return data_inicio, data_fim
    
    @staticmethod
    def calcular_totais_ciclo(data_inicio: date, data_fim: date, conta_id: str = None) -> dict:
        """Calcula totais de receita, despesa e saldo previsto para um ciclo"""
        query = TransacaoModel.query.filter(
            TransacaoModel.data_transacao >= data_inicio,
            TransacaoModel.data_transacao <= data_fim,
            TransacaoModel.status.in_(['PAGO', 'RECEBIDO', 'PREVISTO', 'AGENDADO', 'REC_PENDENTE'])
        )
        
        if conta_id:
            query = query.filter_by(conta_id=conta_id)
        
        transacoes = query.all()
        
        total_receita = sum(t.valor for t in transacoes if t.tipo_transacao == 'CREDITO')
        total_despesa = sum(t.valor for t in transacoes if t.tipo_transacao == 'DEBITO')
        
        return {
            'total_receita': round(total_receita, 2),
            'total_despesa': round(total_despesa, 2),
            'saldo': round(total_receita - total_despesa, 2),
            'transacoes_count': len(transacoes)
        }

class DashboardService:
    """Serviço para gerar dados para o dashboard"""
    
    @staticmethod
    def gerar_resumo_geral() -> dict:
        """Gera resumo geral financeiro"""
        contas = ContaModel.query.filter_by(ativo=True).all()
        
        resumo = {
            'total_saldo_manual': 0.0,
            'total_saldo_automatico': 0.0,
            'contas': [],
            'data_atualizacao': datetime.now().isoformat()
        }
        
        for conta in contas:
            # Saldo manual
            saldo_manual = SaldoModel.query.filter_by(
                conta_id=conta.id,
                tipo='MANUAL'
            ).order_by(SaldoModel.data_referencia.desc()).first()
            
            # Saldo automático
            saldo_automatico = SaldoService.calcular_saldo_automatico(conta.id)
            
            conta_info = {
                'id': conta.id,
                'bandeira': conta.bandeira,
                'tipo': conta.tipo,
                'saldo_manual': saldo_manual.valor if saldo_manual else 0.0,
                'saldo_automatico': saldo_automatico
            }
            
            resumo['contas'].append(conta_info)
            resumo['total_saldo_manual'] += conta_info['saldo_manual']
            resumo['total_saldo_automatico'] += saldo_automatico
        
        return resumo
    
    @staticmethod
    def gerar_dados_grafico_por_categoria() -> dict:
        """Gera dados para gráfico de despesas por categoria"""
        transacoes = TransacaoModel.query.filter(
            TransacaoModel.status.in_(['PAGO', 'RECEBIDO']),
            TransacaoModel.tipo_transacao == 'DEBITO'
        ).all()
        
        dados = {}
        for t in transacoes:
            categoria = t.categoria or 'Sem Categoria'
            if categoria not in dados:
                dados[categoria] = 0.0
            dados[categoria] += t.valor
        
        return dados
    
    @staticmethod
    def gerar_dados_grafico_por_conta() -> dict:
        """Gera dados para gráfico de saldos por conta"""
        contas = ContaModel.query.filter_by(ativo=True).all()
        
        dados = {}
        for conta in contas:
            saldo = SaldoService.calcular_saldo_automatico(conta.id)
            dados[conta.bandeira] = saldo
        
        return dados
