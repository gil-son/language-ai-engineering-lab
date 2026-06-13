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

## 01.2.2.2 Semantic Syntactic Analysis

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="80"/> Introduction

While Intent & Entity recognition identifies "what" is wanted, **Semantic & Syntactic Analysis** explores "how" the language is structured and "what" it truly means in context.

**Semantic and Syntactic Analysis** are fundamental steps in **Natural Language Understanding (NLU)**.

- **Syntax** focuses on *structure*: how words are arranged in a sentence.
- **Semantics** focuses on *meaning*: what the sentence actually means.

Together, they allow systems to go beyond keyword matching and understand *who did what to whom*, *when*, and *how*.

Example:

> “The model predicts customer churn.”

- **Syntactic structure:**  
  - Subject: *The model*  
  - Verb: *predicts*  
  - Object: *customer churn*

- **Semantic meaning:**  
  - An ML model is responsible for making a prediction about churn.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/5557/5557844.png" width="80"/> Why use it?

- **Ensure Grammatical Correctness:** Validates that input follows the expected linguistic patterns.
- **Resolve Ambiguity:** Differentiates between multiple meanings of the same word (Polysemy).
- **Logical Validation:** Identifies "semantic anomalies" (e.g., "The colorless green ideas sleep furiously").
- **Structural Mapping:** Essential for machine translation and complex query understanding where word order changes meaning (e.g., "Dog bites man" vs. "Man bites dog").

Without semantic and syntactic analysis, systems struggle with:
- Long or nested sentences  
- Passive voice  
- Negation  
- Complex queries  

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7527/7527144.png" width="80"/> How it works?

#### Step-by-step Process

**1. Tokenization (Lexical)**
The input text is split into smaller units called tokens (words, subwords, or symbols).
This step operates at the lexical level, focusing on word boundaries and vocabulary units.

**2. POS Tagging (Syntactic)**
Assigning parts of speech (noun, verb, adjective, etc.) to each token, enabling grammatical analysis.

**3. Dependency Parsing (Syntactic)**
Building a tree structure that represents how words depend on each other
(e.g., which noun is the subject of a verb or which adjective modifies which noun).

**4. Word Sense Disambiguation - WSD (Semantic)**
Selecting the correct meaning of a word based on its context
(e.g., “Apple” as a fruit vs. “Apple” as a company).

**5. Semantic Role Labeling - SRL (Semantic)**
Identifying the roles entities play in an action
(Who did what to whom, when, and how?).

#### Example

Sentence:
> “The data scientist trained the model with historical data.”

- POS tagging:
  - data scientist (noun)
  - trained (verb)
  - model (noun)

- Dependency relations:
  - *trained* → subject → *data scientist*
  - *trained* → object → *model*
  - *trained* → instrument → historical data

#### Diagram

```mermaid
graph TD
    A[Text Input] --> B[Tokenization - Lexical]
    B --> C[POS Tagging - Syntactic]
    C --> D[Dependency Parsing - Syntactic]
    D --> E[Semantic Analysis]
    E --> F[Structured Meaning]
```

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2299/2299623.png" width="80"/> Components

**1. Lexical Analysis (Pre-Syntactic)**
Operates at the word level before grammatical interpretation.
- Tokenization
- Vocabulary normalization
- Handling subwords and symbols

**2. Syntactic Analysis**
- Part-of-Speech tagging  
- Dependency parsing  
- Constituency parsing  

**3. Semantic Analysis**
- Word meaning  
- Sentence meaning  
- Semantic role labeling (who did what)  

**4. Disambiguation**
- Resolves ambiguity using context  
- Example:
  - “I saw the man with a telescope”  

**5. Meaning Representation**
- Logical forms  
- Graphs  
- Embedding-based representations  

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="80"/> Use Cases

- Question Answering Systems  
- Search Query Understanding  
- Chatbots & Virtual Assistants  
- RAG Pipelines  
- Legal and Medical NLP  
- Text Summarization  
- Command Interpretation  

---

### Key Takeaway

> **Syntax tells you how a sentence is built.  
> Semantics tells you what it means.  
> Together, they enable true language understanding.**

### <img src="https://cdn-icons-png.flaticon.com/512/2956/2956457.png" width="80"> Contents
- [Mindwalkai](https://www.mindwalkai.com/blog/natural-language-understanding-nlu-basics-and-applications-in-bioinformatics)

---

### <img src="https://cdn-icons-png.flaticon.com/512/2112/2112889.png" width="80"> Videos

A few recommended resources to visualize:

<div align="center">
  <a href="https://www.youtube.com/watch?v=WaXOcZb9OhU" target="_blank">
      <img width="640" height="360" src="https://i.ytimg.com/vi/WaXOcZb9OhU/hqdefault.jpg?sqp=-oaymwEnCOADEI4CSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBbus-OtEtULDDyZSdVx8nKm3Q32w"/>
  </a>
</div>

---

<div align="center">
  <a href="https://www.youtube.com/watch?v=vDkpwnUybi0" target="_blank">
      <img width="640" height="360" src="https://i.ytimg.com/vi/vDkpwnUybi0/hqdefault.jpg?sqp=-oaymwFBCOADEI4CSFryq4qpAzMIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB8AEB-AHUBoAC4AOKAgwIABABGHIgQig8MA8=&rs=AOn4CLD0_F-jmmyIHqy9ib7Jv9GGe0xggw"/>
  </a>
</div>
