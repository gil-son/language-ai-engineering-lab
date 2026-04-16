from langsmith import evaluate, Client
from langsmith.evaluation import evaluate_comparative
from datetime import datetime

from shared.clients import get_openai_client
from shared.prompts import load_yaml_prompt, execute_chat_prompt
from pairwise_helpers import create_pairwise_judge
from doc_evaluators import create_evaluators_for_documentation

# Configuration
DATASET_NAME = "dataset_docgen"
PROMPT_A_ID = "prompt_doc_a"
PROMPT_B_ID = "prompt_doc_b"

# Setup
client = Client()
llm_client = get_openai_client()
timestamp = datetime.now().strftime("%H%M")

# Load judge template and prompts
judge_template = load_yaml_prompt("llm_judge_pairwise.yaml")
prompt_a_obj = client.pull_prompt(PROMPT_A_ID)
prompt_b_obj = client.pull_prompt(PROMPT_B_ID)

print(f"Prompt A: {PROMPT_A_ID}")
print(f"Prompt B: {PROMPT_B_ID}\n")


def run_prompt_a(inputs: dict) -> dict:
    """Execute Prompt A."""
    return execute_chat_prompt(
        prompt_a_obj,
        inputs,
        llm_client,
        files=inputs['files']
    )


def run_prompt_b(inputs: dict) -> dict:
    """Execute Prompt B."""
    return execute_chat_prompt(
        prompt_b_obj,
        inputs,
        llm_client,
        files=inputs['files']
    )


# Create pairwise judge and doc evaluators
pairwise_judge = create_pairwise_judge(judge_template, llm_client)
doc_evaluators = create_evaluators_for_documentation()

if __name__ == "__main__":
    print("Evaluating Prompt A - conformance with reference...")
    results_a = evaluate(
        run_prompt_a,
        data=DATASET_NAME,
        evaluators=doc_evaluators,
        experiment_prefix=f"DocPromptA_{timestamp}",
        max_concurrency=2
    )

    print("Evaluating Prompt B - conformance with reference...")
    results_b = evaluate(
        run_prompt_b,
        data=DATASET_NAME,
        evaluators=doc_evaluators,
        experiment_prefix=f"DocPromptB_{timestamp}",
        max_concurrency=2
    )

    print("Running pairwise comparison (LLM-as-Judge)...")
    pairwise_results = evaluate_comparative(
        [results_a.experiment_name, results_b.experiment_name],
        evaluators=[pairwise_judge],
        experiment_prefix=f"DocPairwise_{timestamp}",
        max_concurrency=2
    )

