from dotenv import load_dotenv
from langchain_core.prompts.loading import load_prompt
from langsmith import Client

from prompt_registry import registry

load_dotenv()

prompt = registry.get_prompt("agent-pull-request-creator")
prompt_template = load_prompt(prompt.path)

client = Client()
url = client.push_prompt(
    "agent-pull-request-creator", 
    object=prompt_template, 
    tags=[
        f"v{prompt.version}",
        f"model: {prompt.model}",
    ], 
    description=prompt.description,
)
print(url)
