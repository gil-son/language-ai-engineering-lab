# 06.2. Retrieval

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://gitlab.com/gil-son/useful-images-collection/-/raw/main/png/rag1.png?ref_type=heads" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7778/7778942.png" width="80"/></td>
      <td align="center"><img src="https://gitlab.com/gil-son/useful-images-collection/-/raw/main/png/rag3.png?ref_type=heads" width="80"/></td>
      <td align="center"><img src="https://gitlab.com/gil-son/useful-images-collection/-/raw/main/png/rag4.png?ref_type=heads" width="80"/></td>
    </tr>
  </table>
</div>

## 06.2.1. Retrieval Strategies

---

### <img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="40"/> Introduction

**Retrieval** is the query-time engine of a RAG pipeline. Once the knowledge base is built — documents loaded, preprocessed, chunked, embedded, and stored — retrieval is what happens every time a user asks a question.

Given a query, the retrieval stage must find the most relevant chunks from the vector store and return them to the generation stage. This sounds straightforward, but query quality, search technique, and result ranking all have a dramatic impact on the final answer.

A well-designed retrieval stage handles ambiguous queries, narrow questions, long natural-language questions, and even multi-part questions — returning the right chunks with high precision, even across a corpus of millions of documents.

---

### <img src="https://cdn-icons-png.flaticon.com/512/5557/5557844.png" width="40"/> Why Use It?

Even with a perfect knowledge base, poor retrieval means poor answers. Retrieval is the bottleneck between stored knowledge and generated responses:

- **Relevance determines quality**: the LLM can only synthesize what it receives. If the wrong chunks are retrieved, the answer will be wrong or hallucinated — no matter how capable the model is.
- **Queries are noisy**: users rarely phrase questions in the same language as the documents. Retrieval strategies like query rewriting and expansion bridge this gap.
- **Single-vector search has limits**: one embedding per query assumes the question has one intent. Multi-query and decomposition strategies handle complex, multi-part questions.
- **Re-ranking improves precision**: the initial vector search optimizes for recall; re-ranking re-scores results for precision before passing them to the LLM.

Investing in retrieval strategy design consistently delivers the highest ROI in RAG pipeline optimization.

---

### <img src="https://cdn-icons-png.flaticon.com/512/7527/7527144.png" width="40"/> How It Works

```
User Query
    │
    ▼
┌─────────────────────────┐
│    QUERY PROCESSING     │
│  embed / transform /    │
│  expand the query       │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│    SEARCH / RETRIEVAL   │
│  semantic, hybrid,      │
│  filtered, multi-query  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  RANKING & REFINEMENT   │
│  re-rank, score,        │
│  deduplicate, top-K     │
└───────────┬─────────────┘
            │
            ▼
  Top-K Relevant Chunks
  (passed to Generation stage)
```

The pipeline has three sequential sub-stages: **Query Processing** prepares and optionally transforms the query before search. **Search** performs the actual lookup against the vector store. **Ranking and Refinement** post-processes the raw results to maximize relevance before passing them to the LLM.

---

### <img src="https://cdn-icons-png.flaticon.com/512/2299/2299623.png" width="40"/> Components

---

#### 1. Query Processing

##### Query Embedding

The most fundamental step: the user's raw query is passed through the **same embedding model** used at ingestion time, producing a vector that can be compared against stored chunk vectors.

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
query = "What are the main chunking strategies for RAG?"
query_vector = embeddings.embed_query(query)
# Returns: list of 1536 floats
```

> ⚠️ **Critical**: query and document embeddings must use the same model. Mixing models produces meaningless similarity scores.

---

##### Query Transformation — Decomposition

Complex, multi-part questions are split into simpler sub-questions. Each sub-question is retrieved independently, and the results are merged before generation. This prevents a single composite query from retrieving chunks that only partially address the question.

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini")

decomposition_prompt = PromptTemplate.from_template("""
Break the following question into 2-4 simpler sub-questions that together cover the full intent.
Return only the sub-questions, one per line.

Question: {question}
""")

def decompose_query(question: str) -> list[str]:
    response = llm.invoke(decomposition_prompt.format(question=question))
    return [q.strip() for q in response.content.strip().split("\n") if q.strip()]

sub_questions = decompose_query(
    "How does RAG work and what are the main differences between FAISS and Pinecone?"
)
# Returns:
# ["How does RAG work?",
#  "What is FAISS and what are its main features?",
#  "What is Pinecone and what are its main features?",
#  "What are the key differences between FAISS and Pinecone?"]
```

---

##### Query Transformation — Rewriting

Rewrites the query to be more explicit, detailed, or document-like — improving alignment with how the knowledge base was written. Particularly useful when user queries are short, ambiguous, or colloquial.

```python
rewrite_prompt = PromptTemplate.from_template("""
Rewrite the following user question to be more specific and detailed,
as if it were a passage from a technical document. Do not answer it.

Original question: {question}
Rewritten:
""")

def rewrite_query(question: str) -> str:
    return llm.invoke(rewrite_prompt.format(question=question)).content.strip()

rewritten = rewrite_query("how does rag work")
# Returns: "Retrieval-Augmented Generation (RAG) is a technique that combines
# a retrieval system with a language model to generate answers grounded in..."
```

---

##### Query Expansion

Generates **multiple alternative phrasings** of the same query. Each variant is embedded and searched independently, broadening the recall net to capture relevant chunks that might not surface under a single query formulation.

```python
expansion_prompt = PromptTemplate.from_template("""
Generate 3 alternative phrasings of the following question that preserve its meaning
but use different vocabulary and structure.

Question: {question}
Alternatives (one per line):
""")

def expand_query(question: str) -> list[str]:
    response = llm.invoke(expansion_prompt.format(question=question))
    variants = [q.strip() for q in response.content.strip().split("\n") if q.strip()]
    return [question] + variants  # include original

variants = expand_query("What embedding models work best for RAG?")
```

---

#### 2. Search Techniques

##### Semantic Search (Vector Similarity)

The baseline retrieval technique. The query vector is compared against all stored chunk vectors using a similarity metric (typically cosine), and the top-K most similar chunks are returned.

```python
from langchain_community.vectorstores import Chroma

vectorstore = Chroma(collection_name="rag_docs", embedding_function=embeddings)

results = vectorstore.similarity_search(
    query="What are the best embedding models for RAG?",
    k=5
)

for doc in results:
    print(doc.page_content[:200])
    print(doc.metadata)
```

With similarity scores:

```python
results_with_scores = vectorstore.similarity_search_with_score(
    "embedding models for RAG", k=5
)
for doc, score in results_with_scores:
    print(f"Score: {score:.4f} | {doc.page_content[:100]}")
```

---

##### Hybrid Search (Keyword + Vector)

Combines **dense vector similarity** (semantic) with **sparse keyword matching** (BM25 / TF-IDF). The scores from both methods are fused using Reciprocal Rank Fusion (RRF) or weighted combination. Best for corpora where exact terms matter (product codes, names, IDs) alongside semantic meaning.

```python
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

# Keyword retriever
bm25_retriever = BM25Retriever.from_documents(chunks)
bm25_retriever.k = 5

# Semantic retriever
semantic_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Ensemble: 40% keyword + 60% semantic
hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, semantic_retriever],
    weights=[0.4, 0.6]
)

results = hybrid_retriever.invoke("BM25 retrieval for RAG pipelines")
```

---

##### Metadata / Filtered Retrieval

Applies structured **pre-filters** on document metadata before or alongside vector search. Dramatically improves precision when queries are naturally scoped (by date, author, document type, language, etc.).

```python
# Chroma metadata filter
results = vectorstore.similarity_search(
    "retrieval augmented generation overview",
    k=5,
    filter={"language": "en", "doc_type": "pdf"}
)

# Qdrant with must-match filter
from qdrant_client.models import Filter, FieldCondition, MatchValue

results = vectorstore.similarity_search(
    "RAG pipeline evaluation",
    k=5,
    filter=Filter(
        must=[
            FieldCondition(key="language", match=MatchValue(value="en")),
            FieldCondition(key="year", match=MatchValue(value=2024))
        ]
    )
)
```

---

##### Multi-Query Retrieval

Generates several rephrased versions of the original query, retrieves results for each, and merges them with deduplication. This naturally expands recall without requiring explicit query expansion prompts.

```python
from langchain.retrievers.multi_query import MultiQueryRetriever

base_retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever,
    llm=llm
)

# Internally generates ~3 query variants and merges results
results = multi_query_retriever.invoke("How do I evaluate a RAG pipeline?")
print(f"Retrieved {len(results)} unique chunks")
```

---

#### 3. Ranking and Refinement

##### Re-Ranking (Cross-Encoder / BM25 Hybrid)

Initial vector search optimizes for **recall** — finding broadly relevant chunks. Re-ranking adds a second pass that scores each retrieved chunk against the query using a more powerful (but slower) cross-encoder model, reordering results for **precision**.

```python
from sentence_transformers import CrossEncoder

cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query: str, docs: list, top_n: int = 3):
    pairs = [(query, doc.page_content) for doc in docs]
    scores = cross_encoder.predict(pairs)
    ranked = sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)
    return [doc for _, doc in ranked[:top_n]]

# Step 1: broad retrieval
candidates = vectorstore.similarity_search(query, k=10)
# Step 2: precise re-ranking
top_docs = rerank(query, candidates, top_n=3)
```

With Cohere's managed re-ranker:

```python
from langchain_cohere import CohereRerank
from langchain.retrievers import ContextualCompressionRetriever

reranker = CohereRerank(model="rerank-english-v3.0", top_n=3)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=vectorstore.as_retriever(search_kwargs={"k": 10})
)

results = compression_retriever.invoke("RAG re-ranking techniques")
```

---

##### Relevance Scoring

Assigns an explicit relevance score to each retrieved chunk relative to the query. Used for filtering out low-confidence results before passing them to the LLM.

```python
results_with_scores = vectorstore.similarity_search_with_relevance_scores(
    "evaluation metrics for RAG", k=10
)

# Filter: keep only chunks with relevance score > 0.75
threshold = 0.75
filtered = [(doc, score) for doc, score in results_with_scores if score >= threshold]

print(f"Retained {len(filtered)} / {len(results_with_scores)} chunks above threshold")
```

---

##### Context Refinement

Removes redundant or low-value content from retrieved chunks before passing them to the LLM. Reduces token usage and improves generation focus.

```python
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers import ContextualCompressionRetriever

# Extract only the relevant sentences from each retrieved chunk
compressor = LLMChainExtractor.from_llm(llm)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever(search_kwargs={"k": 5})
)

refined_docs = compression_retriever.invoke("What is HNSW indexing?")
```

---

##### Top-K Selection Strategies

Choosing K involves a precision/recall/cost trade-off:

| K Value | Effect | Best For |
|---------|--------|----------|
| K = 3–5 | High precision, narrow context | Factual Q&A, short answers |
| K = 5–10 | Balanced recall and context size | General knowledge base |
| K = 10–20 | High recall (before re-ranking) | Complex queries, then re-rank to 3–5 |

```python
# Dynamic K based on query complexity
def adaptive_k(query: str) -> int:
    word_count = len(query.split())
    if word_count <= 5:
        return 3    # short, specific query
    elif word_count <= 15:
        return 6    # medium query
    else:
        return 10   # complex multi-part query

k = adaptive_k(query)
results = vectorstore.similarity_search(query, k=k)
```

---

### <img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="40"/> Use Cases

| Scenario | Query Processing | Search Technique | Ranking |
|----------|-----------------|-----------------|---------|
| **Simple FAQ bot** | Query embedding only | Semantic search | Top-K (K=3) |
| **Legal document search** | Query rewriting | Hybrid (BM25 + vector) | Cross-encoder re-rank |
| **Multi-topic research assistant** | Query decomposition | Multi-query retrieval | Relevance score filter |
| **Time-scoped news retrieval** | Query embedding | Semantic + metadata filter (date range) | Top-K |
| **Low recall / high noise corpus** | Query expansion | Multi-query + hybrid | Re-rank + context refinement |
| **Multilingual knowledge base** | Language-aware rewriting | Semantic (multilingual model) | Cross-encoder re-rank |
| **Product catalog search** | Query embedding | Hybrid (SKU keyword + semantic) | Metadata filter + top-K |

---

**Retrieval Strategy Selection Guide:**

```
Is your recall too low (missing relevant chunks)?
  → Add query expansion or multi-query retrieval

Are irrelevant chunks reaching the LLM?
  → Add cross-encoder re-ranking or relevance score threshold

Do queries contain exact terms (IDs, names, codes)?
  → Use hybrid search (BM25 + vector)

Are queries scoped by date, author, or category?
  → Add metadata filtering

Are questions complex or multi-part?
  → Use query decomposition

Is the LLM receiving too many tokens per call?
  → Use context refinement / compression

Starting fresh with no known issues?
  → Semantic search + K=5 + cosine similarity (solid default)
```

---

> **Next Step →** Retrieved chunks are passed to the **Generation** stage (`06-3-1-Generation-and-Synthesis.md`), where they are injected into a prompt and a language model synthesizes a grounded, accurate answer.
