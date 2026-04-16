"""Helpers for pairwise evaluation."""


def create_pairwise_evaluator(judge_prompt_obj, oai_client):
    """
    Create pairwise evaluator function for evaluate_comparative.

    Args:
        judge_prompt_obj: Judge prompt template (PromptTemplate)
        oai_client: OpenAI client

    Returns:
        Evaluator function with signature:
        (inputs: dict, outputs: list, reference_outputs: dict) -> list[float]

    The evaluator returns:
    - [1.0, 0.0] if A is better
    - [0.0, 1.0] if B is better
    - [0.5, 0.5] if tie

    Example:
        >>> from shared.prompts import load_yaml_prompt
        >>> from shared.clients import get_openai_client
        >>>
        >>> judge = load_yaml_prompt("pairwise_judge.yaml")
        >>> client = get_openai_client()
        >>> evaluator = create_pairwise_evaluator(judge, client)
        >>>
        >>> # Use in evaluate_comparative
        >>> results = evaluate_comparative(
        ...     [exp_a, exp_b],
        ...     evaluators=[evaluator]
        ... )
    """
    from shared.clients import get_model_name, get_temperature

    def evaluate_pairwise(inputs: dict, outputs: list, reference_outputs: dict = None):
        """Pairwise comparison evaluator."""
        code = inputs.get("code", "")
        answer_a = outputs[0].get("output", "")
        answer_b = outputs[1].get("output", "")

        # Format judge prompt
        judge_prompt = judge_prompt_obj.format(
            code=code,
            answer_a=answer_a,
            answer_b=answer_b
        )

        # Get judge decision
        response = oai_client.chat.completions.create(
            messages=[{"role": "user", "content": judge_prompt}],
            model=get_model_name(),
            temperature=get_temperature()
        )

        decision = response.choices[0].message.content.strip().upper()

        # Parse decision
        if "A" in decision and "B" not in decision:
            return [1.0, 0.0]  # A wins
        elif "B" in decision and "A" not in decision:
            return [0.0, 1.0]  # B wins
        else:
            return [0.5, 0.5]  # Tie

    return evaluate_pairwise
