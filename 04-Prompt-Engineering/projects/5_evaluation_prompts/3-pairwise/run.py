from langsmith import evaluate, Client
from langsmith.evaluation import evaluate_comparative
from datetime import datetime

from shared.clients import get_openai_client
from shared.prompts import load_yaml_prompt, execute_chat_prompt
from pairwise_helpers import create_pairwise_evaluator

# Configuration
DATASET_NAME = "pairwise_initial_comparison"
PROMPT_A_ID = "pairwise_comparison_security"
PROMPT_B_ID = "pairwise_comparison_performance"

# Setup
client = Client()
llm_client = get_openai_client()
timestamp = datetime.now().strftime("%H%M")

# Load judge template and prompts
judge_template = load_yaml_prompt("pairwise_judge.yaml")
prompt_a_obj = client.pull_prompt(PROMPT_A_ID)
prompt_b_obj = client.pull_prompt(PROMPT_B_ID)

print(f" Prompt A: {PROMPT_A_ID}")
print(f" Prompt B: {PROMPT_B_ID}\n")


def run_prompt_a(inputs: dict) -> dict:
    """Execute Prompt A."""
    return execute_chat_prompt(
        prompt_a_obj,
        inputs,
        llm_client,
        code=inputs['code'],
        language=inputs['language']
    )


def run_prompt_b(inputs: dict) -> dict:
    """Execute Prompt B."""
    return execute_chat_prompt(
        prompt_b_obj,
        inputs,
        llm_client,
        code=inputs['code'],
        language=inputs['language']
    )


# Create pairwise judge
pairwise_judge = create_pairwise_evaluator(judge_template, llm_client)

# Main
if __name__ == "__main__":

    # Run Prompt A
    results_a = evaluate(
        run_prompt_a,
        data=DATASET_NAME,
        experiment_prefix=f"PairwiseA_{timestamp}",
        max_concurrency=2
    )

    # Run Prompt B
    results_b = evaluate(
        run_prompt_b,
        data=DATASET_NAME,
        experiment_prefix=f"PairwiseB_{timestamp}",
        max_concurrency=2
    )

    # Pairwise comparison
    pairwise_results = evaluate_comparative(
        [results_a.experiment_name, results_b.experiment_name],
        evaluators=[pairwise_judge],
        experiment_prefix=f"Pairwise_{timestamp}",
        max_concurrency=2
    )

    print("\n" + "="*80)
    print(f"Evaluation completed! (Timestamp: {timestamp})")
    print(f"Experiment A: {results_a.experiment_name}")
    print(f"Experiment B: {results_b.experiment_name}")
    print(f"Comparison: Pairwise_{timestamp}")
    print("\nView results in LangSmith dashboard:")
    print("  • https://smith.langchain.com")
    print("  • Datasets and Testing > Pairwise Experiments")
    print("="*80)
