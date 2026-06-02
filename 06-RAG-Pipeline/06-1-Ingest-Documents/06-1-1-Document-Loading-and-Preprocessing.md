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

## 06.1.1. Document Loading and Preprocessing

---

### <img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="40"/> Introduction

Document Loading and Preprocessing is the **first and most critical stage** of a RAG (Retrieval-Augmented Generation) pipeline. Before a language model can answer questions grounded in your knowledge base, raw documents must be collected from various sources, cleaned, and prepared for downstream processing.

This stage acts as the **data ingestion layer** — transforming heterogeneous, raw documents into a clean, structured, and consistent format that can be reliably chunked, embedded, and stored in a vector database.

The quality of everything downstream — retrieval accuracy, answer relevance, hallucination rates — is directly shaped by how well documents are loaded and preprocessed.

---

### <img src="https://cdn-icons-png.flaticon.com/512/5557/5557844.png" width="40"/> Why Use It?

Without proper document loading and preprocessing, RAG pipelines suffer from:

- **Garbage in, garbage out**: Noisy or malformed text produces poor embeddings and irrelevant retrievals.
- **Inconsistent formats**: PDFs, HTML, CSVs, and APIs return data in wildly different structures. A unified preprocessing pipeline normalizes them.
- **Missing metadata**: Without author, date, or source tags, retrieved chunks lack the context needed for reliable attribution and filtering.
- **Duplicate content**: Repeated documents inflate the index and bias retrieval results.
- **Language mismatches**: If your pipeline assumes English but ingests multilingual documents without detection, retrieval quality degrades silently.

Investing in a robust ingestion layer ensures that every subsequent stage — chunking, embedding, retrieval — operates on high-quality, trustworthy input.

---

### <img src="https://cdn-icons-png.flaticon.com/512/7527/7527144.png" width="40"/> How It Works

The document loading and preprocessing pipeline follows a two-phase flow:

```
Raw Sources
    │
    ▼
┌─────────────────────────┐
│    DOCUMENT LOADING     │
│  (Extract raw content)  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│     PREPROCESSING       │
│  (Clean & enrich text)  │
└───────────┬─────────────┘
            │
            ▼
  Cleaned Documents with Metadata
  (ready for chunking)
```

**Phase 1 — Document Loading** reads content from its source and converts it into raw text. Different loaders handle different source types and file formats, normalizing their output into a common `Document` object containing text and basic metadata.

**Phase 2 — Preprocessing** cleans and enriches that raw text: removing noise, detecting language, deduplicating, applying OCR when needed, and extracting structured metadata. The output is a set of clean, annotated documents ready to be chunked and embedded.

---

### <img src="https://cdn-icons-png.flaticon.com/512/2299/2299623.png" width="40"/> Components

#### 1. Document Loading

##### Local Files

The most common ingestion source. Loaders parse each file format and extract plain text.

| Format | Common Tools | Notes |
|--------|-------------|-------|
| PDF | `PyPDFLoader`, `pdfplumber`, `PyMuPDF` | Layout-aware parsers handle columns and tables |
| DOCX | `Docx2txtLoader`, `python-docx` | Preserves headings and paragraph structure |
| TXT / Markdown | Direct file read | Minimal processing needed |
| CSV / Excel | `pandas`, `CSVLoader` | Row-by-row or batch ingestion |

```python
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader

# PDF
loader = PyPDFLoader("report.pdf")
docs = loader.load()

# Plain text
loader = TextLoader("notes.txt")
docs = loader.load()
```

##### APIs (External Data)

Structured or semi-structured data fetched from REST or GraphQL APIs. Often requires authentication and pagination handling.

```python
import requests

response = requests.get("https://api.example.com/articles", headers={"Authorization": "Bearer TOKEN"})
articles = response.json()

from langchain.schema import Document
docs = [Document(page_content=a["body"], metadata={"title": a["title"], "id": a["id"]}) for a in articles]
```

##### Web Scraping

HTML pages, blogs, and news sites scraped for their text content. Boilerplate (navbars, footers, ads) must be stripped.

```python
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://example.com/blog/post-1")
docs = loader.load()
```

Popular libraries: `BeautifulSoup`, `Playwright` (for JavaScript-rendered pages), `Scrapy`.

##### Databases

SQL or NoSQL databases queried and ingested row by row or in batches.

```python
import sqlite3
from langchain.schema import Document

conn = sqlite3.connect("knowledge.db")
rows = conn.execute("SELECT id, content, author FROM articles").fetchall()
docs = [Document(page_content=row[1], metadata={"id": row[0], "author": row[2]}) for row in rows]
```

##### Cloud Storage

Files stored in S3, Azure Blob, Google Cloud Storage, or Google Drive.

```python
from langchain_community.document_loaders import S3FileLoader

loader = S3FileLoader(bucket="my-bucket", key="documents/report.pdf")
docs = loader.load()
```

---

#### 2. Preprocessing

##### Text Cleaning

Removes noise that would corrupt embeddings: HTML tags, escape sequences, excessive whitespace, control characters, and meaningless symbols.

```python
import re

def clean_text(text: str) -> str:
    text = re.sub(r'<[^>]+>', '', text)          # strip HTML tags
    text = re.sub(r'\s+', ' ', text)              # normalize whitespace
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)   # remove non-ASCII noise
    text = text.strip()
    return text
```

##### OCR for Scanned Files

Scanned PDFs and images contain no machine-readable text. OCR engines extract text from pixel data.

```python
from PIL import Image
import pytesseract

image = Image.open("scanned_page.png")
text = pytesseract.image_to_string(image)
```

Alternatively, use `pdf2image` + `pytesseract` for scanned PDFs, or cloud OCR APIs (AWS Textract, Google Document AI) for higher accuracy.

##### Language Detection

Identifies the language of each document to enable language-specific processing or filtering.

```python
from langdetect import detect

lang = detect("This is an English sentence.")
# Returns: 'en'
```

Libraries: `langdetect`, `lingua`, `fasttext`.

##### Deduplication

Removes exact or near-duplicate documents to prevent index bloat and retrieval bias.

```python
import hashlib

def deduplicate(docs):
    seen = set()
    unique = []
    for doc in docs:
        h = hashlib.md5(doc.page_content.encode()).hexdigest()
        if h not in seen:
            seen.add(h)
            unique.append(doc)
    return unique
```

For near-duplicate detection: MinHash, SimHash, or cosine similarity on TF-IDF vectors.

##### Metadata Extraction

Enriches each document with structured attributes used later for filtered retrieval.

```python
from langchain.schema import Document
from datetime import datetime

doc = Document(
    page_content=clean_text(raw_text),
    metadata={
        "source": "s3://my-bucket/report.pdf",
        "author": "Jane Doe",
        "date": "2024-11-15",
        "language": "en",
        "doc_type": "pdf",
        "tags": ["finance", "Q3"]
    }
)
```

Metadata enables downstream filtering: e.g., "retrieve only documents from 2024 tagged `finance`."

---

### <img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="40"/> Use Cases

| Scenario | Loading Source | Key Preprocessing Steps |
|----------|---------------|--------------------------|
| **Internal knowledge base** | Local DOCX, PDF files | Text cleaning, metadata extraction (author, department) |
| **Customer support bot** | Database of support tickets | Deduplication, language detection, cleaning |
| **News / research assistant** | Web scraping + APIs | HTML stripping, date extraction, deduplication |
| **Legal document search** | Scanned PDFs | OCR, text cleaning, metadata (case ID, date) |
| **Multilingual FAQ bot** | Cloud storage (S3/GCS) | Language detection, per-language normalization |
| **Product documentation** | GitHub repos (Markdown) | Minimal cleaning, tag/section metadata extraction |

---

> **Next Step →** Once documents are loaded and preprocessed, they are passed to the **Chunking** stage (`06-1-2-Chunking-Strategies.md`), where each document is split into smaller, semantically coherent pieces ready for embedding.
