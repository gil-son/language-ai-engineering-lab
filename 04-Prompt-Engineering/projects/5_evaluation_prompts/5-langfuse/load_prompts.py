"""Load prompts into Langfuse."""
from dotenv import load_dotenv
load_dotenv()

from langfuse import Langfuse
import yaml

langfuse = Langfuse()

# Load and create prompt
with open("prompts/1-correctness-langfuse.yaml") as f:
    config = yaml.safe_load(f)

langfuse.create_prompt(
    name="1-correctness-langfuse",
    type="chat",
    prompt=config["messages"],
    labels=["production", "code-analysis"],
    config={"model": "gpt-4o-mini", "temperature": 0}
)

print("Prompt '1-correctness-langfuse' created successfully!")
