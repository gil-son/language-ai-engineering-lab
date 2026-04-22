# 03. Fundamentals

<div align="center">
<img src="https://cdn-icons-png.flaticon.com/512/2013/2013631.png" width="80">
</div>
  
## 03.2. Key-Terms

A glossary of essential terms that will help you navigate LLM fundamentals and documentation.

---

#### Core Concepts

- **Token** – The smallest unit of text an LLM processes (word, subword, or character).  
- **Vocabulary** – The set of all tokens a model can recognize.  
- **Context Window** – The maximum number of tokens the model can handle at once (e.g., 128k for GPT-4 Turbo).  
- **Parameters** – Model weights learned during training; larger models have more parameters.  

---

#### Representations and Vectors

- **Embedding** – Dense vector representation of tokens, words, or sentences capturing semantic meaning.  
- **Vector Space** – The multidimensional space where embeddings live; similarity is measured by distance metrics (e.g., cosine similarity).  
- **Vector Database** – Specialized storage for embeddings, enabling efficient similarity search (e.g., FAISS, Weaviate, Pinecone).  

---

#### Model Architecture

- **Transformer** – The core architecture of LLMs, based on *self-attention*.  
- **Attention** – Mechanism that lets the model focus on relevant tokens within context.  

---

#### Training Approaches

- **Pretraining** – Initial training on large corpora with tasks like next-token prediction.  
- **Fine-Tuning** – Adapting the pretrained model to specific tasks or domains.  
- **Instruction Tuning** – Teaching the model to follow instructions better through curated data.  
- **RLHF (Reinforcement Learning with Human Feedback)** – Aligning model outputs with human preferences.  

---

#### Inference and Generation

- **Inference** – Running the trained model to generate outputs.  
- **Prompt** – Input text provided to guide the model’s response.  
- **Prompt Engineering** – Crafting effective prompts for better outputs.  
- **Temperature** – Controls randomness in generation (low = deterministic, high = creative).  
- **Top-k / Top-p Sampling** – Methods to control token selection during generation.  

---

#### Ecosystem

Key frameworks simplify connecting LLMs to external data, APIs, and workflows.  
They provide **high-level abstractions and tools** for tasks like prompt engineering, memory, document loading, and vector store integration — streamlining LLM application development.  

- **LangChain** – Comprehensive framework for building LLM-powered apps (chains, agents, retrievers, memory).  
- **LlamaIndex** – Specializes in connecting LLMs to external structured/unstructured data. Great for retrieval-augmented generation (RAG).  
- **Haystack** – Open-source framework for semantic search and question-answering systems. Useful for knowledge-intensive applications.  
- **Hugging Face Transformers** – Provides efficient access to thousands of pretrained LLMs with simple APIs.  
- **Semantic Kernel** – Microsoft’s orchestration framework for building AI workflows with LLMs.  

---

✅ These terms are your quick reference to better understand papers, tools, and practical LLM usage.
