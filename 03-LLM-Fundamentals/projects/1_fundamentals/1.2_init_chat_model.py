from langchain.chat_models import init_chat_model

# 1. Initialize the model
model = init_chat_model(
        model="llama3.2",
        model_provider="ollama",
        temperature=0.5,
    )

# 2. Invoke the model
answer = model.invoke("Hello World")

# 3. Output
print(answer.content)