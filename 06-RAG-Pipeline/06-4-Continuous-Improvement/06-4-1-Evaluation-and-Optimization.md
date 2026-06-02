# 06.4. Continuous Improvement

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://gitlab.com/gil-son/useful-images-collection/-/raw/main/png/rag1.png?ref_type=heads" width="80"/></td>
      <td align="center"><img src="https://gitlab.com/gil-son/useful-images-collection/-/raw/main/png/rag2.png?ref_type=heads" width="80"/></td>
      <td align="center"><img src="https://gitlab.com/gil-son/useful-images-collection/-/raw/main/png/rag3.png?ref_type=heads" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/4064/4064650.png" width="80"/></td>
    </tr>
  </table>
</div>

## 06.4.1. Evaluation and Optimization

---

### <img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="40"/> Introduction

**Evaluation and Optimization** is the continuous improvement layer of a RAG pipeline. Deploying a RAG system is not a one-time event — knowledge bases grow, queries evolve, and model capabilities change. Without systematic evaluation, regressions go undetected and improvements remain unmeasurable.

This stage closes the feedback loop by measuring how well each component of the pipeline performs: whether retrieval surfaces the right chunks, whether the generated answer is faithful to the sources, and whether the end-to-end system satisfies real users. Evaluation data drives targeted optimization — from index updates and re-ranking tuning to fine-tuning and A/B testing.

A RAG system without evaluation is flying blind. A RAG system with rigorous evaluation becomes progressively more accurate, efficient, and trustworthy over time.

---

### <img src="https://cdn-icons-png.flaticon.com/512/5557/5557844.png" width="40"/> Why Use It?

- **Silent failures are common**: retrieval can degrade silently as the knowledge base grows or queries drift. Only measurement surfaces these issues.
- **Multi-component pipelines are hard to debug**: when a RAG answer is wrong, was it retrieval, generation, or chunking? Component-level metrics pinpoint the root cause.
- **Hallucination is not binary**: faithfulness scoring quantifies how well answers stay within retrieved context, enabling proactive detection before users notice.
- **Iteration needs a baseline**: without metrics, you cannot know whether a change (new chunk size, new embedding model, new prompt) improved or degraded performance.
- **Cost and latency matter in production**: optimizing for quality alone is insufficient. Evaluation must cover operational efficiency.

---

### <img src="https://cdn-icons-png.flaticon.com/512/7527/7527144.png" width="40"/> How It Works

```
RAG Pipeline (Retrieval + Generation)
        │
        ▼
  Evaluation Dataset
  (queries + expected answers + relevant doc IDs)
        │
        ├─────────────────────┐
        ▼                     ▼
  Retrieval Metrics      Generation Metrics
  (Precision, Recall,    (Faithfulness, Relevance,
   MRR, NDCG, Hit Rate)   Completeness, Hallucination)
        │                     │
        └──────────┬──────────┘
                   ▼
         End-to-End Metrics
         (Latency, Cost, User Satisfaction)
                   │
                   ▼
         Continuous Improvement
         (Feedback loops, Index updates,
          A/B tests, Fine-tuning, Caching)
```

---

### <img src="https://cdn-icons-png.flaticon.com/512/2299/2299623.png" width="40"/> Components

---

#### 1. Retrieval Evaluation

Retrieval evaluation measures whether the vector search returns the right chunks for a given query. An **evaluation dataset** is required: a set of `(query, relevant_doc_ids)` pairs where the ground-truth relevant documents are known.

---

##### Precision, Recall, F1

- **Precision**: of the K chunks retrieved, what fraction were actually relevant?
- **Recall**: of all relevant chunks in the index, what fraction were retrieved?
- **F1**: harmonic mean of precision and recall.

```python
def precision_at_k(retrieved_ids: list, relevant_ids: set, k: int) -> float:
    top_k = retrieved_ids[:k]
    hits = sum(1 for doc_id in top_k if doc_id in relevant_ids)
    return hits / k

def recall_at_k(retrieved_ids: list, relevant_ids: set, k: int) -> float:
    top_k = retrieved_ids[:k]
    hits = sum(1 for doc_id in top_k if doc_id in relevant_ids)
    return hits / len(relevant_ids) if relevant_ids else 0.0

def f1_at_k(retrieved_ids: list, relevant_ids: set, k: int) -> float:
    p = precision_at_k(retrieved_ids, relevant_ids, k)
    r = recall_at_k(retrieved_ids, relevant_ids, k)
    return 2 * p * r / (p + r) if (p + r) > 0 else 0.0

# Example
retrieved = ["doc_3", "doc_7", "doc_1", "doc_9", "doc_2"]
relevant = {"doc_1", "doc_3", "doc_5"}

print(f"P@5: {precision_at_k(retrieved, relevant, 5):.3f}")   # 0.400
print(f"R@5: {recall_at_k(retrieved, relevant, 5):.3f}")      # 0.667
print(f"F1@5: {f1_at_k(retrieved, relevant, 5):.3f}")         # 0.500
```

---

##### Mean Reciprocal Rank (MRR)

Measures how high the **first** relevant document appears in the ranked list. Especially useful for Q&A where one correct answer is expected.

```
MRR = (1/|Q|) × Σ (1 / rank_of_first_relevant_doc)
```

```python
def reciprocal_rank(retrieved_ids: list, relevant_ids: set) -> float:
    for rank, doc_id in enumerate(retrieved_ids, start=1):
        if doc_id in relevant_ids:
            return 1.0 / rank
    return 0.0

def mean_reciprocal_rank(results: list[tuple]) -> float:
    # results: list of (retrieved_ids, relevant_ids) pairs
    return sum(reciprocal_rank(r, rel) for r, rel in results) / len(results)

mrr = mean_reciprocal_rank([
    (["doc_3", "doc_1", "doc_7"], {"doc_1"}),  # first hit at rank 2 → 0.5
    (["doc_5", "doc_2", "doc_8"], {"doc_5"}),  # first hit at rank 1 → 1.0
    (["doc_9", "doc_4", "doc_6"], {"doc_1"}),  # no hit → 0.0
])
print(f"MRR: {mrr:.3f}")  # 0.500
```

---

##### Normalized Discounted Cumulative Gain (NDCG)

Measures retrieval quality accounting for **graded relevance** (e.g., a chunk can be highly relevant, partially relevant, or irrelevant) and **position** (higher-ranked relevant chunks score more).

```python
import numpy as np

def dcg_at_k(scores: list, k: int) -> float:
    scores = scores[:k]
    return sum(rel / np.log2(rank + 2) for rank, rel in enumerate(scores))

def ndcg_at_k(retrieved_ids: list, relevance_scores: dict, k: int) -> float:
    # relevance_scores: {doc_id: score} where score in {0, 1, 2}
    actual = [relevance_scores.get(doc_id, 0) for doc_id in retrieved_ids[:k]]
    ideal = sorted(relevance_scores.values(), reverse=True)[:k]

    dcg = dcg_at_k(actual, k)
    idcg = dcg_at_k(ideal, k)
    return dcg / idcg if idcg > 0 else 0.0

relevance = {"doc_1": 2, "doc_3": 1, "doc_5": 2}  # 2=highly relevant, 1=partially
retrieved = ["doc_1", "doc_7", "doc_3", "doc_9", "doc_5"]
print(f"NDCG@5: {ndcg_at_k(retrieved, relevance, 5):.3f}")
```

---

##### Hit Rate and Coverage

- **Hit Rate @K**: the fraction of queries where at least one relevant document appears in the top-K results. Simple and intuitive.
- **Coverage**: the fraction of queries for which the knowledge base contains any relevant answer at all.

```python
def hit_rate_at_k(eval_dataset: list[tuple], k: int) -> float:
    # eval_dataset: list of (retrieved_ids, relevant_ids) pairs
    hits = sum(
        1 for retrieved, relevant in eval_dataset
        if any(doc_id in relevant for doc_id in retrieved[:k])
    )
    return hits / len(eval_dataset)

hr = hit_rate_at_k([
    (["doc_1", "doc_3", "doc_7"], {"doc_3"}),  # hit
    (["doc_9", "doc_4", "doc_6"], {"doc_2"}),  # miss
    (["doc_5", "doc_2", "doc_8"], {"doc_5"}),  # hit
], k=3)
print(f"Hit Rate@3: {hr:.3f}")  # 0.667
```

---

#### 2. Generation Evaluation

Generation evaluation measures the quality of the LLM's output relative to the retrieved context and the user's intent. These metrics can be computed using an **LLM-as-judge** approach (a second LLM scores the output) or dedicated evaluation frameworks.

---

##### Answer Relevance

Does the generated answer address the user's question?

```python
RELEVANCE_PROMPT = """
Rate how well the following answer addresses the question on a scale of 1-5.
1 = completely off-topic, 5 = perfectly addresses the question.

Question: {question}
Answer: {answer}

Return only the integer score.
"""

def score_relevance(question: str, answer: str, llm) -> int:
    prompt = RELEVANCE_PROMPT.format(question=question, answer=answer)
    score = llm.invoke(prompt).content.strip()
    return int(score)
```

---

##### Faithfulness to Sources

Does the generated answer stay within the bounds of the retrieved context, or does it introduce facts not present in the documents?

```python
FAITHFULNESS_PROMPT = """
Given the context documents and the generated answer, identify any claims in the answer
that are NOT supported by the context.

Context:
{context}

Answer:
{answer}

List unsupported claims (if any). If all claims are supported, respond: "FULLY FAITHFUL".
"""

def evaluate_faithfulness(context: str, answer: str, llm) -> dict:
    prompt = FAITHFULNESS_PROMPT.format(context=context, answer=answer)
    result = llm.invoke(prompt).content.strip()
    is_faithful = result == "FULLY FAITHFUL"
    return {"faithful": is_faithful, "unsupported_claims": result if not is_faithful else None}
```

---

##### Completeness

Does the answer fully address all aspects of the question, or does it only partially respond?

```python
COMPLETENESS_PROMPT = """
Given the question and the answer, rate the completeness of the answer on a scale of 1-5.
1 = only addresses a small part of the question
5 = thoroughly addresses all aspects

Question: {question}
Answer: {answer}

Return only the integer score.
"""
```

---

##### Hallucination Detection

Systematically identifies generated statements that contradict or are absent from the retrieved context.

```python
from ragas.metrics import faithfulness, answer_relevancy
from ragas import evaluate
from datasets import Dataset

# Using RAGAS framework (pip install ragas)
eval_data = Dataset.from_dict({
    "question": ["What is HNSW?", "How does RAG work?"],
    "answer": [generated_answers[0], generated_answers[1]],
    "contexts": [retrieved_contexts[0], retrieved_contexts[1]],
    "ground_truth": ["HNSW is a graph-based ANN algorithm...", "RAG combines retrieval..."]
})

results = evaluate(eval_data, metrics=[faithfulness, answer_relevancy])
print(results)
```

---

#### 3. End-to-End Metrics

##### User Satisfaction

Collected from explicit feedback (thumbs up/down, star ratings, written feedback) or inferred from implicit signals (follow-up questions, session abandonment).

```python
# Simple feedback collection schema
feedback_record = {
    "query_id": "q_20241115_001",
    "query": "What are chunking strategies for RAG?",
    "answer": answer_text,
    "retrieved_doc_ids": [doc.metadata["id"] for doc in retrieved_docs],
    "user_rating": None,        # 1-5, collected post-interaction
    "user_comment": None,       # optional free text
    "timestamp": "2024-11-15T14:32:00Z"
}
```

---

##### Latency and Cost

```python
import time

def timed_rag_call(query: str, rag_chain) -> dict:
    t0 = time.perf_counter()
    answer = rag_chain.invoke(query)
    elapsed = time.perf_counter() - t0

    return {
        "answer": answer,
        "latency_ms": round(elapsed * 1000, 1)
    }

# Tracking cost via token usage (OpenAI)
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    answer = rag_chain.invoke(query)
    print(f"Tokens used: {cb.total_tokens} | Cost: ${cb.total_cost:.5f}")
```

---

##### Query Success Rate

The fraction of queries that produce a useful, non-fallback response. A high rate of "I don't have enough information" responses indicates retrieval coverage gaps.

```python
def query_success_rate(answers: list[str]) -> float:
    fallback_phrases = [
        "i don't have enough information",
        "cannot be found in",
        "not available in the provided"
    ]
    successes = sum(
        1 for a in answers
        if not any(p in a.lower() for p in fallback_phrases)
    )
    return successes / len(answers)
```

---

#### 4. Continuous Improvement

##### Feedback Loops

Route low-rated answers or failed queries into a review queue. Use them to identify retrieval gaps (missing documents), chunking failures (chunks too large/small), or prompt weaknesses.

```python
def route_feedback(feedback: dict, threshold: int = 3) -> str:
    rating = feedback.get("user_rating", 5)
    if rating <= threshold:
        return "review_queue"   # flag for human review
    return "accepted"
```

---

##### Index Updates (New Documents / Embeddings)

```python
def update_index(new_docs: list, vectorstore, embeddings) -> None:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    new_chunks = splitter.split_documents(new_docs)

    # Upsert: add new or replace existing by document ID
    vectorstore.add_documents(new_chunks)
    print(f"Added {len(new_chunks)} new chunks to index.")
```

---

##### Query Caching

Cache answers for frequent queries to reduce latency and cost. Use semantic similarity to match cached entries — not just exact string matching.

```python
from langchain.cache import InMemoryCache
import langchain

langchain.llm_cache = InMemoryCache()

# Or use semantic cache (requires Redis + vector similarity)
from langchain_community.cache import RedisSemanticCache
langchain.llm_cache = RedisSemanticCache(
    redis_url="redis://localhost:6379",
    embedding=embeddings,
    score_threshold=0.95   # cache hit if query similarity >= 0.95
)
```

---

##### A/B Testing

Compare two pipeline variants (e.g., different chunk sizes, embedding models, or prompts) on a shared traffic split, measuring which produces better user satisfaction or retrieval metrics.

```python
import random

def ab_route(query: str, variant_a, variant_b, traffic_split: float = 0.5) -> dict:
    variant = "A" if random.random() < traffic_split else "B"
    pipeline = variant_a if variant == "A" else variant_b
    answer = pipeline.invoke(query)
    return {"variant": variant, "answer": answer}

# Log results by variant for statistical comparison
```

---

##### Fine-Tuning Based on Feedback

Use collected query-answer pairs (filtered to high-quality examples) to fine-tune the embedding model or LLM for domain-specific improvement.

```python
# Prepare fine-tuning dataset from high-rated feedback
fine_tune_data = [
    {"prompt": f"Q: {fb['query']}\nContext: {fb['context']}", "completion": fb['answer']}
    for fb in feedback_log
    if fb.get("user_rating", 0) >= 4
]

# Export for fine-tuning (OpenAI format)
import json
with open("finetune_dataset.jsonl", "w") as f:
    for record in fine_tune_data:
        f.write(json.dumps({"messages": [
            {"role": "user", "content": record["prompt"]},
            {"role": "assistant", "content": record["completion"]}
        ]}) + "\n")
```

---

### <img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="40"/> Use Cases

| Scenario | Key Metrics | Improvement Strategy |
|----------|-------------|---------------------|
| **Retrieval quality declining** | Precision@K, NDCG, Hit Rate | Re-chunk documents, upgrade embedding model |
| **LLM hallucinating frequently** | Faithfulness score | Tighten system prompt, lower temperature, add CoT |
| **High query failure rate** | Query success rate | Add missing documents, expand knowledge base |
| **Slow response times** | Latency (p50/p95) | Enable query caching, reduce K, use smaller model |
| **High API costs** | Cost per query | Cache top queries, compress context, reduce K |
| **New domain/language added** | All retrieval metrics | Retrain or swap embedding model, update index |
| **User satisfaction plateau** | Star ratings, feedback | A/B test chunking strategy and prompt variants |
| **Stale knowledge base** | Coverage, recall | Schedule periodic index updates, add ingestion triggers |

---

**Evaluation-Driven Optimization Checklist:**

```
Retrieval Issues (low Precision, Recall, Hit Rate)?
  → Revisit chunking strategy or chunk size
  → Try a better embedding model
  → Add hybrid search (BM25 + vector)

Generation Issues (low Faithfulness, Relevance)?
  → Strengthen the system prompt grounding instructions
  → Lower temperature (toward 0.0)
  → Add chain-of-thought prompting
  → Use context refinement / compression

End-to-End Issues (high latency, high cost)?
  → Enable query caching
  → Reduce K (top-K retrieved chunks)
  → Switch to a smaller/faster LLM for simple queries

Unknown root cause?
  → Run RAGAS end-to-end evaluation on a test set
  → Inspect low-scoring examples manually
  → Profile each pipeline stage separately
```

---

> **You've completed the RAG pipeline!** This stage feeds back into every upstream component: evaluation data informs ingestion quality (`06-1-*`), chunking decisions (`06-1-2`), embedding model selection (`06-1-3`), retrieval strategy tuning (`06-2-1`), and generation prompt design (`06-3-1`). Continuous improvement is not a final step — it is an ongoing loop.
