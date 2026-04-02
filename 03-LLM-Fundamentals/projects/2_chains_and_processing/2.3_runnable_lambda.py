from langchain_core.runnables import RunnableLambda

# RunnableLambda allows you to wrap a standard Python function
# into a LangChain Runnable, enabling it to be part of a chain.
# It could be in another folder/module

def sum_values(inputs: dict) -> int:
    return inputs["a"] + inputs["b"]

sum_runnable = RunnableLambda(sum_values)

# Now, you can use sum_values directly 

print("Sum:", sum_values({"a": 3, "b": 5}))

# or can use in a chain
chain_result = sum_runnable.invoke({"a": 10, "b": 20})

print("Chain Sum Result:", chain_result)
