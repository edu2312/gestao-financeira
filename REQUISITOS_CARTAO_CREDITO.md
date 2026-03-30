# 💳 Requisitos - Sistema de Cartão de Crédito

## 1. CADASTRO DE CARTÕES
- [ ] Cadastrar novos cartões de crédito
- [ ] Informações do cartão:
  - Bandeira (Visa, Mastercard, Elo, Amex, etc)
  - Últimos 4 dígitos
  - Limite de crédito
  - Data de fechamento da fatura (1-31)
  - Data de vencimento da fatura (1-31)
  - Status (ativo/inativo)

---

## 2. GERENCIAMENTO DE FATURAS
- [ ] Criar faturas automaticamente baseado em data de fechamento
- [ ] Sinalizar fatura como **ABERTA** ou **FECHADA**
- [ ] Fatura tem:
  - Data de fechamento (quando encerra as transações do período)
  - Data de vencimento (quando precisa pagar)
  - Saldo atual da fatura
  - Status (aberta/fechada)

---

## 3. IMPACTO NOS SALDOS

### Saldo Atual
- ❌ Saldo de cartão **NÃO impacta** o saldo atual da conta
- ✅ Saldo atual = apenas contas corrente/poupança

### Saldo Projetado
- ✅ Leva em conta **vencimentos de faturas** no período selecionado
- ✅ Se fatura vence no período → deduz do saldo projetado
- Fórmula: Saldo Atual - (Faturas vencidas no período)

---

## 4. TRANSAÇÕES PARCELADAS
- [ ] Permitir parcelar transações em 2x até 12x (ou mais)
- [ ] Transação parcelada distribui:
  - 1ª parcela na fatura atual
  - 2ª parcela na próxima fatura
  - etc...
- [ ] Exemplo: Compra de R$ 1.200 em 3x
  - Fatura Março: R$ 400
  - Fatura Abril: R$ 400
  - Fatura Maio: R$ 400

---

## 5. CICLO DE VIDA DA FATURA

### Estado: ABERTA ✅
- Transações podem ser adicionadas/removidas
- Saldo da fatura = soma de transações abertas
- Fatura pode ser editada

### Estado: FECHADA 🔒
- Transações são **finalizadas** (locked)
- Não podem ser adicionadas novas transações
- Fatura tem data de vencimento definida
- Saldo da fatura = fixo (não muda mais)
- Sensibiliza o saldo projetado até a data de vencimento

---

## 6. FLUXO DE TRANSAÇÕES

```
Transação criada
    ↓
Atribuída a um Cartão
    ↓
Entra na Fatura ABERTA do cartão
    ↓
(Opcional) Parcelada em múltiplas faturas
    ↓
Fatura é FECHADA na data de fechamento
    ↓
Fatura vira BLOQUEADA (não pode editar transações)
    ↓
Fatura tem data de vencimento
    ↓
Vencimento = sensibiliza saldo projetado
    ↓
Data de vencimento = quando "sai do saldo"
```

---

## 7. DADOS A ARMAZENAR

### Cartão
```json
{
  "id": 1,
  "bandeira": "Visa",
  "ultimos_digitos": "1234",
  "limite_credito": 5000.00,
  "data_fechamento": 10,
  "data_vencimento": 20,
  "status": "ativo"
}
```

### Fatura
```json
{
  "id": 1,
  "cartao_id": 1,
  "mes": "2026-03",
  "data_fechamento": "2026-03-10",
  "data_vencimento": "2026-03-20",
  "status": "aberta",
  "saldo": 1250.50
}
```

### Transação (com parcelamento)
```json
{
  "id": 1,
  "valor": 1200.00,
  "parcelas": 3,
  "numero_parcela": 1,
  "cartao_id": 1,
  "fatura_id": 1,
  "descricao": "Notebook",
  "status": "pendente"
}
```

---

## 8. PRIORIDADE DE IMPLEMENTAÇÃO

### Fase 1 (MVP)
1. Cadastro de cartões
2. Gerenciamento de faturas (aberta/fechada)
3. Transações associadas a cartões
4. Impacto no saldo projetado

### Fase 2 (Expansão)
1. Transações parceladas
2. Histórico de faturas
3. Relatórios por cartão

### Fase 3 (Refinamento)
1. Alertas de vencimento
2. Integração com valores de limite
3. Previsão de limite disponível

---

## 9. INTERFACES NECESSÁRIAS

### Admin Panel
- [ ] Seção "Cartões de Crédito"
- [ ] Lista de cartões com opções CRUD
- [ ] Visualizar faturas por cartão
- [ ] Abrir/Fechar faturas manualmente

### Home Page
- [ ] Card mostrando "Saldo em Cartões" (informativo)
- [ ] Card mostrando "Faturas Vencendo" (próximas 30 dias)
- [ ] Impacto no Saldo Projetado

### Nova Transação
- [ ] Campo "Cartão" (select com cartões cadastrados)
- [ ] Campo "Parcelar em" (número de parcelas)

---

## 10. REGRAS DE NEGÓCIO

1. Cartão só pode ter UMA fatura ABERTA por ciclo
2. Fatura FECHADA não pode ser editada
3. Transações de cartão não afetam saldo de conta corrente
4. Faturas com data de vencimento > hoje afetam saldo projetado
5. Transação parcelada distribui valor automaticamente nas faturas

