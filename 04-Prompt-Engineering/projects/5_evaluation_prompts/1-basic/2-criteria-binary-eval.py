"""
Binary criteria evaluation: Pass/Fail evaluation using LLM judges.

Demonstrates binary evaluators (0 or 1) for quick yes/no validation.
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


def run_criteria_evaluation(inputs: dict) -> dict:
    """Target function for evaluate()."""
    return execute_text_prompt(prompt, inputs, llm_client, input_key="code")


# BINARY EVALUATORS: criteria (0 or 1)
#
# criteria: Returns 0 (fail) or 1 (pass)
# - Faster and more direct
# - Ideal for pass/fail yes/no validations
# - Examples: "Is JSON valid?", "Is response concise?", "Is it harmful?"
#
# Use criteria when:
# - You need simple pass/fail validation
# - Question is yes/no type
# - You want fast binary decisions
#
# NOTE: Next example (3-criteria-score-eval.py) shows score_string,
# which returns continuous values (0.0-1.0) for nuanced evaluations.

# Judge LLM pointing to Ollama
judge_llm = get_judge_llm()

evaluators = [
    LangChainStringEvaluator(
        "criteria",
        config={"criteria": "conciseness", "llm": judge_llm},
        prepare_data=prepare_with_input
    ),
    LangChainStringEvaluator(
        "criteria",
        config={"criteria": "helpfulness", "llm": judge_llm},
        prepare_data=prepare_with_input
    ),
    LangChainStringEvaluator(
        "labeled_criteria",
        config={"criteria": "correctness", "llm": judge_llm},
        prepare_data=prepare_with_reference
    ),
]

# Run evaluation
results = evaluate(
    run_criteria_evaluation,
    data=DATASET_NAME,
    evaluators=evaluators,
    experiment_prefix="CriteriaBinary",
    max_concurrency=2
)

print("="*80)
print(f"EXPERIMENT: {results.experiment_name}")
print("="*80)
