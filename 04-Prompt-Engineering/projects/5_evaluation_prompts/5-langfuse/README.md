# 5-langfuse - Evaluation com Langfuse

Este diretório contém exemplos de evaluation usando **Langfuse** como alternativa ao LangSmith, replicando os conceitos dos diretórios anteriores.

## Estrutura

```
5-langfuse/
├── create_prompts.py         # Cria prompts no Langfuse
├── upload_dataset.py         # Faz upload do dataset.jsonl
├── run.py                    # Executa pairwise evaluation
├── dataset.jsonl             # Dataset com exemplos
├── prompts/
│   ├── prompt_doc_a.yaml     # Prompt A: Documentação técnica
│   ├── prompt_doc_b.yaml     # Prompt B: Documentação alto nível
│   └── llm_judge_pairwise.yaml # Judge para comparação pairwise
└── README.md
```

## Configuração

### 1. Variáveis de Ambiente

Configure no `.env` na raiz do projeto:

```bash
# Langfuse Configuration
LANGFUSE_SECRET_KEY="sk-lf-..."
LANGFUSE_PUBLIC_KEY="pk-lf-..."
LANGFUSE_HOST="http://localhost:3000"  # ou https://cloud.langfuse.com

# OpenAI (para usar nos prompts)
OPENAI_API_KEY="sk-..."
```

### 2. Instalação

```bash
pip install langfuse openai pyyaml python-dotenv
```

### 3. Langfuse Server

**Opção A: Docker (Recomendado para desenvolvimento)**
```bash
# Clone o repo oficial
git clone https://github.com/langfuse/langfuse.git
cd langfuse

# Inicie com docker-compose
docker-compose up -d

# Acesse: http://localhost:3000
```

## Como Usar

### 1. Criar Prompts

```bash
python 5-langfuse/create_prompts.py
```

Isso criará 2 prompts no Langfuse:
- `prompt_doc_a`: Documentação técnica estruturada com detalhes de implementação
- `prompt_doc_b`: Documentação de alto nível sem especificidades técnicas

### 2. Upload Dataset

```bash
python 5-langfuse/upload_dataset.py
```

Isso criará o dataset `dataset_docgen` com exemplos de projetos Python para documentar:
- 1 exemplo no `dataset.jsonl` (Text2SQL project)
- Input: Arquivos Python do projeto
- Expected Output: Documentação de referência
- Metadata: project, version

### 3. Run Pairwise Evaluation

```bash
python 5-langfuse/run.py
```

Isso executará:
- Carrega os 3 prompts do Langfuse (prompt_doc_a, prompt_doc_b, llm_judge_pairwise)
- Para cada item do dataset:
  1. Executa Prompt A → output_a
  2. Executa Prompt B → output_b
  3. Executa Pairwise Judge → compara A vs B
  4. Adiciona scores aos runs originais
- Cria 3 runs por item no dataset

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
