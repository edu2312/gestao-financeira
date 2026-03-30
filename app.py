"""
Aplicação Principal - Flask
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from database import db, ContaModel, TransacaoModel, SaldoModel, CategoriaModel
from services import SaldoService, TransacaoService, DashboardService, CicloService
from datetime import datetime, date
import os

# Criar app Flask
app = Flask(__name__)

# Configuração
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/financas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# Inicializar extensões
db.init_app(app)
CORS(app)

# Criar tabelas
with app.app_context():
    db.create_all()
    print("✅ Banco de dados inicializado")

# =============== ROTAS ===============

@app.route('/')
def index():
    """Página principal - Dashboard"""
    return render_template('dashboard.html')

# =============== API - DASHBOARD ===============

@app.route('/api/dashboard/resumo', methods=['GET'])
def api_dashboard_resumo():
    """Retorna resumo geral do dashboard"""
    try:
        resumo = DashboardService.gerar_resumo_geral()
        return jsonify(resumo), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/dashboard/categorias', methods=['GET'])
def api_dashboard_categorias():
    """Retorna dados de despesas por categoria"""
    try:
        dados = DashboardService.gerar_dados_grafico_por_categoria()
        return jsonify(dados), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/dashboard/contas', methods=['GET'])
def api_dashboard_contas():
    """Retorna saldos por conta"""
    try:
        dados = DashboardService.gerar_dados_grafico_por_conta()
        return jsonify(dados), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# =============== API - CONTAS ===============

@app.route('/api/contas', methods=['GET'])
def api_listar_contas():
    """Lista todas as contas"""
    try:
        contas = ContaModel.query.filter_by(ativo=True).all()
        dados = []
        for conta in contas:
            saldo_manual = SaldoModel.query.filter_by(
                conta_id=conta.id, tipo='MANUAL'
            ).order_by(SaldoModel.data_referencia.desc()).first()
            
            dados.append({
                'id': conta.id,
                'bandeira': conta.bandeira,
                'tipo': conta.tipo,
                'saldo_manual': saldo_manual.valor if saldo_manual else 0.0,
                'saldo_automatico': SaldoService.calcular_saldo_automatico(conta.id),
                'data_atualizacao': conta.data_atualizacao.isoformat()
            })
        return jsonify(dados), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/contas', methods=['POST'])
def api_criar_conta():
    """Cria uma nova conta"""
    try:
        dados = request.get_json()
        conta = ContaModel(
            bandeira=dados['bandeira'],
            tipo=dados['tipo'],  # CORRENTE ou CARTAO
            saldo_manual=float(dados.get('saldo_manual', 0))
        )
        db.session.add(conta)
        db.session.commit()
        
        # Salvar saldo inicial
        if dados.get('saldo_manual'):
            SaldoService.atualizar_saldo_manual(conta.id, float(dados['saldo_manual']))
        
        return jsonify({
            'id': conta.id,
            'mensagem': 'Conta criada com sucesso'
        }), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/contas/<conta_id>/saldo-manual', methods=['PUT'])
def api_atualizar_saldo_manual(conta_id):
    """Atualiza saldo manual de uma conta"""
    try:
        dados = request.get_json()
        saldo = SaldoService.atualizar_saldo_manual(
            conta_id,
            float(dados['novo_saldo'])
        )
        return jsonify({
            'mensagem': 'Saldo atualizado',
            'saldo_manual': saldo.valor,
            'data_atualizacao': saldo.data_atualizacao.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# =============== API - TRANSAÇÕES ===============

@app.route('/api/transacoes', methods=['GET'])
def api_listar_transacoes():
    """Lista transações com filtros opcionais"""
    try:
        # Parâmetros de filtro
        conta_id = request.args.get('conta_id')
        status = request.args.get('status')
        categoria = request.args.get('categoria')
        limite = int(request.args.get('limite', 50))
        
        query = TransacaoModel.query
        
        if conta_id:
            query = query.filter_by(conta_id=conta_id)
        if status:
            query = query.filter_by(status=status)
        if categoria:
            query = query.filter_by(categoria=categoria)
        
        transacoes = query.order_by(TransacaoModel.data_transacao.desc()).limit(limite).all()
        
        dados = []
        for t in transacoes:
            dados.append({
                'id': t.id,
                'data_transacao': t.data_transacao.isoformat(),
                'data_vencimento': t.data_vencimento.isoformat() if t.data_vencimento else None,
                'tipo_transacao': t.tipo_transacao,
                'tipo_conta': t.tipo_conta,
                'valor': t.valor,
                'parcela': t.parcela,
                'estabelecimento': t.estabelecimento,
                'status': t.status,
                'categoria': t.categoria,
                'subcategoria': t.subcategoria,
                'tipo_fixo_variavel': t.tipo_fixo_variavel,
                'descricao': t.descricao
            })
        
        return jsonify(dados), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/transacoes', methods=['POST'])
def api_criar_transacao():
    """Cria uma nova transação"""
    try:
        dados = request.get_json()
        transacao = TransacaoService.criar_transacao(dados)
        
        return jsonify({
            'id': transacao.id,
            'mensagem': 'Transação criada com sucesso'
        }), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/transacoes/<transacao_id>/status', methods=['PUT'])
def api_atualizar_status_transacao(transacao_id):
    """Atualiza o status de uma transação"""
    try:
        dados = request.get_json()
        transacao = TransacaoService.atualizar_status_transacao(
            transacao_id,
            dados['novo_status']
        )
        return jsonify({
            'id': transacao.id,
            'status': transacao.status,
            'mensagem': 'Status atualizado'
        }), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# =============== API - CICLOS ===============

@app.route('/api/ciclos/<int:mes>/<int:ano>', methods=['GET'])
def api_ciclo_detalhes(mes, ano):
    """Retorna detalhes de um ciclo específico"""
    try:
        data_inicio, data_fim = CicloService.calcular_datas_ciclo(mes, ano)
        totais = CicloService.calcular_totais_ciclo(data_inicio, data_fim)
        
        return jsonify({
            'mes': mes,
            'ano': ano,
            'data_inicio': data_inicio.isoformat(),
            'data_fim': data_fim.isoformat(),
            **totais
        }), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/ciclos/<int:mes>/<int:ano>/pendentes', methods=['GET'])
def api_ciclo_pendentes(mes, ano):
    """Retorna transações pendentes de um ciclo"""
    try:
        data_inicio, data_fim = CicloService.calcular_datas_ciclo(mes, ano)
        
        pendentes = TransacaoModel.query.filter(
            TransacaoModel.data_transacao >= data_inicio,
            TransacaoModel.data_transacao <= data_fim,
            TransacaoModel.status.in_(['PREVISTO', 'AGENDADO', 'REC_PENDENTE'])
        ).all()
        
        dados = []
        for t in pendentes:
            dados.append({
                'id': t.id,
                'data_transacao': t.data_transacao.isoformat(),
                'estabelecimento': t.estabelecimento,
                'valor': t.valor,
                'status': t.status,
                'categoria': t.categoria
            })
        
        return jsonify(dados), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# =============== ERROR HANDLERS ===============

@app.errorhandler(404)
def nao_encontrado(e):
    return jsonify({'erro': 'Recurso não encontrado'}), 404

@app.errorhandler(500)
def erro_interno(e):
    return jsonify({'erro': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    print("🚀 Iniciando aplicação em http://localhost:8080")
    app.run(debug=True, host='127.0.0.1', port=8080)
