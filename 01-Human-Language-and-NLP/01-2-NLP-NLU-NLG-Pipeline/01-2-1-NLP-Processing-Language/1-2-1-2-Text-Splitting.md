# 01.2.1 NLP — Processing Language

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/1713/1713860.png" width="80"/></td>
      <td align="center"><img src="https://raw.githubusercontent.com/gil-son/experimental/refs/heads/main/matrizero/v001/src/assets/images/understating-meaning.png" width="80"/></td>
      <td align="center"><img src="https://raw.githubusercontent.com/gil-son/experimental/refs/heads/main/matrizero/v001/src/assets/images/generating-text.png" width="80"/></td>
      <td align="center"><img src="https://raw.githubusercontent.com/gil-son/experimental/refs/heads/main/matrizero/v001/src/assets/images/evaluating.png" width="80"/></td>
    </tr>
  </table>
</div>

## 01.2.1.2 Text Splitting 

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="80"/> Introduction

Text splitting is the process of breaking large blocks of text into
smaller, manageable chunks.\
This is essential for NLP tasks, especially when working with LLMs that
operate on limited context windows.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/5557/5557844.png" width="80"/> Why use it?

Why use it?

-   Large texts exceed LLM context window limits
-   Efficient indexing for RAG pipelines
-   Enables parallel processing
-   Reduces noise and improves embedding quality
-   Allows chunk-level retrieval instead of retrieving entire documents

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2299/2299623.png" width="80"/> Components

Core components of the text preprocessing pipeline include:

1. **Text Raw** — unprocessed input; may contain punctuation, emojis, typos, and irregular spacing
2. **Normalization** — unify format (lowercasing, normalize whitespace, expand contractions) 
3. **Splitting** — divide text into sentences or segments for structured processing.
3. **Tokenization** — split text into words, subwords, or characters  
4. **Embeddings** — map tokens to dense numerical vectors encoding meaning.
5. **Vectorization** — transform text into numeric representations (TF-IDF, Word2Vec, embeddings)

If we focus on **Splitting**:
- **Choose Splitter**  
  Select a splitting method or library (e.g., LangChain RecursiveCharacterTextSplitter, SentenceSplitter, MarkdownSplitter).  
  The splitter defines the rules and hierarchy used when breaking the document.

- **Chunk Size**  
  Maximum number of **characters or tokens** per chunk.  
  Character-based splitting is more common because it keeps text readable and compatible with downstream steps.

- **Chunk Overlap**  
  Amount of repeated text between chunks.  
  Provides continuity so retrieval does not miss context around chunk boundaries.

- **Split Text (Strategy)**  
  How the splitter breaks the text:  
  - By characters (most common in RAG)  
  - By sentences  
  - By paragraphs  
  - By Markdown/HTML structure  
  - By semantic similarity (advanced)

- **Generate Chunks**
Produce the final list of processed text segments.
Each chunk includes:
- The selected slice of text
- The defined overlap (if any)
- Clean boundaries aligned with the chosen strategy
These chunks are now ready to be embedded or indexed, ensuring efficient and context-aware retrieval.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7527/7527144.png" width="80"/> How it works?

---

The pipeline converts raw input into standardized, structured, vectorized data suitable for retrieval or modeling.

Let's go focus on Splitting step:

#### Simple Diagram

```mermaid
graph TD
    A[Raw Text] --> B[Normalization]
    B --> C[Splitting]
    style C fill:#1971c2,stroke:#0369a1,stroke-width:2px
    C --> D[Tokenization]
    D --> E[Embedding]
    E --> F[Vector Store Ingestion]
```

We received a block of Normalized Text, and now we start the Splitting process:
1. **Choose Splitter**: Here we choose which strategy or library will break the text.
This includes selecting tools such as RecursiveCharacterTextSplitter, SentenceSplitter, MarkdownSplitter, or any custom rule-based splitter.
The splitter determines the hierarchy (characters → sentences → paragraphs → sections) and how strictly boundaries are respected.
2. **Define Chunk Size & Overlap**: After deciding the splitter, we set the **maximum chunk length** (characters or tokens) and the overlap size.
This controls how large each chunk can be and how much context should repeat across chunks to preserve meaning at boundaries.
3. **Split Text**: The splitter now traverses the normalized text and applies its rules.
Depending on the selected strategy, it may break text by:
- character windows
- sentence boundaries
- paragraphs
- markdown/HTML sections
- or semantic boundaries
The output at this stage is a list of raw segments before overlap insertion.
5. **Generate Chunks**: Finally, the system assembles the processed segments into final chunks, applying overlap and trimming boundaries if needed.
The result is a structured list of chunks ready for tokenization and embedding, each carrying consistent context and size.

```mermaid
graph TD
    A[Raw Text] --> B[Normalization]
    B --> C[Choose Splitter]
      %% ---------- Splitting ----------
        subgraph Splitting
        C --> D[Define Chunk Size & Overlap]
      	D --> E[Split Text]
      	E --> F[Generate Chunks]
      end
```

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="80"/> Use Cases

[In the soon]

### <img src="https://cdn-icons-png.flaticon.com/512/6675/6675847.png" width="80"> Limitations

-   Overlapping increases computational cost\
-   Very small chunks reduce semantic meaning\
-   Incorrect strategy harms retrieval quality\
-   Token-level splitting may cut sentences unnaturally

---


### <img src="https://cdn-icons-png.flaticon.com/512/2147/2147809.png" width="80"> Code/Notebook/Projects

- [NLP, NLU, NLG with RAG - Make Matthew notebook from bible](https://github.com/gil-son/llm-engineering-lab/tree/main/notebooks/02-NLP-NLU-NLG)
---

### <img src="https://cdn-icons-png.flaticon.com/512/2112/2112889.png" width="80"> Videos

A few recommended resources to visualize:

<div align="center">
  <a href="https://www.youtube.com/watch?v=8OJC21T2SL4" target="_blank">
      <img width="640" height="360" src="https://i.ytimg.com/vi/8OJC21T2SL4/hq720.jpg?sqp=-oaymwEnCNAFEJQDSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBBVCNDPT9jYGN9hNcK7iOppT0xTQ"/>
  </a>
</div>
