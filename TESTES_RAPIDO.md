# 🧪 GUIA RÁPIDO - TESTES AUTOMATIZADOS

## 🚀 TL;DR (Resumo Executivo)

Montei uma estrutura de testes que **impede que você commite código quebrado**. Toda vez que eu altero algo, os testes rodam automaticamente para garantir que nada foi danificado.

---

## ✨ O que foi criado?

### 📁 Estrutura de Testes `tests/`

```
tests/
├── __init__.py              # Inicialização
├── conftest.py              # Configuração central + fixtures
├── test_backup.py           # ✅ Testes de backup automático
├── test_contas.py           # ✅ Testes de CRUD de contas
├── test_faturas.py          # ✅ Testes de faturas de cartão
└── test_resumo.py           # ✅ Testes do dashboard
```

### 📝 Arquivos de Configuração

- `requirements-test.txt` - Dependências para rodar testes
- `run_tests.sh` - Script para rodar TODOS os testes
- `test_dev.sh` - Script para modo desenvolvimento
- `demo_tests.sh` - Demonstração de como funciona
- `.git/hooks/pre-commit` - Hook que bloqueia commits com testes falhando

### 📚 Documentação

- `TESTING.md` - Guia completo (leia se precisar de detalhes)

---

## 🎯 Como usar (3 formas)

### Forma 1: Rodar TODOS os testes
```bash
./run_tests.sh
```

**Saída esperada:**
```
✅ TODOS OS TESTES PASSARAM!
```

Ou se algo quebrou:
```
❌ TESTES FALHARAM!
   - linha 42: Backup não foi criado
   - linha 87: Saldo incorreto
```

### Forma 2: Modo desenvolvimento (teste específico)
```bash
./test_dev.sh backup    # Testa apenas backup
./test_dev.sh contas    # Testa apenas contas
./test_dev.sh faturas   # Testa apenas faturas
./test_dev.sh resumo    # Testa apenas resumo
```

### Forma 3: pytest direto (para desenvolvedores)
```bash
# Um teste específico
python3 -m pytest tests/test_backup.py::TestBackup::test_backup_criado_ao_salvar_dados -v

# Todos os testes com cobertura
python3 -m pytest tests/ --cov=app_v2 --cov-report=html

# Modo "watch" (rerun ao salvar código)
python3 -m pytest tests/ --watch
```

---

## 🛡️ Como os testes protegem?

### Cenário Real 1: Você altera função de backup
```python
# ❌ ANTES: Código arrisca
def salvar_dados(dados):
    # Oops... esqueci de fazer backup!
    with open(DADOS_FILE, 'w') as f:
        json.dump(dados, f)
```

**Resultado:**
```bash
$ ./run_tests.sh

❌ TESTE FALHOU!
tests/test_backup.py::TestBackup::test_backup_criado_ao_salvar_dados
AssertionError: Nenhum backup foi criado

COMMIT BLOQUEADO! ⛔
```

### Cenário Real 2: Você altera cálculo de saldo
```python
# ❌ ANTES: Cálculo errado
saldo = saldo_manual - receita + despesa  # Inverteu!
```

**Resultado:**
```bash
$ ./run_tests.sh

❌ TESTE FALHOU!
tests/test_contas.py::TestContas::test_calcular_saldo_dinamico
AssertionError: esperava 1100.00, mas foi -900.00

COMMIT BLOQUEADO! ⛔
```

### Cenário Real 3: Você descobre bug e corrige
```python
# ✅ DEPOIS: Código correto
saldo = saldo_manual + receita - despesa  # Correto!
```

**Resultado:**
```bash
$ ./run_tests.sh

✅ TODOS OS TESTES PASSARAM!
COMMIT PERMITIDO! ✅
```

---

## 📊 Testes que Cobrem Cada Feature

| Feature | Testes | O que valida |
|---------|--------|-------------|
| **Backup** | 4 testes | Backup criado? Outros 10? Antes de deletar? |
| **Contas** | 6 testes | CRUD, saldo dinâmico, validações |
| **Faturas** | 5 testes | Listagem, vencimento dinâmico, deletar fechada |
| **Dashboard** | 5 testes | Campos obrigatórios, receita/despesa, sem double-count |
| **Total** | **20 testes** | Cobertura completa das funcionalidades críticas |

---

## 🔧 Instalação (uma vez)

```bash
# Instalar dependências de teste
pip3 install -r requirements-test.txt

# Ou instalar manualmente
pip3 install pytest pytest-cov pytest-flask pytest-mock werkzeug==2.3.7

# Ativar pre-commit hook (automático em cada commit)
chmod +x .git/hooks/pre-commit
```

---

## ⚡ Fluxo Típico Agora

**Antes (você sofria com bugs aleatórios 😡):**
1. Você pede para consertar X
2. Eu conserto X
3. Acidentalmente quebro Y
4. Você descobre B dias depois
5. Raiva 🔴

**Agora (protegido com testes 😊):**
1. Você pede para consertar X
2. Eu conserto X
3. Rodam testes automaticamente
4. Testes detectam que Y quebrou
5. Eu corrijo ANTES de commitar
6. Você recebe código 100% funcional ✅

---

## 📈 Cobertura de Código

Ver quais linhas estão sendo testadas:

```bash
python3 -m pytest tests/ --cov=app_v2 --cov-report=html
# Abre: htmlcov/index.html
```

---

## 🚨 Se um teste falhar

1. **Leia a mensagem:**
   ```
   AssertionError: Esperava X mas foi Y
   ```

2. **Rode em modo verbose para ver detalhes:**
   ```bash
   python3 -m pytest tests/test_seu_teste.py -vv --tb=long
   ```

3. **Opções:**
   - Se é um **bug real**: corrija o código
   - Se é um **teste ruim**: atualize o teste com o novo comportamento

---

## 📝 Adicionando Novos Testes

Se eu adicionei nova feature, faça assim:

```python
# tests/test_nova_feature.py
import pytest

class TestNovaFeature:
    """Testes da nova feature"""
    
    def test_nova_funcionalidade(self, client, dados_teste):
        # Arrange (preparar)
        dados = dados_teste
        
        # Act (executar)
        response = client.get('/api/endpoint')
        
        # Assert (validar)
        assert response.status_code == 200
```

---

## 🎓 Boas Práticas

✅ **Faça:**
- Rodar testes antes de qualquer mudança
- Escrever testes junto com o código
- Ler mensagens de erro completamente
- Rodar testes em modo development durante desenvolvimento

❌ **Não faça:**
- Desabilitar pre-commit hook (❌ você vai sofrer depois)
- Ignorar testes falhando
- Fazer mudanças grandes sem testar
- Commitar código quebrado

---

## 📞 Precisa de Ajuda?

**Ver tudo:**
```bash
cat TESTING.md
```

**Ver demonstração:**
```bash
./demo_tests.sh
```

**Ver logs de erro detalhados:**
```bash
python3 -m pytest tests/ -vv --tb=long --capture=no
```

---

## 🎉 Resultado Final

```
┌─────────────────────────────────────────────────┐
│  Sem testes:                                    │
│  • Você arruma X, quebra Y, Z fica instável    │
│  • Surpresas ruins depois                       │
│  • Confiança baixa no código ❌                 │
├─────────────────────────────────────────────────┤
│  Com testes:                                    │
│  • Você arruma X, testes avisam se Y quebrar   │
│  • Sem surpresas                                │
│  • Confiança alta no código ✅                 │
│  • Dormir tranquilo à noite 😴                 │
└─────────────────────────────────────────────────┘
```

---

**Próximo passo:** Execute `./run_tests.sh` agora para validar! 🚀
