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

## 01.2.2.3 Contextual Disambiguation

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="80"/> Introduction

Contextual Disambiguation is the process of determining the correct meaning of a word, phrase, or sentence based on its **context**.

In Natural Language Understanding (NLU), many words and sentences are inherently ambiguous. Context allows systems to resolve these ambiguities by analyzing surrounding words, previous conversation turns, and domain knowledge.

Example:

> “I went to the bank.”

- Could mean:
  - Financial institution  
  - River bank  

Only context (e.g., “to deposit money” vs. “to relax near the water”) reveals the correct meaning.


### Types of Ambiguity in Language

Understanding contextual disambiguation requires recognizing different types of ambiguity:

#### 1. Lexical Ambiguity (Word-level)

Words with multiple meanings:

- **Same spelling** → bat, bank, can, present  
- **Same sound** → buy, by, bye | oar, or, ore  
- **Proper nouns** → Jack vs jack | Mark vs mark  

---

#### 2. Semantic Scope Ambiguity (Sentence-level)

Sentences with multiple interpretations:

- **Subject** → “I can see the man with glasses.”  
- **Plurality** → “They only ate the pizza.”  
- **Preposition** → “There’s a dog with a frog on a log.”  

---

#### 3. Contextual Ambiguity (Pragmatic)

Meaning depends on real-world or conversational context:

- **Sarcasm** → “Yay, I get to wait in line.”  
- **Hyperbole** → “This is taking forever.”  
- **Metaphors** → “This place is a zoo.”  
- **Implied meaning** → “Sit tight”, “Go with the flow”  
- **Cultural nuances** → “Y’all”, dialect expressions  

---

#### 4. Evolving Language Ambiguity

Language changes over time:

- **Slang** → cool, groovy, fly, gnarly, phat, fire  
- **Internet slang** → lol, lmao, imo, jk, irl, dm  
- **Emojis** → 🙂 😬 🤔  
- **Technology influence** → “cell phone” (device vs communication context)  

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/5557/5557844.png" width="80"/> Why use it?

- Resolve **ambiguity** in language (polysemy & homonyms)  
- Improve **accuracy** of NLU systems  
- Enable **better conversational understanding**  
- Enhance **RAG retrieval relevance**  
- Avoid incorrect actions in automation systems  
- Support multi-turn conversations with evolving meaning  

Without contextual disambiguation, systems may:
- Misinterpret user intent
- Retrieve irrelevant documents
- Execute wrong actions

---
 
### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7527/7527144.png" width="80"/> How it works?

#### Step-by-step Process

1. **Input Processing**
   - Tokenization and embeddings generation

2. **Context Gathering**
   - Sentence-level context  
   - Conversation history  
   - External knowledge (documents, KBs)

3. **Candidate Meanings**
   - Identify possible interpretations for ambiguous terms

4. **Context Matching**
   - Compare candidates against context using embeddings or probabilistic models

5. **Selection**
   - Choose the most likely meaning

#### Example Flow

```mermaid
graph TD
    A[User Input] --> B[Tokenization]
    B --> C[Embeddings]
    C --> D[Candidate Meanings]
    D --> E[Context Matching]
    E --> F[Best Interpretation]
```
     
---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2299/2299623.png" width="80"/> Components

**1. Context Sources**
- Surrounding words (local context)  
- Previous messages (conversation context)  
- External knowledge bases  

**2. Word Sense Disambiguation (WSD)**
- Core technique to select the correct meaning of a word  

**3. Embeddings & Similarity**
- Semantic similarity used to match meaning with context  

**4. Attention Mechanisms (Transformers)**
- Focus on relevant parts of the input sequence  

**5. Memory / State Tracking**
- Maintains conversation continuity  

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="80"/> Use Cases

- Chatbots & Virtual Assistants  
- Multi-turn Conversations  
- Search Query Understanding  
- RAG Systems (better document retrieval)  
- Machine Translation  
- Voice Assistants  
- Recommendation Systems

---

### <img src="https://cdn-icons-png.flaticon.com/512/2112/2112889.png" width="80"> Videos

A few recommended resources to visualize:

<div align="center">
  <a href="https://www.youtube.com/watch?v=ZdjAmjwhfTE" target="_blank">
      <img width="640" height="360" src="https://i.ytimg.com/vi/ZdjAmjwhfTE/hqdefault.jpg?sqp=-oaymwEnCOADEI4CSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLDwOb4OOCICVj6z6q-RqBbt6Lm7hQ"/>
  </a>
</div>

---

<div align="center">
  <a href="https://www.youtube.com/watch?v=gWx7ClWg9WU&pp=ygUcbmx1IGNvbnRleHR1YWwgZGlzYWJpZ3VhdGlvbg%3D%3D" target="_blank">
      <img width="640" height="360" src="https://i.ytimg.com/vi/gWx7ClWg9WU/hqdefault.jpg?sqp=-oaymwEnCOADEI4CSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBwHFAzZGh9IK-QSm6MVgZKjrv7wg"/>
  </a>
</div>

---

<div align="center">
  <a href="https://www.youtube.com/watch?v=5s8Har3xgrs" target="_blank">
      <img width="640" height="360" src="https://i.ytimg.com/vi/5s8Har3xgrs/hqdefault.jpg?sqp=-oaymwEnCOADEI4CSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLCydNxbG_yP85SMzfti4r91b6PXDQ"/>
  </a>
</div>
