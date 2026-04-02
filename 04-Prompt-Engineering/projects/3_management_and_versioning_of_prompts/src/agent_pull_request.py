"""
Simple agent to create pull requests using native LangChain.
"""

from dataclasses import dataclass, asdict
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts.loading import load_prompt
from langchain_core.output_parsers import StrOutputParser
try:
    from prompt_registry import registry
except ImportError:
    from .prompt_registry import registry

# Load environment variables
load_dotenv()


@dataclass
class PullRequestRequest:
    """Request model for pull request creation."""
    changes_summary: str
    files_changed: str
    issue_number: str = ""
    branch_name: str = ""
    breaking_changes: str = "No"
    testing_done: str = ""



request = PullRequestRequest(
    changes_summary="Implementation of cache system to improve performance",
    files_changed="src/cache.py, tests/test_cache.py, README.md",
    issue_number="42",
    branch_name="feature/add-cache-system",
    breaking_changes="No",
    testing_done="Unit tests added with 95% coverage"
)

prompt = registry.get_prompt("agent-pull-request-creator")
prompt_template = load_prompt(prompt.path)

llm = init_chat_model("llama3.2")

# Create simple chain: prompt -> llm -> parser
chain = prompt_template | llm | StrOutputParser()

print("Creating Pull Request description...")
print("=" * 60)

# Execute the chain
result = chain.invoke(asdict(request))
print(result)