"""
Custom criteria evaluation: Demonstrating domain-specific evaluation criteria.
Shows how to define custom criteria beyond the 14 built-in options.
"""
from langsmith import evaluate
from langsmith.evaluation import LangChainStringEvaluator
from pathlib import Path
from shared.clients import get_openai_client, get_judge_llm
from shared.prompts import load_yaml_prompt, execute_text_prompt
from shared.evaluators import prepare_with_input

# Configuration
DATASET_NAME = "evaluation_basic_dataset"
BASE_DIR = Path(__file__).parent

# Setup
llm_client = get_openai_client()
prompt = load_yaml_prompt("additional_criteria.yaml")

def run_custom_criteria_evaluation(inputs: dict) -> dict:
    """Target function for evaluate()."""
    return execute_text_prompt(prompt, inputs, llm_client, input_key="code")

judge_llm = get_judge_llm()

evaluators = [
    LangChainStringEvaluator(
        "score_string",
        config={
            "criteria": {
                "faithfulness": "Is the response grounded ONLY in the provided code? Doesn't invent problems or context that doesn't exist in the code? Doesn't add assumptions about code that wasn't shown?"
            },
            "normalize_by": 10,
            "llm": judge_llm
        },
        prepare_data=prepare_with_input
    ),
    LangChainStringEvaluator(
        "score_string",
        config={
            "criteria": {
                "format_adherence": "Did the response follow EXACTLY the format instructions? Returned ONLY valid JSON without additional text before or after? No markdown, no extra explanations?"
            },
            "normalize_by": 10,
            "llm": judge_llm
        },
        prepare_data=prepare_with_input
    ),
    LangChainStringEvaluator(
        "score_string",
        config={
            "criteria": {
                "code_specificity": "Does the analysis mention specific line numbers? Uses precise technical terminology (e.g., sql_injection, n_plus_1_query)? Provides actionable details instead of generic ones?"
            },
            "normalize_by": 10,
            "llm": judge_llm
        },
        prepare_data=prepare_with_input
    ),
]

results = evaluate(
    run_custom_criteria_evaluation,
    data=DATASET_NAME,
    evaluators=evaluators,
    experiment_prefix="CustomCriteriaEval",
    max_concurrency=2
)

print("="*80)
print(f"EXPERIMENT: {results.experiment_name}")
print("="*80)