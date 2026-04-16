"""
Continuous criteria evaluation: Score-based evaluation using LLM judges.

Demonstrates continuous evaluators (0.0-1.0) for nuanced quality assessment.
"""
from langsmith import evaluate
from langsmith.evaluation import LangChainStringEvaluator
from pathlib import Path
from shared.clients import get_openai_client, get_judge_llm
from shared.prompts import load_yaml_prompt, execute_text_prompt
from shared.evaluators import prepare_with_input, prepare_with_reference

# Configuration
DATASET_NAME = "evaluation_basic_dataset"
BASE_DIR = Path(__file__).parent

# Setup
llm_client = get_openai_client()
prompt = load_yaml_prompt("criteria_eval.yaml")


def run_score_evaluation(inputs: dict) -> dict:
    """Target function for evaluate()."""
    return execute_text_prompt(prompt, inputs, llm_client, input_key="code")


# CONTINUOUS EVALUATORS: score_string (0.0-1.0)
#
# Difference from example 2:
# - Example 2 uses criteria (binary 0/1)
# - Example 3 uses score_string (continuous 0.0-1.0)
#
# Criteria chosen for CODE REVIEW:
# - conciseness: Also in ex.2 (shows difference binary vs continuous)
# - coherence: Analysis should be coherent and well-structured
# - detail: Code review needs technical details (lines, issue types)
# - depth: Analysis should go beyond obvious, identify non-trivial issues
# - relevance: Should be relevant to analyzed code (with reference)



# Judge LLM pointing to Ollama
judge_llm = get_judge_llm()

evaluators = [
    LangChainStringEvaluator(
        "score_string",
        config={"criteria": "conciseness", "normalize_by": 10, "llm": judge_llm},
        prepare_data=prepare_with_input
    ),
    LangChainStringEvaluator(
        "score_string",
        config={"criteria": "coherence", "normalize_by": 10, "llm": judge_llm},
        prepare_data=prepare_with_input
    ),
    LangChainStringEvaluator(
        "score_string",
        config={"criteria": "detail", "normalize_by": 10, "llm": judge_llm},
        prepare_data=prepare_with_input
    ),
    LangChainStringEvaluator(
        "score_string",
        config={"criteria": "depth", "normalize_by": 10, "llm": judge_llm},
        prepare_data=prepare_with_input
    ),
    LangChainStringEvaluator(
        "labeled_score_string",
        config={"criteria": "relevance", "normalize_by": 10, "llm": judge_llm},
        prepare_data=prepare_with_reference
    ),
]

# Run evaluation
results = evaluate(
    run_score_evaluation,
    data=DATASET_NAME,
    evaluators=evaluators,
    experiment_prefix="CriteriaScoreEval",
    max_concurrency=2
)

print("="*80)
print(f"EXPERIMENT: {results.experiment_name}")
print("="*80)
