# AGENTS.md

This file provides guidance to AI Agents when working with code in this repository.

## Project Overview

This is a comprehensive LLM evaluation project demonstrating systematic prompt evaluation strategies for code review automation and documentation generation. The project uses LangSmith Python SDK v0.2 and Langfuse as evaluation platforms, organized in 5 progressive phases: basic evaluators, precision/recall metrics, pairwise comparisons, pairwise with individual metrics, and Langfuse integration (open-source alternative).

## Environment Setup

**Required Environment Variables** (in `.env`):

**LangSmith (required for folders 1-4):**
- `LANGSMITH_API_KEY` - LangSmith API key for running evaluations
- `LANGCHAIN_TRACING_V2=true` - Enable LangSmith tracing
- `LANGCHAIN_PROJECT` - Optional project name for LangSmith

**OpenAI (required for all folders):**
- `OPENAI_API_KEY` - OpenAI API key for running LLM calls

**Langfuse (required only for folder 5-langfuse):**
- `LANGFUSE_SECRET_KEY` - Langfuse secret key (format: sk-lf-...)
- `LANGFUSE_PUBLIC_KEY` - Langfuse public key (format: pk-lf-...)
- `LANGFUSE_HOST` - Langfuse host URL (e.g., http://localhost:3000 or https://cloud.langfuse.com)

**Model Configuration (optional):**
- `LLM_MODEL` - Model name (default: gpt-4o-mini)
- `LLM_TEMPERATURE` - Temperature value (default: 0)

**Virtual Environment**:
```bash
# Activate venv (REQUIRED for all operations)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Dependencies:**
- langsmith langchain langchain-openai langchain-core langchain-community openai python-dotenv jsonschema numpy langfuse openevals pyyaml

**Notes**:
- `langchain-community` and `numpy` are required for `embedding_distance` evaluator
- `langfuse` is required only for folder 5-langfuse (optional for others)
- `openevals` is used in evaluation utilities
- `pyyaml` is required for loading YAML prompts

## Project Structure

The project is organized in 5 numbered phases, each building on previous concepts:

### 1-basic/ - Basic Evaluators
Individual evaluators testing single aspects of LLM outputs (in progressive complexity):

**Main Examples (Good Prompts):**
- `1-format-eval.py` - JSON validity and schema validation (deterministic, no LLM)
- `2-criteria-binary-eval.py` - Binary evaluators (0/1 pass/fail) using LLM
- `3-criteria-score-eval.py` - Continuous evaluators (conciseness, coherence, detail, depth, relevance)
- `4-correctness-eval.py` - Correctness and relevance (with reference outputs)
- `5-additional-criteria.py` - Custom criteria: faithfulness, format_adherence, code_specificity
- `6-embedding-distance-eval.py` - Semantic similarity using embeddings (deterministic, no LLM)

**Bad Prompt Examples (Demonstrate Common Issues):**
- `7-bad-text-before.py` - LLM returns explanatory text before JSON
- `8-bad-verbose.py` - LLM returns overly verbose responses
- `9-bad-hallucination.py` - LLM hallucinates non-existent bugs
- `10-bad-not-helpful.py` - LLM returns unhelpful generic responses

**Utility Scripts:**
- `upload_dataset.py` - Upload dataset to LangSmith (run once)
- `reset.py` - Clean up dataset from LangSmith

**Dataset**: `dataset.jsonl` - 18 examples of Go code reviews

**Learning Path**:
1. Start with deterministic validation (format)
2. Learn binary LLM evaluation (yes/no)
3. Progress to nuanced LLM scoring (0.0-1.0)
4. Add reference comparisons
5. Create custom criteria
6. Use semantic similarity without LLM

### 2-precision/ - Precision/Recall/F1 Evaluators
Objective metrics using ground truth structured data:

**Main Examples:**
- `1-conservative-high-precision.py` - Conservative approach (high precision, low recall)
- `2-aggressive-high-recall.py` - Aggressive approach (high recall, low precision)
- `3-balanced-best-f1.py` - Balanced approach (best F1 score)

**Shared Utilities:**
- `metrics.py` - Shared P/R/F1 calculation functions and evaluators

**Utility Scripts:**
- `upload_dataset.py` - Upload dataset to LangSmith (run once)
- `reset.py` - Clean up dataset from LangSmith

**Dataset**: `dataset.jsonl` - 10 examples with structured ground truth

### 3-pairwise/ - Pairwise Evaluation & Prompt Evolution
Head-to-head prompt comparison using LLM judges:

**Main Scripts:**
- `create_prompts.py` - Creates V1 prompts (Security Expert + Performance Expert) in LangSmith
- `run.py` - Runs pairwise experiment (automatically uses latest prompt version from LangSmith)
- `update_prompt_v2.py` - Updates Prompt A to V2 (Security + Performance combined)

**Shared Utilities:**
- `pairwise_helpers.py` - Shared utilities (create_pairwise_evaluator function)

**Utility Scripts:**
- `upload_dataset.py` - Upload dataset to LangSmith (run once, reused by experiments)
- `reset.py` - Cleans up prompts and datasets

**Dataset**: `dataset.jsonl` - 10 examples (5 security + 5 performance issues)

**Note**: `run.py` always pulls the latest version of prompts from LangSmith. No need for separate `run_v2.py` - just update the prompt and run again. Experiments are differentiated by timestamp (HHMM format).

### 4-pairwise-doc/ - Pairwise Evaluation with Individual Metrics
Combines pairwise evaluation (LLM-as-Judge) with individual metrics for documentation generation:

**Main Scripts:**
- `create_prompt.py` - Creates two documentation prompts (Prompt A and B) in LangSmith
- `run.py` - Runs pairwise evaluation with 6 individual metrics + LLM judge

**Shared Utilities:**
- `doc_evaluators.py` - Custom evaluators for documentation quality (faithfulness, completeness)
- `pairwise_helpers.py` - Factory functions for prompts and pairwise judge

**Utility Scripts:**
- `upload_dataset.py` - Upload dataset to LangSmith (run once)
- `reset.py` - Clean up prompts and datasets

**Dataset**: `dataset.jsonl` - Examples of Python codebases for documentation generation

**Metrics Evaluated:**

*Individual Metrics (6 total):*
- **Built-in LangChain**: conciseness, coherence, detail, helpfulness
- **Custom Domain-specific**: faithfulness (no hallucination), completeness (covers all aspects)

*Pairwise Judge Metrics (5 dimensions):*
1. Completude Estrutural (0-10)
2. Precisao Tecnica (0-10)
3. Clareza e Utilidade (0-10)
4. Alinhamento com Referencia (0-10) - uses ground truth
5. Concisao vs Detalhe (0-10)

**Key Concept**: Unlike 3-pairwise (only shows "A wins" or "B wins"), this example provides granular insights into WHY a prompt wins through individual metric scores and detailed judge reasoning with JSON output.

**Results**: Creates 3 experiments in LangSmith:
1. `DocPromptA_HHMM` - Prompt A with 6 individual metrics
2. `DocPromptB_HHMM` - Prompt B with 6 individual metrics
3. `DocPairwise_HHMM` - Pairwise comparison (judge with 5 dimensions + reasoning)

### 5-langfuse/ - Langfuse Integration (Open-Source Alternative)
Demonstrates evaluation using Langfuse as an open-source, self-hosted alternative to LangSmith:

**Main Scripts:**
- `create_prompts.py` - Creates prompts in Langfuse (prompt_doc_a, prompt_doc_b, llm_judge_pairwise)
- `run.py` - Runs pairwise evaluation using Langfuse SDK
- `example.py` - Simple example of Langfuse basic usage

**Shared Utilities:**
- `langfuse_helpers.py` - Factory functions adapted for Langfuse API

**Utility Scripts:**
- `upload_dataset.py` - Upload dataset to Langfuse (run once)

**Dataset**: `dataset.jsonl` - Same concept as 4-pairwise-doc (documentation generation)

**Key Differences from LangSmith:**

| Aspect | LangSmith (folders 1-4) | Langfuse (folder 5) |
|--------|------------------------|---------------------|
| **Hosting** | Cloud only | Self-hosted (Docker) or Cloud |
| **Open Source** | No | Yes |
| **Pairwise Native** | `evaluate_comparative()` | Manual implementation |
| **Prompt Management** | `ChatPromptTemplate` | Dict format (native) |
| **Scoring** | Automatic | Manual (`create_score()`) |
| **Setup** | API key only | Docker compose + API keys |

**Setup Requirements:**
```bash
# Option 1: Docker (recommended)
git clone https://github.com/langfuse/langfuse.git
cd langfuse
docker-compose up -d
# Access: http://localhost:3000

# Option 2: Cloud
# Use https://cloud.langfuse.com
```

**Results**: Creates 3 runs in Langfuse:
1. `ExperimentA_HHMM` - Prompt A execution
2. `ExperimentB_HHMM` - Prompt B execution
3. `PairwiseJudge_HHMM` - Comparison with decision + scores

## Shared Utilities Architecture

The project uses a centralized `shared/` directory for common utilities:

### shared/clients.py
LLM and observability platform clients:
- `get_openai_client()` - Returns OpenAI client with LangSmith tracing
- `get_model_name()` - Get configured model (default: gpt-4o-mini, override with `LLM_MODEL`)
- `get_temperature()` - Get temperature (default: 0, override with `LLM_TEMPERATURE`)
- `get_langsmith_client()` - Returns LangSmith Client instance
- `get_langfuse_client()` - Returns Langfuse client instance

### shared/prompts.py
Utilities for loading and executing prompts:
- `load_yaml_prompt(filename, prompts_dir=None)` - Load YAML prompt from file (auto-detects prompts/ directory)
- `execute_text_prompt(prompt_obj, inputs, oai_client, ...)` - Execute simple text prompt (PromptTemplate)
- `execute_chat_prompt(prompt_obj, inputs, oai_client, ...)` - Execute chat prompt (ChatPromptTemplate)
- `convert_langchain_to_openai_messages(messages)` - Convert LangChain messages to OpenAI format

### shared/datasets.py
Dataset upload utilities with metadata support:
- `upload_langsmith_dataset(dataset_file, dataset_name, description, client)` - Upload to LangSmith
- `upload_langfuse_dataset(dataset_file, dataset_name, description, client)` - Upload to Langfuse
- Both functions extract and upload the `metadata` field from JSONL

### shared/evaluators.py
Helper functions for creating prepare_data functions:
- `prepare_prediction_only(run, example)` - For evaluators that don't need input/reference (json_validity, json_schema)
- `prepare_with_input(run, example, input_key="code")` - For evaluators without reference (criteria, score_string)
- `prepare_with_reference(run, example, input_key="code")` - For labeled evaluators (labeled_criteria, embedding_distance)

### shared/parsers.py
JSON and markdown parsing utilities:
- `parse_json_response(text)` - Parse JSON from LLM response, removing markdown blocks if present

## Running Evaluations

All scripts must be run from within the venv and from their respective directories:

```bash
# Activate venv first
source venv/bin/activate

# Basic evaluators
cd 1-basic
python 1-format-eval.py

# Precision/Recall
cd ../2-precision
python 1-conservative-high-precision.py

# Pairwise (full workflow)
cd ../3-pairwise
python upload_dataset.py       # Upload dataset (first time only)
python create_prompts.py       # Create V1 prompts (first time only)
python run.py                  # Run experiment (uses latest prompt version)
python update_prompt_v2.py     # Update Prompt A to V2
python run.py                  # Run again (automatically uses V2)
# python reset.py              # Clean all (optional, to start fresh)

# Pairwise with Individual Metrics (documentation generation)
cd ../4-pairwise-doc
python upload_dataset.py       # Upload dataset (first time only)
python create_prompt.py        # Create prompts (first time only)
python run.py                  # Run evaluation (6 metrics + pairwise judge)

# Langfuse (open-source alternative)
cd ../5-langfuse
python upload_dataset.py       # Upload dataset (first time only)
python create_prompts.py       # Create prompts in Langfuse (first time only)
python run.py                  # Run pairwise evaluation
```

## Architecture & Key Concepts

### Prompt Management Pattern (Standardized)

All examples in this project follow this standardized pattern for loading prompts:

```python
from shared.prompts import load_yaml_prompt, execute_text_prompt
from shared.clients import get_openai_client

# Load prompt from YAML file
prompt = load_yaml_prompt("format_eval.yaml")  # Auto-detects prompts/ directory
oai_client = get_openai_client()

# Use prompt in target function
def run_prompt(inputs: dict) -> dict:
    return execute_text_prompt(prompt, inputs, oai_client, input_key="code")
```

**YAML Prompt Format** (`prompts/*.yaml`):
```yaml
_type: prompt
input_variables:
  - code
template: |
  You are a code reviewer.

  Analyze this code:
  {code}

  Return JSON in format:
  {{
    "findings": [
      {{"type":"", "line":0, "description":"", "severity":""}}
    ],
    "summary": ""
  }}
```

**YAML Format for Multi-Message Prompts** (ChatPromptTemplate with system/user):
```yaml
_type: prompt
input_variables:
  - language
  - code
template_format: f-string
messages:
  - role: system
    content: |
      You are a security expert.
  - role: user
    content: |
      Analyze this {language} code:
      {code}
```

**Key Benefits**:
- All prompts in YAML (standardized across entire project)
- No manual parsing - uses `load_yaml_prompt()` utility
- Clean separation: Python = logic, YAML = prompts
- Easy to edit prompts without touching Python code
- YAML handles `{{}}` escaping naturally (no manual escape needed)
- Supports both simple templates and multi-message (system/user) formats

**Note**: Use `PromptTemplate` (not `ChatPromptTemplate`) for simple single-message prompts. Use YAML `messages:` format for multi-turn conversations or when you need explicit system/user role separation (e.g., pairwise prompts).

### LangSmith API v0.2 (December 2024)

**Key Changes from v0.1**:
- Import `evaluate` directly: `from langsmith import evaluate`
- Evaluators use `(inputs, outputs, reference_outputs)` signature
- Custom evaluators return primitives (`bool`, `int`, `float`) or `dict` with `{"key": str, "score": float}`
- `max_concurrency` parameter controls parallel execution

### Evaluation Flow

1. **Dataset Upload**: Each folder uploads its own dataset to LangSmith via `upload_langsmith_dataset()` or inline
2. **Target Function**: Accepts `inputs: dict`, returns `{"output": str}`
3. **Evaluators**: Process outputs and return scores
4. **Results**: Visible in LangSmith dashboard with experiment names

### Evaluator Types

LangSmith provides three categories of evaluators:

#### 1. LLM-Based Evaluators (Use LLM to Judge)

**Criteria Evaluators** (Binary 0 or 1):
```python
from langsmith.evaluation import LangChainStringEvaluator

# Binary pass/fail without reference
LangChainStringEvaluator("criteria", config={"criteria": "conciseness"})

# Binary pass/fail with reference
LangChainStringEvaluator("labeled_criteria", config={"criteria": "correctness"})
```

**Score Evaluators** (Continuous 0-1):
```python
# Numeric score 1-10 (normalized to 0-1) without reference
LangChainStringEvaluator("score_string", config={"criteria": "conciseness", "normalize_by": 10})

# Numeric score 1-10 (normalized to 0-1) with reference
LangChainStringEvaluator("labeled_score_string", config={"criteria": "correctness", "normalize_by": 10})
```

**Binary vs Continuous - When to use each:**

Use **`criteria`** (binary 0/1) when:
- Need simple pass/fail validation
- Questions like "Is it X?" (yes/no)
- Examples: "Is JSON valid?", "Is response concise?", "Is it harmful?"
- Faster execution (simpler LLM task)

Use **`score_string`** (continuous 0.0-1.0) when:
- Need nuanced measurement
- Questions like "How X is it?" (degree/quality)
- Examples: "How concise?", "How helpful?", "How correct?"
- Want to track gradual improvements

**Built-in vs Custom Criteria:**

Built-in criteria (use string name):
```python
# 14 available: conciseness, relevance, correctness, coherence, harmfulness,
# maliciousness, helpfulness, controversiality, misogyny, criminality,
# insensitivity, depth, creativity, detail
LangChainStringEvaluator("score_string", config={"criteria": "detail", "normalize_by": 10})
```

Custom criteria (use dict with description):
```python
# Define your own criteria with detailed description
LangChainStringEvaluator(
    "score_string",
    config={
        "criteria": {
            "faithfulness": "Is the response grounded ONLY in the provided code? No invented issues?"
        },
        "normalize_by": 10
    }
)
```

Use **custom criteria** when:
- Domain-specific requirements not covered by built-in
- Need precise control over evaluation aspects
- See example: `5-additional-criteria.py`

**When to use LLM-based evaluators:**
- Subjective quality assessment (conciseness, helpfulness, coherence)
- No exact ground truth available
- Need nuanced judgment

#### 2. Deterministic Evaluators (No LLM Required)

**Embedding Distance** (Semantic Similarity):
```python
# Measures semantic similarity using embeddings (lower score = more similar)
# Uses OpenAI embeddings by default
LangChainStringEvaluator("embedding_distance")

# With custom embeddings (e.g., HuggingFace - no API key needed)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.evaluation import load_evaluator, EmbeddingDistance

embedding_model = HuggingFaceEmbeddings()
evaluator = load_evaluator(
    "embedding_distance",
    embeddings=embedding_model,
    distance_metric=EmbeddingDistance.COSINE  # or EUCLIDEAN, MANHATTAN
)
```

**String Distance** (Exact Matching):
```python
# Exact match (0 or 1)
LangChainStringEvaluator("exact_match")

# Regex match (0 or 1)
LangChainStringEvaluator("regex_match")

# String edit distance (Levenshtein, Jaro-Winkler)
LangChainStringEvaluator("string_distance", config={"distance": "levenshtein"})
```

**JSON Evaluators** (Format Validation):
```python
# JSON validity (0 or 1)
LangChainStringEvaluator("json_validity")

# JSON equality with reference (0 or 1)
LangChainStringEvaluator("json_equality")

# JSON edit distance (numeric)
LangChainStringEvaluator("json_edit_distance")

# JSON schema validation (0 or 1)
LangChainStringEvaluator("json_schema")
```

**When to use deterministic evaluators:**
- Objective metrics (exact match, format validation)
- Semantic similarity without subjective judgment
- Faster and cheaper than LLM-based
- Reproducible results

#### 3. Summary Evaluators (for Precision/Recall)
```python
def bug_detection_f1_summary(outputs: list[dict], examples: list) -> dict:
    # Calculate global metrics across ALL examples
    # Return: {"key": "precision", "score": 0.75}, {"key": "recall", "score": 0.44}, ...
    return {"results": [{"key": "precision", "score": p}, {"key": "recall", "score": r}, {"key": "f1_score", "score": f1}]}
```

**Pairwise Evaluators**:
```python
def pairwise_judge(inputs: dict, outputs: list[dict], reference_outputs: dict = None) -> list[float]:
    # outputs[0] = Prompt A, outputs[1] = Prompt B
    # Return preference scores: [1.0, 0.0] if A wins, [0.0, 1.0] if B wins, [0.5, 0.5] if tie
```

### Pairwise Evaluation Implementation

**Utility Functions (3-pairwise/pairwise_helpers.py)**:

The project uses factory functions to create pairwise evaluators:

```python
# pairwise_helpers.py - Shared utilities for pairwise evaluation

def create_pairwise_evaluator(judge_prompt_obj, oai_client):
    """
    Create pairwise evaluator function for evaluate_comparative.

    Returns:
        Evaluator function with signature:
        (inputs: dict, outputs: list, reference_outputs: dict) -> list[float]

    The evaluator returns:
    - [1.0, 0.0] if A is better
    - [0.0, 1.0] if B is better
    - [0.5, 0.5] if tie
    """
    def evaluate_pairwise(inputs: dict, outputs: list, reference_outputs: dict = None):
        # Implementation here
        ...
    return evaluate_pairwise
```

**Prompt Creation with ChatPromptTemplate**:
```python
from langchain_core.prompts import ChatPromptTemplate

PROMPT_MESSAGES = [
    ("system", "You are an expert..."),
    ("user", "Analyze this {language} code:\n{code}")
]

prompt_obj = ChatPromptTemplate.from_messages(PROMPT_MESSAGES)
client.push_prompt("prompt_id", object=prompt_obj, description="...")
```

**Using Factory Functions in run.py**:
```python
from shared.prompts import load_yaml_prompt, execute_chat_prompt
from shared.clients import get_openai_client
from pairwise_helpers import create_pairwise_evaluator

# Load judge template
judge_template = load_yaml_prompt("pairwise_judge.yaml")
oai_client = get_openai_client()

# Fetch prompts from LangSmith
prompt_a_obj = client.pull_prompt(PROMPT_A_ID)
prompt_b_obj = client.pull_prompt(PROMPT_B_ID)

# Create functions using factory (no duplication)
def run_prompt_a(inputs: dict) -> dict:
    return execute_chat_prompt(prompt_a_obj, inputs, oai_client,
                               code=inputs['code'], language=inputs['language'])

def run_prompt_b(inputs: dict) -> dict:
    return execute_chat_prompt(prompt_b_obj, inputs, oai_client,
                               code=inputs['code'], language=inputs['language'])

pairwise_judge = create_pairwise_evaluator(judge_template, oai_client)
```

**Running Pairwise Comparisons**:
```python
from langsmith.evaluation import evaluate, evaluate_comparative

# Run two experiments first
results_a = evaluate(run_prompt_a, data=DATASET_NAME, experiment_prefix="ExperimentA")
results_b = evaluate(run_prompt_b, data=DATASET_NAME, experiment_prefix="ExperimentB")

# Compare them
pairwise_results = evaluate_comparative(
    [results_a.experiment_name, results_b.experiment_name],
    evaluators=[pairwise_judge]
)
```

### Prompt Evolution Workflow (3-pairwise/)

Demonstrates how prompt improvements are visible in LangSmith dashboard:

1. Upload dataset: `python upload_dataset.py` - Dataset created once, reused by all experiments
2. Create V1 prompts: `python create_prompts.py` - Security Expert (A) + Performance Expert (B)
3. Run V1 experiment: `python run.py` - Creates "Pairwise_HHMM" (e.g., Pairwise_1430)
4. Update Prompt A to V2: `python update_prompt_v2.py` - Commits new version (Security + Performance combined)
5. Run V2 experiment: `python run.py` - Creates "Pairwise_HHMM" with new timestamp (e.g., Pairwise_1445)
6. Result: Two separate pairwise experiments visible in dashboard, showing evolution impact

**How it Works**:
- `client.pull_prompt()` always fetches the **latest version** from LangSmith
- After `update_prompt_v2.py`, the next `run.py` automatically uses V2
- Experiments differentiated by **timestamp** (HHMM format) instead of separate files
- No need for `run_v2.py` - same script, different prompt version

**Key Benefits**:
- Dataset upload separated from experiments (run once, reuse everywhere)
- Factory functions eliminate code duplication
- Single `run.py` handles all experiments (less maintenance)
- Clear separation: `upload_dataset.py` = data, `run.py` = experiments, utilities = shared logic

## Dataset Structures

### Basic & Pairwise Format
```json
{
  "inputs": {
    "code": "package main...",
    "task": "Review this code",
    "language": "go"
  },
  "outputs": {
    "category": "security",
    "expected_findings": ["sql_injection"]
  }
}
```

### Precision Format (with ground truth)
```json
{
  "inputs": {
    "code": "...",
    "task": "...",
    "language": "go"
  },
  "outputs": {
    "expected_issue_types": ["sql_injection", "missing_timeout"],
    "expected_severities": {
      "sql_injection": "critical",
      "missing_timeout": "medium"
    },
    "expected_vulnerable_functions": ["GetUser", "QueryRow"]
  }
}
```

## LangSmith vs Langfuse - When to Use Each

This project demonstrates evaluation with both platforms. Here's a comprehensive comparison to help you choose:

### Feature Comparison

| Feature | LangSmith (folders 1-4) | Langfuse (folder 5) |
|---------|------------------------|---------------------|
| **Hosting** | Cloud only (smith.langchain.com) | Self-hosted (Docker) or Cloud |
| **Open Source** | No (proprietary) | Yes (MIT license) |
| **Cost** | Paid plans only | Free (self-hosted) or Cloud plans |
| **Setup Complexity** | Simple (API key) | Medium (Docker compose) |
| **Pairwise Evaluation** | Native `evaluate_comparative()` | Manual implementation |
| **Prompt Versioning** | Git-style commits | Version tracking |
| **LangChain Integration** | Native SDK | Requires custom adapters |
| **UI/Dashboard** | Polished, feature-rich | Clean, functional |
| **Data Control** | Cloud (external) | Full control (self-hosted) |

### When to Use LangSmith (folders 1-4)

**Choose LangSmith if:**
- You want quick setup (just API key, no infrastructure)
- You prefer managed cloud service (no maintenance)
- You need native LangChain integration (`evaluate`, `evaluate_comparative`)
- You want polished UI with advanced filtering/analytics
- You're prototyping or in early development
- Data hosting in cloud is acceptable

**Folders using LangSmith:**
- `1-basic/` - Basic evaluators (criteria, score_string, embedding_distance)
- `2-precision/` - Precision/Recall/F1 metrics
- `3-pairwise/` - Pairwise evaluation (security vs performance)
- `4-pairwise-doc/` - Pairwise with individual metrics (documentation)

### When to Use Langfuse (folder 5)

**Choose Langfuse if:**
- You need self-hosted solution (data privacy/control)
- You want open-source platform (inspect/modify code)
- You're budget-conscious (free self-hosted option)
- You need custom workflows not covered by LangSmith
- You want multi-language support (not just Python)
- You're building production systems with strict data requirements

**Folder using Langfuse:**
- `5-langfuse/` - Pairwise evaluation with manual implementation

### Implementation Differences

**LangSmith Pairwise (4-pairwise-doc):**
```python
from langsmith.evaluation import evaluate, evaluate_comparative

# Run two experiments
results_a = evaluate(run_prompt_a, data=dataset, evaluators=[...])
results_b = evaluate(run_prompt_b, data=dataset, evaluators=[...])

# Compare automatically
pairwise_results = evaluate_comparative(
    [results_a.experiment_name, results_b.experiment_name],
    evaluators=[pairwise_judge]
)
```

**Langfuse Pairwise (5-langfuse):**
```python
from langfuse import Langfuse

langfuse = Langfuse()

# Manual implementation: collect outputs, run judge, save scores
for item in dataset:
    # Run prompts and collect outputs
    output_a = run_prompt_a(item)
    output_b = run_prompt_b(item)

    # Run judge manually
    decision = pairwise_judge(output_a, output_b)

    # Save scores manually
    langfuse.score(trace_id=trace_a.id, name="pairwise_result", value=1.0 if decision == "A" else 0.0)
    langfuse.score(trace_id=trace_b.id, name="pairwise_result", value=0.0 if decision == "A" else 1.0)
```

### Hybrid Approach

For production systems, consider using BOTH:
- **LangSmith** for rapid experimentation and prototyping (folders 1-4)
- **Langfuse** for production deployment and long-term storage (folder 5)

This project demonstrates both approaches so you can learn and choose based on your needs.

## Type Hints

Always use Python 3.9+ compatible type hints:
```python
from typing import List, Optional, Dict

# Correct
def func(data: List[dict]) -> Optional[Dict[str, str]]:
    pass

# Wrong (Python 3.10+ only)
def func(data: list[dict]) -> dict | None:  # DO NOT USE
    pass
```

## Common Warnings (Safe to Ignore)

**JsonValidityEvaluator**:
```
UserWarning: Ignoring input in JsonValidityEvaluator, as it is not expected.
```
This is informational - JsonValidityEvaluator only needs `prediction` field.

**CriteriaEvalChain**:
```
UserWarning: Ignoring reference in CriteriaEvalChain, as it is not expected.
```
Use `labeled_criteria` evaluators if you need reference comparison.

## Important Notes

- **Always activate venv** before running any script: `source venv/bin/activate`
- **Run from correct directory**: Scripts expect relative paths to `dataset.jsonl`
- **LangSmith dashboard**: All results are visible at https://smith.langchain.com/
- **Experiment prefixes**: Different prefixes create separate experiments in dashboard
- **Dataset reuse**: Pairwise experiments reuse same dataset for fair comparison
- **Prompt commits**: LangSmith tracks prompt versions like Git commits
- Always update `requirements.txt` when installing new dependencies
- When researching LangChain, always search for latest 2025 version
