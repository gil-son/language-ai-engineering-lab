# Basic Evaluators - Guia de Referência

Este diretório contém exemplos progressivos de evaluators do LangSmith, organizados para facilitar o aprendizado.

## Ordem de Estudo Recomendada

1. **`1-format-eval.py`** - Validação determinística (JSON)
2. **`2-criteria-binary-eval.py`** - Avaliação binária LLM (0/1)
3. **`3-criteria-score-eval.py`** - Avaliação contínua LLM (0.0-1.0)
4. **`4-correctness-eval.py`** - Avaliação com referência
5. **`5-additional-criteria.py`** - Critérios customizados
6. **`6-embedding-distance-eval.py`** - Similaridade semântica

---

## Tipos de Evaluators

### 1. Determinísticos (Sem LLM)

**Características:**
- Rápidos e baratos
- Reproduzíveis (sempre mesmo resultado)
- Objetivos

**Exemplos:**
- `json_validity` - JSON é válido?
- `exact_match` - Texto é idêntico?
- `embedding_distance` - Quão similar semanticamente?

**Arquivo:** `1-format-eval.py`, `6-embedding-distance-eval.py`

---

### 2. LLM-Based Evaluators

Usam LLM para julgar a qualidade do output.

#### 2.1. Binary vs Continuous

| Tipo | Retorno | Quando Usar | Exemplo |
|------|---------|-------------|---------|
| **`criteria`** | 0 ou 1 | Pass/fail simples | "É conciso?" → Sim(1) ou Não(0) |
| **`score_string`** | 0.0 - 1.0 | Avaliação nuançada | "Quão conciso?" → 0.75 |

**Arquivo:**
- `2-criteria-binary-eval.py` - Binary (0/1)
- `3-criteria-score-eval.py` - Continuous (0.0-1.0)

#### 2.2. Com vs Sem Referência

| Tipo | Precisa Reference? | Avalia | Exemplo |
|------|-------------------|--------|---------|
| **`score_string`** | Não | Qualidade subjetiva | "Quão útil é a resposta?" |
| **`labeled_score_string`** | Sim | Correção vs esperado | "Quão correto está comparado ao esperado?" |

**Arquivo:** `3-criteria-score-eval.py`, `4-correctness-eval.py`

#### 2.3. Built-in vs Custom Criteria

**Built-in Criteria** (já vem pronto no LangChain):
```python
# Uso: apenas nome do critério
LangChainStringEvaluator(
    "score_string",
    config={"criteria": "helpfulness", "normalize_by": 10}
)
```

**Critérios disponíveis (14 total):**
- `conciseness`, `relevance`, `correctness`, `coherence`
- `harmfulness`, `maliciousness`, `helpfulness`, `controversiality`
- `misogyny`, `criminality`, `insensitivity`
- `depth`, `creativity`, `detail`

**Custom Criteria** (você define):
```python
# Uso: dict com nome e descrição detalhada
LangChainStringEvaluator(
    "score_string",
    config={
        "criteria": {
            "faithfulness": "A resposta está fundamentada APENAS no código fornecido? Não inventa problemas?"
        },
        "normalize_by": 10
    }
)
```

**Arquivo:** `5-additional-criteria.py`

---

## Comparação: score_string vs labeled_score_string

### `score_string` (SEM referência)

**O que faz:**
Avalia a predição baseado **apenas em critérios**, sem comparar com ground truth.

**Características:**
- Não precisa de `reference` (expected output)
- Avalia qualidade subjetiva
- Pergunta: "Quão X é?"

**Exemplo:**
```python
def prepare_data_no_ref(run, example):
    return {
        "prediction": run.outputs.get("output", ""),
        "input": example.inputs.get("code", "")
        # Sem reference!
    }

LangChainStringEvaluator(
    "score_string",
    config={"criteria": "conciseness", "normalize_by": 10},
    prepare_data=prepare_data_no_ref
)
```

**Use quando:**
- Avaliar qualidade subjetiva (conciseness, helpfulness, coherence)
- Não tem ground truth
- Quer medir "quão bem" algo foi feito

---

### `labeled_score_string` (COM referência)

**O que faz:**
Avalia a predição **comparando com ground truth** (reference output).

**Características:**
- **Requer** `reference` (expected output do dataset)
- Avalia correção/acurácia
- Pergunta: "Quão correto está comparado ao esperado?"

**Exemplo:**
```python
def prepare_data_with_ref(run, example):
    return {
        "prediction": run.outputs.get("output", ""),
        "input": example.inputs.get("code", ""),
        "reference": example.outputs  # Com reference!
    }

LangChainStringEvaluator(
    "labeled_score_string",
    config={"criteria": "correctness", "normalize_by": 10},
    prepare_data=prepare_data_with_ref
)
```

**Use quando:**
- Avaliar correção/acurácia (correctness, relevance)
- Tem ground truth (expected output) no dataset
- Quer medir "quão próximo do esperado"

---

## Resumo Visual Completo

| Evaluator | Tipo | LLM? | Reference? | Retorno | Exemplo de Uso |
|-----------|------|------|-----------|---------|----------------|
| `json_validity` | Determinístico | Não | Não | 0 ou 1 | JSON válido? |
| `embedding_distance` | Determinístico | Não | Sim | 0.0-1.0+ | Similaridade semântica |
| `criteria` | LLM Binary | Sim | Não | 0 ou 1 | É conciso? |
| `labeled_criteria` | LLM Binary | Sim | Sim | 0 ou 1 | Está correto? |
| `score_string` | LLM Continuous | Sim | Não | 0.0-1.0 | Quão útil? |
| `labeled_score_string` | LLM Continuous | Sim | Sim | 0.0-1.0 | Quão correto? |

---

## Progressão de Aprendizado

### Nível 1: Validação Simples
- **Exemplo 1**: Validação determinística (JSON)
- **Conceito**: Validação objetiva sem LLM

### Nível 2: LLM Básico
- **Exemplo 2**: Binary criteria (0/1)
- **Conceito**: Decisões simples pass/fail com LLM

### Nível 3: LLM Nuançado
- **Exemplo 3**: Score criteria (0.0-1.0)
- **Conceito**: Avaliações graduais de qualidade

### Nível 4: Comparação com Ground Truth
- **Exemplo 4**: Labeled evaluators
- **Conceito**: Validar correção comparando com esperado

### Nível 5: Critérios Específicos do Domínio
- **Exemplo 5**: Custom criteria
- **Conceito**: Criar avaliações específicas para seu caso

### Nível 6: Similaridade Semântica
- **Exemplo 6**: Embedding distance
- **Conceito**: Medir similaridade sem LLM judge

---

## Quando Usar Cada Abordagem

### Use `criteria` (binary) quando:
- Precisa de validação simples pass/fail
- Pergunta é tipo "É X?" (sim/não)
- Quer decisões rápidas e claras
- Exemplo: "É conciso?", "É prejudicial?"

### Use `score_string` (continuous sem ref) quando:
- Precisa medir qualidade subjetiva
- Pergunta é tipo "Quão X é?"
- Quer rastrear melhorias graduais
- Não tem ground truth
- Exemplo: "Quão útil?", "Quão coerente?"

### Use `labeled_score_string` (continuous com ref) quando:
- Tem ground truth (expected output)
- Precisa validar correção/acurácia
- Quer medir distância do ideal
- Exemplo: "Quão correto?", "Quão relevante comparado ao esperado?"

### Use `embedding_distance` quando:
- Quer similaridade semântica objetiva
- Não precisa de julgamento subjetivo
- Quer economizar em chamadas LLM
- Tem expected output para comparar
- Exemplo: Outputs semanticamente similares?

### Use custom criteria quando:
- Built-in não cobre seu caso
- Precisa de avaliação específica do domínio
- Quer controle total sobre o que avaliar
- Exemplo: "Fidelidade ao código", "Especificidade técnica"

---

## Dicas de Performance

1. **Determinísticos são mais rápidos**: Use quando possível (json_validity, embedding_distance)
2. **Binary é mais rápido que Continuous**: criteria é mais rápido que score_string
3. **Rode em paralelo**: Use `max_concurrency=2` ou mais
4. **Cache com embeddings**: embedding_distance é rápido após primeiro embedding

---

## Setup do Ambiente

Este exemplo é auto-contido e possui seus próprios arquivos de configuração.

### 1. Criar ambiente virtual

```bash
cd 1-basic
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e configure suas chaves de API:

```bash
cp .env.example .env
# Edite o arquivo .env com suas chaves
```

## Executando os Exemplos

```bash
# Ativar ambiente virtual (se não estiver ativo)
source venv/bin/activate

# Executar exemplos na ordem
python 1-format-eval.py
python 2-criteria-binary-eval.py
python 3-criteria-score-eval.py
python 4-correctness-eval.py
python 5-additional-criteria.py
python 6-embedding-distance-eval.py
```

---

## Dataset

- **Nome LangSmith**: `evaluation_basic_dataset`
- **Arquivo local**: `dataset.jsonl`
- **Conteúdo**: 18 exemplos de code review em Go
- **Compartilhado**: Todos os exemplos usam o MESMO dataset

---

## Referências

- **LangSmith Docs**: https://docs.smith.langchain.com/
- **LangChain Evaluators**: https://python.langchain.com/docs/guides/productionization/evaluation/
- **Projeto completo**: `../AGENTS.md`
