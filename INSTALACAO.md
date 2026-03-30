# 💰 Gestor Financeiro - Guia de Instalação e Distribuição

## 📋 Opções de Distribuição

Existem **3 formas principais** de compartilhar esta aplicação:

---

## 🎯 **OPÇÃO 1: Executável Standalone (Recomendado para usuários finais)**

### ✅ Vantagens:
- ✓ Não precisa instalar nada (nem Python)
- ✓ Um único arquivo para compartilhar
- ✓ Abre automaticamente no navegador
- ✓ Funciona offline

### 📦 Como Gerar o Executável:

#### **No Mac:**

```bash
# 1. Abra o Terminal
# 2. Navegue até a pasta do projeto
cd ~/Downloads/vscode

# 3. Execute o script de build
chmod +x build.sh
./build.sh
```

#### **No Windows:**

```bash
# 1. Abra o Prompt de Comando (cmd)
# 2. Navegue até a pasta do projeto
cd Downloads\vscode

# 3. Execute o script de build
build.bat
```

### 📁 Resultado:
- Arquivo executável em: `dist/Gestor_Financeiro` (Mac) ou `dist/Gestor_Financeiro.exe` (Windows)
- Tamanho: ~150-200 MB

### 🚀 Como Usar o Executável:
1. Copie o arquivo para o local desejado (Desktop, Documents, etc.)
2. Dê um duplo-clique para executar
3. Aguarde 2-3 segundos
4. O navegador abrirá automaticamente com a aplicação

---

## 🐳 **OPÇÃO 2: Docker (Para usuários com Docker instalado)**

### ✅ Vantagens:
- ✓ Mesma aplicação em qualquer SO
- ✓ Não conflita com outras versões do Python
- ✓ Fácil de atualizar

### 📥 Instruções:

#### **Instalação do Docker:**
- **Mac**: Baixe em https://www.docker.com/products/docker-desktop
- **Windows**: Baixe em https://www.docker.com/products/docker-desktop

#### **Como Executar:**

```bash
# Na pasta do projeto
docker-compose up
```

A aplicação estará disponível em: `http://127.0.0.1:3333`

---

## 💻 **OPÇÃO 3: Python + Manual (Para desenvolvedores)**

### Pré-requisitos:
- Python 3.8 ou superior
- pip (geralmente vem com Python)

### 📥 Instalação:

```bash
# 1. Clonar/copiar o repositório
cd seu-diretorio

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente virtual
# Mac/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Executar
python launcher.py
```

---

## 🎁 Para Compartilhar o Executável

### Mac:
```bash
# 1. Gere o executável usando `build.sh`
# 2. Comprima a pasta
cd dist
zip -r Gestor_Financeiro.zip Gestor_Financeiro
# 3. Compartilhe o arquivo .zip
```

### Windows:
```bash
# 1. Gere o executável usando `build.bat`
# 2. Copie apenas: dist/Gestor_Financeiro.exe
# 3. Comprima em ZIP (ou envie direto)
# 4. Compartilhe
```

### Google Drive/OneDrive/Dropbox:
1. Faça upload da pasta ou do arquivo
2. Compartilhe o link
3. Recebedores baixam e executam

---

## ⚙️ Requisitos Mínimos do Sistema

### Para Executável:
- **Mac**: macOS 10.14+
- **Windows**: Windows 7+ (64-bit)
- **RAM**: 512 MB
- **Disco**: 500 MB

### Para Docker:
- Docker Desktop instalado
- Espaço em disco para imagem Docker (~1 GB)

---

## 🆘 Troubleshooting

### ❌ "Python não encontrado"
- **Solução**: Instale Python 3.8+ de https://www.python.org

### ❌ Executável não inicia
- **Mac**: Abra Terminal e execute:
  ```bash
  xattr -d com.apple.quarantine /caminho/para/Gestor_Financeiro
  ```
- **Windows**: Clique com botão direito → Propriedades → Desbloquear

### ❌ Porta 3333 em uso
- **Solução**: Feche outras aplicações que usam essa porta ou modifique em `app_v2.py`

### ❌ Aplicação não abre navegador
- **Solução**: Abra manualmente http://127.0.0.1:3333 no navegador

---

## 📝 Notas Importantes

- A aplicação armazena dados em `/tmp/financas_dados.json` (Linux/Mac) ou pasta TEMP (Windows)
- Faça backup periódico dos dados
- Para atualizar: Baixe a nova versão e execute novamente

---

## 📧 Suporte

Para dúvidas ou problemas, consulte o arquivo de logs gerado durante a execução.

Versão: 1.0  
Última atualização: 29 de Março de 2026
