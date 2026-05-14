# Desafio MBA Engenharia de Software com IA - Full Cycle
## Sistema RAG: Ingestão e Busca Semântica em Documentos

Um sistema de **Retrieval-Augmented Generation (RAG)** que permite fazer perguntas sobre documentos PDF. O sistema ingere o PDF, cria embeddings semânticos usando OpenAI, armazena em PostgreSQL com pgvector, e responde perguntas baseado exclusivamente no conteúdo do documento.

---

## 📋 Pré-requisitos

Certifique-se de ter:

- **Docker Desktop** (ou Docker + Docker Compose)
- **Python 3.8+**
- **OpenAI API key** — obtenha em https://platform.openai.com/api-keys
- **Git** (para versionamento)
- **PostgreSQL** não precisa de instalação (roda via Docker)

---

## 🚀 Quick Start (5 minutos)

Se você quer ir direto ao ponto:

```bash
# 1. Navegar ao diretório
cd 06-desafios-tecnicos/mba-ia-desafio-ingestao-busca

# 2. Criar arquivo .env com sua chave da OpenAI
echo "OPENAI_API_KEY=sk-xxxxx" > .env
echo "OPENAI_MODEL=text-embedding-3-small" >> .env
echo "PGVECTOR_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:5433/rag_desafio" >> .env
echo "PGVECTOR_COLLECTION=rag_desafio" >> .env

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Iniciar PostgreSQL
docker-compose up -d

# 5. Adicionar document.pdf e ingerir
python src/ingest.py

# 6. Chat!
python src/chat.py
```

---

## 📖 Guia Passo-a-Passo Detalhado

### **Passo 1: Preparar o Ambiente**

#### 1.1. Navegar ao diretório do projeto
```bash

```

#### 1.2. Criar arquivo `.env` com variáveis de ambiente

Crie um arquivo chamado `.env` na raiz do projeto com o seguinte conteúdo:

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-xxxxx                                         # Cole sua chave da OpenAI aqui
OPENAI_MODEL=text-embedding-3-small                             # Modelo de embedding

# PostgreSQL Configuration
PGVECTOR_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:5433/rag_desafio
PGVECTOR_COLLECTION=rag_desafio
```

**⚠️ Importante**: Nunca commite o `.env` com chaves reais! Adicione ao `.gitignore`:
```bash
echo ".env" >> .gitignore

```

#### 1.3. Instalar dependências Python

```bash
pip install -r requirements.txt
```

**Output esperado**:
```
Successfully installed langchain==0.1.x openai==1.x psycopg==x.x python-dotenv==x.x ...
```

---

### **Passo 2: Iniciar o Banco de Dados (PostgreSQL)**

#### 2.1. Iniciar os serviços Docker

```bash
docker-compose up -d
```

**Output esperado**:
```
Creating mba-ia-desafio-ingestao-busca_postgres_rag_desafio_1 ... done
Creating mba-ia-desafio-ingestao-busca_bootstrap_vector_ext_1 ... done
```

#### 2.2. Verificar status dos serviços

```bash
docker-compose ps
```

**Output esperado** (ambos em status "Up"):
```
NAME                              STATUS
postgres_rag_desafio              Up 2 minutes
bootstrap_vector_ext              Exited (0)
```

#### 2.3. Validar que a extensão pgvector foi instalada

```bash
psql postgresql://postgres:postgres@127.0.0.1:5433/rag_desafio -c "\dx"
```

**Output esperado** (deve listar a extensão "vector"):
```
                     List of installed extensions
 Schema |  Name   | Version |   Description
--------+---------+---------+---------------------
 public | plpgsql | 1.0     | PL/pgSQL language
 public | vector  | 0.5.0   | vector data type
```

---

### **Passo 3: Ingerir o Documento (Setup inicial — executar UMA VEZ)**

#### 3.1. Adicionar o arquivo PDF

Coloque seu arquivo `document.pdf` na **raiz do projeto**:

```
mba-ia-desafio-ingestao-busca/
├── document.pdf                    ← Adicione aqui
├── src/
├── docker-compose.yml
├── requirements.txt
└── README.md
```

#### 3.2. Executar o script de ingestão

```bash
python src/ingest.py
```

**Output esperado**:
```
Loading document from: document.pdf
Splitting document into chunks...
Generating embeddings with OpenAI...
Storing embeddings in PostgreSQL...
✓ Ingestão concluída com sucesso!
  Chunks armazenados: 1,234
  Embedding model: text-embedding-3-small
```

#### 3.3. Validar que os embeddings foram armazenados

```bash
psql postgresql://postgres:postgres@127.0.0.1:5433/rag_desafio -c "SELECT COUNT(*) as total_chunks FROM langchain_pg_collection;"
```

**Output esperado** (deve retornar um número > 0):
```
 total_chunks
--------------
        1234
```

---

### **Passo 4: Executar o Chat/Busca Semântica**

#### 4.1. Iniciar a interface de chat

```bash
python src/chat.py
```


#### 4.2. Exemplos de uso

```
PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.

---

Perguntas fora do contexto:

PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.

```

#### 4.3. Sair da aplicação

```
Pergunta: sair
(ou pressione Ctrl+C)
```

---

## 🏗️ Arquitetura e Estrutura de Arquivos

```
mba-ia-desafio-ingestao-busca/
├── README.md                      # Este arquivo
├── requirements.txt               # Dependências Python
├── docker-compose.yml             # Configuração PostgreSQL + pgvector
├── .env                           # Variáveis de ambiente (criar)
├── .gitignore                     # (Adicionar .env e document.pdf)
├── document.pdf                   # Documento a ser ingerido (adicionar)
└── src/
    ├── ingest.py                  # Script de ingestão de PDF
    ├── search.py                  # Busca semântica e geração de respostas
    └── chat.py                    # Interface CLI
```

### **O que cada arquivo faz:**

| Arquivo | Responsabilidade |
|---------|-----------------|
| **ingest.py** | Carrega um PDF, divide em chunks (1000 caracteres, overlap de 150), gera embeddings com OpenAI, e armazena vetores em PostgreSQL |
| **search.py** | Realiza busca de similaridade semântica no PostgreSQL, recupera top-10 resultados mais relevantes, e usa ChatGPT para gerar resposta baseada no contexto |
| **chat.py** | Interface CLI interativa que prompta o usuário por perguntas e chama `search_prompt()` para obter respostas |

---

## ❌ Troubleshooting

### Erro: `OpenAI API key not found`
**Causa**: Variável `OPENAI_API_KEY` não configurada  
**Solução**: 
```bash
# Opção 1: Adicionar ao .env
echo "OPENAI_API_KEY=sk-xxxxx" >> .env

# Opção 2: Exportar como variável de ambiente
export OPENAI_API_KEY=sk-xxxxx
```

### Erro: `Connection refused: 127.0.0.1:5433`
**Causa**: PostgreSQL não está rodando  
**Solução**: 
```bash
docker-compose up -d
docker-compose ps  # Verificar status
```

### Erro: `FileNotFoundError: document.pdf`
**Causa**: Arquivo PDF não encontrado no diretório raiz  
**Solução**: 
```bash
# Adicione o arquivo PDF na raiz do projeto
ls -la document.pdf
```

### Erro: `FATAL: password authentication failed`
**Causa**: Credenciais incorretas no `.env`  
**Solução**: Usar credenciais padrão do docker-compose.yml:
```env
PGVECTOR_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:5433/rag_desafio
```

### Erro: `relation "langchain_pg_collection" does not exist`
**Causa**: Banco não foi inicializado (ingestão não foi executada)  
**Solução**: 
```bash
python src/ingest.py  # Executar ingestão primeiro
```

### Erro: `No chunks found / No relevant documents for this query`
**Causa**: PDF ingerido mas nenhum chunk é semanticamente similar à pergunta  
**Solução**: Tentar pergunta diferente ou verificar conteúdo do PDF ingerido

---
---

## 🔒 Notas Importantes

### Segurança
- **Nunca commite `.env` com chaves reais** — use `.env.example` no repo com placeholders
- Valores padrão `postgres:postgres` são apenas para desenvolvimento local
- Em produção: alterar credenciais do PostgreSQL e usar secrets manager

### Custos
- Cada ingestão e busca **consome tokens da OpenAI**
- Monitorar uso em https://platform.openai.com/usage
- Usar modelos mais econômicos se necessário (ex: `text-embedding-3-large` é mais caro)

### Performance
- O sistema busca apenas os **top-10 documentos mais relevantes** por pergunta
- Ingestão em lote é recomendada para muitos PDFs
- PostgreSQL com pgvector é otimizado para busca vetorial

---

