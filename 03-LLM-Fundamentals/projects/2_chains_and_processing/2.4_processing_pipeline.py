from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

template_translate = ChatPromptTemplate.from_template(
    template="Translate the following text to English:\n ```{initial_text}````"
)

template_summary = ChatPromptTemplate.from_template(
    template="Summarize the following text in 4 words:\n ```{text}```"
)

llm_en = ChatOllama(model="llama3.2", temperature=0)

translate = template_translate | llm_en | StrOutputParser()
pipeline = {"text": translate} | template_summary | llm_en | StrOutputParser()

result = pipeline.invoke({"initial_text": "LangChain é um framework para desenvolvimento de aplicações de IA"})
print(result)