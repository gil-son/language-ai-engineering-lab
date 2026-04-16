# Experimento 1: Pairwise Evaluation com Evolução de Prompt

## Objetivo

Demonstrar **comparação pairwise** e **evolução de prompt** através de 2 experimentos:
- **V1**: Security Expert vs Performance Expert (cada um domina seu domínio)
- **V2**: Security Expert EVOLUÍDO (Security + Performance) vs Performance Expert

Dataset balanceado (50% security, 50% performance) para demonstrar evolução do Prompt A.

---

## Prompts

### Prompt A - Security Expert (`pairwise_comparison_security`)

**V1 - Security Only**: Identifica apenas vulnerabilidades de segurança
- SQL injection, XSS, Command injection
- Missing input validation
- Authentication/authorization issues
- Hardcoded credentials
- Session management issues

**V2 - Security + Performance**: Identifica vulnerabilidades E problemas de performance
- Tudo do V1 +
- N+1 query problems
- Memory leaks e unbounded growth
- Blocking operations e falta de concorrência
- Missing timeouts e context cancellation
- Inefficient locking

### Prompt B - Performance Expert (`pairwise_comparison_performance`)

**Especialização**: Identificar problemas de performance (não muda entre V1 e V2)
- N+1 query problems
- Memory leaks e unbounded growth
- Blocking operations e falta de concorrência
- Missing timeouts e context cancellation
- Inefficient locking (RWMutex vs Mutex)
- Sequential processing que poderia ser paralelo

---

## Dataset

**Arquivo**: `pairwise/dataset.jsonl` (compartilhado)

**Conteúdo**: 10 exemplos balanceados

### Security (5 exemplos)
1. SQL Injection (concatenação de string em query)
2. XSS (HTML injection sem sanitização)
3. Command Injection (exec.Command com input do usuário)
4. Hardcoded Credentials (senha hardcoded no código)
5. Session Fixation (session ID vem do usuário)

### Performance (5 exemplos)
1. N+1 Query Problem (loop com queries individuais)
2. Memory Leak (unbounded cache sem eviction)
3. Blocking Operations (processamento sequencial sem concorrência)
4. Missing Timeout (http.Get sem context/timeout)
5. Inefficient Locking (Mutex quando deveria usar RWMutex)

---

## Como Executar

### Pré-requisitos
```bash
# Ativar venv
source ../../venv/bin/activate
cd pairwise/1-initial-comparison
```

### Fluxo Completo - Reset e Execução

**1. Limpar recursos (opcional)**
```bash
python reset.py
```
Remove dataset e prompts anteriores.


**1. Upload dataset**
```bash
python PYTHONPATH=. python 3-pairwise/upload_dataset.py
```


**2. Criar prompts V1**
```bash
python create_prompts.py
```
Cria Prompt A (Security only) e Prompt B (Performance).

**3. Executar experimento V1**
```bash
python run.py
```
Cria primeira linha no dashboard: Security Expert vs Performance Expert.

**4. Atualizar Prompt A para V2**
```bash
python update_prompt_v2.py
```
Atualiza Prompt A para incluir Security + Performance (commit V2).

**5. Executar experimento V2**
```bash
python run_v2.py
```
Cria segunda linha no dashboard: Security Expert V2 vs Performance Expert.

### Resultados no Dashboard

Após executar todos os passos, você verá 2 linhas em **Pairwise Experiments**:
1. **PairwiseA_Security** vs **PairwiseB_Performance** (V1)
2. **PairwiseA_V2_SecurityAndPerformance** vs **PairwiseB_Performance** (V2)

Comparação visual: V2 deve ter win rate MAIOR que V1.

---

## Resultados Esperados

### Experimento V1 (Security Only vs Performance)
- **Win Rate Prompt A**: ~50% (ganha nos 5 casos de security)
- **Win Rate Prompt B**: ~50% (ganha nos 5 casos de performance)
- **Interpretação**: Cada prompt domina em sua especialidade

### Experimento V2 (Security + Performance vs Performance)
- **Win Rate Prompt A**: ~80-90% (ganha em security + empata em performance)
- **Win Rate Prompt B**: ~10-20% (ainda pode ganhar em alguns casos de performance pura)
- **Interpretação**: Prompt A evoluiu para cobrir AMBOS os domínios

### Evolução do Prompt A
- **V1 → V2**: +40% win rate (de 50% para 90%)
- **Ganho**: Cobertura de performance SEM perder qualidade em security
- **Lição**: Prompts generalistas bem projetados podem superar especialistas

---

## LLM Judge

### Critérios de Comparação
1. **Correctness**: Identificou os problemas reais do código?
2. **Completeness**: Encontrou TODOS os problemas relevantes?
3. **Relevance**: Os problemas são relevantes para a especialidade?
4. **Specificity**: Descrições específicas e acionáveis?

### Lógica de Decisão
- **Winner = A**: Prompt A é objetivamente melhor (score [1.0, 0.0])
- **Winner = B**: Prompt B é objetivamente melhor (score [0.0, 1.0])
- **Winner = tie**: Ambos igualmente bons/ruins (score [0.5, 0.5])

---

## Arquivos

```
1-initial-comparison/
├── create_prompts.py      # Cria Prompt A (V1 - Security) e Prompt B no LangSmith
├── run.py                 # Executa experimento V1 (Security vs Performance)
├── update_prompt_v2.py    # Atualiza Prompt A para V2 (Security + Performance)
├── run_v2.py              # Executa experimento V2 (Security+Perf vs Performance)
├── reset.py               # Limpa dataset e prompts
└── README.md              # Este arquivo
```

## Implementação Técnica

### ChatPromptTemplate
Prompts são criados com `ChatPromptTemplate.from_messages()`:
```python
from langchain_core.prompts import ChatPromptTemplate

PROMPT_A_MESSAGES = [
    ("system", "Você é um especialista em..."),
    ("user", "Analise o código em {language}:\n{code}")
]

prompt_obj = ChatPromptTemplate.from_messages(PROMPT_A_MESSAGES)
client.push_prompt(prompt_id, object=prompt_obj)
```

### Pairwise Judge
Judge recebe outputs de ambos prompts e retorna preferência:
```python
def pairwise_judge(inputs: dict, outputs: List[dict], reference_outputs=None) -> List[float]:
    # outputs[0] = Prompt A, outputs[1] = Prompt B
    decision = llm_judge(...)

    if "A" in decision:
        return [1.0, 0.0]  # A wins
    elif "B" in decision:
        return [0.0, 1.0]  # B wins
    else:
        return [0.5, 0.5]  # Tie
```

### Prompt Evolution
- **Commit V1**: `create_prompts.py` → Security only
- **Commit V2**: `update_prompt_v2.py` → Security + Performance
- **Dashboard**: Ambos commits visíveis em experimentos separados
