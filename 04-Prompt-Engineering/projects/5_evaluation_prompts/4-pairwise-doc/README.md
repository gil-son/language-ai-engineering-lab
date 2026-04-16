# 4-pairwise-doc: Pairwise Evaluation com Métricas Individuais

Este exemplo demonstra como combinar **avaliação pairwise** (LLM-as-Judge) com **métricas individuais** para avaliar geração de documentação de código.

## Conceito

**Problema**: Pairwise evaluation tradicional apenas responde "Qual prompt ganhou?", mas não fornece insights sobre **por que** um prompt é melhor.

**Solução**: Executar **métricas individuais** em cada prompt (A e B) antes da comparação pairwise, permitindo análise granular.

## Arquitetura

```
run.py
  |
  +-- evaluate(prompt_a, evaluators=[6 métricas])  → Experiment A com scores
  |
  +-- evaluate(prompt_b, evaluators=[6 métricas])  → Experiment B com scores
  |
  +-- evaluate_comparative([A, B], judge)          → Pairwise: qual ganhou?
```

**Resultado**: 3 experiments no LangSmith dashboard:
1. `DocPromptA_HHMM`: Prompt A com 6 métricas individuais
2. `DocPromptB_HHMM`: Prompt B com 6 métricas individuais
3. `DocPairwise_HHMM`: Comparação head-to-head (apenas juiz)

## Métricas Avaliadas

### 1. Métricas Individuais (Built-in + Custom)

Cada prompt (A e B) é avaliado separadamente com 6 métricas:

**Built-in LangChain**:
- **conciseness** (0.0-1.0): Documentação não é verbosa ou redundante
- **coherence** (0.0-1.0): Estrutura clara e lógica
- **detail** (0.0-1.0): Nível de detalhe técnico adequado
- **helpfulness** (0.0-1.0): Útil para desenvolvedores

**Custom Domain-specific**:
- **faithfulness** (0.0-1.0): Baseada apenas no código fornecido (não inventa funcionalidades)
- **completeness** (0.0-1.0): Documenta todos aspectos relevantes (classes, funções, parâmetros)

### 2. Métricas do Juiz Pairwise (LLM-as-Judge)

O juiz compara A vs B usando **documentação de referência (ground truth)** e 5 dimensões robustas:

#### 2.1 Completude Estrutural (0-10)
- Documenta contexto e objetivos do projeto?
- Lista tecnologias e dependências principais?
- Explica arquitetura e fluxo de dados?
- Identifica pontos críticos, limitações ou trade-offs?
- Cobre todos os componentes principais do código?

#### 2.2 Precisão Técnica (0-10)
- Nomes de classes, funções e variáveis estão corretos?
- Tipos de dados e assinaturas estão precisos?
- Descrições de parâmetros e retornos estão corretas?
- NÃO inventa código, funcionalidades ou comportamentos inexistentes?
- Terminologia técnica usada corretamente?

#### 2.3 Clareza e Utilidade (0-10)
- Linguagem clara e acessível para desenvolvedores?
- Organização lógica das seções (fácil de navegar)?
- Facilita onboarding de novos desenvolvedores?
- Fornece exemplos práticos quando relevante?
- Evita jargão desnecessário ou ambiguidade?

#### 2.4 Alinhamento com Referência (0-10)
- Segue a estrutura da documentação de referência?
- Cobre os mesmos tópicos essenciais da referência?
- Nível de detalhe similar ao esperado na referência?
- Estilo e tom consistentes com o padrão da referência?
- Prioriza as mesmas informações críticas da referência?

#### 2.5 Concisão vs Detalhe (0-10)
- Balanceia completude sem verbosidade excessiva?
- Evita redundâncias e repetições desnecessárias?
- Detalha onde necessário (ex: pontos críticos)?
- Resume onde apropriado (ex: conceitos básicos)?
- Densidade de informação adequada (não muito raso, não muito denso)?

**Regras de Decisão do Juiz**:
- Score total = soma das 5 métricas (máximo 50 pontos)
- Prioridade: Precisão Técnica e Alinhamento com Referência (peso maior)
- Decisão: diferença < 5 pontos = EMPATE, >= 5 pontos = vencedor

## Dataset

`dataset.jsonl` contém exemplos de codebases Python com **ground truth** (documentação de referência):

```json
{
  "inputs": {
    "files": {
      "prompts.py": "QA_SYSTEM_PROMPT = ...",
      "utils.py": "def get_engine_for_chinook_db(): ...",
      "simple_text2sql.py": "class OverallState(TypedDict): ..."
    }
  },
  "outputs": {
    "reference": "### Documentação Técnica — Projeto Text2SQL\n\n#### Contexto\nO projeto implementa um fluxo Text2SQL usando LangGraph...\n\n#### Objetivos\n- Traduzir perguntas em queries SQL válidas.\n- Executar consultas em tempo real...\n\n#### Tecnologias\n- Python 3.11+\n- LangChain / LangGraph\n...\n\n#### Pontos Críticos\n- Dependência de schema remoto.\n- Falta de cache e validação intermediária.\n- Possibilidade de SQL injection se usado fora do ambiente controlado."
  },
  "metadata": {
    "project": "text2sql",
    "version": "v1"
  }
}
```

**Ground Truth** serve como:
1. Padrão ouro para o juiz comparar A vs B
2. Referência estrutural (seções esperadas)
3. Benchmark de qualidade técnica

## Prompts

Dois prompts para geração de documentação:

- **Prompt A** (`prompt_doc_a`): Abordagem 1
- **Prompt B** (`prompt_doc_b`): Abordagem 2

Ambos recebem `{files: dict}` e retornam documentação em formato markdown.

## Como Executar

```bash
# 1. Ativar venv
source ../venv/bin/activate

# 2. Upload do dataset (primeira vez)
python upload_dataset.py

# 3. Criar prompts no LangSmith (primeira vez)
python create_prompt.py

# 4. Executar avaliação (sempre usa versão mais recente dos prompts)
python run.py
```

## Análise dos Resultados

### Exemplo: Como Interpretar

Suponha que você executou `run.py` e obteve:

**DocPromptA_1430** (Experiment A):
```
conciseness:   0.85
coherence:     0.90
detail:        0.65
helpfulness:   0.88
faithfulness:  0.95
completeness:  0.70
```

**DocPromptB_1430** (Experiment B):
```
conciseness:   0.60
coherence:     0.85
detail:        0.92
helpfulness:   0.80
faithfulness:  0.98
completeness:  0.95
```

**DocPairwise_1430** (Pairwise Comparison - Juiz com Ground Truth):
```json
{
  "decision": "B",
  "reasoning": {
    "completude_estrutural": {
      "score_a": 7,
      "score_b": 9,
      "justificativa": "B documenta contexto, objetivos, tecnologias E pontos críticos (mais completo que A)"
    },
    "precisao_tecnica": {
      "score_a": 8,
      "score_b": 9,
      "justificativa": "Ambos precisos, mas B detalha melhor tipos e parâmetros das funções"
    },
    "clareza_utilidade": {
      "score_a": 9,
      "score_b": 7,
      "justificativa": "A é mais claro e direto, B tem seções mais densas"
    },
    "alinhamento_referencia": {
      "score_a": 6,
      "score_b": 9,
      "justificativa": "B segue estrutura da referência (Contexto > Objetivos > Tecnologias > Pontos Críticos), A diverge"
    },
    "concisao_detalhe": {
      "score_a": 8,
      "score_b": 6,
      "justificativa": "A mais conciso (melhor densidade), B mais verboso mas completo"
    },
    "score_total_a": 38,
    "score_total_b": 40,
    "decisao_final": "B vence por 2 pontos (40 vs 38). Principal diferença: alinhamento_referencia (9 vs 6) - B segue melhor a estrutura esperada do ground truth. Trade-off: A é mais conciso (8 vs 6), mas B é mais completo (9 vs 7 em completude_estrutural). Para documentação técnica, completude e alinhamento têm maior peso."
  }
}
```

### Insights da Análise

**Decisão do Juiz**: Prompt B ganhou (score 40 vs 38)

**Por que B ganhou? (análise das 5 métricas do juiz)**
1. **Alinhamento com Referência** (9 vs 6): B segue estrutura do ground truth (Contexto > Objetivos > Tecnologias > Pontos Críticos)
2. **Completude Estrutural** (9 vs 7): B documenta todos aspectos esperados (contexto, objetivos, tecnologias, pontos críticos)
3. **Precisão Técnica** (9 vs 8): B detalha melhor tipos e parâmetros

**Trade-offs identificados**:
- A vence em **Clareza** (9 vs 7): Mais direto e fácil de ler
- A vence em **Concisão** (8 vs 6): Melhor densidade de informação
- **Mas**: Para documentação técnica, completude e alinhamento com padrão têm maior peso

**Correlação com métricas individuais**:
- Métricas individuais: B tem **completeness** 0.95 vs 0.70 (alinha com score 9 vs 7 do juiz)
- Métricas individuais: A tem **conciseness** 0.85 vs 0.60 (alinha com score 8 vs 6 do juiz)

**Decisão de Engenharia**:
- Se objetivo é **seguir padrão corporativo** (ground truth): escolha Prompt B
- Se objetivo é documentação **rápida e clara**: escolha Prompt A
- Se objetivo é **balanceado**: crie Prompt C (estrutura de B + clareza de A)

## Vantagens dessa Abordagem

### 1. Transparência Total
- **Antes**: "B ganhou" (sem contexto)
- **Agora**: "B ganhou com score 40 vs 38, principalmente por alinhamento_referencia (9 vs 6) e completude_estrutural (9 vs 7)"

### 2. Debugging Granular
- Métricas individuais: identificam problemas gerais (ex: "conciseness baixa")
- Métricas do juiz: detalham trade-offs específicos (ex: "A sacrifica completude para ganhar clareza")

### 3. Iteração Direcionada
- Sabe **exatamente** o que melhorar: "Próximo prompt deve manter clareza de A (score 9) e adicionar completude de B (score 9)"

### 4. Ground Truth como Padrão
- Juiz compara com documentação de referência
- Identifica desvios estruturais (ex: "A não segue seções esperadas")
- Garante consistência com padrões corporativos

### 5. Justificativas Acionáveis
- Cada métrica tem justificativa específica (não genérica)
- Cita trechos e exemplos concretos
- Facilita decisões de engenharia de prompts

## Diferenças vs 3-pairwise/

| Aspecto | 3-pairwise/ | 4-pairwise-doc/ |
|---------|-------------|-----------------|
| Domínio | Code Review (security + performance) | Documentation Generation |
| Dataset | Code snippets (Go) | Codebases (múltiplos arquivos Python) |
| Ground Truth | Não | Sim (documentação de referência) |
| Prompts | Especialistas (security vs performance) | Abordagens de documentação |
| Métricas Individuais | Não | Sim (6 métricas: conciseness, coherence, detail, helpfulness, faithfulness, completeness) |
| Métricas do Juiz | Simples (A/B/EMPATE) | Robustas (5 dimensões com scores 0-10 + justificativas) |
| Output do Juiz | String ("A", "B", "EMPATE") | JSON estruturado (scores + reasoning detalhado) |
| Insights | "A ou B ganhou?" | "A ou B ganhou? Por quê? Scores por métrica? Trade-offs? Correlação com ground truth?" |

## Quando Usar Métricas Individuais?

**Use métricas individuais quando**:
- Precisa entender **por que** um prompt é melhor
- Quer **debugar** prompts (identificar pontos fracos)
- Precisa **justificar** escolha de prompt para stakeholders
- Quer **iterar** rapidamente (sabe exatamente o que melhorar)

**Apenas pairwise quando**:
- Decisão simples: "qual melhor?" (sem necessidade de breakdown)
- Rapidez é prioridade (menos LLM calls)
- Métricas individuais não agregam valor (ex: comparação A/B simples)

## Arquivos

- `run.py`: Script principal (executa avaliações)
- `utils.py`: Factories (prompts, judge, evaluators)
- `upload_dataset.py`: Upload de dataset para LangSmith
- `create_prompt.py`: Cria prompts A e B no LangSmith
- `dataset.jsonl`: Exemplos de codebases Python
- `prompts/llm_judge_pairwise.yaml`: Template do juiz (LLM-as-Judge)
