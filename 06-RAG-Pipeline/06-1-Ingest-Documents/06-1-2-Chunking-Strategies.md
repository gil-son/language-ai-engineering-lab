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

## 06.1.2. Chunking Strategies

---

### <img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="40"/> Introduction

**Chunking** is the process of splitting preprocessed documents into smaller, discrete pieces — called *chunks* — that are individually embedded and stored in a vector database.

This step sits between document loading and embedding generation. It is deceptively simple in concept but profoundly impactful in practice: the size, shape, and boundaries of your chunks directly determine the quality of retrieval, and therefore the quality of the final generated answer.

Chunks that are too large carry too much irrelevant content and dilute the retrieved signal. Chunks that are too small lose surrounding context and produce cryptic, incomplete results. The right chunking strategy depends on your document types, query patterns, and embedding model's token limits.

---

### <img src="https://cdn-icons-png.flaticon.com/512/5557/5557844.png" width="40"/> Why Use It?

Embedding models have **fixed context windows** (typically 512–8192 tokens). You cannot embed an entire book or a 50-page report as a single unit. Chunking solves this by breaking content into embeddable pieces.

Beyond technical necessity, good chunking:

- **Improves retrieval precision**: Smaller, focused chunks match narrower queries more accurately than large, multi-topic blocks.
- **Reduces hallucination**: The LLM receives only the most relevant context, with less noise to misinterpret.
- **Controls cost**: Smaller context windows passed to the LLM at generation time reduce token usage and latency.
- **Enables granular attribution**: Each chunk can be individually cited, allowing precise source references in the final answer.

Choosing the wrong chunking strategy is one of the most common causes of poor RAG performance.

---

### <img src="https://cdn-icons-png.flaticon.com/512/7527/7527144.png" width="40"/> How It Works

The general chunking flow:

```
Preprocessed Document (full text)
        │
        ▼
  Apply Chunking Strategy
  (split by size, structure, or semantics)
        │
        ▼
  List of Chunks
  [chunk_1, chunk_2, chunk_3, ...]
        │
        ▼
  Each chunk inherits metadata
  from the parent document
        │
        ▼
  Ready for Embedding
```

Each resulting chunk is a `Document` object containing:
- `page_content`: the text of this chunk
- `metadata`: inherited from the parent (source, author, date) plus chunk-level info (chunk index, page number)

---

### <img src="https://cdn-icons-png.flaticon.com/512/2299/2299623.png" width="40"/> Components

#### 1. Fixed-Size Chunking (500–1000 tokens)

The simplest and most common strategy. Text is split at regular character or token intervals, regardless of sentence or paragraph boundaries.

- **When to use**: General-purpose pipelines, mixed document types, when simplicity matters.
- **Risk**: Can cut mid-sentence, severing meaning across chunk boundaries.

```python
from langchain.text_splitter import CharacterTextSplitter

splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0, separator="\n")
chunks = splitter.split_documents(docs)
```

**Visual:**
```
[   Document Text   ]
[chunk_1][chunk_2][chunk_3]...
```

**Typical sizes:**
| Use Case | Chunk Size |
|----------|-----------|
| Short Q&A, FAQs | 256–512 tokens |
| General knowledge base | 512–1000 tokens |
| Long-form documents | 1000–2000 tokens |

---

#### 2. Overlapping Chunks (Preserve Context)

Extends fixed-size chunking by adding a configurable **overlap** — a number of tokens from the end of one chunk that is repeated at the start of the next. This prevents important context from being lost at chunk boundaries.

- **When to use**: Documents with dense, continuous prose where cross-boundary context matters (legal text, research papers, narratives).
- **Trade-off**: Increases total chunk count and index size.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,       # 200 tokens repeated between consecutive chunks
    separators=["\n\n", "\n", " ", ""]
)
chunks = splitter.split_documents(docs)
```

**Visual:**
```
[        chunk_1        ]
              [        chunk_2        ]
                            [        chunk_3        ]
              ↑ overlap ↑   ↑ overlap ↑
```

A 15–20% overlap relative to chunk size is a common starting point.

---

#### 3. Semantic / Adaptive Chunking

Instead of splitting by character count, this strategy splits based on **meaning shifts** — using embedding similarity to detect where one topic ends and another begins. Chunks are formed around semantically coherent units.

- **When to use**: High-quality retrieval requirements, well-structured documents, when chunk uniformity is less important than semantic coherence.
- **Trade-off**: Slower to compute; requires an embedding model at chunking time.

```python
# Using LangChain's SemanticChunker (requires an embedding model)
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

splitter = SemanticChunker(
    OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile"  # split when similarity drops significantly
)
chunks = splitter.split_documents(docs)
```

Alternatively, split on structural markers (headings, paragraph breaks, section delimiters) as a lightweight proxy for semantic boundaries.

---

#### 4. Advanced: Parent-Child Chunking

A hierarchical strategy where **large parent chunks** provide broad context and **small child chunks** are what's actually embedded and retrieved. When a child chunk is retrieved, its parent is passed to the LLM — giving the model richer context than the small child alone.

- **When to use**: When you need precise retrieval (small child chunks) but rich generation context (large parent chunks).

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.storage import InMemoryStore

# Parent splitter: large chunks
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)
# Child splitter: small chunks for embedding
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)

vectorstore = Chroma(embedding_function=embeddings)
store = InMemoryStore()

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)
retriever.add_documents(docs)
```

**Visual:**
```
[          Parent Chunk (2000 tokens)           ]
  [child_1] [child_2] [child_3] [child_4]
      ↑ embedded & retrieved
      ↑ parent returned to LLM
```

---

#### 5. Advanced: Summary / Metadata Chunking

Each chunk is augmented with an **auto-generated summary or set of hypothetical questions** that describe its content. These summaries are embedded alongside (or instead of) the raw chunk text — improving retrieval by matching the *intent* of a query rather than its literal keywords.

```python
from langchain_openai import ChatOpenAI
from langchain.schema import Document

llm = ChatOpenAI(model="gpt-4o-mini")

def summarize_chunk(chunk: Document) -> Document:
    summary = llm.invoke(f"Summarize this passage in 2 sentences:\n\n{chunk.page_content}")
    return Document(
        page_content=summary.content,
        metadata={**chunk.metadata, "original_text": chunk.page_content}
    )

summary_chunks = [summarize_chunk(c) for c in chunks]
```

The original text is stored in metadata and returned at generation time; only the summary is embedded.

---

### <img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="40"/> Use Cases

| Scenario | Recommended Strategy | Reasoning |
|----------|---------------------|-----------|
| **FAQ / Support docs** | Fixed-size (256–512 tokens) | Short answers are self-contained; overlap not needed |
| **Legal contracts** | Overlapping chunks (1000 + 200 overlap) | Dense, continuous text; cross-boundary context is critical |
| **Research papers** | Semantic / section-based | Sections are already semantically coherent units |
| **Long-form books** | Parent-Child | Retrieve precise passages, return chapter-level context |
| **Mixed document corpus** | Recursive character splitter | Balances simplicity and structure-awareness |
| **Multilingual knowledge base** | Semantic chunking per language | Different languages have different structural patterns |
| **Low retrieval recall** | Summary chunking | Boosts retrieval by matching query intent, not just keywords |

---

**Choosing the Right Strategy — Quick Guide:**

```
Is your document highly structured (headings, sections)?
  → Semantic / structure-aware chunking

Do you need precise retrieval + rich generation context?
  → Parent-Child chunking

Is retrieval recall low despite good embeddings?
  → Summary / metadata augmented chunks

Are you building a general-purpose pipeline quickly?
  → RecursiveCharacterTextSplitter with overlap (good default)

Is content dense and continuous (legal, academic)?
  → Overlapping fixed-size chunks
```

---

> **Next Step →** Once chunks are created, they are passed to the **Embedding & Vector Storage** stage (`06-1-3-Embeddings-and-Vector-Storage.md`), where each chunk is converted into a numerical vector and stored for similarity search.
