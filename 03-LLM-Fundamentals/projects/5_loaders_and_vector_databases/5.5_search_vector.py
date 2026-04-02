import os
from dotenv import load_dotenv

from langchain_community.embeddings import OllamaEmbeddings
from langchain_postgres import PGVector

# ─────────────────────────────────────────────────────────────
# Load environment
# ─────────────────────────────────────────────────────────────
load_dotenv()
for k in ("PGVECTOR_URL", "PGVECTOR_COLLECTION"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")

# ─────────────────────────────────────────────────────────────
# Search vector database
# ─────────────────────────────────────────────────────────────
query = "Tell me more about the gpt-5 thinking evaluation and performance results comparing to gpt-4"

embeddings = OllamaEmbeddings(model=os.getenv("OLLAMA_MODEL", "nomic-embed-text"))

store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PGVECTOR_COLLECTION"),
    connection=os.getenv("PGVECTOR_URL"),
    use_jsonb=True,
)

# ─────────────────────────────────────────────────────────────
# Perform similarity search
# ─────────────────────────────────────────────────────────────
results = store.similarity_search_with_score(query, k=3)

for i, (doc, score) in enumerate(results, start=1):
    print("="*50)
    print(f"Resultado {i} (score: {score:.2f}):")
    print("="*50)

    print("\nTexto:\n")
    print(doc.page_content.strip())

    print("\nMetadados:\n")
    for k, v in doc.metadata.items():
        print(f"{k}: {v}")

