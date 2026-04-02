from langchain_ollama import ChatOllama

# 1. Initialize the model
model = ChatOllama(
        model="llama3.2",
        temperature=0.5,
    )

# 2. Invoke the model
message = model.invoke("Hello World")

# 3. Output
print(message.content)