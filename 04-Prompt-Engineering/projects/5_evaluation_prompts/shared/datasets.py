"""Dataset upload utilities with metadata support."""
from pathlib import Path
import json
from typing import Optional


def upload_langsmith_dataset(
    dataset_file: Path,
    dataset_name: str,
    description: str,
    langsmith_client
) -> int:
    """
    Upload dataset to LangSmith with metadata support.

    IMPORTANT: Extracts and uploads the 'metadata' field from JSONL.

    Dataset JSONL format:
    {
        "inputs": {...},
        "outputs": {...},
        "metadata": {...}  # <- Extracted and uploaded
    }

    Args:
        dataset_file: Path to JSONL file
        dataset_name: Name for dataset in LangSmith
        description: Dataset description
        langsmith_client: LangSmith client instance

    Returns:
        Number of examples uploaded

    Example:
        >>> from shared.clients import get_langsmith_client
        >>> client = get_langsmith_client()
        >>> count = upload_langsmith_dataset(
        ...     Path("dataset.jsonl"),
        ...     "my_dataset",
        ...     "My evaluation dataset",
        ...     client
        ... )
    """
    # Load examples from JSONL
    with open(dataset_file, 'r') as f:
        examples = [json.loads(line) for line in f if line.strip()]

    # Try to read existing dataset, or create new one
    try:
        dataset = langsmith_client.read_dataset(dataset_name=dataset_name)

        # Delete all existing examples
        for example in langsmith_client.list_examples(dataset_name=dataset_name):
            langsmith_client.delete_example(example.id)

    except Exception:
        # Dataset doesn't exist, create it
        dataset = langsmith_client.create_dataset(
            dataset_name=dataset_name,
            description=description
        )

    # Upload examples with metadata
    for example in examples:
        inputs = example["inputs"]
        outputs = example["outputs"]
        metadata = example.get("metadata", {})  # Extract metadata

        langsmith_client.create_example(
            inputs=inputs,
            outputs=outputs,
            metadata=metadata,  # Upload metadata!
            dataset_id=dataset.id
        )

    return len(examples)


def upload_langfuse_dataset(
    dataset_file: Path,
    dataset_name: str,
    description: str,
    langfuse_client,
    metadata_override: Optional[dict] = None
) -> int:
    """
    Upload dataset to Langfuse with metadata support.

    IMPORTANT: Extracts and uploads the 'metadata' field from JSONL.

    Args:
        dataset_file: Path to JSONL file
        dataset_name: Name for dataset in Langfuse
        description: Dataset description
        langfuse_client: Langfuse client instance
        metadata_override: Optional metadata to add to dataset itself

    Returns:
        Number of examples uploaded

    Example:
        >>> from shared.clients import get_langfuse_client
        >>> client = get_langfuse_client()
        >>> count = upload_langfuse_dataset(
        ...     Path("dataset.jsonl"),
        ...     "my_dataset",
        ...     "My evaluation dataset",
        ...     client
        ... )
    """
    # Load examples from JSONL
    with open(dataset_file, 'r') as f:
        examples = [json.loads(line) for line in f if line.strip()]

    # Try to create dataset (may already exist)
    try:
        langfuse_client.create_dataset(
            name=dataset_name,
            description=description,
            metadata=metadata_override or {"source": "upload_script"}
        )
    except Exception:
        pass  # Dataset already exists

    # Upload items with metadata
    for example in examples:
        inputs = example["inputs"]
        outputs = example["outputs"]
        metadata = example.get("metadata", {})  # Extract metadata

        langfuse_client.create_dataset_item(
            dataset_name=dataset_name,
            input=inputs,
            expected_output=outputs,
            metadata=metadata  # Upload metadata!
        )

    langfuse_client.flush()
    return len(examples)
