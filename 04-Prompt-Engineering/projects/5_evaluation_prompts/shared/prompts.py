"""Utilities for loading and executing prompts."""
from langchain.prompts import load_prompt
from pathlib import Path
from typing import Optional


def load_yaml_prompt(filename: str, prompts_dir: Optional[Path] = None):
    """
    Load YAML prompt from file.

    Args:
        filename: Prompt filename (e.g., "format_eval.yaml")
        prompts_dir: Directory containing prompts (default: ./prompts from caller)

    Returns:
        Loaded prompt object (PromptTemplate or ChatPromptTemplate)

    Example:
        >>> prompt = load_yaml_prompt("format_eval.yaml")
        >>> # Auto-detects prompts/ directory in caller's location
    """
    if prompts_dir is None:
        import inspect
        caller_file = Path(inspect.stack()[1].filename)
        prompts_dir = caller_file.parent / "prompts"

    return load_prompt(prompts_dir / filename)


def execute_text_prompt(prompt_obj, inputs: dict, oai_client,
                        input_key: str = "code", model: str = None,
                        temperature: float = None):
    """
    Execute simple text prompt (PromptTemplate).

    Args:
        prompt_obj: Loaded prompt object
        inputs: Input dictionary from dataset
        oai_client: OpenAI client
        input_key: Key to extract from inputs (default: "code")
        model: Model name (default: from environment)
        temperature: Temperature (default: from environment)

    Returns:
        {"output": str} - Model response

    Example:
        >>> result = execute_text_prompt(prompt, {"code": "..."}, client)
        >>> print(result["output"])
    """
    from shared.clients import get_model_name, get_temperature

    # Use environment defaults if not specified
    if model is None:
        model = get_model_name()
    if temperature is None:
        temperature = get_temperature()

    prompt_text = prompt_obj.format(**{input_key: inputs[input_key]})

    response = oai_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt_text}],
        model=model,
        temperature=temperature
    )

    return {"output": response.choices[0].message.content}


def convert_langchain_to_openai_messages(messages):
    """
    Convert LangChain messages to OpenAI format.

    Args:
        messages: List of LangChain message objects

    Returns:
        List of dicts in OpenAI format: [{"role": "user", "content": "..."}]

    Example:
        >>> lc_messages = prompt.format_messages(code="...")
        >>> openai_msgs = convert_langchain_to_openai_messages(lc_messages)
    """
    openai_messages = []
    for m in messages:
        role = "user" if m.type == "human" else m.type
        openai_messages.append({"role": role, "content": m.content})
    return openai_messages


def execute_chat_prompt(prompt_obj, inputs: dict, oai_client,
                       model: str = None, temperature: float = None,
                       **format_kwargs):
    """
    Execute chat prompt (ChatPromptTemplate).

    Args:
        prompt_obj: ChatPromptTemplate object
        inputs: Input dictionary from dataset
        oai_client: OpenAI client
        model: Model name (default: from environment)
        temperature: Temperature (default: from environment)
        **format_kwargs: Arguments for format_messages()

    Returns:
        {"output": str} - Model response

    Example:
        >>> result = execute_chat_prompt(
        ...     prompt, inputs, client,
        ...     code=inputs['code'],
        ...     language=inputs['language']
        ... )
    """
    from shared.clients import get_model_name, get_temperature

    # Use environment defaults if not specified
    if model is None:
        model = get_model_name()
    if temperature is None:
        temperature = get_temperature()

    messages = prompt_obj.format_messages(**format_kwargs)
    openai_messages = convert_langchain_to_openai_messages(messages)

    response = oai_client.chat.completions.create(
        messages=openai_messages,
        model=model,
        temperature=temperature
    )

    return {"output": response.choices[0].message.content}
