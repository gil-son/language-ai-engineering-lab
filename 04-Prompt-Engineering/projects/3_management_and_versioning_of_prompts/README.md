# Prompt Management and Versioning

This project demonstrates two practical approaches to managing prompts for AI agents built with **LangChain**:

## 1. Local Prompt Versioning
- **Registry-based management** using a centralized `registry.yaml`
- **Directory-based versioning** with isolated prompt versions
- **Static validation** through structured configuration and automated tests
- **Native LangChain prompt loading** with YAML prompt files

## 2. Prompt Versioning with LangSmith
- **Remote synchronization** of prompts using LangSmith
- **Push and pull workflows** for prompt distribution
- **Version control via tags and metadata**
- **Collaboration and centralized prompt storage**

---

# Project Structure

This project is organized to separate **prompt definitions**, **agent logic**, **registry configuration**, **prompt tests**, and **LangSmith integration**.

```bash
project/
├── prompts/
│   ├── registry.yaml
│   │
│   ├── agent-code-reviewer/
│   │   └── v1.0.0/
│   │       ├── prompt.yaml
│   │       └── prompt.tests.yaml
│   │
│   └── agent-pull-request-creator/
│       └── v1.0.1/
│           ├── prompt.yaml
│           └── prompt.tests.yaml
│
├── src/
│   ├── agent_code_reviewer.py
│   ├── agent_pull_request.py
│   ├── prompt_registry.py
│   ├── langsmith_push.py
│   └── langsmith_client.py
│
├── tests/
│   └── test_prompts.py
│
├── .env.example
├── requirements.txt
└── README.md
```

---

# Environment Setup

## 1. Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Configure Environment Variables

Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

Then configure the required environment variables.

---

# Environment Variables

## Required Variables

```bash
# LLM provider / local model configuration
# Example if using Ollama
OLLAMA_BASE_URL=http://localhost:11434
```

## Optional Variables (LangSmith Integration)

```bash
LANGCHAIN_TRACING_V2=false
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your-langsmith-api-key
LANGCHAIN_PROJECT=prompt-management-system
```

## Variable Description

- `OLLAMA_BASE_URL`: Base URL for your local Ollama instance
- `LANGCHAIN_TRACING_V2`: Enables or disables LangSmith tracing
- `LANGCHAIN_ENDPOINT`: LangSmith API endpoint
- `LANGCHAIN_API_KEY`: LangSmith API key for push/pull operations
- `LANGCHAIN_PROJECT`: Project name used to group traces and prompt assets in LangSmith

> **Note:**  
> Your agents currently use the model `llama3.2`, so you should have **Ollama** installed and running locally.

Example:

```bash
ollama run llama3.2
```

---

# Prompt Registry

The file `prompts/registry.yaml` is the central source of truth for prompt management.

Example:

```yaml
agents:
  agent-code-reviewer:
    description: "Agent specialized in rigorous code review"
    current_version: "1.0.0"
    path: "agent-code-reviewer/v1.0.0/prompt.yaml"
    model: llama3.2

  agent-pull-request-creator:
    description: "Agent for creating professional pull requests"
    current_version: "1.0.1"
    path: "agent-pull-request-creator/v1.0.1/prompt.yaml"
    model: llama3.2
```

This registry maps each agent to:

- its **current active version**
- its **prompt file path**
- its **description**
- its **target model**

This allows your application to load prompts dynamically without hardcoding paths.

---

# Local Prompt Management

## How It Works

The local prompt system is powered by `PromptRegistry`, which:

- reads `registry.yaml`
- validates prompt metadata
- resolves the correct versioned prompt file
- loads prompts using LangChain’s `load_prompt()`

### Main Registry Logic

Implemented in:

```bash
src/prompt_registry.py
```

The registry returns a `PromptInfo` object containing:

- `id`
- `version`
- `path`
- `description`
- `model`

This makes prompt retrieval structured, explicit, and reusable.

---

# Running the Agents

## 1. Code Review Agent

This agent loads the versioned prompt for `agent-code-reviewer` and runs a code review chain.

### Run:

```bash
python src/agent_code_reviewer.py
```

### What it does:
- Builds a `CodeReviewRequest`
- Loads the correct prompt from the registry
- Initializes the model with LangChain
- Executes the prompt chain
- Prints the generated review

### Example use case:
- Reviewing diffs before merge
- Enforcing repository standards
- Detecting quality or performance issues

---

## 2. Pull Request Creation Agent

This agent generates professional pull request descriptions using a versioned prompt.

### Run:

```bash
python src/agent_pull_request.py
```

### What it does:
- Builds a `PullRequestRequest`
- Loads the correct prompt from the registry
- Initializes the model
- Executes the chain
- Prints the PR description

### Example use case:
- Standardizing pull request templates
- Improving team documentation
- Automating PR authoring workflows

---

# LangSmith Integration

This project also supports **remote prompt management** using LangSmith.

---

## 1. Push a Local Prompt to LangSmith

Use the following script to upload a locally versioned prompt to LangSmith:

```bash
python src/langsmith_push.py
```

### What it does:
- Loads the prompt from the local registry
- Converts it into a LangChain prompt object
- Pushes it to LangSmith
- Attaches metadata such as:
  - version tag
  - model tag
  - description

### Example metadata:

```python
tags=[
    f"v{prompt.version}",
    f"model: {prompt.model}",
]
```

This makes prompts easier to search, organize, and track in LangSmith.

---

## 2. Pull and Use a Prompt from LangSmith

Use the following script to retrieve a prompt directly from LangSmith:

```bash
python src/langsmith_client.py
```

### What it does:
- Connects to LangSmith
- Pulls the prompt by name
- Combines it with the selected model
- Executes the chain with runtime inputs

This is useful when you want to:
- centralize prompt ownership
- share prompts across projects
- avoid local prompt duplication
- deploy prompt changes without changing application code

---

# Prompt Package Structure

Each prompt version should be stored as a **self-contained prompt package**, including both the prompt definition and its test scenarios.

Example:

```bash
prompts/
└── agent-code-reviewer/
    └── v1.0.0/
        ├── prompt.yaml
        └── prompt.tests.yaml
```

This structure makes each prompt version self-contained and easier to maintain, validate, and evolve over time.

## 1. `prompt.yaml`

This file contains the actual prompt definition used by the agent.

Example:

```yaml
_type: prompt
id: agent-code-reviewer
version: 1.0.0
input_variables:
  - code_diff
  - language
  - repo_rules
  - security_level
  - review_focus
template: |
  Você é um revisor de código sênior especializado em análise rigorosa e detalhada.
```

### Purpose
- Defines the prompt template
- Declares required input variables
- Stores prompt metadata such as `id` and `version`
- Serves as the source loaded by LangChain using `load_prompt()`

---

## 2. `prompt.tests.yaml`

This file defines **prompt-level test cases** used to validate prompt behavior.

Example:

```yaml
cases:
  - name: basic_code_review
    inputs:
      code_diff: |
        + def calculate_total(items):
        +     total = 0
        +     for item in items:
        +         total += item['price']
        +     return total
      language: "python"
      repo_rules: "Use type hints and handle exceptions"
      security_level: "standard"
      review_focus: "general"
    expect_contains:
      - "type hints"
      - "exception"
      - "python"
      - "RESUMO EXECUTIVO"
      - "MELHORIAS RECOMENDADAS"
```

### Purpose
- Defines expected prompt behavior
- Validates whether the model output includes key concepts or sections
- Helps detect regressions when prompts are updated
- Makes prompt changes safer and more testable

This approach is especially useful when prompt versions evolve over time and you want to ensure output consistency.

---

# Automated Tests

The project includes automated tests to validate both **prompt structure** and **prompt behavior**.

## What is tested

Your test suite should validate:

- registry loading
- required registry fields
- prompt path existence
- prompt YAML syntax and structure
- prompt loading with LangChain
- prompt test case definitions
- backward compatibility between versions
- expected output behavior based on test scenarios

---

## Prompt-Level Test Cases

Each prompt version can include its own `prompt.tests.yaml` file.

These files define structured test cases such as:

- sample inputs
- expected keywords
- expected sections in the generated response

This gives you a lightweight but effective way to validate prompt quality without needing a full evaluation platform.

---

## Run All Tests

```bash
pytest tests/test_prompts.py -v
```

Or run directly:

```bash
python tests/test_prompts.py
```

Using versioned prompt tests makes your prompt system more reliable, maintainable, and production-friendly.

---

# Why This Approach Is Useful

This architecture gives you a practical and scalable prompt management workflow:

## Benefits of Local Versioning
- simple and transparent
- easy to review in Git
- explicit prompt history
- works offline

## Benefits of LangSmith Integration
- centralized prompt distribution
- easier collaboration
- remote reuse across projects
- better observability and lifecycle management

Together, they provide a strong foundation for **PromptOps**, **AI agent maintenance**, and **production prompt governance**.

---

# Notes on LangChain Version

Although many tutorials and examples still reference older LangChain APIs, this project follows the **newer LangChain style**, including:

- `init_chat_model()`
- `load_prompt()`
- composable chains using `|`
- `StrOutputParser()`

Because LangChain has evolved significantly, some APIs may differ depending on the installed version.

> If you run into compatibility issues, verify the version installed in your environment and adjust imports accordingly.

---

# Example Workflow

A typical workflow for this project is:

1. Create or update a prompt locally
2. Register the prompt in `registry.yaml`
3. Test it locally through the agent script
4. Validate behavior with automated tests
5. Push the prompt to LangSmith
6. Pull and reuse it remotely when needed

This creates a clean and maintainable prompt lifecycle for AI applications.