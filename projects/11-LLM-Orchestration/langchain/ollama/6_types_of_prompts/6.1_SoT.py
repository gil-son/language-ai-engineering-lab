from langchain_ollama import ChatOllama
from utils import print_llm_result

msg1 = """
You are a senior backend engineer. A junior developer asked you how to optimize SQL queries for better performance. 
Follow the Skeleton of Thought approach: 

Step 1: Generate only the skeleton of your answer in 3–5 concise bullet points. 
Step 2: Expand each bullet point into a clear and detailed explanation with examples. 
Make sure the final answer is structured and easy to follow.
"""

msg2 = f"""
You are a software architect. I want you to produce an Architecture Decision Record (ADR) about choosing PostgreSQL instead of MongoDB. 

Follow the Skeleton of Thought approach:
Step 1: First, output only the skeleton of the ADR as section headers (no explanations yet). 
Use the standard ADR structure with 5 sections: Context, Decision, Alternatives Considered, Consequences, References. 
Step 2: After showing the skeleton, expand each section with clear and detailed content. 
Keep the final ADR professional, structured, and easy to read.
"""

msg3 = f"""
You are a senior Go developer. I want you to help me plan a REST API for managing products in Go.

Follow the Skeleton of Thought approach:

Step 1: Output only the skeleton of the solution in 6–8 concise bullet points. 
The skeleton must cover: data model definition in Go (structs), choice of HTTP framework or net/http, routing, handlers, validations, database layer, error handling, and project structure. Do not expand yet.

Step 2: Expand each bullet point with clear technical details, examples, and Go best practices. 
Include sample code snippets in Go (structs, handlers, routes) and considerations about packages (e.g., chi, or net/http), error handling with idiomatic Go, and how to organize the project into packages (handlers, models, db). 
Use concise and professional language.

The API must implement CRUD operations for products with fields: id, name, description, price, stock.
"""

llm = ChatOllama(model="llama3.2")

response1 = llm.invoke(msg1)
response2 = llm.invoke(msg2)
response3 = llm.invoke(msg3)

print_llm_result(msg1, response1)
print_llm_result(msg2, response2)
print_llm_result(msg3, response3)