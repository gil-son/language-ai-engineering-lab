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

## 01.2.1.4 Embeddings Vectors

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="80"/> Introduction

---

Embeddings are numerical vector representations of text (words, sentences, or documents) that capture their **semantic meaning**. They allow machines to understand relationships between words — like similarity, context, and meaning — in a **continuous vector space**.

For example:
- “King” - “Man” + “Woman” ≈ “Queen”  
- Similar sentences will have similar embedding vectors.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/5557/5557844.png" width="80"/> Why use it?
  
- To represent text numerically for ML/LLM models.  
- To capture **semantic similarity** rather than surface-level similarity.  
- To enable efficient search, clustering, and reasoning over language.  
- Essential for **RAG pipelines**, **semantic search**, and **recommendation systems**.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2299/2299623.png" width="80"/> Components

1. **Text Raw** — unprocessed input; may contain punctuation, emojis, typos, and irregular spacing
2. **Normalization** — unify format (lowercasing, normalize whitespace, expand contractions) 
3. **Splitting** — divide text into sentences or segments for structured processing.
3. **Tokenization** — split text into words, subwords, or characters  
4. **Embeddings** — map tokens to dense numerical vectors encoding meaning.
5. **Vectorization** — transform text into numeric representations (TF-IDF, Word2Vec, embeddings)

If we focus on **Embeddings**:

- **Tokens → Token IDs:** The tokenizer maps each token to an integer ID from the model’s vocabulary. Example:
```
  ["intelligent", "agent"] → [49281, 1287]
```

- **Vectorization - Embedding Model:** The embedding model converts each token ID into a high-dimensional vector.
This step uses a learned embedding matrix or a transformer-based encoder to generate vectors that encode:
    - semantics
    - context
    - relationships between concepts
 Example:

```
  49281 → [0.12, -0.88, 0.47, ...] (typically 384–1536 dimensions)
```

- **Vector Representation - Output:** The final output is a dense vector that represents the meaning of the text chunk, sentence, or document. These vectors can then be used for:
similarity search
  - retrieval in RAG systems
  - clustering
  - classification
  - semantic search

The vector is what gets stored in the Vector Store, not the text itself.
Example (embedding for the whole chunk):

```
  [0.21, 0.09, -0.77, 0.33, ...]
```
---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7527/7527144.png" width="80"/> How it works?

#### Step-by-step Process

The pipeline converts raw input into standardized, structured, vectorized data suitable for retrieval or modeling.

Let's go focus on **Embeddings** step:

#### Simple Diagram

```mermaid
graph TD
    A[Raw Text] --> B[Normalization]
    B --> C[Splitting]
    C --> D[Tokenization]
    D --> E[Embedding]
    style E fill:#1971c2,stroke:#0369a1,stroke-width:2px
    E --> F[Vector Store Ingestion]
```
How we saw during Tokenization, every chunk is converted into tokens and then into Token IDs.
The Embedding step consumes those IDs and produces numeric vector representations.

- **1. Token IDs (Input to Embedding Model)**
  - Before embedding, text is already represented as integer IDs. Example:
    - Tokens: ["Ne", "ural", " network", "s"]
    - IDs: [101, 1045, 2293, 17953]

These IDs are the fundamental inputs for the embedding model.
      
- **2. Token IDs (Input to Embedding Model):** the embedding model takes each token ID (or the entire chunk) and transforms it into a dense vector using learned weights.
  - It's basically a **lookup** into a giant matrix (for token-level embeddings) **or**
  - A full forward pass through a smaller model (for text-embedding models like OpenAI text-embedding-3 or Sentence Transformers)


- **3. Vector Representation (Output):** the output is a high-dimensional vector (e.g., 768, 1024, 1536 dimensions) that mathematically captures the meaning of the text. Examples:
  ```
      [
        0.023, -0.117, 0.884, 0.002, ...  (1536 imensions)
      ]
  ```
This vector becomes the unit stored inside the Vector Database / Vector Store.

```mermaid
graph TD
    A[Tokenization] --> B[Token IDs - Input to Embedding Model]
  %% ---------- Embedding ----------
        subgraph Embedding
      	B --> C[Vectorization - Embedding Model]
        C --> D[Vector Representation - Output]
      end
        D --> E[Vector Store Ingestion]
```

In the next step, we’ll explore Vector Store Ingestion.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="80"/> Use Cases

- **Semantic Search** (find text with similar meaning)  
- **Recommendation Systems**  
- **RAG Pipelines** (Retrieve relevant documents by vector similarity)  
- **Clustering or Visualization of text**  
- **Intent Detection or Classification**  

---

### <img src="https://cdn-icons-png.flaticon.com/512/6675/6675847.png" width="80"> Limitations

- Embeddings depend on the **training corpus** → bias risk.  
- High-dimensional vectors can be **computationally expensive**.  
- Semantic similarity ≠ logical reasoning.  
- May fail for **rare words or domain-specific jargon**.

---

### <img src="https://cdn-icons-png.flaticon.com/512/2147/2147809.png" width="80"> Code/Notebook/Projects

 - [NLP, NLU, NLG with RAG - Make Matthew notebook from bible](https://github.com/gil-son/llm-engineering-lab/tree/main/notebooks/02-NLP-NLU-NLG)


---

### <img src="https://cdn-icons-png.flaticon.com/512/2112/2112889.png" width="80"> Videos

A few recommended resources to visualize:

<div align="center">
  <a href="https://www.youtube.com/watch?v=izbifbq3-eI" target="_blank">
      <img width="640" height="360" src="https://i.ytimg.com/vi/izbifbq3-eI/hq720.jpg?sqp=-oaymwEnCNAFEJQDSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLB7eYOYt31W_QwtEHOhRbTKJm0tcg"/>
  </a>
</div>
<hr/>
<div align="center">
  <a href="https://www.youtube.com/watch?v=wgfSDrqYMJ4" target="_blank">
      <img width="640" height="360" src="https://i.ytimg.com/vi/wgfSDrqYMJ4/hq720.jpg?sqp=-oaymwEnCNAFEJQDSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLB4JQaAFm37tOg6cy7IM1CgJFCIQg"/>
  </a>
</div>
