"""
Bad prompt test: Unhelpful responses.
Tests a prompt that provides generic, unhelpful feedback.
Expected: LOW scores in helpfulness, detail, and depth.
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

def run_bad_not_helpful(inputs: dict) -> dict:
    """Runs the bad_not_helpful prompt"""
    prompt = load_yaml_prompt("bad_not_helpful.yaml")
    return execute_text_prompt(prompt, inputs, llm_client, input_key="code", temperature=0.3)

judge_llm = get_judge_llm()

evaluators = [
    LangChainStringEvaluator(
        "score_string",
        config={"criteria": "helpfulness", "normalize_by": 10, "llm": judge_llm},
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
        "score_string",
        config={"criteria": "coherence", "normalize_by": 10, "llm": judge_llm},
        prepare_data=prepare_with_input
    ),
    LangChainStringEvaluator(
        "score_string",
        config={"criteria": "conciseness", "normalize_by": 10, "llm": judge_llm},
        prepare_data=prepare_with_input
    ),
]

print("="*80)
print("TEST: BAD_NOT_HELPFUL")
print("="*80)
print("\nExpected: LOW scores in helpfulness, detail and depth (< 0.4)")
print("Prompt: Lazy reviewer with generic responses")
print("="*80)
print()

results = evaluate(
    run_bad_not_helpful,
    data=DATASET_NAME,
    evaluators=evaluators,
    experiment_prefix="BadNotHelpful_Test",
    max_concurrency=2
)

print("="*80)
print(f"EXPERIMENT: {results.experiment_name}")
print("="*80)