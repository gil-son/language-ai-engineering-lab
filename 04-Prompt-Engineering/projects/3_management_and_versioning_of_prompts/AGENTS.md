# AGENTS.md

This file provides guidance for developing and managing agents in this prompt management system.

## Environment Setup Commands

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY and optionally LangSmith keys
```

## Testing and Validation

```bash
# Run all prompt validation tests
pytest tests/test_prompts.py -v

# Run tests directly
python tests/test_prompts.py

# Test specific aspects
pytest tests/test_prompts.py::test_registry_yaml_syntax -v
pytest tests/test_prompts.py::test_prompt_structure -v
```

## Running Agents

```bash
# Execute local agents using registry system
python src/agent_code_reviewer.py
python src/agent_pull_request.py

# Push prompts to LangSmith (requires LANGCHAIN_API_KEY)
python src/langsmith_push.py
```

## Core Architecture

### Prompt Management System
This project implements a dual-layer prompt management approach:

1. **Local Registry System** (`src/prompt_registry.py`):
   - Simplified registry class (~50 lines) with single public `get_prompt()` method
   - Centralized registry in `prompts/registry.yaml` mapping agent IDs to versioned prompts
   - Hierarchical directory structure: `prompts/{agent-name}/v{version}/prompt.yaml`
   - Returns `PromptInfo` NamedTuple with id, version, path, description, and optional model
   - Direct path resolution using `Path(__file__).parent.parent`

2. **LangSmith Integration** (`src/langsmith_*.py`):
   - Push/pull functionality for remote prompt synchronization
   - Version tagging with metadata (model, description)
   - Collaborative prompt development through LangSmith platform

### Prompt Structure Standards
All prompts follow this YAML structure:
```yaml
id: "agent-{name}"
version: "x.y.z"
template: "Prompt content with {variable} placeholders"
input_variables: ["variable"]
# Optional metadata fields
```

### Versioning Strategy
- Semantic versioning (x.y.z) for all prompts
- Version-specific directories maintain prompt history
- Registry points to current active version per agent
- Test files accompany each prompt version (`prompt.tests.yaml`)

### Testing Framework Architecture
The test suite (`tests/test_prompts.py`) provides comprehensive validation using pytest fixtures:

- **Static Analysis**: YAML syntax, file existence, structure validation
- **Template Validation**: F-string syntax, variable consistency checking
- **Rendering Tests**: Template rendering with test cases, expected output validation
- **Fixture-Based Testing**: Session-scoped fixtures for efficient testing

Key fixtures:
- `prompts_dir`: Session-scoped fixture for prompts directory
- `registry_data`: Loads registry.yaml once per test session
- `all_prompts`: Discovers all registry prompts
- `prompts_with_tests`: Finds prompts with test files
- `all_test_cases`: Loads all test scenarios

### Dependencies Note
Uses LangChain 1.0.0a5 (alpha) which has significant API changes from stable 0.3.x versions. Key integrations:
- `langchain-core` for prompt loading and templates
- `langsmith` for remote prompt management
- `python-dotenv` for environment configuration
- `pytest` for testing framework
- Standard Python libraries for YAML processing and path management