# 🔄 Changelog: Funcionalidade de TRANSFERÊNCIA

## Data: 29 de Março de 2026

### ✨ Novas Funcionalidades

#### 1. **Novo Tipo de Transação: TRANSFERÊNCIA**
- Adicionado tipo `TRANSFERENCIA` aos tipos de transação
- Permite transferir valores entre contas sem usar categoria
- Funciona de forma independente de RECEITA e DESPESA

#### 2. **Novo Tipo de Conta: INVESTIMENTO**
- Adicionado tipo `INVESTIMENTO` aos tipos de conta (além de CORRENTE e CARTAO)
- Contas de investimento podem participar de transferências

#### 3. **Restrições de Transferência**
- ✅ Permitido entre: **CORRENTE** ↔ **CORRENTE**
- ✅ Permitido entre: **CORRENTE** ↔ **INVESTIMENTO**
- ✅ Permitido entre: **INVESTIMENTO** ↔ **INVESTIMENTO**
- ❌ **NÃO permitido** com: **CARTAO** (cartão de crédito)

#### 4. **Validações de Transferência**
- Conta origem e destino não podem ser iguais
- Saldo verifica se é suficiente na conta origem
- Transferência só é efetuada quando status é alterado para "Pago"

### 🛠️ Alterações Técnicas

#### Backend (app_v2.py)
- Modificado `models.py`:
  - Adicionado `INVESTIMENTO` ao enum `TipoConta`
  
- Modificada rota `/api/transacoes` (POST):
  - Adicionada validação para tipo `TRANSFERENCIA`
  - Validação que contas não podem ser cartão de crédito
  - Adicionados campos `conta_origem_id` e `conta_destino_id`
  
- Modificada rota `/api/transações/<id>/efetivar` (PUT):
  - Adicionada lógica para processar transferências
  - Débito na conta origem
  - Crédito na conta destino
  - Validação de saldo insuficiente
  
- Modificada rota `/api/transações/<id>` (DELETE):
  - Adicionada lógica para reverter transferências
  - Reverte débito e crédito em ambas as contas

#### Frontend (simples.html)
- Adicionado seletor `TRANSFERENCIA` no dropdown de tipo
- Adicionada função `atualizarCamposporTipo()`:
  - Mostra/ocupa campos de conta origem/destino conforme o tipo
  - Carrega apenas contas válidas (não cartão)
  
- Adicionada função `carregarContasTransferencia()`:
  - Busca contas CORRENTE e INVESTIMENTO
  - Mostra saldo de cada conta
  
- Modificada função de submissão:
  - Adicionada validação para seleção de contas na transferência
  - Adicionada verificação se contas são diferentes
  - Adicionados campos `conta_origem_id` e `conta_destino_id` ao payload

### 📊 Especificações

#### Estrutura de Transação (TRANSFERÊNCIA)
```json
{
  "id": 42,
  "tipo": "TRANSFERENCIA",
  "tipo_conta": "CORRENTE",
  "conta_origem_id": 1,
  "conta_destino_id": 3,
  "valor": 500.00,
  "data_vencimento": "2026-03-29",
  "status": "PREVISTO",
  "efetuada": false,
  "categoria": "Transferência",
  "descricao": "Transferência para investimento"
}
```

#### Fluxo de Efetivação
1. Usuário cria transferência (status = PREVISTO, efetuada = false)
2. Usuário marca como "Pago" (efetiva)
3. Sistema verifica:
   - Ambas as contas existem
   - Contas não são cartão de crédito
   - Contas são diferentes
   - Saldo da origem é suficiente
4. Sistema sensibiliza os saldos:
   - `conta_origem.saldo_manual -= valor`
   - `conta_destino.saldo_manual += valor`
   - `transacao.efetuada = true`
   - `transacao.status = "PAGO"`

### 🔄 Reversão
Se usuário deletar uma transferência efetuada:
1. Sistema identifica que é transferência
2. Reverte em ambas as contas
3. Remove transação da lista

### 🎯 Casos de Uso

**Exemplo 1: Transferência Corrente → Investimento**
- Usuário tem R$ 1.000 em Bradesco (Corrente)
- Deseja transferir R$ 300 para Tesouro (Investimento)
- Cria transferência
- Efetiva
- Bradesco passa a R$ 700
- Tesouro passa a receber R$ 300

**Exemplo 2: Transferência entre Correntes**
- Transferência entre Bradesco e C6 Bank
- Permitido sem restrição

**Exemplo 3: Tentativa com Cartão (Bloqueada)**
- NÃO permite transferência COM cartão de crédito
- Sistema retorna erro: "Transferência não permitida com cartão de crédito"

### 📝 Notas Importantes

1. **Transferências não aparecem em categorias** (nova linha "Transferência" é usada)
2. **Transferências não afetam saldo projetado** (uma transferência nterna não muda o total, apenas redistribui)
3. **Transferências reversas são automáticas** ao deletar a transação
4. **Sem limite de transferência** - qualquer valor é permitido enquanto houver saldo

### ✅ Testes Recomendados

- [ ] Criar transferência entre contas correntes
- [ ] Criar transferência entre corrente e investimento
- [ ] Tentar criar transferência com cartão (deve falhar)
- [ ] Tentar transferir valor maior que saldo (deve falhar)
- [ ] Efetuar transferência e verificar saldos
- [ ] Deletar transferência e verificar se saldos reverteram
- [ ] Verificar se contas de origem/destino aparecem no seletor
- [ ] Verificar se campos são mostrados/ocultados conforme tipo

### 🚀 Futuras Melhorias

- [ ] Histórico de transferências
- [ ] Transferências agendadas
- [ ] Limites de transferência por dia
- [ ] Notificações de transferência
- [ ] Relatório de movimentação entre contas
