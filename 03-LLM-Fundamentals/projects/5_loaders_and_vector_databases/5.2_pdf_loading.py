from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = PyPDFLoader("./gpt5.pdf")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

chunks = splitter.split_documents(docs)

print("Total chunks created:", len(chunks) ,"\n")

for chunk in chunks[0:10]:  # Print only first 10 chunks for brevity
    print(chunk)
    print("-"*30)