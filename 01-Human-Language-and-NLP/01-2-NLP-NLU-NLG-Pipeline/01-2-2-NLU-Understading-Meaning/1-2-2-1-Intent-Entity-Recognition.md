# 01.2.2 NLU Understating Meaning

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://raw.githubusercontent.com/gil-son/experimental/refs/heads/main/matrizero/v001/src/assets/images/processing-language.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6062/6062503.png" width="80"/></td>
      <td align="center"><img src="https://raw.githubusercontent.com/gil-son/experimental/refs/heads/main/matrizero/v001/src/assets/images/generating-text.png" width="80"/></td>
      <td align="center"><img src="https://raw.githubusercontent.com/gil-son/experimental/refs/heads/main/matrizero/v001/src/assets/images/evaluating.png" width="80"/></td>
    </tr>
  </table>
</div>

## 01.2.2.1 Intent Entity Recognition

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="80"/> Introduction

Intent & Entity Recognition is at the core of **NLU (Natural Language Understanding)**.
It answers two essential questions:

1. **What is the user trying to do?** → *Intent*
2. **What pieces of information matter in their request?** → *Entities*

Example:

> “Book a flight to New York tomorrow.”

- **Intent:** book_flight  
- **Entities:**  
  - destination = New York  
  - date = tomorrow  

These two components enable chatbots, assistants, and RAG pipelines to interpret user meaning with precision.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/5557/5557844.png" width="80"/> Why use it?

- Understand what the user **wants**  
- Extract **structured data** from unstructured text  
- Enable task automation  
- Power conversational agents  
- Improve accuracy in RAG retrieval  
- Connect natural language with system actions  

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2299/2299623.png" width="80"/> Components

**1. Intent Classification**  
Predicts the *goal* of the utterance.  
Examples:  
- order_pizza  
- cancel_order  
- ask_weather  
- search_product  

**2. Entity Recognition (NER)**  
Extracts key parameters needed to fulfill the intent.  
Common entity types:  
- person  
- location  
- date  
- product  
- amount  
- organization  

**3. Context State**  
Tracks conversation history and filling missing info (slot filling):  
- “I want pizza”  
- “Which size?”  
- “Large.”  

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7527/7527144.png" width="80"/> How it works?

#### Step-by-step Process

1. **Text Input**  
2. **Tokenization & Embeddings**  
3. **NLU Model predicts:**  
   - intent  
   - entities  
4. **Slots filled** from extracted entities  
5. **Actions triggered** (API call, DB query, RAG retrieval…)

#### Simple Diagram

```mermaid
graph TD
    A[User Input] --> B[Tokenization]
    B --> C[Embeddings]
    C --> D[Intent Classifier]
    C --> E[Entity Recognizer]
    D --> F[Intent Output]
    E --> G[Entities Output]
```

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="80"/> Use Cases

- Chatbots & Virtual Assistants  
- Customer Support Automation  
- RAG Query Understanding  
- Voice Assistants  
- Search Understanding  
- Forms Extraction  
- Command-based systems (“Play music”, “Turn off lights”)  

---

### <img src="https://cdn-icons-png.flaticon.com/512/6675/6675847.png" width="80"> Limitations

- Ambiguous user input  
- Multi-intent sentences  
- Requires good labeled data (unless using LLMs)  
- Domain shift problems  
- Entities with unusual spelling  

---

### <img src="https://cdn-icons-png.flaticon.com/512/2147/2147809.png" width="80"> Code/Notebook/Projects

 - [NLP, NLU, NLG with RAG - Make Matthew notebook from bible](https://github.com/gil-son/llm-engineering-lab/tree/main/notebooks/02-NLP-NLU-NLG)

---

### <img src="https://cdn-icons-png.flaticon.com/512/2112/2112889.png" width="80"> Video

Recommended to visualize:

<div align="center">
  <a href="https://www.youtube.com/watch?v=2WFaoFD8eL8&t=199s" target="_blank">
      <img width="640" height="360" src="https://i.ytimg.com/vi/2WFaoFD8eL8/hq720.jpg?sqp=-oaymwEnCNAFEJQDSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBHEQY-IQbyrOJZX8e9V2uftT0pQA"/>
  </a>
</div>
