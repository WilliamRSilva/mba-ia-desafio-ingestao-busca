import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

###########################
PROMPT_TEMPLATE = """
CONTEXTO:
{results}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""
###########################

#CARREGA VARIAVEL DE AMBIENTE DO .env
load_dotenv()
    
def search_prompt(pergunta):
  #INICIA A BUSCA  
  print(f"Buscando por: '{pergunta}'...")

  #DEFINE MODELO DE EMBEDDING E CONECTA AO POSTGRES PARA REALIZAR A BUSCA DE SIMILARIDADE
  embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL","text-embedding-3-small"))

  store = PGVector(
      embeddings=embeddings,
      collection_name=os.getenv("PGVECTOR_COLLECTION"),
      connection=os.getenv("PGVECTOR_URL"),
      use_jsonb=True,
  )

  results = store.similarity_search_with_score(pergunta, k=10)

  # Formata o contexto de forma limpa para a LLM
  context_text = "\n\n---\n\n".join([res[0].page_content for res in results])

  # Preparação do Prompt 
  chat_prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

  final_prompt = chat_prompt.format(results=context_text, pergunta=pergunta)

  model = ChatOpenAI(model="gpt-5-nano", temperature=0.3)
  response = model.invoke(final_prompt)
  return response.content




