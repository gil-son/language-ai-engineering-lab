"""JSON and markdown parsing utilities."""
import json


def parse_json_response(text: str) -> dict:
    """
    Parse JSON from LLM response, removing markdown blocks if present.

    LLMs often wrap JSON in markdown code blocks like:
    ```json
    {"key": "value"}
    ```

    This function handles both raw JSON and markdown-wrapped JSON.

    Args:
        text: Raw text from LLM (may contain markdown)

    Returns:
        Parsed dictionary, or empty dict {} if parsing fails

    Example:
        >>> parse_json_response('```json\\n{"a": 1}\\n```')
        {'a': 1}
        >>> parse_json_response('{"a": 1}')
        {'a': 1}
        >>> parse_json_response('invalid')
        {}
    """
    text = text.strip()

    # Remove markdown code blocks
    if text.startswith("```"):
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end > start:
            text = text[start:end]

    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return {}
