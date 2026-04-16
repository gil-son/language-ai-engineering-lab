from dotenv import load_dotenv
load_dotenv()

from langfuse import Langfuse
import yaml
import os

PROMPT_A_NAME = "prompt_doc_a"
PROMPT_B_NAME = "prompt_doc_b"
PROMPT_JUDGE_NAME = "llm_judge_pairwise"
PROMPT_CODE_ANALYZER_NAME = "1-correctness-langfuse"

langfuse = Langfuse()
script_dir = os.path.dirname(os.path.abspath(__file__))

def load_yaml_prompt(filename):
    """Loads YAML prompt and extracts information"""
    with open(os.path.join(script_dir, f"prompts/{filename}"), "r") as f:
        config = yaml.safe_load(f)

    if "messages" not in config:
        raise ValueError(f"YAML format not supported: {filename}")

    return config["messages"]

def create_chat_prompt(name: str, messages: list, description: str, labels: list = None):
    """Creates a chat prompt in Langfuse"""
    # Convert messages from YAML format to Langfuse format
    # Expected format: [{"role": "system", "content": "..."}, ...]
    langfuse_messages = []
    for msg in messages:
        langfuse_messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    try:
        prompt = langfuse.create_prompt(
            name=name,
            type="chat",
            prompt=langfuse_messages,
            labels=labels or [],
            config={
                "model": "gpt-4o-mini",
                "temperature": 0
            }
        )
        print(f"✓ Prompt '{name}' created successfully")
        return prompt
    except Exception as e:
        print(f"✗ Error creating prompt '{name}': {str(e)}")
        raise

if __name__ == "__main__":
    print("Creating prompts in Langfuse...")
    print("="*60)

    # Load prompts from YAML files
    prompt_a_messages = load_yaml_prompt("prompt_doc_a.yaml")
    prompt_b_messages = load_yaml_prompt("prompt_doc_b.yaml")
    prompt_code_analyzer_messages = load_yaml_prompt("1-correctness-langfuse.yaml")

    # Load judge prompt (text format, not chat)
    with open(os.path.join(script_dir, "prompts/llm_judge_pairwise.yaml"), "r") as f:
        judge_config = yaml.safe_load(f)
        judge_prompt_text = judge_config["template"]

    # Create Prompt A
    create_chat_prompt(
        name=PROMPT_A_NAME,
        messages=prompt_a_messages,
        description="Prompt A: Generates structured technical documentation with implementation details",
        labels=["production", "documentation"]
    )

    # Create Prompt B
    create_chat_prompt(
        name=PROMPT_B_NAME,
        messages=prompt_b_messages,
        description="Prompt B: Generates high-level factual documentation without technical specifics",
        labels=["production", "documentation"]
    )

    # Create Prompt Judge (text prompt, not chat)
    try:
        langfuse.create_prompt(
            name=PROMPT_JUDGE_NAME,
            type="text",
            prompt=judge_prompt_text,
            labels=["evaluation", "pairwise"],
            config={
                "model": "gpt-4o-mini",
                "temperature": 0
            }
        )
        print(f"✓ Prompt '{PROMPT_JUDGE_NAME}' created successfully")
    except Exception as e:
        print(f"✗ Error creating prompt '{PROMPT_JUDGE_NAME}': {str(e)}")

    # Create Code Analyzer Prompt
    create_chat_prompt(
        name=PROMPT_CODE_ANALYZER_NAME,
        messages=prompt_code_analyzer_messages,
        description="Code Analyzer: Identifies security, performance, and quality issues in Go code",
        labels=["production", "code-analysis"]
    )

    print("="*60)
    print("Prompts created successfully:")
    print(f"  - {PROMPT_A_NAME}")
    print(f"  - {PROMPT_B_NAME}")
    print(f"  - {PROMPT_JUDGE_NAME}")
    print(f"  - {PROMPT_CODE_ANALYZER_NAME}")
    print()
    print("Access Langfuse UI to view the created prompts.")
