"""
Configuração do banco de dados e modelos SQLAlchemy
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class ContaModel(db.Model):
    """Modelo de Conta para banco de dados"""
    __tablename__ = 'contas'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    bandeira = db.Column(db.String(100), nullable=False)  # "Bradesco", "Nubank", etc
    tipo = db.Column(db.String(20), nullable=False)  # "CORRENTE" ou "CARTAO"
    saldo_manual = db.Column(db.Float, default=0.0)
    data_atualizacao = db.Column(db.DateTime, default=datetime.now)
    ativo = db.Column(db.Boolean, default=True)
    
    # Relacionamentos
    saldos = db.relationship('SaldoModel', backref='conta', lazy=True, cascade='all, delete-orphan')
    transacoes = db.relationship('TransacaoModel', backref='conta', lazy=True)
    
    def __repr__(self):
        return f'<Conta {self.bandeira}>'

class CategoriaModel(db.Model):
    """Modelo de Categoria"""
    __tablename__ = 'categorias'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.Text)
    ordem = db.Column(db.Integer, default=0)
    
    # Relacionamentos
    subcategorias = db.relationship('SubcategoriaModel', backref='categoria', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Categoria {self.nome}>'

class SubcategoriaModel(db.Model):
    """Modelo de Subcategoria"""
    __tablename__ = 'subcategorias'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = db.Column(db.String(100), nullable=False)
    categoria_id = db.Column(db.String(36), db.ForeignKey('categorias.id'), nullable=False)
    ordem = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Subcategoria {self.nome}>'

class TransacaoModel(db.Model):
    """Modelo de Transação"""
    __tablename__ = 'transacoes'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Datas
    data_transacao = db.Column(db.Date, nullable=False)
    data_vencimento = db.Column(db.Date)
    mes_pagto = db.Column(db.String(7))  # "2026-03"
    
    # Tipos
    tipo_transacao = db.Column(db.String(20), nullable=False)  # CREDITO, DEBITO
    tipo_conta = db.Column(db.String(20), nullable=False)  # CORRENTE, CARTAO
    tipo_fixo_variavel = db.Column(db.String(20))  # FIXO, VARIAVEL
    
    # Conta
    conta_id = db.Column(db.String(36), db.ForeignKey('contas.id'), nullable=False)
    
    # Valor e parcela
    valor = db.Column(db.Float, nullable=False)
    parcela = db.Column(db.String(20))  # "ROT", "1/2", "3/10"
    
    # Estabelecimento
    estabelecimento = db.Column(db.String(200))
    
    # Status
    status = db.Column(db.String(30), nullable=False)  # PREVISTO, AGENDADO, PAGO, REC_PENDENTE, RECEBIDO
    
    # Categoria
    categoria = db.Column(db.String(100))
    subcategoria = db.Column(db.String(100))
    
    # Descrição
    descricao = db.Column(db.Text)
    
    # Meta
    data_criacao = db.Column(db.DateTime, default=datetime.now)
    data_atualizacao = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'<Transacao {self.data_transacao} - R${self.valor}>'

class SaldoModel(db.Model):
    """Modelo de Saldo (Manual ou Automático)"""
    __tablename__ = 'saldos'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conta_id = db.Column(db.String(36), db.ForeignKey('contas.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # MANUAL, AUTOMATICO
    valor = db.Column(db.Float, nullable=False)
    data_referencia = db.Column(db.Date, nullable=False)  # Data a qual se refere
    data_atualizacao = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<Saldo {self.tipo} - R${self.valor}>'

class CicloModel(db.Model):
    """Modelo de Ciclo Financeiro"""
    __tablename__ = 'ciclos'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    mes = db.Column(db.Integer, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    saldo_inicial = db.Column(db.Float, default=0.0)
    total_receita_prevista = db.Column(db.Float, default=0.0)
    total_despesa_prevista = db.Column(db.Float, default=0.0)
    saldo_previsto = db.Column(db.Float, default=0.0)
    
    db.UniqueConstraint('mes', 'ano', name='uq_ciclo_mes_ano')
    
    def __repr__(self):
        return f'<Ciclo {self.mes}/{self.ano}>'

class UsuarioModel(db.Model):
    """Modelo de Usuário (para futuro compartilhamento)"""
    __tablename__ = 'usuarios'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    senha_hash = db.Column(db.String(255))  # Para futuro
    data_criacao = db.Column(db.DateTime, default=datetime.now)
    ativo = db.Column(db.Boolean, default=True)
