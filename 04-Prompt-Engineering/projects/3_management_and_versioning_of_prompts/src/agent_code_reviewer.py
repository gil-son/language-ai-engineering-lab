"""
Simple code review agent using native LangChain.
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

load_dotenv()

@dataclass
class CodeReviewRequest:
    """Request model for code review."""
    code_diff: str
    language: str = "python"
    repo_rules: str = "Apply general best practices"
    security_level: str = "standard"
    review_focus: str = "general"

request = CodeReviewRequest(
    code_diff="""
    + def calculate_total(items):
    +     total = 0
    +     for item in items:
    +         total = total + item['price'] * item['quantity']
    +     return total
    """,
    language="python",
    repo_rules="Use type hints and docstrings",
    security_level="standard",
    review_focus="quality and performance"
)

# Get prompt path using the registry
prompt = registry.get_prompt("agent-code-reviewer")

# Load prompt with native LangChain load_prompt
prompt_template = load_prompt(prompt.path)

# Create the model using init_chat_model (LangChain 1.0 recommended way)
llm = init_chat_model("llama3.2")

# Create simple chain: prompt -> llm -> parser
chain = prompt_template | llm | StrOutputParser()

print("Starting code review...")
print("-" * 50)

# Execute the chain
result = chain.invoke(asdict(request))
print(result)