"""Helper functions for creating prepare_data functions."""


def prepare_prediction_only(run, example):
    """
    Prepare data with only prediction (for evaluators that don't need input/reference).

    Use for:
    - json_validity
    - json_schema

    Args:
        run: LangSmith run object
        example: Dataset example

    Returns:
        {"prediction": str}
    """
    return {"prediction": run.outputs.get("output", "")}


def prepare_with_input(run, example, input_key="code"):
    """
    Prepare data with prediction + input (for evaluators without reference).

    Use for:
    - criteria (binary)
    - score_string (continuous)
    - Custom criteria

    Args:
        run: LangSmith run object
        example: Dataset example
        input_key: Key to extract from inputs (default: "code")

    Returns:
        {"prediction": str, "input": str}
    """
    return {
        "prediction": run.outputs.get("output", ""),
        "input": example.inputs.get(input_key, "")
    }


def prepare_with_reference(run, example, input_key="code"):
    """
    Prepare data with prediction + input + reference (for labeled evaluators).

    Use for:
    - labeled_criteria
    - labeled_score_string
    - embedding_distance

    Args:
        run: LangSmith run object
        example: Dataset example
        input_key: Key to extract from inputs (default: "code")

    Returns:
        {"prediction": str, "input": str, "reference": dict}
    """
    return {
        "prediction": run.outputs.get("output", ""),
        "input": example.inputs.get(input_key, ""),
        "reference": example.outputs
    }
