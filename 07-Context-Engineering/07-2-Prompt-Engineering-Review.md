# 07. Context Engineering

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/10087/10087719.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6062/6062189.png" width="80"/></td>
    </tr>
  </table>
</div>
<br/>

---

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/9722/9722973.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/11149/11149936.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2351/2351559.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2581/2581996.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/1990/1990934.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6062/6062146.png" width="80"/></td>
      <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6062/6062142.png" width="80"/></td>
    </tr>
  </table>
</div>
<br/>

## 07.2. Prompt Engineering — Review

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="80"/> Introduction

---

> **Note —** This is a review. Prompt Engineering has its own complete section in this lab. This page is a short recap; its real purpose is to explain **why prompting belongs to Context Engineering**.
>
> **Full section:** **[04-Prompt-Engineering](https://github.com/gil-son/language-ai-engineering-lab/tree/main/04-Prompt-Engineering)**

Prompt Engineering is the craft of writing the **instructions** that guide a model's reasoning and output — telling the model *what to do* and *how to respond*.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/5557/5557844.png" width="80"/> Why it belongs to Context Engineering

---

Context Engineering is about designing **everything the model sees** before it answers. The prompt is part of that "everything" — in fact, it is the layer that holds all the other context together.

Three basic reasons prompting is a pillar of Context Engineering:

1. **The prompt is where all context meets.** Instructions, retrieved documents (RAG), memory, and conversation history are not sent separately — they are all assembled into one prompt. Prompting is the glue.

2. **In a system, the prompt is built, not typed.** In a chat you type a message by hand. In a production system the prompt is **assembled automatically on every call** from static parts (the role, the rules) and dynamic parts (the user's question, the retrieved data). Designing that assembly is a Context Engineering task.

3. **The instructions decide how the other context is used.** Good retrieved data is wasted if the instructions don't tell the model to rely on it, cite it, or ignore everything else. Prompting controls *how the model treats* the rest of the context.

```
A prompt in a production system is assembled from several context sources:

[1] Role & instructions      <- Prompt Engineering (this page)
[2] Retrieved knowledge      <- RAG                 (07-3)
[3] Long-term user facts     <- Memory              (07-4)
[4] Conversation history     <- State / History     (07-5)
[5] Output format contract   <- Structured Outputs  (07-6)
[6] User question            <- runtime input
```

> In short: prompt engineering, on its own, is about writing one good instruction. Inside Context Engineering, it becomes about **designing how the instruction is built and how it orchestrates every other piece of context.**

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2299/2299623.png" width="80"/> Quick Recap

---

The core techniques, covered in full in [04-Prompt-Engineering](https://github.com/gil-son/language-ai-engineering-lab/tree/main/04-Prompt-Engineering):

| Technique | One-line summary |
|---|---|
| **Zero-shot** | Ask the task directly, with no examples |
| **One-shot / Few-shot** | Provide one or more worked examples to steer format and behavior |
| **Chain-of-Thought (CoT)** | Ask the model to reason step by step before answering |
| **Decomposition** | Break a complex task into smaller, ordered sub-prompts |
| **Role / Persona** | Assign the model a role to shape tone and expertise |
| **Prompt templates** | Parameterized, reusable prompt structures with slots |
| **Constraints & formatting** | Explicitly specify output shape, length, and boundaries |

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="80"/> Continue Learning

---

This recap intentionally stays high-level. For prompt patterns, hands-on examples, reasoning techniques, and optimization strategies, go to the complete section:

**[04-Prompt-Engineering — Full Section](https://github.com/gil-son/language-ai-engineering-lab/tree/main/04-Prompt-Engineering)**
