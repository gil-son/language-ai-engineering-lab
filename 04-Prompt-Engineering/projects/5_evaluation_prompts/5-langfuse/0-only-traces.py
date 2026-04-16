"""Demonstracao de uso de traces no Langfuse com LangChain."""
from datetime import datetime
from langfuse.langchain import CallbackHandler
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Inicializa o callback handler do Langfuse
langfuse_handler = CallbackHandler()

# Inicializa o LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, max_tokens=500)

# Define o prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """Voce e um historiador especializado em linguagens de programacao.
Seu objetivo e contar a historia de linguagens de programacao de forma interessante e educativa.

Inclua em sua resposta:
- Quando a linguagem foi criada e por quem
- Qual problema ela veio resolver
- Principais caracteristicas e diferenciais
- Evolucao ao longo do tempo
- Impacto no desenvolvimento de software

Seja conciso mas informativo. Use um tom narrativo envolvante."""),
    ("user", "Conte a historia da linguagem de programacao {linguagem}.")
])

# Cria a chain
chain = prompt | llm


def generate_language_history(linguagem):
    """Gera historia de uma linguagem usando LLM com trace automatico."""
    response = chain.invoke(
        {"linguagem": linguagem},
        config={"callbacks": [langfuse_handler]}
    )

    return response.content


if __name__ == "__main__":
    linguagens = ["Python", "Go", "JavaScript"]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"\nExecutando traces - {timestamp}")
    print("=" * 60)

    for linguagem in linguagens:
        print(f"\nLinguagem: {linguagem}")
        generate_language_history(linguagem)