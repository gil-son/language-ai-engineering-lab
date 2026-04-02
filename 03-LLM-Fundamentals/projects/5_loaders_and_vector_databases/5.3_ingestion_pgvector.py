import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

# ─────────────────────────────────────────────────────────────
# Load environment
# ─────────────────────────────────────────────────────────────
load_dotenv()

required_vars = ("PGVECTOR_URL", "PGVECTOR_COLLECTION")
for k in required_vars:
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")

# ─────────────────────────────────────────────────────────────
# Load PDF
# ─────────────────────────────────────────────────────────────
current_dir = Path(__file__).parent
pdf_path = current_dir / "gpt5.pdf"

docs = PyPDFLoader(str(pdf_path)).load()

# ─────────────────────────────────────────────────────────────
# Split documents
# ─────────────────────────────────────────────────────────────
splits = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
).split_documents(docs)

if not splits:
    raise SystemExit("No text extracted from PDF")

# ─────────────────────────────────────────────────────────────
# Add metadata if not present
# ─────────────────────────────────────────────────────────────
enriched = [
    Document(
        page_content=d.page_content,
        metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
    )
    for d in splits
]

# enriched = []
# for d in splits:
#     meta = {k: v for k, v in d.metadata.items() if v not in ("", None)}
#     new_doc = Document(
#         page_content=d.page_content,
#         metadata=meta
#     )
#     enriched.append(new_doc)

ids = [f"doc-{i}" for i in range(len(enriched))]

# ─────────────────────────────────────────────────────────────
# Ollama embeddings
# ─────────────────────────────────────────────────────────────
embeddings = OllamaEmbeddings(
    model=os.getenv("OLLAMA_MODEL", "nomic-embed-text"),
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
)

# ─────────────────────────────────────────────────────────────
# PGVector store
# ─────────────────────────────────────────────────────────────
store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PGVECTOR_COLLECTION"),
    connection=os.getenv("PGVECTOR_URL"),
    use_jsonb=True,
)

store.add_documents(documents=enriched, ids=ids)