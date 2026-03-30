# 💰 Sistema de Controle Financeiro

Uma aplicação web profissional para gerenciar seu fluxo financeiro com visualizações gráficas, saldo manual e automático, ciclos de pagamento e drill-down para detalhes.

## 🎯 Recursos

✅ **Saldo Manual** - Você alimenta o saldo inicial
✅ **Saldo Automático** - Calculado automaticamente a partir das transações  
✅ **Múltiplas Contas** - Controle várias contas correntes e cartões
✅ **Categorias & Subcategorias** - Organize despesas e receitas
✅ **Parcelas** - Suporte para parcelas (ROT, 1/2, 3/10, etc)
✅ **Ciclos Mensais** - Sistema de ciclos começando no penúltimo dia do mês
✅ **Dashboard Visual** - Gráficos interativos e drill-down
✅ **Transações Pendentes** - Acompanhe o que falta pagar/receber
✅ **Sincronização em Nuvem** - Pronto para OneDrive/iCloud

## 🚀 Como Usar

### 1. Instalar Dependências

```bash
cd /Users/eduardomoretti/Downloads/vscode
pip3 install -r requirements.txt
```

### 2. Iniciar a Aplicação

```bash
python3 app.py
```

A aplicação abrirá em: **http://localhost:5000**

### 3. Primeiro Acesso

- Clique em "Nova Conta" para adicionar suas contas
- Configure um saldo inicial (manual)
- Adicione transações (receitas e despesas)
- Visualize os gráficos automaticamente

## 📊 Estrutura de Dados

### Campos de uma Transação:
```
- Data da Transação: Quando foi efetivada
- Data de Vencimento: Quando vence/paga
- Tipo: CREDITO (receita) ou DEBITO (despesa)
- Tipo Conta: CORRENTE ou CARTAO
- Bandeira: Nome da conta/cartão
- Valor: Montante
- Parcela: ROT (rotativa), 1/2, 3/10, etc
- Estabelecimento: Onde foi gasto
- Status: PREVISTO, AGENDADO, PAGO, REC_PENDENTE, RECEBIDO
- Categoria: Ex. ALIMENTACAO, TRANSPORTE
- Subcategoria: Ex. PIZZA, COMBUSTIVEL
- Tipo Fixo/Variável: FIXO ou VARIAVEL
- Descrição: Observações
```

## 📱 Acessar em Qualquer Lugar

### Local (Seu Computador):
- Mac: http://localhost:5000
- Windows: http://localhost:5000

### De Outros Dispositivos (mesmo Wi-Fi):
1. Descubra o IP da máquina: `ifconfig | grep inet`
2. Acesse: `http://seu-ip:5000`

### De Qualquer Lugar (com sincronização em nuvem):
- Implante em servidor (próximo passo)
- Configure OneDrive/iCloud para sincronização

## 🗄️ Banco de Dados

Sistema usa **SQLite** com os seguintes modelos:

- **Contas**: Suas contas correntes e cartões
- **Categorias**: Organização de despesas
- **Subcategorias**: Subdivisão de categorias
- **Transações**: Registros de gastos/receitas
- **Saldos**: Histórico de saldos (manual e automático)
- **Ciclos**: Períodos financeiros

## 🔄 Próximos Passos

1. ✏️ Editar transações existentes
2. 📤 Exportar para Excel
3. ☁️ Sincronizar com OneDrive
4. 🔐 Sistema de login e segurança
5. 📊 Relatórios avançados
6. 🌐 Deploy em servidor

## 🛠️ Desenvolvimento

Estrutura do projeto:
```
/
├── app.py              # Aplicação principal Flask
├── database.py         # Modelos SQLAlchemy
├── services.py         # Lógica de negócio
├── models.py           # Classes de negócio
├── requirements.txt    # Dependências
├── templates/
│   └── dashboard.html  # Interface web
└── static/             # CSS, JS, imagens (futuro)
```

## 📞 Suporte

Se tiver problemas:
1. Verifique se Python 3.9+ está instalado
2. Verifique se as dependências foram instaladas
3. Tente recarregar a página (F5)
4. Abra o console do navegador (F12) para ver erros

---

**Desenvolvido com ❤️ para organizar suas finanças**
