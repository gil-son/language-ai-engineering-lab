"""Upload dataset to LangSmith with metadata support."""
from pathlib import Path
from shared.clients import get_langsmith_client
from shared.datasets import upload_langsmith_dataset

SCRIPT_DIR = Path(__file__).parent
DATASET_FILE = SCRIPT_DIR / "dataset.jsonl"
DATASET_NAME = "evaluation_precision_dataset"

client = get_langsmith_client()

count = upload_langsmith_dataset(
    DATASET_FILE,
    DATASET_NAME,
    "Precision/Recall dataset with structured ground truth for bug detection",
    client
)

print(f"Dataset '{DATASET_NAME}' updated with {count} examples")
