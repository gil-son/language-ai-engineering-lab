"""Precision, Recall, and F1 Score metrics for evaluation."""
from typing import Set, Callable, List, Dict
from shared.parsers import parse_json_response


def calculate_precision_recall_f1(
    outputs: List[Dict],
    examples: List,
    extract_predicted: Callable[[Dict], Set],
    extract_expected: Callable[[Dict], Set]
) -> List[Dict]:
    """
    Calculate precision, recall, and F1 score.

    Generic implementation that works with any extraction functions.

    Args:
        outputs: List of model outputs
        examples: List of dataset examples
        extract_predicted: Function to extract predicted set from output
        extract_expected: Function to extract expected set from example

    Returns:
        List of metric dictionaries:
        [
            {"key": "precision", "score": float, "comment": str},
            {"key": "recall", "score": float, "comment": str},
            {"key": "f1", "score": float, "comment": str}
        ]

    Example:
        >>> results = calculate_precision_recall_f1(
        ...     outputs,
        ...     examples,
        ...     extract_predicted=extract_issue_types,
        ...     extract_expected=lambda ex: set(ex.outputs["expected_issue_types"])
        ... )
    """
    tp = fp = fn = 0

    for output, example in zip(outputs, examples):
        predicted = extract_predicted(output)
        expected = extract_expected(example)

        tp += len(predicted & expected) # {"bug", "error"} & {"bug", "crash"} = {"bug"} (1 TP)
        fp += len(predicted - expected) # {"bug", "error"} - {"bug", "crash"} = {"error"} (1 FP)
        fn += len(expected - predicted) # {"bug", "crash"} - {"bug", "error"} = {"crash"} (1 FN)

    # Calculate metrics
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return [
        {
            "key": "precision",
            "score": precision,
            "comment": f"TP:{tp} FP:{fp}"
        },
        {
            "key": "recall",
            "score": recall,
            "comment": f"TP:{tp} FN:{fn}"
        },
        {
            "key": "f1",
            "score": f1,
            "comment": f"P:{precision:.2f} R:{recall:.2f}"
        }
    ]


def extract_findings_comparable(output: Dict) -> Set[tuple]:
    """
    Extract ONLY comparable fields (type, severity) as tuples.

    Ignores line, description, and summary (cannot exact match).
    Only compares structured fields that can match exactly.

    Why only type + severity?
    - Text fields (description, summary) will NEVER match exactly between
      ground truth and LLM output due to natural language variation
    - Line numbers may vary depending on how LLM counts
    - Only structured, controlled vocabulary fields can be compared fairly

    Args:
        output: Model output dictionary with "output" key containing JSON

    Returns:
        Set of (type, severity) tuples

    Example:
        >>> output = {
        ...     "output": '''{
        ...         "findings": [
        ...             {"type": "sql_injection", "severity": "critical", "line": 9, ...},
        ...             {"type": "missing_timeout", "severity": "medium", "line": 8, ...}
        ...         ]
        ...     }'''
        ... }
        >>> extract_findings_comparable(output)
        {('sql_injection', 'critical'), ('missing_timeout', 'medium')}
    """
    data = parse_json_response(output.get("output", ""))
    findings = set()

    for f in data.get("findings", []):
        finding_tuple = (
            f.get("type", ""),
            f.get("severity", "").lower()  # Normalize to lowercase
        )
        findings.add(finding_tuple)

    return findings
