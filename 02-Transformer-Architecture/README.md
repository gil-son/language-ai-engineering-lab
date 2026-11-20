# 02. Transformer Architecture

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/9722/9722973.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/11149/11149936.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2351/2351559.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2582/2582078.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6062/6062146.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/10817/10817413.png" width="80"/></td>
    </tr>
  </table>
</div>

## <img src="https://cdn-icons-png.flaticon.com/512/8592/8592294.png" width="10%"/> Overview

The **Transformer** is the architecture that powers virtually every modern Large Language Model. Introduced in 2017 in the paper *"Attention Is All You Need"*, it replaced the slow, word-by-word processing of earlier models with a design that reads an entire sequence **at once** and learns how every token relates to every other token through a mechanism called **attention**.

> **"How does a model turn one sequence into another — and understand meaning without reading word by word?"**

This section breaks the Transformer into its two halves — the **Encoder** (which understands the input) and the **Decoder** (which generates the output) — and shows how attention, embeddings, and stacked layers work together.

| Aspect | Older Sequential Models (RNN / LSTM) | Transformer |
|--------|--------------------------------------|-------------|
| Processing | Word by word, left to right | Whole sequence in parallel |
| Long-range dependencies | Weak (vanishing gradients) | Strong (self-attention) |
| Parallelization | Difficult | Native |
| Context handling | Limited / local | Global across the sequence |
| Scalability | Limited | Scales to billions of parameters |

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="80"/> Introduction

Transformers were originally created to solve **sequence-to-sequence** problems — turning one sequence of information into another, such as translating a sentence from one language to another. Because they *transform* an input into an output, they are called "Transformers".

Instead of reading text step by step like a human, a Transformer looks at the whole sentence and focuses on the **relationships** between words. It learns which words are important to each other and which provide context, using the idea of **attention** — learning where to "pay attention" when understanding or generating text.

> **Key mindset:** A word is not a fixed dictionary entry. A Transformer turns each token into a **context-aware meaning vector** that reflects how the word is being used in the sentence.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/5557/5557844.png" width="80"/> Why use it?

Transformers became the foundation of modern AI because they:

- **Scale efficiently** with large datasets and model sizes
- **Process tokens in parallel** (unlike RNNs that go one word at a time)
- **Capture long-range dependencies** using self-attention
- **Generalize across modalities** (text, images, audio)
- **Provide a unified architecture** for NLP, vision, and multimodal tasks

> These properties are exactly why Transformers became the basis for **foundation models** like BERT, GPT, and the LLMs explored in the next section.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2299/2299623.png" width="80"/> Components

A Transformer is built from a small set of repeating building blocks. Understanding each one makes the full architecture easy to follow.

```mermaid
graph TD
    T(["Transformer"])

    ENC["Encoder\nUnderstands the input"]
    DEC["Decoder\nGenerates the output"]
    EMB["Embeddings\nTokens to meaning vectors"]
    POS["Positional Encoding\nInjects word order"]
    ATT["Attention\nRelates tokens by meaning"]
    FFN["Feed-Forward Layers\nProcesses representations"]

    T --> ENC
    T --> DEC
    ENC --> EMB
    ENC --> POS
    ENC --> ATT
    ENC --> FFN
    DEC --> ATT
    DEC --> FFN

    style T fill:#4A90D9,color:#fff,stroke:#2c6fad
    style ENC fill:#2D9E6B,color:#fff,stroke:#1e7a50
    style DEC fill:#7B61FF,color:#fff,stroke:#5a3fd4
    style EMB fill:#2D9E6B,color:#fff,stroke:#1e7a50
    style POS fill:#2D9E6B,color:#fff,stroke:#1e7a50
    style ATT fill:#2D9E6B,color:#fff,stroke:#1e7a50
    style FFN fill:#7B61FF,color:#fff,stroke:#5a3fd4
```

| Component | Role |
|-----------|------|
| **Encoder** | Reads the input and turns it into context-aware representations |
| **Decoder** | Uses those representations to generate the output, one token at a time |
| **Embeddings** | Convert tokens into numerical meaning vectors |
| **Positional Encoding** | Adds information about the order of words |
| **Attention** | Learns how strongly each token relates to the others |
| **Feed-Forward Layers** | Process and refine the representations in each layer |

> In the original Transformer, the Encoder and Decoder are each a stack of **6 identical layers**; the output of one layer feeds the next. Modern models use more or fewer layers depending on the task.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7527/7527144.png" width="80"/> How it works?

At a high level, data flows from input text to output text through the Encoder and Decoder:

```mermaid
graph LR
A[Input Text] --> B[Tokenization & Embeddings]
B --> C[Encoder - Attention + Layers]
C --> D[Decoder - Attention + Layers]
D --> E[Output Text]
```

Internally, the process follows these steps:

1. The input text is broken into smaller pieces called **tokens**.
2. Tokens are converted into **embeddings** and combined with **positional information**.
3. **Attention** analyzes the relationships between all tokens.
4. The results pass through **feed-forward processing layers**.
5. **Multiple stacked layers** refine the understanding step by step.
6. The **Decoder** generates the output autoregressively — one token at a time — until it produces an end-of-sequence token.

> **Plain-language analogy:** think of a human translator — reading words (embeddings), understanding meaning and context (Encoder + attention), then speaking the translation (Decoder).

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="80"/> Use Cases

| Domain | Application |
|--------|-------------|
| **Machine Translation** | Translating text between languages (the original use case) |
| **Text Summarization** | Condensing long documents into short summaries |
| **Question Answering** | Answering questions from a passage or knowledge base |
| **Conversational AI** | Chatbots and virtual assistants |
| **Code Generation** | Writing and completing source code |
| **Speech Recognition** | Converting audio into text |
| **Vision** | Image captioning and Vision Transformers (ViT) |

---

### <img src="https://cdn-icons-png.flaticon.com/512/6675/6675847.png" width="80"> Limitations

| Limitation | Description |
|------------|-------------|
| **Quadratic attention cost** | Self-attention scales with the square of sequence length, making very long inputs expensive |
| **Context window limits** | The model can only attend to a fixed maximum number of tokens at once |
| **High compute & data needs** | Training requires large datasets and significant GPU/TPU resources |
| **Lack of inherent order** | Word order must be added explicitly via positional encoding |
| **Interpretability** | Internal attention patterns are hard to fully explain |
| **Data bias** | Patterns learned from training data can reproduce its biases |

---

### <img src="https://cdn-icons-png.flaticon.com/512/2112/2112889.png" width="80"> Real-Life Transformer Models

| Model | Year | Focus |
|-------|------|-------|
| **BERT** (Google) | 2018 | Bidirectional understanding; question answering, search |
| **GPT** (OpenAI) | 2018+ | Autoregressive text generation |
| **LaMDA** (Google) | 2021 | Conversational / dialogue applications |

---

## <img src="https://cdn-icons-png.flaticon.com/512/18310/18310876.png" width="80"/> Transformer Architecture Structure

```
02-Transformer-Architecture/
├── 02-1-What-is-a-Transformer.md     # Overview, history, encoder-decoder big picture
├── 02-2-The-Encoder-Workflow.md      # How the encoder builds context-aware representations
└── 02-3-The-Decoder-Workfkow.md      # How the decoder generates output autoregressively
```

---

### <img src="https://cdn-icons-png.flaticon.com/512/2956/2956457.png" width="80"> References

- [DataCamp — How Transformers Work](https://www.datacamp.com/tutorial/how-transformers-work)
- [Building a Transformer with PyTorch](https://www.datacamp.com/tutorial/building-a-transformer-with-py-torch)
- [Build a Transformer from Scratch (notebook)](https://github.com/gil-son/language-ai-engineering-lab/tree/main/notebooks/02-Transformers)
