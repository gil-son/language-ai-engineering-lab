# Precision, Recall e F1 Score - Guia Prático

Este diretório demonstra métricas de classificação (Precision/Recall/F1) aplicadas à avaliação de LLMs para code review.

## Conceitos Fundamentais

### Precision (Precisão)
**Definição:** De tudo que o modelo detectou como bug, quanto estava correto?

```
Precision = True Positives / (True Positives + False Positives)
```

- **Alta precision**: Poucos falsos positivos (quando reporta, está certo)
- **Baixa precision**: Muitos falsos positivos (reporta bugs que não existem)

### Recall (Revocação)
**Definição:** De todos os bugs que deveriam ser detectados, quanto o modelo encontrou?

```
Recall = True Positives / (True Positives + False Negatives)
```

- **Alto recall**: Encontra a maioria dos bugs (poucos escapam)
- **Baixo recall**: Perde muitos bugs (deixa passar problemas)

### F1 Score
**Definição:** Média harmônica entre Precision e Recall (equilíbrio).

```
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

- **F1 alto**: Bom equilíbrio (encontra bugs sem muitos falsos positivos)
- **F1 baixo**: Desequilíbrio (ou perde bugs, ou inventa problemas)

## Estrutura dos Exemplos

### Trade-off Precision vs Recall (Scripts 1-3)

Demonstra o **trade-off entre Precision e Recall** através de estratégias de prompt diferentes.

**Todos medem a mesma métrica:** Detecção de tipos de bugs (sql_injection, xss_vulnerability, etc)

| Script | Prompt | Estratégia | Métricas |
|--------|--------|------------|----------|
| `1-conservative-high-precision.py` | `conservative.yaml` | Reporta apenas bugs CRÍTICOS e ÓBVIOS | Precision ~70-90%<br>Recall ~30-50% |
| `2-aggressive-high-recall.py` | `aggressive.yaml` | Reporta TUDO que pode ser problema | Precision ~30-50%<br>Recall ~60-80% |
| `3-balanced-best-f1.py` | `balanced.yaml` | Nomenclatura padronizada, equilíbrio | Precision ~60-75%<br>Recall ~60-75% |

**Objetivo:** Mostrar que mudanças no prompt afetam o trade-off entre P/R e demonstrar quando usar cada estratégia.

## Quando Usar Cada Estratégia?

### Conservative (Alta Precision) - Script 1
**Use quando:**
- Code review automatizado em CI/CD
- Falsos positivos custam tempo dos desenvolvedores
- Melhor deixar passar alguns bugs do que incomodar o time

**Exemplo:** Bloqueio de merge no GitHub que só alerta sobre bugs críticos confirmados.

### Aggressive (Alto Recall) - Script 2
**Use quando:**
- Auditoria de segurança pré-release
- Não podemos deixar nenhuma vulnerabilidade passar
- Humanos vão revisar todos os alertas manualmente

**Exemplo:** Scanner de segurança antes de deploy em produção.

### Balanced (Melhor F1) - Script 3
**Use quando:**
- Uso geral no dia-a-dia
- Queremos equilíbrio entre encontrar bugs e evitar alertas falsos
- Feedback contínuo para desenvolvedores

**Exemplo:** Plugin do IDE que sugere melhorias enquanto você codifica.

## Como Executar

### Ativar ambiente virtual
```bash
cd 7-evaluation
source venv/bin/activate
```

### Executar exemplos
```bash
cd 2-precision

# Trade-off Precision vs Recall
python 1-conservative-high-precision.py
python 2-aggressive-high-recall.py
python 3-balanced-best-f1.py
```

### Comparar resultados no LangSmith
1. Acesse https://smith.langchain.com/
2. Vá para "Experiments"
3. Compare os 3 experimentos lado a lado:
   - `Conservative_HighPrecision` - Alta precision, baixo recall
   - `Aggressive_HighRecall` - Alto recall, baixa precision
   - `Balanced_BestF1` - Melhor equilíbrio (F1)

## Dataset

`dataset.jsonl` - 10 exemplos de código Go com ground truth:

```json
{
  "inputs": {"code": "...", "language": "go"},
  "outputs": {
    "expected_issue_types": ["sql_injection", "missing_timeout"],
    "expected_severities": {"sql_injection": "critical", ...},
    "expected_vulnerable_functions": ["GetUser", "Sprintf"]
  }
}
```

## Arquitetura

### Módulo Compartilhado (`shared_utils.py`)

- `create_run_function(prompt_name)` - Factory para criar funções de análise
- `calculate_pr_f1()` - Lógica genérica de P/R/F1
- `extract_bug_types()`, `extract_severity_pairs()`, `extract_vulnerable_functions()` - Extração de dados

### Prompts YAML

| Arquivo | Descrição | Usado em |
|---------|-----------|----------|
| `conservative.yaml` | Foco em bugs críticos | Script 1 |
| `aggressive.yaml` | Detecta tudo | Script 2 |
| `balanced.yaml` | Nomenclatura padronizada | Script 3 |

## Resultados Esperados (Aproximados)

| Experimento | Precision | Recall | F1 | Interpretação |
|-------------|-----------|--------|----|--------------|
| Conservative | 70-90% | 30-50% | 40-60% | Poucos erros, mas perde bugs |
| Aggressive | 30-50% | 60-80% | 40-60% | Acha mais bugs, mas erra mais |
| Balanced | 60-75% | 60-75% | 60-75% | Melhor equilíbrio geral |

## Entendendo os Resultados

### True Positives (TP), False Positives (FP), False Negatives (FN)

- **TP**: Encontrou corretamente (está no esperado E no predito)
- **FP**: Alarme falso (está no predito mas NÃO no esperado)
- **FN**: Perdeu (está no esperado mas NÃO no predito)

### Cenários Práticos

**Cenário 1: Alta Precision, Baixo Recall**
- Precision=0.9, Recall=0.3, F1=0.45
- Interpretação: O que encontrou está correto (90%), mas perdeu 70% dos bugs
- Ação: Melhorar o prompt para ser mais abrangente (script 2)

**Cenário 2: Baixa Precision, Alto Recall**
- Precision=0.3, Recall=0.9, F1=0.45
- Interpretação: Encontrou 90% dos bugs, mas 70% são falsos alarmes
- Ação: Melhorar o prompt para ser mais específico (script 1)

**Cenário 3: Balanceado**
- Precision=0.7, Recall=0.7, F1=0.7
- Interpretação: Performance consistente e boa (script 3)
- Ação: Continuar iterando para chegar próximo de 1.0

## LangSmith não possui evaluators nativos para P/R/F1

Durante a pesquisa, confirmamos que **LangSmith não oferece evaluators prontos para Precision/Recall/F1**.

O framework foca em:
- LLM-as-judge evaluators (criteria, score_string)
- JSON match evaluators
- Embedding distance

Para métricas de classificação, é necessário implementar **summary evaluators customizados** (como feito neste projeto).

## Quando usar Precision/Recall vs Score String?

| Métrica | Tipo | Uso | Requer Ground Truth | Exemplo |
|---------|------|-----|---------------------|---------|
| **Precision/Recall/F1** | Objetivo | Detecção de items específicos | Sim | Encontrou os bugs corretos? |
| **score_string** | Subjetivo | Qualidade geral | Não | A resposta foi útil? (0-10) |

**Use Precision/Recall quando**:
- Você sabe exatamente o que espera (ground truth)
- Está avaliando detecção (bugs, entidades, classes)
- Precisa de métricas objetivas e reproduzíveis

**Use score_string quando**:
- Está avaliando qualidade subjetiva (helpfulness, conciseness)
- Não tem ground truth exato
- Quer feedback nuanced (0-10 normalizado para 0-1)

## Upload do Dataset (primeira vez)

```bash
source venv/bin/activate
python 2-precision/upload_dataset.py
```

## Reset (Limpeza)

Para deletar o dataset do LangSmith e começar do zero:

```bash
python 2-precision/reset.py
```

## Referências

- [LangSmith Summary Evaluators](https://docs.langchain.com/langsmith/summary)
- [Precision, Recall, F1 - Google ML Course](https://developers.google.com/machine-learning/crash-course/classification/precision-and-recall)
