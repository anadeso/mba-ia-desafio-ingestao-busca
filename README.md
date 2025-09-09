# Desafio MBA Engenharia de Software com IA - Full Cycle

## 📋 Descrição do Projeto

Este projeto implementa um sistema RAG (Retrieval-Augmented Generation) que permite fazer perguntas sobre o conteúdo de documentos PDF utilizando inteligência artificial. O sistema é composto por três componentes principais:

- **Ingestão**: Processa documentos PDF e armazena embeddings no banco de dados
- **Busca**: Realiza busca semântica nos documentos indexados
- **Chat**: Interface interativa para fazer perguntas sobre os documentos

## 🛠️ Tecnologias Utilizadas

- **LangChain**: Framework para desenvolvimento de aplicações com LLM
- **OpenAI**: API para embeddings e chat completion
- **PostgreSQL + pgvector**: Banco de dados vetorial para armazenar embeddings
- **Docker**: Containerização do banco de dados
- **Python**: Linguagem de programação principal

## 📋 Pré-requisitos

Antes de executar o projeto, certifique-se de ter instalado:

- **Python 3.9+**
- **Docker e Docker Compose**
- **Git** (para clonar o repositório)
- **Conta OpenAI** com API Key ativa

## ⚙️ Configuração do Ambiente

### 1. Clone o repositório (se necessário)
```bash
git clone <url-do-repositorio>
cd mba-ia-desafio-ingestao-busca
```

### 2. Crie o arquivo de configuração `.env`
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=text-embedding-3-small

# PostgreSQL Configuration
PGVECTOR_URL=postgresql://postgres:postgres@localhost:5433/rag
PGVECTOR_COLLECTION=documents
```

> ⚠️ **Importante**: Substitua `sk-your-openai-api-key-here` pela sua chave de API real da OpenAI.

### 3. Configure o ambiente Python

#### Opção A: Usando ambiente virtual (Recomendado)
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No macOS/Linux:
source venv/bin/activate
# No Windows:
# venv\Scripts\activate

# Instalar dependências
pip install -r ../requirements.txt
```

#### Opção B: Instalação global
```bash
pip install -r ../requirements.txt
```

## 🚀 Execução do Projeto

### 1. Inicie o banco de dados PostgreSQL

```bash
# Inicia o PostgreSQL com extensão pgvector
docker-compose up -d

# Aguarde alguns segundos para o banco inicializar completamente
# Verifique se os containers estão rodando:
docker-compose ps
```

### 2. Execute a ingestão do documento

```bash
# Navegue para o diretório src
cd src

# Execute o script de ingestão
python ingest.py
```

> 📝 **Nota**: Este comando processará o arquivo `document.pdf` na raiz do projeto e criará os embeddings no banco de dados.

### 3. Inicie o chat interativo

```bash
# No diretório src
python chat.py
```

### 4. Interaja com o sistema

Agora você pode fazer perguntas sobre o conteúdo do documento PDF:

```
==== Chat com Base de Conhecimento ====
Digite 'sair' para encerrar o chat
Perguntas serão respondidas com base no PDF disponível

Faça sua pergunta: Qual é o assunto principal do documento?
Processando...
RESPOSTA: [Resposta baseada no conteúdo do PDF]
```

Para encerrar o chat, digite: `sair`, `exit` ou `quit`

## 📁 Estrutura do Projeto

```
mba-ia-desafio-ingestao-busca/
├── src/
│   ├── ingest.py          # Script de ingestão de documentos
│   ├── search.py          # Módulo de busca semântica
│   └── chat.py            # Interface de chat interativo
├── docker-compose.yml     # Configuração do PostgreSQL
├── document.pdf           # Documento para indexação
├── README.md              # Este arquivo
└── .env                   # Variáveis de ambiente (criar)
```

## 🔧 Comandos Úteis

### Gerenciar o banco de dados
```bash
# Parar o banco de dados
docker-compose down

# Reiniciar o banco (apaga todos os dados)
docker-compose down -v
docker-compose up -d

# Ver logs do banco
docker-compose logs postgres
```

### Testar a busca diretamente
```bash
cd src
python -c "from search import search_prompt; print(search_prompt('sua pergunta aqui'))"
```

## 🐛 Solução de Problemas

### Erro: "Environment variable X is not set"
- Verifique se o arquivo `.env` foi criado corretamente
- Confirme se todas as variáveis necessárias estão preenchidas
- Certifique-se de que o arquivo `.env` está na raiz do projeto

### Erro de conexão com PostgreSQL
- Verifique se o Docker está rodando: `docker ps`
- Confirme se o container está saudável: `docker-compose ps`
- Aguarde alguns segundos após iniciar o Docker

### Erro de API da OpenAI
- Verifique se sua API Key está correta e ativa
- Confirme se você tem créditos disponíveis na conta OpenAI
- Teste a API Key em uma requisição simples

### Erro: "ModuleNotFoundError"
- Certifique-se de que o ambiente virtual está ativado
- Reinstale as dependências: `pip install -r ../requirements.txt`

### Container PostgreSQL não inicia
```bash
# Limpe volumes antigos
docker-compose down -v
docker system prune -f

# Recrie os containers
docker-compose up -d
```

## 📊 Funcionamento Detalhado

### 1. Processo de Ingestão
- Carrega o arquivo PDF usando `PyPDFLoader`
- Divide o texto em chunks de 1000 caracteres com overlap de 150
- Gera embeddings usando OpenAI
- Armazena no PostgreSQL com pgvector

### 2. Processo de Busca
- Recebe uma pergunta do usuário
- Gera embedding da pergunta
- Busca os 10 documentos mais similares
- Usa GPT para gerar resposta baseada no contexto

### 3. Interface de Chat
- Loop interativo para receber perguntas
- Integra com o módulo de busca
- Trata erros e exceções graciosamente

## 📞 Suporte

Se encontrar problemas não cobertos neste guia:

1. Verifique os logs do Docker: `docker-compose logs`
2. Confirme as versões das dependências
3. Teste cada componente separadamente
4. Verifique a conectividade com a API da OpenAI

---

**Developed for MBA Engenharia de Software com IA - Full Cycle**