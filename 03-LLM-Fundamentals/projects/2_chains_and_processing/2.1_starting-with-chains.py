from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# 1. Define the prompt template (DO NOT format it yet)
prompt = ChatPromptTemplate.from_template(
    "Hi, I'm {name}! Tell me a joke with my name!"
)

# 2. Initialize the model
model = ChatOllama(
    model="llama3.2",
    temperature=0.5
)

# 3. Create the chain
chain = prompt | model

# 4. Invoke the chain with variables
result = chain.invoke({"name": "Goku"})

# 5. Output
print(result.content)