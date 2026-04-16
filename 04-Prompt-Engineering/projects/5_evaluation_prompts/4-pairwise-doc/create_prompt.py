from dotenv import load_dotenv
load_dotenv()

from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
import yaml
import os

PROMPT_A_ID = "prompt_doc_a"
PROMPT_B_ID = "prompt_doc_b"

client = Client()
script_dir = os.path.dirname(os.path.abspath(__file__))

def load_yaml_as_chat_template(filename):
    with open(os.path.join(script_dir, f"prompts/{filename}"), "r") as f:
        config = yaml.safe_load(f)

    if "messages" in config:
        messages = [(msg["role"], msg["content"]) for msg in config["messages"]]
        return ChatPromptTemplate.from_messages(messages)

    raise ValueError(f"YAML format not supported: {filename}")

def push_prompt(prompt_id: str, prompt_obj, description: str):
    try:
        commit_hash = client.push_prompt(
            prompt_identifier=prompt_id,
            object=prompt_obj,
            description=description
        )
        return commit_hash
    except Exception as e:
        if "Nothing to commit" not in str(e):
            raise

PROMPT_A_OBJ = load_yaml_as_chat_template("prompt_doc_a.yaml")
PROMPT_B_OBJ = load_yaml_as_chat_template("prompt_doc_b.yaml")

if __name__ == "__main__":
    push_prompt(
        PROMPT_A_ID,
        PROMPT_A_OBJ,
        description="Prompt A - Generates structured technical documentation from multiple Python files."
    )

    push_prompt(
        PROMPT_B_ID,
        PROMPT_B_OBJ,
        description="Prompt B - Generates narrative documentation explaining project functionality and decisions."
    )

    print("Prompts created successfully:")
    print(f"  - {PROMPT_A_ID}")
    print(f"  - {PROMPT_B_ID}")
