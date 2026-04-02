from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains.summarize import load_summarize_chain

long_text = """
1:1 In the beginning God created the heaven and the earth.

1:2 And the earth was without form, and void; and darkness was upon
the face of the deep. And the Spirit of God moved upon the face of the
waters.

1:3 And God said, Let there be light: and there was light.

1:4 And God saw the light, that it was good: and God divided the light
from the darkness.

1:5 And God called the light Day, and the darkness he called Night.
And the evening and the morning were the first day.

1:6 And God said, Let there be a firmament in the midst of the waters,
and let it divide the waters from the waters.

1:7 And God made the firmament, and divided the waters which were
under the firmament from the waters which were above the firmament:
and it was so.

1:8 And God called the firmament Heaven. And the evening and the
morning were the second day.

1:9 And God said, Let the waters under the heaven be gathered together
unto one place, and let the dry land appear: and it was so.

1:10 And God called the dry land Earth; and the gathering together of
the waters called he Seas: and God saw that it was good.

.
.
.

.
.
.

Could be more text here, but to keep the example concise, we will stop at this point.
"""

# Split long text into smaller parts
# Optimal chunk size and overlap for summarization
splitter = RecursiveCharacterTextSplitter(
    chunk_size=250, chunk_overlap=70, 
)

# Create documents from the long text
parts = splitter.create_documents([long_text])

# Print the parts (optional - for verification)
print("\nDOCUMENTS PARTS WITH CHUNK(250) AND OVERLAP(70):\n")
for i, part in enumerate(parts[:10], start=1):
    print(f"DOCUMENT PART {i}:\n{part.page_content}\n{'-'*30}")

print(f"\nNow, waiting LLM to summarize {len(parts)} parts...\n")

# Initialize the language model
llm = ChatOllama(model="llama3.2", temperature=0)

# Create the summarization chain
# Using "map_reduce" method for summarization
# if verbose=True, it shows the LLM calls with prompts and responses
chain_sumarize = load_summarize_chain(llm, chain_type="map_reduce", verbose=False) # prompt=PROMPT as optional argument

# Invoke the chain on the document parts
result = chain_sumarize.invoke({"input_documents": parts})


# Print the final summarized result
print("\n RESUMED AND ESSENTIAL:\n", result["output_text"])