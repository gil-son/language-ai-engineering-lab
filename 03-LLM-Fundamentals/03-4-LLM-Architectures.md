# 03. Fundamentals


<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/9722/9722973.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/11149/11149936.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2351/2351559.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6062/6062146.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6062/6062142.png" width="80"/></td>
    </tr>
  </table>
</div>
<br/>

## 03.4. LLM Architectures

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="80"/> Introduction

Large Language Models (LLMs) are built on different architectural patterns that define how they process input, learn context, and generate outputs.  
While most modern LLMs are based on the Transformer architecture, there are multiple variations depending on how attention and data flow are structured.

Understanding these architectures is essential because they directly impact:

- Model performance  
- Latency and cost  
- Context handling  
- Use case suitability  

---

#### Core Architecture: Transformer

The **Transformer** is the backbone of modern LLMs.

**Key components:**

-   **Self-Attention Mechanism**: captures relationships between
    tokens
-   **Feedforward Neural Networks**: processes representations
-   **Positional Encoding**: injects sequence order
-   **Multi-head Attention**: enables parallel attention patterns

---

#### Main Transformer Variants

#### Encoder-Only (Bidirectional)

-   Focus: Understanding
-   Examples: Classification, semantic search, embeddings
-   Strength: Deep contextual comprehension

#### Decoder-Only (Autoregressive)

-   Focus: Generation
-   Examples: Chatbots, code generation
-   Strength: Natural text generation

#### Encoder-Decoder (Seq2Seq)

-   Focus: Transformation
-   Examples: Translation, summarization
-   Strength: Input → Output mapping

---

#### Advanced Architectural Patterns

#### Mixture of Experts (MoE)

-   Activates only subsets of parameters per request
-   Improves scalability and efficiency

#### Retrieval-Augmented Generation (RAG)

-   Combines LLMs with external data sources
-   Improves factual accuracy and grounding

#### Multimodal Models

-   Process multiple data types (text, images, audio)
-   Enable richer AI applications


### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="80"/> Use Cases

| Use Case           | Recommended Architecture |
|-------------------|--------------------------|
| Understanding     | Encoder-only             |
| Generation        | Decoder-only             |
| Transformation    | Encoder-decoder          |
| Knowledge Systems | RAG                      |
| Scalable Systems  | MoE                      |

---

### <img src="https://cdn-icons-png.flaticon.com/512/2112/2112889.png" width="80"> Videos

A few recommended resources to visualize how LLMs work:

<div align="center">
  <a href="https://www.youtube.com/watch?v=5sLYAQS9sWQ&t" target="_blank">
      <img width="640" height="360" src="https://i.ytimg.com/vi/5sLYAQS9sWQ/maxresdefault.jpg"/>
  </a>
</div>
<hr/>
<div align="center">
  <a href="https://www.youtube.com/watch?v=ZLbVdvOoTKM" target="_blank">
      <img width="640" height="360" src="https://i.ytimg.com/vi/ZLbVdvOoTKM/maxresdefault.jpg"/>
  </a>
</div>
