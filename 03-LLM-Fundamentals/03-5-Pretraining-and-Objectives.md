# 03. Fundamentals

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

## 03.5. Pretraining and Objectives

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="80"/> Introduction

---

Pretraining is the **foundation phase** in building a Large Language Model (LLM).  
During this stage, a model learns **general language patterns, grammar, facts, and reasoning** from large-scale text corpora — typically scraped from the internet, books, code, and articles.

The model learns through **self-supervised learning**, predicting hidden or next words in text sequences.  
This gives it a strong base to later specialize (fine-tuning, instruction-tuning, RLHF).

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/5557/5557844.png" width="80"/> Why use it?
  
- Builds **language understanding** without labeled data.  
- Enables the model to learn **syntax, semantics, and context**.  
- Reduces the need for task-specific data later (fine-tuning).  
- Provides **transferable knowledge** that can be adapted to many NLP tasks.  
- Forms the **backbone of generalization** for LLMs like GPT, LLaMA, and PaLM.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2299/2299623.png" width="80"/> Components

1. **Massive Text Corpus** – The raw data source for training (Wikipedia, web crawl, books, code).  
2. **Tokenizer** – Converts text into subword tokens.  
3. **Model Architecture** – Typically a transformer with encoder-decoder or decoder-only design.  
4. **Objective Function** – Defines how the model learns from text (e.g., Masked LM, Causal LM).  
5. **Optimization Process** – Gradually adjusts weights to minimize prediction loss.  
6. **Compute Infrastructure** – High-performance GPUs/TPUs for distributed training.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7527/7527144.png" width="80"/> How it works?

Pretraining teaches the model to predict or reconstruct text — enabling it to develop statistical and semantic understanding of language.

#### Common Pretraining Objectives

- **Masked Language Modeling (MLM)** – Used in *BERT*: mask some words and predict them.  
- **Causal Language Modeling (CLM)** – Used in *GPT*: predict the next token given previous ones.  
- **Seq2Seq (Denoising Autoencoding)** – Used in *T5*: reconstruct corrupted text sequences.  
- **Span Prediction / Permutation LM** – Used in *XLNet*: predict random token spans or permutations.  

#### Step-by-step Process

1. **Collect Text Data** (massive corpus).  
2. **Tokenize Text** into subword pieces.  
3. **Feed Sequences** into the model.  
4. **Predict Missing or Next Tokens.**  
5. **Compute Loss (Cross-Entropy).**  
6. **Backpropagate to Update Weights.**  
7. **Repeat for Billions of Steps.**

#### Simple Diagram

```mermaid
graph TD
    A[Raw Text Data] --> B[Tokenization]
    B --> C[Input Tokens + Context]
    C --> D[Transformer Layers]
    D --> E[Predict Masked/Next Tokens]
    E --> F[Loss Calculation]
    F --> G[Weight Updates]
    G --> H[Trained Language Model]
```

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="80"/> Use Cases

- Foundation for all downstream fine-tuning and instruction tasks.  
- Enables **zero-shot** and **few-shot** reasoning.  
- Used to build:  
  - **General-purpose chatbots (GPT, Claude)**  
  - **Multilingual models (BLOOM)**  
  - **Code models (Codex, StarCoder)**  
  - **Scientific or domain models (BioBERT, MedPaLM)**  

---

### <img src="https://cdn-icons-png.flaticon.com/512/6675/6675847.png" width="80"> Limitations

- **Extremely costly** (data + compute).  
- **Data bias** can lead to biased outputs.  
- **No explicit reasoning** — learns statistical associations.  
- **Hard to interpret** internal representations.  
- **Catastrophic forgetting** during fine-tuning if not careful.

---

### <img src="https://cdn-icons-png.flaticon.com/512/2147/2147809.png" width="80"> Code/Notebook/Projects

- [Create an LLM from scratch](https://github.com/gil-son/language-ai-engineering-lab/tree/main/notebooks/02-Transformers)

---

### <img src="https://cdn-icons-png.flaticon.com/512/2112/2112889.png" width="80"> Video

A recommended video to visualize:

<div align="center">
  <a href="https://www.youtube.com/watch?v=ZLbVdvOoTKM" target="_blank">
      <img width="640" height="360" src="https://i.ytimg.com/vi/ZLbVdvOoTKM/maxresdefault.jpg"/>
  </a>
</div>
