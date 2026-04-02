from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.messages import trim_messages
from langchain_core.runnables import RunnableLambda



prompt = ChatPromptTemplate.from_messages([
    ("system", "You're a helpful assistant that answers with a short joke when possible."),
    MessagesPlaceholder("history"),
    ("human", "{input}"),
])

llm = ChatOllama(model="llama3.2", temperature=0.9)

def prepare_inputs(payload: dict) -> dict:
    """Trim the history based on a sliding window strategy before passing to the model."""
    raw_history = payload.get("raw_history", [])
    trimmed = trim_messages(
        raw_history,               # list of messages to trim
        token_counter=len,         # a simple token counter based on character length, but you can use number of tokens or more sophisticated methods such as tiktoken
        max_tokens=2,              # set a very low token limit for demonstration
        strategy="last",           # keep the last messages within the token limit
        start_on="human",          # start trimming from the last human message
        include_system=True,       # include system messages
        allow_partial=False,       # do not include partial messages
    )
    return {"input": payload.get("input",""), "history": trimmed}


prepare = RunnableLambda(prepare_inputs)
chain = prepare | prompt | llm

session_store: dict[str, InMemoryChatMessageHistory] = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
    return session_store[session_id]

conversational_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

config = {"configurable": {"session_id": "demo-session"}}

# Interactions
resp1 = conversational_chain.invoke({"input": "My name is Wesley. Reply only with 'OK' and do not mention my name."}, config=config)
print("Assistant:", resp1.content)
print("-"*30)

resp2 = conversational_chain.invoke({"input": "Tell me a one-sentence fun fact. Do not mention my name."}, config=config)
print("Assistant:", resp2.content)
print("-"*30)

resp3 = conversational_chain.invoke({"input": "What is my name?"}, config=config)
print("Assistant:", resp3.content)
print("-"*30)

#print("\nFull conversation history:", get_session_history("demo-session").messages)

i=0
print("\nFull conversation history:")
for msg in get_session_history("demo-session").messages:
    i+=1
    print(f"\nPart:{i} | {msg.type}: {msg.content}")