from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.runnables import chain

# -------------------------
# 1. Decorator chain
# -------------------------
@chain
def square_number(inputs: dict) -> dict:
    number = inputs["number"]
    return {"square_result": number * number}

# -------------------------
# 2. Prompt templates
# -------------------------
prompt_template1 = ChatPromptTemplate.from_template(
    "Hi, I'm {name} professor. Please give me a number from 1 to 10. Just the number without any more charactere!"
)

prompt_template2 = ChatPromptTemplate.from_template(
    "Explain why the number {square_result} is interesting."
)

# -------------------------
# 3. Model
# -------------------------
model = ChatOllama(
    model="llama3.2",
    temperature=0.5
)

# -------------------------
# 4. Chains
# -------------------------
chain1 = prompt_template1 | model
chain2 = square_number | prompt_template2 | model

# -------------------------
# 5. Call chain1
# -------------------------
result1 = chain1.invoke({"name": "Goku"})

print("Chain 1 output:")
print(result1.content)

# -------------------------
# 6. Prepare input for chain2
# -------------------------
input_for_chain2 = {
    "number": int(result1.content.strip().split()[-1])  # Extract the number from the response
}

# -------------------------
# 7. Call chain2
# -------------------------
result2 = chain2.invoke(input_for_chain2)

print("\nChain 2 output:")
print(result2.content)