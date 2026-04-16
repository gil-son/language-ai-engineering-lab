# 5-langfuse - Evaluation with Langfuse

This directory contains examples of evaluation using **Langfuse** as an alternative to LangSmith, replicating the concepts from previous directories.

## Structure

```
5-langfuse/
├── create_prompts.py         # Creates prompts in Langfuse
├── upload_dataset.py         # Uploads dataset.jsonl
├── run.py                    # Executes pairwise evaluation
├── dataset.jsonl             # Dataset with examples
├── prompts/
│   ├── prompt_doc_a.yaml     # Prompt A: Technical documentation
│   ├── prompt_doc_b.yaml     # Prompt B: High-level documentation
│   └── llm_judge_pairwise.yaml # Judge for pairwise comparison
└── README.md
```

## Setup

### 1. Environment Variables

Configure the `.env` file in the project root:

```bash
# Langfuse Configuration
LANGFUSE_SECRET_KEY="sk-lf-..."
LANGFUSE_PUBLIC_KEY="pk-lf-..."
LANGFUSE_HOST="http://localhost:3000"  # or [https://cloud.langfuse.com](https://cloud.langfuse.com)

# OpenAI (optional for prompts)
OPENAI_API_KEY="sk-..."

# Local LLM (Ollama) - Optional
# You can use qwen2.5-coder:7b via Ollama for evaluations
```

### 2. Installation

```bash
pip install langfuse openai pyyaml python-dotenv
```

### 3. Langfuse Server

**Option A: Docker (Recommended for development)**
```bash
# Clone the official repo
git clone [https://github.com/langfuse/langfuse.git](https://github.com/langfuse/langfuse.git)
cd langfuse

# Start with docker-compose
docker-compose up -d

# Access: http://localhost:3000
```

## How to Use

### 1. Create Prompts

```bash
python 5-langfuse/create_prompts.py
```

This will create 2 prompts in Langfuse:
- `prompt_doc_a`: Structured technical documentation with implementation details.
- `prompt_doc_b`: High-level documentation without technical specifics.

### 2. Upload Dataset

```bash
python 5-langfuse/upload_dataset.py
```

This will create the `dataset_docgen` dataset with Python project examples for documentation:
- 1 example in dataset.jsonl (Text2SQL project)
- Input: Project Python files
- Expected Output: Reference documentation
- Metadata: project, version

### 3. Run Pairwise Evaluation

```bash
python 5-langfuse/run.py
```

This process will:
- Load the 3 prompts from Langfuse (prompt_doc_a, prompt_doc_b, llm_judge_pairwise).
- For each dataset item:
  1. Execute Prompt A → output_a
  2. Execute Prompt B → output_b
  3. Execute Pairwise Judge → compares A vs B
  4. Add scores to the original runs.
- Create 3 runs per dataset item.

**Resultado:**
- Decision: A, B, ou TIE
- Scores atribuídos aos traces
- Reasoning detalhado do judge

### 4. Visualizar no Langfuse UI

**Prompts:**
1. Acesse http://localhost:3000 (ou seu Langfuse Cloud)
2. Navegue para **Prompts** no menu lateral
3. Você verá os 2 prompts criados com:
   - Labels: `production`, `documentation`
   - Config: `model: gpt-4o-mini`, `temperature: 0`
   - Versioning automático (se rodar novamente, cria nova versão)

**Dataset:**
1. Navegue para **Datasets** no menu lateral
2. Clique em `dataset_docgen`
3. Visualize os items com inputs, expected outputs e metadata

## Recursos

- [Langfuse Docs](https://langfuse.com/docs)
- [Langfuse Python SDK](https://langfuse.com/docs/sdk/python)
- [Prompt Management](https://langfuse.com/docs/prompt-management)
- [Evaluation Methods](https://langfuse.com/docs/evaluation/overview)