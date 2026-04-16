# Requires: pip install langchain-community numpy
"""
Embedding distance evaluation: Semantic similarity measurement.
Demonstrates deterministic evaluator using vector embeddings.
"""
from langsmith import evaluate
from langsmith.evaluation import LangChainStringEvaluator
from langchain_community.embeddings import OllamaEmbeddings
from pathlib import Path
import os
from shared.clients import get_openai_client
from shared.prompts import load_yaml_prompt, execute_text_prompt
from shared.evaluators import prepare_with_reference

# Configuration
DATASET_NAME = "evaluation_basic_dataset"
BASE_DIR = Path(__file__).parent

# Setup
llm_client = get_openai_client()
prompt = load_yaml_prompt("embedding_distance_eval.yaml")

def run_embedding_evaluation(inputs: dict) -> dict:
    """Target function for evaluate()."""
    return execute_text_prompt(prompt, inputs, llm_client, input_key="code")

# OllamaEmbeddings uses nomic-embed-text — you already have it pulled
embeddings = OllamaEmbeddings(
    model=os.getenv("EMBEDDING_MODEL", "nomic-embed-text"),
)

evaluators = [
    LangChainStringEvaluator(
        "embedding_distance",
        config={"embeddings": embeddings},
        prepare_data=prepare_with_reference
    )
]

results = evaluate(
    run_embedding_evaluation,
    data=DATASET_NAME,
    evaluators=evaluators,
    experiment_prefix="EmbeddingDistanceEval",
    max_concurrency=2
)

print("="*80)
print(f"EXPERIMENT: {results.experiment_name}")
print("="*80)