# 06.3. Generation

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://gitlab.com/gil-son/useful-images-collection/-/raw/main/png/rag1.png?ref_type=heads" width="80"/></td>
      <td align="center"><img src="https://gitlab.com/gil-son/useful-images-collection/-/raw/main/png/rag2.png?ref_type=heads" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/5695/5695072.png" width="80"/></td>
      <td align="center"><img src="https://gitlab.com/gil-son/useful-images-collection/-/raw/main/png/rag4.png?ref_type=heads" width="80"/></td>
    </tr>
  </table>
</div>

## 06.3.1. Generation and Synthesis

---

### <img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="40"/> Introduction

**Generation and Synthesis** is the final active stage of the RAG pipeline — the moment where retrieved knowledge becomes a natural language answer. After relevant chunks have been retrieved and ranked, they are combined into a structured prompt and passed to a Large Language Model (LLM), which synthesizes a grounded, coherent response.

Unlike standalone LLM prompting, RAG generation is explicitly **grounded in retrieved context**: the model is instructed to base its answer on the provided documents rather than on its parametric knowledge alone. This dramatically reduces hallucinations and enables the model to cite specific, verifiable sources.

This stage spans three sub-areas: **Context Injection** (how retrieved chunks are assembled into the prompt), **LLM Generation** (how the model produces the response), and **Post-Processing** (how the raw output is refined before delivery).

---

### <img src="https://cdn-icons-png.flaticon.com/512/5557/5557844.png" width="40"/> Why Use It?

Without a carefully designed generation stage, even perfect retrieval fails:

- **Context ordering matters**: LLMs suffer from "lost in the middle" — they attend more strongly to content at the beginning and end of a long context. Poor ordering buries the most relevant chunks in the middle.
- **Context window is finite**: retrieved chunks can exceed the LLM's token limit. Intelligent context management is essential to avoid truncation of critical information.
- **Prompts shape grounding**: without clear instructions to stay within the provided context, LLMs blend retrieved facts with hallucinated content. System prompt design is the primary defense against this.
- **Post-processing adds reliability**: raw LLM output may lack citations, have inconsistent formatting, or make claims unsupported by the retrieved chunks. Post-processing validates and enriches the output.

---

### <img src="https://cdn-icons-png.flaticon.com/512/7527/7527144.png" width="40"/> How It Works

```
Top-K Retrieved Chunks
        │
        ▼
┌──────────────────────────┐
│    CONTEXT INJECTION     │
│  combine, order, fit     │
│  chunks into prompt      │
└───────────┬──────────────┘
            │
            ▼
┌──────────────────────────┐
│     LLM GENERATION       │
│  system prompt + context │
│  + query → response      │
└───────────┬──────────────┘
            │
            ▼
┌──────────────────────────┐
│     POST-PROCESSING      │
│  cite, format, validate, │
│  score confidence        │
└───────────┬──────────────┘
            │
            ▼
    Final Answer to User
```

---

### <img src="https://cdn-icons-png.flaticon.com/512/2299/2299623.png" width="40"/> Components

---

#### 1. Context Injection

##### Combining Retrieved Documents

Retrieved chunks are concatenated into a single context block, with clear delimiters separating each chunk. Each chunk is labeled with its source metadata to enable attribution.

```python
def format_context(docs: list) -> str:
    context_parts = []
    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "Unknown")
        context_parts.append(f"[Document {i}] (Source: {source})\n{doc.page_content}")
    return "\n\n---\n\n".join(context_parts)

context = format_context(retrieved_docs)
```

---

##### Context Window Management

LLMs have fixed context windows (e.g., 128K tokens for GPT-4o, 200K for Claude). The combined context — system prompt + retrieved chunks + user query — must fit within this limit. Strategies include token counting, dynamic K reduction, and chunk truncation.

```python
import tiktoken

def fit_context_to_window(
    docs: list,
    query: str,
    system_prompt: str,
    max_tokens: int = 4000,
    model: str = "gpt-4o"
) -> list:
    enc = tiktoken.encoding_for_model(model)
    overhead = len(enc.encode(system_prompt)) + len(enc.encode(query)) + 200  # buffer
    budget = max_tokens - overhead

    selected = []
    used = 0
    for doc in docs:
        tokens = len(enc.encode(doc.page_content))
        if used + tokens <= budget:
            selected.append(doc)
            used += tokens
        else:
            break  # stop before exceeding budget

    return selected

context_docs = fit_context_to_window(retrieved_docs, query, system_prompt)
```

---

##### Document Ordering Strategies

Research shows LLMs pay more attention to content at the **beginning and end** of a long context ("lost in the middle" effect). Ordering strategies counteract this:

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| **Relevance descending** | Highest-scoring chunk first | Default; most relevant gets most attention |
| **Relevance sandwich** | Most relevant at top and bottom | When context is long and middle may be ignored |
| **Chronological** | Ordered by document date | Time-sensitive narratives or news |
| **Diversity-first** | Alternate by source/topic | Mixed-source corpora to avoid source bias |

```python
def order_documents(docs: list, strategy: str = "relevance_descending") -> list:
    if strategy == "relevance_descending":
        return docs  # assumes already sorted by retrieval score

    if strategy == "sandwich":
        # Put most relevant at start and end, less relevant in the middle
        if len(docs) <= 2:
            return docs
        mid = docs[1:-1][::-1]  # reverse middle (least relevant in center)
        return [docs[0]] + mid + [docs[-1]]

    if strategy == "chronological":
        return sorted(docs, key=lambda d: d.metadata.get("date", ""), reverse=False)

    return docs
```

---

#### 2. LLM Generation

##### Prompt Engineering (System Prompts, Few-Shot)

The system prompt is the primary mechanism for grounding the LLM in retrieved context. A well-designed system prompt explicitly instructs the model to answer only from the provided documents, cite sources, and express uncertainty when information is missing.

```python
SYSTEM_PROMPT = """You are a knowledgeable assistant. Answer the user's question based ONLY on the provided context documents.

Rules:
1. If the answer is found in the context, provide a clear, complete answer and cite the source document(s) using [Document N].
2. If the context does not contain enough information to answer the question, say: "I don't have enough information in the provided documents to answer this question."
3. Do NOT use your general knowledge. Stay strictly within the provided context.
4. Be concise but thorough. Use bullet points for multi-part answers.
"""
```

**Few-shot example** appended to the system prompt to demonstrate expected output format:

```python
FEW_SHOT_EXAMPLE = """
Example:
Context: [Document 1] HNSW (Hierarchical Navigable Small World) is a graph-based ANN algorithm...
Question: What is HNSW?
Answer: HNSW is a graph-based Approximate Nearest Neighbor algorithm used in vector databases for fast similarity search [Document 1].
"""
```

---

##### Grounding in Retrieved Context

The full prompt assembly — system prompt + formatted context + user query — sent to the LLM:

```python
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

llm = ChatOpenAI(model="gpt-4o", temperature=0)

def generate_answer(query: str, docs: list) -> str:
    context = format_context(docs)
    ordered_docs = order_documents(docs, strategy="sandwich")
    context = format_context(ordered_docs)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query}")
    ]

    response = llm.invoke(messages)
    return response.content
```

With LangChain's built-in RAG chain:

```python
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Pull standard RAG prompt from LangChain Hub
rag_prompt = hub.pull("rlm/rag-prompt")

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

answer = rag_chain.invoke("What are the main chunking strategies for RAG?")
```

---

##### Temperature and Sampling Strategies

Generation parameters control the creativity/determinism trade-off:

| Parameter | Recommended (RAG) | Effect |
|-----------|------------------|--------|
| `temperature` | 0.0 – 0.2 | Low = more factual, deterministic; high = creative but riskier |
| `top_p` | 0.9 – 1.0 | Nucleus sampling; restrict to top probability mass |
| `max_tokens` | 512 – 2048 | Cap answer length; prevent runaway generation |

```python
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.1,    # near-deterministic for factual RAG
    max_tokens=1024,
    top_p=0.95
)
```

For **creative summarization** or report generation, `temperature=0.5–0.7` is appropriate. For **strict Q&A or legal/medical RAG**, use `temperature=0.0`.

---

##### Handling Long Contexts

When the total context exceeds what a single LLM call can handle, use **map-reduce** or **refine** patterns:

```python
from langchain.chains.summarize import load_summarize_chain

# Map-Reduce: summarize each chunk independently, then combine
chain = load_summarize_chain(llm, chain_type="map_reduce")
summary = chain.invoke({"input_documents": docs})

# Refine: iteratively update the answer with each new chunk
chain = load_summarize_chain(llm, chain_type="refine")
answer = chain.invoke({"input_documents": docs, "question": query})
```

---

#### 3. Post-Processing

##### Summarization and Reformatting

Raw LLM output may be verbose or inconsistently formatted. Post-processing normalizes it for the intended delivery format (markdown, HTML, plain text, JSON for APIs).

```python
def postprocess_answer(raw_answer: str, output_format: str = "markdown") -> str:
    if output_format == "plain":
        import re
        # Strip markdown
        clean = re.sub(r'\*\*(.+?)\*\*', r'\1', raw_answer)
        clean = re.sub(r'#+\s', '', clean)
        return clean.strip()

    if output_format == "json":
        return {"answer": raw_answer.strip()}

    return raw_answer.strip()  # markdown default
```

---

##### Source Citation and Attribution

Each claim in the answer should be traceable to a specific retrieved chunk. Well-structured prompts produce inline citations; post-processing can validate and enrich them.

```python
def extract_citations(answer: str, docs: list) -> dict:
    import re
    cited_indices = [int(m) - 1 for m in re.findall(r'\[Document (\d+)\]', answer)]
    citations = {}
    for idx in set(cited_indices):
        if 0 <= idx < len(docs):
            citations[f"Document {idx+1}"] = {
                "source": docs[idx].metadata.get("source", "Unknown"),
                "excerpt": docs[idx].page_content[:200]
            }
    return citations

citations = extract_citations(answer, retrieved_docs)
```

---

##### Confidence Scoring

Assigns a confidence score to the generated answer based on retrieval quality signals. Useful for flagging uncertain answers for human review.

```python
def estimate_confidence(docs_with_scores: list, answer: str, threshold: float = 0.75) -> dict:
    if not docs_with_scores:
        return {"score": 0.0, "label": "low", "reason": "No documents retrieved"}

    scores = [s for _, s in docs_with_scores]
    avg_score = sum(scores) / len(scores)
    max_score = max(scores)

    # Penalize if LLM admitted uncertainty
    uncertainty_phrases = ["i don't have", "not enough information", "cannot determine"]
    contains_uncertainty = any(p in answer.lower() for p in uncertainty_phrases)

    final_score = avg_score * (0.7 if contains_uncertainty else 1.0)

    label = "high" if final_score >= threshold else "medium" if final_score >= 0.5 else "low"
    return {"score": round(final_score, 3), "label": label, "max_doc_score": round(max_score, 3)}
```

---

##### Chain-of-Thought Reasoning Traces

For complex questions, instruct the LLM to reason step-by-step before providing the final answer. This improves accuracy and makes the reasoning auditable.

```python
COT_SYSTEM_PROMPT = """You are a precise analytical assistant. When answering questions:

1. First, identify the relevant information from each provided document.
2. Then, reason step by step about how the information addresses the question.
3. Finally, provide a concise, well-supported answer with citations.

Format your response as:
**Reasoning:**
[your step-by-step analysis]

**Answer:**
[your final answer with citations]
"""
```

---

### <img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="40"/> Use Cases

| Scenario | Context Ordering | Prompt Strategy | Post-Processing |
|----------|-----------------|----------------|----------------|
| **Customer support FAQ** | Relevance descending | Strict grounding prompt | Source citation, plain text format |
| **Legal research assistant** | Sandwich (most relevant at top+bottom) | CoT + strict grounding | Citation extraction, confidence scoring |
| **Technical documentation Q&A** | Relevance descending | System prompt + few-shot | Markdown formatting, source links |
| **Medical information retrieval** | Sandwich | Strict grounding, low temperature (0.0) | Confidence score, uncertainty flagging |
| **Executive summary from reports** | Chronological | Map-reduce summarization | Reformatting to structured markdown |
| **Multilingual answer generation** | Relevance descending | Language-aware system prompt | Language normalization |
| **Long-document analysis** | Map-reduce / refine pattern | Chain-of-thought | Summarization + citation |

---

> **Next Step →** Once the system is in production, the pipeline moves to the **Continuous Improvement** stage (`06-4-1-Evaluation-and-Optimization.md`), where retrieval quality, generation faithfulness, and end-to-end performance are measured and optimized through systematic evaluation and feedback loops.
