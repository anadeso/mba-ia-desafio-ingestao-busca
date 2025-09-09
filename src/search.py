import os 
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


load_dotenv()
for k in ("OPENAI_API_KEY", "PGVECTOR_URL","PGVECTOR_COLLECTION"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")
    
PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

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

def search_prompt(question=str):
    try:
        embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL", "text-embedding-3-small"))
        store = PGVector(
          embeddings=embeddings,
          collection_name=os.getenv("PGVECTOR_COLLECTION"),
          connection=os.getenv("PGVECTOR_URL"),
          use_jsonb=True,
        )

        model = ChatOpenAI(model="gpt-5-nano", temperature=0)
        prompt_template = PromptTemplate(
            input_variables=["contexto", "pergunta"],
            template=PROMPT_TEMPLATE
        )
        
        results = store.similarity_search_with_score(question, k=10)
       
        contexto = "\n\n".join(doc.page_content for doc, _ in results).strip()
        
        if not contexto:
            return "Não tenho informações necessárias para responder sua pergunta."
        
        chain = prompt_template | model
        response = chain.invoke({"contexto": contexto, "pergunta": question})
        answer = (getattr(response, "content", None) or "").strip()

        return answer or "Não tenho informações necessárias para responder sua pergunta."
    except Exception as e:
        return f" Erro ao executar busca: {e}"