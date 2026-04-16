# Prompt Evaluation - Practical Guide

Educational project demonstrating systematic prompt evaluation strategies to objectively measure and compare variations.

## Project Structure

This project is organized into **5 progressive examples**, each building on previous concepts:

### Index

1. [**1-basic/**](1-basic/README.md) - Basic Evaluators  
2. [**2-precision/**](2-precision/README.md) - Classification Metrics (P/R/F1)  
3. [**3-pairwise/**](3-pairwise/README.md) - Pairwise Comparison  
4. [**4-pairwise-doc/**](4-pairwise-doc/README.md) - Pairwise with Individual Metrics  
5. [**5-langfuse/**](5-langfuse/README.md) - Langfuse (Open-Source Alternative)  

---

## 1. Basic Evaluators

**Folder:** [`1-basic/`](1-basic/)

**Demonstrates:** How different types of evaluators reveal different aspects of LLM output quality.

**Evaluators Covered:**
- **Format validators**: JSON validity, schema validation (deterministic)
- **Binary LLM judges**: Pass/fail evaluation (criteria)
- **Continuous LLM judges**: Scoring from 0–1 (score_string)
- **Reference-based**: Correctness evaluation using ground truth
- **Custom criteria**: Domain-specific evaluators (faithfulness, format adherence)
- **Embedding distance**: Semantic similarity without LLM

**Includes:** 6 well-designed prompt examples + 4 problematic prompt examples (verbosity, hallucination, formatting issues, unhelpful responses)

**Dataset:** 18 Go code review examples

[Full documentation →](1-basic/README.md)

---

## 2. Precision/Recall/F1

**Folder:** [`2-precision/`](2-precision/)

**Demonstrates:** Using structured ground truth for objective evaluation with classification metrics.

**Concepts:**
- **Precision**: Measures false positive rate (how many reported issues are real)
- **Recall**: Measures false negative rate (how many real issues were found)
- **F1 Score**: Harmonic mean balancing precision and recall
- **Strategic trade-offs**: Conservative vs aggressive vs balanced approaches

**Evaluation Strategies:**
- Conservative prompts (optimize precision)
- Aggressive prompts (optimize recall)
- Balanced prompts (optimize F1)

**Dataset:** 10 examples with structured ground truth (expected issue types, severities, functions)

[Full documentation →](2-precision/README.md)

---

## 3. Pairwise Comparison

**Folder:** [`3-pairwise/`](3-pairwise/)

**Demonstrates:** Direct prompt comparison using LLM-as-Judge for measurable prompt evolution.

**Concepts:**
- **LLM-as-Judge**: Using an LLM to compare two outputs
- **Win rate tracking**: Systematic comparison across a dataset
- **Prompt versioning**: Evolution from V1 → V2 with measurable impact
- **Specialization vs generalization**: Focused vs multi-purpose prompts

**Workflow:**
1. Upload dataset to LangSmith
2. Create prompt versions (A and B)
3. Run pairwise comparison
4. Update prompts based on insights
5. Re-run to measure improvements

**Dataset:** 10 examples (security + performance issues)

[Full documentation →](3-pairwise/README.md)

---

## 4. Pairwise with Individual Metrics

**Folder:** [`4-pairwise-doc/`](4-pairwise-doc/)

**Demonstrates:** Understanding WHY a prompt wins by combining pairwise judgment with granular individual metrics.

**Evaluation Layers:**
- **6 individual metrics** (conciseness, coherence, detail, usefulness, faithfulness, completeness)
- **5-dimensional LLM judge** with structured reasoning (structural completeness, technical accuracy, clarity, reference alignment, conciseness vs detail)
- **Detailed justifications** for each dimension

**Key Difference from Phase 3:** Not just "A wins", but "A wins because of X, Y, Z with detailed breakdown"

**Dataset:** Python projects for documentation generation

[Full documentation →](4-pairwise-doc/README.md)

---

## 5. Langfuse (Open-Source)

**Folder:** [`5-langfuse/`](5-langfuse/)

**Demonstrates:** Implementation of evaluation concepts using a self-hosted open-source platform as an alternative to LangSmith.

**Key Differences:**
- **Hosting**: Self-hosted (Docker) or cloud
- **Open Source**: MIT license, full code access
- **Implementation**: Manual pairwise logic vs native APIs
- **Control**: Granular control over evaluation flow

**Concepts:** Same evaluation principles, different implementation platform

**Dataset:** Same concept as Phase 4 (documentation generation)

[Full documentation →](5-langfuse/README.md)

---

## Model Support (OpenAI + Local LLMs)

This project supports both OpenAI models and local/open-source alternatives.

### Supported Options:
- **OpenAI** (default): e.g., `gpt-4o-mini`
- **Local LLM (via Ollama or similar)**:
  - `qwen2.5-coder:7b` (recommended open-source alternative)

You can switch models via environment variables.

---

## Quick Setup

**Important:** This chapter is self-contained and has its own `requirements.txt` and virtual environment (`venv/`), independent from other chapters.

### Prerequisites

```bash
# 1. Create virtual environment (specific to this chapter)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root:

```bash
# LangSmith (examples 1-4)
LANGSMITH_API_KEY=your-api-key
LANGCHAIN_TRACING_V2=true

# OpenAI (default)
OPENAI_API_KEY=your-api-key

# Optional: Model configuration
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0

# Example using local model (Ollama)
# LLM_MODEL=qwen2.5-coder:7b
# LLM_BASE_URL=http://localhost:11434

# Langfuse (example 5 - optional)
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_HOST=http://localhost:3000
```

---

## Running the Examples

Each folder has its own workflow:

```bash
# Activate venv
source venv/bin/activate

# Basic evaluators
cd 1-basic
python 1-format-eval.py

# Precision/Recall
cd ../2-precision
python 1-conservative-high-precision.py

# Pairwise
cd ../3-pairwise
python upload_dataset.py
python create_prompts.py
python run.py

# Pairwise with metrics
cd ../4-pairwise-doc
python upload_dataset.py
python create_prompt.py
python run.py

# Langfuse
cd ../5-langfuse
python upload_dataset.py
python create_prompts.py
python run.py
```

---

## Learning Path

**Recommended progression:**

1. **Phase 1 (Basic)**: Understand different evaluator types and when to use each
2. **Phase 2 (Precision/Recall)**: Learn classification metrics with ground truth
3. **Phase 3 (Pairwise)**: Master LLM-as-Judge for prompt comparison
4. **Phase 4 (Pairwise + Metrics)**: Combine pairwise with individual metrics for deeper insights
5. **Phase 5 (Langfuse)**: Explore alternative platforms and manual implementation

---

## Additional Resources

- **Full technical documentation:** [`AGENTS.md`](AGENTS.md)
- **LangSmith Dashboard:** https://smith.langchain.com/
- **Langfuse Docs:** https://langfuse.com/docs
- **LangChain Evaluation Guide:** https://python.langchain.com/docs/guides/productionization/evaluation/