from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains.summarize import load_summarize_chain

long_text = """
Dawn threads a pale gold through the alley of glass.
The city yawns in a chorus of brakes and distant sirens.
Windows blink awake, one by one, like sleepy eyes.
Streetcloth of steam curls from manholes, a quiet river.
Coffee steam spirals above a newspaper's pale print.
Pedestrians sketch light on sidewalks, hurried, loud with umbrellas.
Buses swallow the morning with their loud yawns.
A sparrow perches on a steel beam, surveying the grid.
The subway sighs somewhere underground, a heartbeat rising.
Neon still glows in the corners where night refused to retire.
A cyclist cuts through the chorus, bright with chrome and momentum.
The city clears its throat, the air turning a little less electric.
Shoes hiss on concrete, a thousand small verbs of arriving.
Dawn keeps its promises in the quiet rhythm of a waking metropolis.
The morning light cascades through towering windows of steel and glass,
casting geometric shadows on busy streets below.
Traffic flows like rivers of metal and light,
while pedestrians weave through crosswalks with purpose.
Coffee shops exhale warmth and the aroma of fresh bread,
as commuters clutch their cups like talismans against the cold.
Street vendors call out in a symphony of languages,
their voices mixing with the distant hum of construction.
Pigeons dance between the feet of hurried workers,
finding crumbs of breakfast pastries on concrete sidewalks.
The city breathes in rhythm with a million heartbeats,
each person carrying dreams and deadlines in equal measure.
Skyscrapers reach toward clouds that drift like cotton,
while far below, subway trains rumble through tunnels.
This urban orchestra plays from dawn until dusk,
a endless song of ambition, struggle, and hope.
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
for part in parts:
     print(part.page_content)
     print("-"*30)
     
print(f"\nNow, waiting LLM to summarize {len(parts)} parts...\n")

# Initialize the language model
llm = ChatOllama(model="llama3.2", temperature=0)

# Create the summarization chain
# Using "stuff" method for summarization
# if verbose=True, it shows the LLM calls with prompts and responses
chain_sumarize = load_summarize_chain(llm, chain_type="stuff", verbose=False)

# Invoke the chain on the document parts
result = chain_sumarize.invoke({"input_documents": parts})


# Print the final summarized result
print("\n RESUMED AND ESSENTIAL:\n", result["output_text"])