"""
Bad prompt test: Overly verbose output.
Tests a prompt that generates excessively verbose responses.
Expected: LOW scores in conciseness and coherence.
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

def run_bad_verbose(inputs: dict) -> dict:
    """Runs the bad_verbose prompt"""
    prompt = load_yaml_prompt("bad_verbose.yaml")
    return execute_text_prompt(prompt, inputs, llm_client, input_key="code", temperature=1.0)

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
        config={"criteria": "helpfulness", "normalize_by": 10, "llm": judge_llm},
        prepare_data=prepare_with_input
    ),
    LangChainStringEvaluator(
        "score_string",
        config={"criteria": "detail", "normalize_by": 10, "llm": judge_llm},
        prepare_data=prepare_with_input
    ),
]

print("="*80)
print("TEST: BAD_VERBOSE")
print("="*80)
print("\nExpected: LOW scores in conciseness and coherence (< 0.4)")
print("Prompt: Detailed teacher with contradictory instructions")
print("="*80)
print()

results = evaluate(
    run_bad_verbose,
    data=DATASET_NAME,
    evaluators=evaluators,
    experiment_prefix="BadVerbose_Test",
    max_concurrency=2
)

print("="*80)
print(f"EXPERIMENT: {results.experiment_name}")
print("="*80)