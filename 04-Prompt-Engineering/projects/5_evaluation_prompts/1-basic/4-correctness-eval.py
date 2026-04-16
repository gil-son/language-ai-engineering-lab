"""
Correctness evaluation: Comparing predictions against reference outputs.
Demonstrates labeled evaluators that use reference outputs for comparison.
"""
from langsmith import evaluate
from langsmith.evaluation import LangChainStringEvaluator
from pathlib import Path
from shared.clients import get_openai_client, get_judge_llm
from shared.prompts import load_yaml_prompt, execute_text_prompt
from shared.evaluators import prepare_with_reference

# Configuration
DATASET_NAME = "evaluation_basic_dataset"
BASE_DIR = Path(__file__).parent

# Setup
llm_client = get_openai_client()
prompt = load_yaml_prompt("correctness_eval.yaml")

def run_correctness_evaluation(inputs: dict) -> dict:
    """Target function for evaluate()."""
    return execute_text_prompt(prompt, inputs, llm_client, input_key="code")

judge_llm = get_judge_llm()

evaluators = [
    LangChainStringEvaluator(
        "labeled_score_string",
        config={"criteria": "correctness", "normalize_by": 10, "llm": judge_llm},
        prepare_data=prepare_with_reference
    ),
    LangChainStringEvaluator(
        "labeled_score_string",
        config={"criteria": "relevance", "normalize_by": 10, "llm": judge_llm},
        prepare_data=prepare_with_reference
    )
]

results = evaluate(
    run_correctness_evaluation,
    data=DATASET_NAME,
    evaluators=evaluators,
    experiment_prefix="CorrectnessEval",
    max_concurrency=2
)

print("="*80)
print(f"EXPERIMENT: {results.experiment_name}")
print("="*80)