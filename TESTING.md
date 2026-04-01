"""
🧪 GUIA DE TESTES AUTOMATIZADOS

Este documento explica como os testes funcionam e como usá-los.

═══════════════════════════════════════════════════════════════════

## INSTALAÇÃO

1. Instalar dependências de teste:
   ```bash
   pip install -r requirements-test.txt
   ```

## EXECUTAR TESTES

### Rodar todos os testes:
```bash
./run_tests.sh
```

### Rodar testes específicos:
```bash
# Apenas testes de backup
pytest tests/test_backup.py -v

# Apenas testes de contas
pytest tests/test_contas.py -v

# Com cobertura de código
pytest tests/ --cov=app_v2 --cov-report=html
```

### Modo desenvolvimento (com relatórios detalhados):
```bash
chmod +x test_dev.sh
./test_dev.sh backup    # Testa backup
./test_dev.sh contas    # Testa contas
./test_dev.sh faturas   # Testa faturas
./test_dev.sh resumo    # Testa resumo
```

═══════════════════════════════════════════════════════════════════

## ESTRUTURA DE TESTES

### tests/conftest.py
Configuração global, fixtures compartilhadas

### tests/test_backup.py
- Backup é criado ao salvar dados
- Apenas 10 últimos backups são mantidos
- Backup é criado ANTES de deletar

### tests/test_contas.py
- Listar contas
- Criar nova conta
- Atualizar saldo
- Deletar conta
- Saldo dinâmico (manual + transações)

### tests/test_faturas.py
- Listar faturas
- Vencimento dinâmico por mês (dia fixo do cartão)
- Não permite deletar fatura fechada
- Permite deletar fatura aberta

### tests/test_resumo.py
- Dashboard retorna estrutura correta
- Cálculo de receita do mês corrente
- Cálculo de despesa do mês corrente
- Faturas não são contadas duas vezes
- Ignora transações de meses anteriores

═══════════════════════════════════════════════════════════════════

## PRÉ-COMMIT HOOK (Automático)

O arquivo `.git/hooks/pre-commit` roda testes automaticamente antes
de cada commit. Se um teste falhar, o commit é bloqueado.

Para ativar:
```bash
chmod +x .git/hooks/pre-commit
```

A partir de agora, toda vez que tentar fazer commit:
1. Testes rodam automaticamente
2. Se tudo passar: ✅ commit permitido
3. Se falhar: ❌ commit bloqueado até consertar

═══════════════════════════════════════════════════════════════════

## COBERTURA DE CÓDIGO

Para ver quais linhas do código estão sendo testadas:

```bash
pytest tests/ --cov=app_v2 --cov-report=html
# Abre: htmlcov/index.html
```

═══════════════════════════════════════════════════════════════════

## ADICIONANDO NOVOS TESTES

1. Criar novo arquivo em `tests/test_minha_feature.py`
2. Importar fixtures de `conftest.py`
3. Escrever testes usando padrão Arrange-Act-Assert:

```python
def test_funcionalidade_nova(self, client, dados_teste):
    # Arrange - preparar dados
    dados = dados_teste
    
    # Act - executar ação
    response = client.get('/api/endpoint')
    
    # Assert - validar resultado
    assert response.status_code == 200
```

4. Rodar: `pytest tests/test_minha_feature.py -v`

═══════════════════════════════════════════════════════════════════

## QUANDO TESTES FALHAM

1. Ler a mensagem de erro
2. Verificar o que mudou no código
3. Rodar testes novamente: `pytest tests/ -v --tb=long`
4. Corrigir o código ou o teste
5. Commitar apenas quando TODOS os testes passam

═══════════════════════════════════════════════════════════════════

## DICA: Testar durante desenvolvimento

```bash
# Terminal 1: rodar app
python3 app_v2.py

# Terminal 2: rodar testes continuamente
pytest tests/ --watch
```

═══════════════════════════════════════════════════════════════════
"""
