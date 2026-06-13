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

## 01.2.1.1 Text Preprocessing / Normalization

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="80"/> Introduction

---

Natural Language Processing (NLP) begins with **text preprocessing**, the stage where raw, unstructured text is cleaned and transformed into a consistent format suitable for computational models.

This process ensures that models receive standardized input and can focus on learning semantics rather than handling noise or inconsistencies.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/5557/5557844.png" width="80"/> Why use it?
  
---

Text preprocessing ensures that the input to NLP or LLM systems is:
- **Clean** — free from noise, typos, and irrelevant symbols
- **Consistent** — unified in structure and format
- **Efficient** — reducing unnecessary complexity before vectorization
- **Meaningful** — preserving semantic value while removing redundancy

Without preprocessing, downstream tasks like tokenization, embedding, or model inference can suffer from **data drift**, **inconsistencies**, and **lower accuracy**.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2299/2299623.png" width="80"/> Components

---

Core components of the text preprocessing pipeline include:

1. **Text Raw** — unprocessed input; may contain punctuation, emojis, typos, and irregular spacing
2. **Normalization** — unify format (lowercasing, normalize whitespace, expand contractions) 
3. **Splitting** — divide text into sentences or segments for structured processing.
3. **Tokenization** — split text into words, subwords, or characters  
4. **Embeddings** — map tokens to dense numerical vectors encoding meaning.
5. **Vectorization** — transform text into numeric representations (TF-IDF, Word2Vec, embeddings)

If we focus on Splitting:

- **Text Cleaning**: remove unwanted elements such as punctuation, HTML tags, URLs, emojis, and other noise that does not contribute to meaning.
- **Text Normalization**: standardize the text by lowercasing, normalizing whitespace, expanding contractions (e.g., don't → do not), and applying consistent formatting rules.
- **Lemmatization / Stemming (optional)**: reduce words to their base or root forms to simplify vocabulary (e.g., running → run). This is optional and more common in classic NLP than in modern LLM pipelines.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7527/7527144.png" width="80"/> How it works?

---

The pipeline converts raw input into standardized, structured, vectorized data suitable for retrieval or modeling.

Let's go focus on **Normalization** step:

#### Simple Diagram

```mermaid
graph TD
    A[Raw Text] --> B[Normalization]
    style B fill:#1971c2,stroke:#0369a1,stroke-width:2px
    B --> C[Splitting]
    C --> D[Tokenization]
    D --> E[Embedding]
    E --> F[Vector Store Ingestion]
```

After receiving Raw Text, the pipeline enters the Normalization step:
1. **Text Cleaning**: remove or fix elements that introduce noise: extra spaces, HTML tags, broken characters, emojis (optional), duplicated lines, and unwanted symbols.
2. **Text Normalization**: 
  - Apply transformations that make the text consistent:
      - lowercasing
      - trimming whitespace
      - standardizing punctuation
      - expanding contractions (e.g., don't → do not)
      - fixing common typos
      - unicode normalization
3. **Lemmatization / Stemming (optional)**:
  - Reduce words to their base form to improve linguistic consistency:
      - **Lemmatization**: reduces words to dictionary form (running → run)
      - **Stemming**: uts words to a root segment (running → runn)

```mermaid
graph TD
    A[Raw Text] --> B[Text Cleaning]
      %% ---------- Normalization ----------
        subgraph Normalization
        B --> C[Text Normalization]
        C --> D[Lemmatization / Stemming - optional]
      end
```

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="80"/> Use Cases

---

- Preprocessing text for **sentiment analysis**, **topic modeling**, and **text classification**  
- Preparing clean input for **LLM fine-tuning** or **RAG pipelines**  
- Building preprocessing modules for **chatbots** or **voice assistants**  
- Data preparation for **embedding-based retrieval systems** (e.g., ChromaDB, FAISS)

---

### <img src="https://cdn-icons-png.flaticon.com/512/6675/6675847.png" width="80"> Limitations

---

- Over-cleaning can **remove important context or meaning**  
- Lemmatization and stemming may **introduce errors** in some languages  
- Handling multilingual text adds **complexity** to preprocessing rules  
- Noise in input data can still propagate if not properly cleaned  

---

### <img src="https://cdn-icons-png.flaticon.com/512/2147/2147809.png" width="80"> Code/Notebook/Projects

 - [NLP, NLU, NLG with RAG - Make Matthew notebook from bible](https://github.com/gil-son/llm-engineering-lab/tree/main/notebooks/02-NLP-NLU-NLG)

---

### <img src="https://cdn-icons-png.flaticon.com/512/2112/2112889.png" width="80"> Videos

A few recommended resources to visualize:

<div align="center">
  <a href="https://www.youtube.com/watch?v=fLvJ8VdHLA0&t" target="_blank">
      <img width="640" height="360" src="https://i.ytimg.com/vi/fLvJ8VdHLA0/hq720.jpg?sqp=-oaymwEnCNAFEJQDSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLCjq8wRRS16ldH-MyWo-oAgb3SjzQ"/>
  </a>
</div>

