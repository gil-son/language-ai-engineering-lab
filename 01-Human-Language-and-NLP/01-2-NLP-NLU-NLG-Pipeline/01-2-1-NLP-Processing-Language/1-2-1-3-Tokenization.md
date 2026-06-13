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

## 01.2.1.3 Tokenization

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="80"/> Introduction

Tokenization is the process of breaking text into smaller units — called **tokens** — which can be words, subwords, or characters.  
These tokens are the foundation of any Natural Language Processing (NLP) or Large Language Model (LLM) pipeline.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/5557/5557844.png" width="80"/> Why use it?
  
- Models cannot directly understand raw text — they operate on numerical representations.  
- Tokenization creates a **bridge** between human-readable language and machine-readable data.  
- Efficient tokenization improves training and inference speed.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2299/2299623.png" width="80"/> Components

1. **Text Raw** — unprocessed input; may contain punctuation, emojis, typos, and irregular spacing
2. **Normalization** — unify format (lowercasing, normalize whitespace, expand contractions) 
3. **Splitting** — divide text into sentences or segments for structured processing.
3. **Tokenization** — split text into words, subwords, or characters  
4. **Embeddings** — map tokens to dense numerical vectors encoding meaning.
5. **Vectorization** — transform text into numeric representations (TF-IDF, Word2Vec, embeddings)

If we focus on **Tokenization**:

- **Tokenizer type** (Word, Subword, Character, Byte-Pair Encoding, SentencePiece)
- **Vocabulary** — the set of all tokens the model recognizes
- **Special tokens** (e.g., `[PAD]`, `[CLS]`, `[SEP]`, `<s>`, `</s>`)
- **Token IDs** — numerical identifiers assigned to tokens

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7527/7527144.png" width="80"/> How it works?


The pipeline converts raw input into standardized, structured, vectorized data suitable for retrieval or modeling.

Let's go focus on **Tokenization** step:

#### Simple Diagram

```mermaid
graph TD
    A[Raw Text] --> B[Normalization]
    B --> C[Splitting]
    C --> D[Tokenization]
    style D fill:#1971c2,stroke:#0369a1,stroke-width:2px
    D --> E[Embedding]
    E --> F[Vector Store Ingestion]
```

How we see in Splliting step we have Generate Chunks:

**Chuncks:**  ["Neural networks are amazing", "It's because we can improve and create new things"]
   

And start **Tokenization** step:

1. **Tokenizer**: the splitter output (chunks) is fed into the tokenizer, which converts text into tokens.
Modern LLM tokenizers use subword encoding (BPE, WordPiece, SentencePiece).

Example:
"Neural networks are amazing" → ["Ne", "ural", " network", "s", " are", " amazing"]

Subword tokenization ensures:

- Rare words can be represented (e.g., “neurosymbolic” → pieces)
- Vocabulary stays compact
- Better generalization across languages

2. **Token Count:**
    - Counting tokens is essential because:
      - LLMs have a **maximum context window**
      - Costs scale with **number of tokens**, not characters
      - Chunking strategy (Embedding models and RAG pipelines) depends on token length, not character length, at embedding time
      - Large chunks → overflow or truncation
      - Too small → weak retrieval performance
    - Goal:
      - Ensure each chunk fits model limits and preserves context.
  Token counting ensures your document pipeline fits within model limits.

3. **IDs are created:**  
   Tokens are mapped to vocabulary IDs:  
   `["Ne", "ural", " network", "s", " are", " amazing"] →
[101, 1045, 2293, 17953, 999, 102]`

These IDs are what models truly “see.”

```mermaid
graph TD
    A[Raw Text] --> B[Normalization]
    B --> C[Splitting]
    C --> D[Tokenization]
  %% ---------- Tokenization ----------
        subgraph Tokenization
        D --> E[Tokenizer- Convert Chunks to Tokens]
      	E --> F[Token Count]
      end
        F --> G[IDs/ Embedding]
```

4. **Embeddings:** Once tokens become IDs, the embedding model (or the LLM itself) transforms them into dense vectors.
  - Vectors represent:
     - Semantics
     - Similarity
     - Contextual meaning
  - These embeddings are then used for:
      - Retrieval
      - Search
      - Classification
      - LLM reasoning and prediction

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="80"/> Use Cases

- Preparing datasets for fine-tuning LLMs  
- Building chatbots and assistants  
- Preprocessing for translation or summarization  
- Enabling token-efficient inference in production

---

### <img src="https://cdn-icons-png.flaticon.com/512/6675/6675847.png" width="80"> Limitations

- Tokenizers trained on limited data may struggle with rare or multilingual words.  
- Different tokenization methods lead to inconsistencies across models.  
- Subword-level tokenization may break linguistic coherence.

---

### <img src="https://cdn-icons-png.flaticon.com/512/2147/2147809.png" width="80"> Code/Notebook/Projects

 - [NLP, NLU, NLG with RAG - Make Matthew notebook from bible](https://github.com/gil-son/llm-engineering-lab/tree/main/notebooks/02-NLP-NLU-NLG)

---

### <img src="https://cdn-icons-png.flaticon.com/512/2112/2112889.png" width="80"> Videos

A few recommended resources to visualize how LLMs work:

<div align="center">
  <a href="https://www.youtube.com/watch?v=hL4ZnAWSyuU" target="_blank">
      <img width="640" height="360" src="https://i.ytimg.com/vi/hL4ZnAWSyuU/hqdefault.jpg?sqp=-oaymwEnCOADEI4CSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLA2dNDV7iR-8ZybtyqHKf04ETQmGQ"/>
  </a>
</div>
<hr/>
<div align="center">
  <a href="https://www.youtube.com/watch?v=nKSk_TiR8YA&t" target="_blank">
      <img width="640" height="360" src="https://i.ytimg.com/vi/nKSk_TiR8YA/hq720.jpg?sqp=-oaymwEnCNAFEJQDSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLCpFpZaVNiXCCPuZDnT597CkpshHQ"/>
  </a>
</div>

