# 06.1. Ingest Documents

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2342/2342156.png" width="80"/></td>
      <td align="center"><img src="https://gitlab.com/gil-son/useful-images-collection/-/raw/main/png/rag2.png?ref_type=heads" width="80"/></td>
      <td align="center"><img src="https://gitlab.com/gil-son/useful-images-collection/-/raw/main/png/rag3.png?ref_type=heads" width="80"/></td>
      <td align="center"><img src="https://gitlab.com/gil-son/useful-images-collection/-/raw/main/png/rag4.png?ref_type=heads" width="80"/></td>
    </tr>
  </table>
</div>

## 06.1.3. Embeddings and Vector Storage

---

### <img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="40"/> Introduction

**Embeddings and Vector Storage** form the backbone of semantic search in a RAG pipeline. After documents are loaded, preprocessed, and chunked, each chunk must be converted into a numerical representation — a **vector embedding** — that captures its meaning. These vectors are then stored in a **vector database** that supports fast similarity search.

This stage is what makes RAG fundamentally different from keyword search: instead of matching exact words, the system retrieves chunks based on *semantic similarity* — meaning that a query about "automobile fuel efficiency" can match a chunk discussing "miles per gallon for cars," even with no word overlap.

---

### <img src="https://cdn-icons-png.flaticon.com/512/5557/5557844.png" width="40"/> Why Use It?

Traditional keyword search (like BM25 or SQL `LIKE`) fails when the vocabulary of the query doesn't match the vocabulary of the document. Embedding-based retrieval solves this by encoding both queries and documents into a shared **semantic vector space** where proximity means similarity of meaning.

Key benefits:

- **Semantic understanding**: Retrieves conceptually related content, not just lexically matching content.
- **Language-agnostic similarity**: Cross-lingual embeddings can retrieve across languages.
- **Scalability**: Approximate nearest-neighbor (ANN) indices like HNSW and IVF enable sub-millisecond search over millions of vectors.
- **Composability**: Vector search can be combined with metadata filtering and keyword search (hybrid retrieval) for best-of-both-worlds precision.

---

### <img src="https://cdn-icons-png.flaticon.com/512/7527/7527144.png" width="40"/> How It Works

```
Chunks (text + metadata)
        │
        ▼
  Embedding Model
  (text → float vector [0.12, -0.87, ..., 0.34])
        │
        ▼
  Vector + Metadata stored
  in Vector Database
        │
        ▼
  At query time:
  Query → embedding → ANN search → Top-K chunks returned
```

**At ingestion time**: each text chunk is passed through an embedding model, producing a dense vector (e.g., 1536 dimensions for `text-embedding-3-small`). That vector is stored alongside the original text and its metadata.

**At query time**: the user's query is embedded using the *same model*, and the vector database performs a nearest-neighbor search to find the stored vectors most similar to the query vector.

---

### <img src="https://cdn-icons-png.flaticon.com/512/2299/2299623.png" width="40"/> Components

#### 1. Embedding Generation

##### Embedding Models

An embedding model encodes a piece of text as a fixed-length numerical vector. The model is trained so that semantically similar texts produce geometrically close vectors.

| Provider | Model | Dimensions | Notes |
|----------|-------|-----------|-------|
| OpenAI | `text-embedding-3-small` | 1536 | Fast, cost-effective |
| OpenAI | `text-embedding-3-large` | 3072 | Higher quality, higher cost |
| HuggingFace | `sentence-transformers/all-MiniLM-L6-v2` | 384 | Lightweight, open-source, local |
| HuggingFace | `BAAI/bge-large-en-v1.5` | 1024 | High quality, open-source |
| Cohere | `embed-english-v3.0` | 1024 | Optimized for retrieval tasks |
| Google | `text-embedding-004` | 768 | Part of Vertex AI |

**Key selection criteria:**
- **Token limit**: how many tokens the model can embed at once (e.g., 8192 for `text-embedding-3-small`)
- **Dimensions**: higher = richer representation, but more storage and slower search
- **Cost vs. quality**: hosted APIs vs. self-hosted open-source models
- **Domain fit**: general-purpose vs. domain-specific (e.g., BioBERT for medical)

##### Converting Chunks to Vectors

```python
# OpenAI
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector = embeddings.embed_query("What is retrieval augmented generation?")
# Returns: list of 1536 floats

# HuggingFace (local, no API key needed)
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector = embeddings.embed_query("What is RAG?")
```

##### Storing with Metadata

When inserting into a vector store, each vector is paired with its original text and metadata for retrieval and filtering:

```python
from langchain_community.vectorstores import Chroma

vectorstore = Chroma.from_documents(
    documents=chunks,          # list of Document objects (text + metadata)
    embedding=embeddings,      # embedding model
    persist_directory="./chroma_db"
)
```

---

#### 2. Vector Databases

A vector database is purpose-built to store high-dimensional vectors and retrieve the most similar ones via **Approximate Nearest Neighbor (ANN)** search — orders of magnitude faster than exact brute-force comparison.

##### Purpose & Core Features

| Feature | Description |
|---------|-------------|
| **Fast similarity search** | ANN algorithms return top-K results in milliseconds, even over millions of vectors |
| **Indexing** | Special data structures (HNSW, IVF, PQ) organize vectors for efficient search |
| **Metadata filtering** | Pre-filter by structured fields (date, source, language) before or after vector search |
| **Upserts** | Insert new vectors or update existing ones without rebuilding the entire index |
| **Persistence** | Store indexes to disk or in managed cloud infrastructure |

##### Indexing Algorithms

| Algorithm | Full Name | Characteristics |
|-----------|-----------|----------------|
| **HNSW** | Hierarchical Navigable Small World | Graph-based; very fast queries; high memory usage; default in most DBs |
| **IVF** | Inverted File Index | Clusters vectors into buckets; scales well; slight recall trade-off |
| **PQ** | Product Quantization | Compresses vectors to reduce memory; used with IVF for large-scale |

```python
# Example: creating a FAISS index with HNSW
import faiss
import numpy as np

d = 1536           # vector dimension
index = faiss.IndexHNSWFlat(d, 32)   # 32 = number of neighbors per layer
index.add(np.array(vectors).astype('float32'))

# Search
query_vector = np.array([embedding]).astype('float32')
distances, indices = index.search(query_vector, k=5)   # top-5 results
```

##### Similarity Metrics

The vector database uses a distance or similarity metric to rank how close two vectors are:

| Metric | Formula | Use When |
|--------|---------|----------|
| **Cosine Similarity** | `cos(θ) = A·B / (‖A‖ ‖B‖)` | Vectors of varying magnitude; most common for text |
| **Dot Product** | `A · B` | When vectors are unit-normalized (equivalent to cosine); faster |
| **Euclidean Distance** | `‖A - B‖₂` | When absolute magnitude matters; less common for text |

For text embeddings, **cosine similarity** is the standard choice. Many vector databases normalize vectors internally so that dot product equals cosine similarity.

```python
from numpy import dot
from numpy.linalg import norm

def cosine_similarity(a, b):
    return dot(a, b) / (norm(a) * norm(b))
```

---

#### 3. Popular Vector Database Options

##### Chroma — Lightweight, Open-Source

Best for: development, prototyping, small-to-medium datasets, local use.

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma(
    collection_name="my_knowledge_base",
    embedding_function=OpenAIEmbeddings(),
    persist_directory="./chroma_db"
)
vectorstore.add_documents(chunks)

results = vectorstore.similarity_search("What is RAG?", k=3)
```

##### FAISS — Local, Facebook AI

Best for: high-performance local retrieval, no server needed, research workloads.

```python
from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_documents(chunks, embeddings)
vectorstore.save_local("faiss_index")

# Load and search
vectorstore = FAISS.load_local("faiss_index", embeddings)
results = vectorstore.similarity_search("RAG pipeline overview", k=5)
```

##### Pinecone — Managed Cloud

Best for: production workloads, serverless scaling, no infrastructure management.

```python
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

pc = Pinecone(api_key="YOUR_API_KEY")
index = pc.Index("my-rag-index")

vectorstore = PineconeVectorStore(index=index, embedding=embeddings)
vectorstore.add_documents(chunks)

results = vectorstore.similarity_search("document ingestion best practices", k=4)
```

##### Weaviate — Hybrid Search

Best for: combined keyword + vector search (BM25 + semantic), rich schema support.

```python
import weaviate
from langchain_weaviate import WeaviateVectorStore

client = weaviate.connect_to_local()
vectorstore = WeaviateVectorStore(client=client, index_name="Documents", text_key="content", embedding=embeddings)
vectorstore.add_documents(chunks)

# Hybrid search (vector + BM25)
results = vectorstore.similarity_search("RAG evaluation metrics", k=5)
```

##### Qdrant — Production-Grade

Best for: rich filtering, on-premise or cloud, fine-grained control over indexing.

```python
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

client = QdrantClient(":memory:")   # or url="http://localhost:6333"
vectorstore = QdrantVectorStore.from_documents(
    chunks, embeddings,
    url="http://localhost:6333",
    collection_name="rag_docs"
)

results = vectorstore.similarity_search("chunking strategies", k=3)
```

##### Milvus — Scalable, Enterprise

Best for: billion-scale vector search, distributed deployments, enterprise RAG.

```python
from langchain_milvus import Milvus

vectorstore = Milvus.from_documents(
    chunks, embeddings,
    connection_args={"host": "localhost", "port": "19530"},
    collection_name="rag_collection"
)

results = vectorstore.similarity_search("embedding models comparison", k=5)
```

---

**Comparison Summary:**

| Database | Deployment | Scale | Hybrid Search | Best For |
|----------|-----------|-------|--------------|----------|
| Chroma | Local / self-hosted | Small–Medium | No | Dev, prototyping |
| FAISS | Local (library) | Medium | No | Fast local search |
| Pinecone | Managed cloud | Large | Limited | Production, serverless |
| Weaviate | Self-hosted / cloud | Medium–Large | ✅ Yes | Hybrid search |
| Qdrant | Self-hosted / cloud | Medium–Large | ✅ Yes | Production, filtering |
| Milvus | Self-hosted / cloud | Very Large | ✅ Yes | Enterprise, billion-scale |

---

### <img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="40"/> Use Cases

| Scenario | Embedding Model | Vector DB | Similarity Metric |
|----------|----------------|-----------|-------------------|
| **Enterprise internal search** | `text-embedding-3-large` | Pinecone / Qdrant | Cosine |
| **Local development / prototyping** | `all-MiniLM-L6-v2` (HuggingFace) | Chroma / FAISS | Cosine |
| **Hybrid keyword + semantic search** | `BAAI/bge-large-en-v1.5` | Weaviate | Cosine + BM25 |
| **Medical / domain-specific RAG** | `PubMedBERT` / BioBERT | Qdrant | Cosine |
| **Billion-document corpus** | `text-embedding-3-small` | Milvus | Dot product (normalized) |
| **Multilingual knowledge base** | `multilingual-e5-large` | Weaviate / Qdrant | Cosine |
| **Real-time product recommendations** | `cohere-embed-v3` | Pinecone | Dot product |

---

> **Next Step →** With vectors stored in the vector database, the pipeline moves to the **Retrieval** stage (`06-2-1-Retrieval-Strategies.md`), where incoming queries are embedded and matched against stored chunks using semantic search, hybrid search, and re-ranking techniques.
