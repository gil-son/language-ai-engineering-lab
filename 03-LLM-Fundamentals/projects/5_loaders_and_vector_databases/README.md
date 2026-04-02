# 5. Loaders and Vector Databases (LangChain + Ollama + PGVector)


## <img src="https://cdn-icons-png.flaticon.com/512/8592/8592294.png" width="80"/>  Overview

This section demonstrates how to **load data, split documents, generate embeddings with Ollama, and store/search vectors using PostgreSQL + PGVector**.

It is part of a larger repository where multiple applications coexist. Each section is **self-contained**, with its own `requirements.txt`, `.env`, and Docker configuration when needed.

---

## <img src="https://cdn-icons-png.flaticon.com/512/18310/18310876.png" width="80"/> Project Structure

Each *Python file is executable*:

```
5_loaders_and_vector_databases/
├── 5.1_loading_using_webbaseloader.py
├── 5.2_pdf_loading.py
├── 5.3_ingestion_pgvector.py
├── 5.4_ingestion_pgvector_hash_ids.py
├── 5.5_search_vector.py
├── gpt5.pdf                  # Sample PDF for loaders, splitting, and embeddings
├── docker-compose.yml         # PostgreSQL + PGVector + Adminer
├── requirements.txt           # Dependencies for this section only
└── README.md                  # You are here
```

---

## <img src="https://cdn-icons-png.flaticon.com/512/8622/8622258.png" width="80"/> Requirements

Make sure you have the following installed:

- **Python 3.11+**
- **Ollama LLM runtime** ([Ollama is running in local]("https://github.com/gil-son/language-ai-engineering-lab/blob/main/projects/11-LLM-Orchestration/langchain/ollama/README.md"))

> If you don't have Ollama installed, then verify the link on above.

- **Embedding model:** `nomic-embed-text` is essential for embeddings process. If you have Ollama installed, just follow this command:

```bash
ollama pull nomic-embed-text
```

- **Docker & Docker Compose**
> If you don't have docker and docker compose installed, Look for it on Web.



---

## <img src="https://cdn-icons-png.flaticon.com/512/7778/7778962.png" width="80"/> Environment Configuration

### <img src="https://cdn-icons-png.flaticon.com/512/1542/1542046.png" width="50"/> About gpt5.pdf File

- This file is just one pdf file with information about GPT 5. It is essential to practice the process of splitting, embeddings and loading
- Feel free to user another pdf file 

### <img src="https://cdn-icons-png.flaticon.com/512/1542/1542046.png" width="50"/> About requirements.txt File

In the requirements files of this section contains essentials aligns dependencies. Then, avoid to use anothers requirements.

### <img src="https://cdn-icons-png.flaticon.com/512/1542/1542046.png" width="50"/> About .env-example File

1. Copy the example file and rename it to **.env**:

```bash
cp .env-example .env
```

2. Use the following configuration:

```env
# Ollama (running on host)
OLLAMA_MODEL=nomic-embed-text
OLLAMA_BASE_URL=http://localhost:11434

# Postgres exposed by Docker to host
PGVECTOR_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PGVECTOR_COLLECTION=gpt5_collection
```

---
    
### <img src="https://cdn-icons-png.flaticon.com/512/9420/9420973.png" width="80"/> Docker (Postgres + PGVector)

This section includes a `docker-compose.yml` that creates:

- **PostgreSQL 17**
- **PGVector extension**
- **Adminer (DB UI)**

Start the services:

```bash
docker compose up -d
```

The PGVector extension is created automatically by a bootstrap container.

Adminer will be available at:  
👉 http://localhost:8080

**Adminer credentials:**

```
System:   PostgreSQL
Server:   postgres_rag
Username: postgres
Password: postgres
Database: rag
```

---

### <img src="https://gitlab.com/gil-son/useful-images-collection/-/raw/main/png/blue-ollama.png?ref_type=heads" width="30"/> Ollama Setup

Make sure [Ollama]("https://github.com/gil-son/language-ai-engineering-lab/blob/main/projects/11-LLM-Orchestration/langchain/ollama/README.md") is installed and running.
> If you don't have Ollama installed, then verify the link on above.

Pull the embedding model (required):

```bash
ollama pull nomic-embed-text
```

You can verify Ollama is running:

```bash
curl http://localhost:11434/api/tags
```

---

## <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7527/7527144.png" width="80"/> Step-by-Step Execution

### 1️⃣ Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

This environment is sufficient for **all scripts in this section**.

---

### 2️⃣ Run loader examples (no vector DB required)

```bash
python 5.1_loading_using_webbaseloader.py
python 5.2_pdf_loading.py
```

These scripts demonstrate:
- WebBaseLoader
- PDF loading
- Text splitting

---

### 3️⃣ Ingest PDF into PGVector

Make sure:
- Docker containers are running via Docker Compose file:

```
run docker-compose up
``` 

- Ollama is running

- Nomic is installed

Then run **one** of the ingestion scripts:

```bash
python 5.3_ingestion_pgvector.py
```

or (recommended, idempotent ingestion):

```bash
python 5.4_ingestion_pgvector_hash_ids.py
```

This step:
- Splits the PDF
- Generates embeddings with Ollama
- Stores vectors in PostgreSQL (PGVector)

---

### 4️⃣ Search vectors

After ingestion, run:

```bash
python 5.5_search_vector.py
```

This script demonstrates:
- Vector similarity search
- Retrieval from PGVector

---

## <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/18310/18310957.png" width="80"/> Runtime Architecture
    
```
Python (host)
 ├─ Ollama (host :11434)
 └─ PostgreSQL + PGVector (Docker :5432)
    └─ Interface to view data (Adminer:8080)
```

---

## <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/13332/13332886.png" width="70"/> Notes

- `PGVECTOR_COLLECTION` defines a **logical vector collection**
- Multiple collections can coexist in the same database
- `5.4_ingestion_pgvector_hash_ids.py` avoids duplicated vectors by using content hashes
- This setup mirrors **production-grade RAG ingestion pipelines**

---

Happy experimenting 🚀