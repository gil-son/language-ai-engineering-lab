# 07. Context Engineering

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/10087/10087719.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6062/6062189.png" width="80"/></td>
    </tr>
  </table>
</div>
<br/>

---

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/9722/9722973.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/11149/11149936.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2351/2351559.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2581/2581996.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/1990/1990934.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6062/6062146.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6062/6062142.png" width="80"/></td>
    </tr>
  </table>
</div>
<br/>

## 07.3. RAG Pipelines — Review

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="80"/> Introduction

---

> **Note —** This is a review. Retrieval-Augmented Generation has its own complete section in this lab. This page is a short recap; its real purpose is to explain **why RAG belongs to Context Engineering**.
>
> **Full section:** **[06-RAG-Pipeline](https://github.com/gil-son/language-ai-engineering-lab/tree/main/06-RAG-Pipeline)**

RAG grounds a model's answers in **external, authoritative data** retrieved at question time, instead of relying only on what the model memorized during training. It is the main tool for reducing hallucinations and giving source-traceable answers.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/5557/5557844.png" width="80"/> Why it belongs to Context Engineering

---

Context Engineering is about giving the model **the right information at the right time**. RAG is the mechanism that *brings external information into the context* — so it is a core pillar, not a separate topic.

Three basic reasons RAG is part of Context Engineering:

1. **It supplies the knowledge the model doesn't have.** A model only knows what it was trained on. RAG is how a system adds fresh, private, or domain-specific facts to the context at runtime. That is literally "engineering the context."

2. **It decides what enters the context window.** Retrieval chooses *which* documents get placed into the prompt. Choosing what the model does and does not see is the central job of Context Engineering.

3. **It must share the context budget with everything else.** Retrieved documents compete for space with instructions, memory, and conversation history. Deciding how much of the window RAG is allowed to use is a system-level trade-off that only makes sense at the Context Engineering layer.

```
RAG feeds one slot of the assembled prompt:

[1] Role & instructions      <- Prompt Engineering  (07-2)
[2] Retrieved knowledge      <- RAG                 (this page)
[3] Long-term user facts     <- Memory              (07-4)
[4] Conversation history     <- State / History     (07-5)
[5] Output format contract   <- Structured Outputs  (07-6)
[6] User question            <- runtime input
```

> In short: RAG on its own is a retrieval technique. Inside Context Engineering, it becomes a **governed context source** — budgeted, balanced against memory and history, and measured for how well it grounds the answer.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2299/2299623.png" width="80"/> Quick Recap

---

The essential stages, covered in full in [06-RAG-Pipeline](https://github.com/gil-son/language-ai-engineering-lab/tree/main/06-RAG-Pipeline):

| Stage | One-line summary |
|---|---|
| **Ingestion** | Load raw documents from their sources |
| **Chunking** | Split documents into retrievable units (fixed, semantic, document-aware) |
| **Embedding** | Convert chunks into vectors with an embedding model |
| **Indexing** | Store vectors in a vector database for fast search |
| **Retrieval** | Find the most relevant chunks for a query (cosine, MMR, hybrid BM25 + dense) |
| **Reranking** | Reorder candidates with a stronger relevance model |
| **Grounding** | Inject retrieved chunks into the prompt as context |
| **Synthesis** | The model generates an answer grounded in that context, ideally with citations |

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="80"/> Continue Learning

---

This recap intentionally stays high-level. For chunking strategies, embedding models, retrieval algorithms, reranking, and evaluation, go to the complete section:

**[06-RAG-Pipeline — Full Section](https://github.com/gil-son/language-ai-engineering-lab/tree/main/06-RAG-Pipeline)**
