
from langchain_ollama import ChatOllama
from utils import print_llm_result

msg = """
You are a senior Go backend engineer.

Problem: We need to design a URL shortener service in Go.

Use the Least-to-Most Prompting method:
1. Start by listing the subproblems that need to be solved as a to-do list. Use markdown checkboxes: [ ] for pending, [x] for completed.
2. As you solve each subproblem, update the to-do list by marking it as [x] and write the solution right below it.
3. Continue until all items are solved.
4. At the end, combine all the solutions into a final integrated design for the URL shortener.

Constraints:
- Service must be implemented in Go.
- Short URLs must be unique and easy to generate.
- Must support endpoints: shorten a URL, retrieve the original URL.
- Use an in-memory store at first, but mention how it could scale with a database.
- Include minimal validation and error handling.
- Keep explanations concise and structured.

Output format:
- To-do list with checkboxes (updating as you progress)
- Each solved subproblem explained with reasoning and minimal Go code snippets
- Final combined design

"""

model = ChatOllama(model="llama3.2")
result = model.invoke(msg)
print_llm_result(msg, result)