"""Langfuse-specific helper functions."""
import json


def run_with_chat_prompt(prompt_obj, inputs, oai_client):
    """
    Execute a chat prompt with Langfuse prompt object.

    Args:
        prompt_obj: Langfuse prompt object
        inputs: Input dictionary
        oai_client: OpenAI client

    Returns:
        String response from model
    """
    from shared.clients import get_model_name, get_temperature

    # Compile prompt (Langfuse SDK handles message formatting)
    compiled_prompt = prompt_obj.compile(**inputs)

    response = oai_client.chat.completions.create(
        messages=compiled_prompt,
        model=get_model_name(),
        temperature=get_temperature()
    )

    return response.choices[0].message.content


def run_with_text_prompt(prompt_obj, oai_client, **kwargs):
    """
    Execute a text prompt with Langfuse prompt object.

    Args:
        prompt_obj: Langfuse text prompt object
        oai_client: OpenAI client
        **kwargs: Variables to compile into prompt

    Returns:
        String response from model
    """
    from shared.clients import get_model_name, get_temperature

    # Compile text prompt with variables
    compiled_prompt = prompt_obj.compile(**kwargs)

    response = oai_client.chat.completions.create(
        messages=[{"role": "user", "content": compiled_prompt}],
        model=get_model_name(),
        temperature=get_temperature()
    )

    return response.choices[0].message.content


def parse_judge_response(response_text: str):
    """
    Parse JSON response from judge, handling markdown blocks.

    Args:
        response_text: Raw judge response

    Returns:
        Tuple of (decision, reasoning)
        decision: "A", "B", or "TIE"
        reasoning: Dictionary of reasoning details
    """
    from shared.parsers import parse_json_response

    result = parse_json_response(response_text)

    if result:
        return result.get("decision", "TIE"), result.get("reasoning", {})
    else:
        return "TIE", {"error": "Failed to parse JSON"}


def format_reasoning_summary(reasoning: dict) -> str:
    """
    Format reasoning dictionary into readable string.

    Args:
        reasoning: Reasoning dictionary from judge

    Returns:
        Formatted multi-line string
    """
    lines = []

    # Total scores
    if "score_total_a" in reasoning and "score_total_b" in reasoning:
        lines.append(
            f"Total Scores - A: {reasoning['score_total_a']}/50, "
            f"B: {reasoning['score_total_b']}/50"
        )

    # Final decision
    if "final_decision" in reasoning:
        lines.append(f"\nDecision: {reasoning['final_decision']}")

    # Detailed breakdown of each dimension
    dimensions = [
        ("structural_completeness", "Structural Completeness"),
        ("technical_precision", "Technical Precision"),
        ("clarity_and_utility", "Clarity and Utility"),
        ("reference_alignment", "Reference Alignment"),
        ("conciseness_vs_detail", "Conciseness vs Detail")
    ]

    for key, label in dimensions:
        if key in reasoning:
            dim = reasoning[key]
            score_a = dim.get("score_a", "?")
            score_b = dim.get("score_b", "?")
            justification = dim.get("justification", "")

            lines.append(f"\n{label}: A={score_a}/10, B={score_b}/10")
            if justification:
                lines.append(f"  -> {justification}")

    return "\n".join(lines) if lines else "No reasoning provided"
