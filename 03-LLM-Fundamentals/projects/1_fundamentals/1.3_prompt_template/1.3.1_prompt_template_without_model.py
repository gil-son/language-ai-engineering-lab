from langchain_core.prompts import PromptTemplate

# 1. Initialize the model
template = PromptTemplate(
    input_variables=["name"],
    template="Hi, I'm {name}! Tell me a history with my name!"
)

# 2. Invoke the model
text = template.format(name="Jesus")

# 3. Output
print(text)