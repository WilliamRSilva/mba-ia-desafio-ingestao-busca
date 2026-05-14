import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()

current_dir = Path(__file__).parent.parent
pdf_path = current_dir / "document.pdf"

print("Carregando PDF...")
docs = PyPDFLoader(str(pdf_path)).load()
print(f"PDF carregado. {len(docs)} páginas encontradas.")

splits = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=150, add_start_index=False).split_documents(docs)
if not splits:
    print("Nenhum split gerado. Encerrando.")
    raise SystemExit(0)
print(f"Documento dividido em {len(splits)} pedaços.")

enriched = [
    Document(
        page_content=d.page_content,
        metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
    )
    for d in splits
]    

ids = [f"doc-{i}" for i in range(len(enriched))]

print("Gerando embeddings e conectando ao Postgres (isso pode demorar)...")
embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL","text-embedding-3-small"))

store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PGVECTOR_COLLECTION"),
    connection=os.getenv("PGVECTOR_URL"),
    use_jsonb=True,
)

print("Enviando documentos para o banco...")
store.add_documents(documents=enriched, ids=ids)
print("Ingestão concluída com sucesso!")

# enriched = []
# for d in splits:
#     meta = {k: v for k, v in d.metadata.items() if v not in ("", None)}
#     new_doc = Document(
#         page_content=d.page_content,
#         metadata=meta
#     )
#     enriched.append(new_doc)