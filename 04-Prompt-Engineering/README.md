# 04.1 Prompt Engineering
<div align="center"> <table> <tr> <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2581/2581957.png" width="80"/></td> <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/5358/5358533.png" width="80"/></td> </tr> </table> </div>

---

## 04 Prompt Engineering
<img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="60"/> Introduction

Prompt Engineering is the practice of designing, structuring, and optimizing prompts to guide Large Language Models (LLMs) toward producing accurate, relevant, and reliable outputs.

Rather than relying solely on model fine-tuning, prompt engineering leverages instruction design, examples, and reasoning strategies to control model behavior at inference time.


---

## <img src="https://cdn-icons-png.flaticon.com/512/5557/5557844.png" width="60"/> Why use it?

Prompt Engineering is essential because it allows you to:

- Improve response accuracy and consistency: add example
- Reduce hallucinations and ambiguous outputs: add example
- Guide reasoning and decision-making steps: add example
- Adapt general-purpose models to specific tasks: add example
- Save costs by avoiding unnecessary fine-tuning: add example
- Enable safer and more controllable AI systems: add example

In production systems, well-designed prompts are often as important as model selection.

---

## <img src="https://cdn-icons-png.flaticon.com/512/7527/7527144.png" width="60"/> How does it work?

LLMs generate responses based on patterns learned during training. Prompts act as **contextual constraints**, influencing:

- What the model should do
- How it should behave
- What format the output should follow
- How it should reason before answering

By shaping the input, we indirectly shape the output.

---

## Core Components – Prompt Engineering

### 1. Role Prompting

<div align="center"> 
  <img src="https://gitlab.com/gil-son/useful-images-collection/-/raw/main/png/role.png?ref_type=heads" width="80%" />
</div>

Define a clear role or persona for the model to shape tone, expertise, and reasoning style.

**Example:**
> You are a senior backend engineer specialized in distributed systems.

**Pros:**
- Improves domain alignment
- More consistent tone and terminology

**Cons:**
- Overly strict roles may limit creativity

---

### 2. Zero-Shot Prompting

<div align="center"> 
  <img src="https://gitlab.com/gil-son/useful-images-collection/-/raw/main/png/zero-shot.png?ref_type=heads" width="80%" />
</div>

Ask a task or question **without providing examples**.

**Example:**
> What is the capital of Brazil?

**Pros:**
- Simple and fast
- Low token usage

**Cons:**
- Less control over output format
- Higher ambiguity for complex tasks

---

### 3. One-Shot / Few-Shot Prompting

<div align="center"> 
  <img src="https://gitlab.com/gil-son/useful-images-collection/-/raw/main/png/one-shot.png?ref_type=heads" width="80%" />
</div>

Provide one or more examples to guide the model’s behavior.

**Example:**
```
Input: 01:00 AM
Output: One hour after midnight

Input: 02:00 AM
Output:
```

**Pros:**
- Better consistency
- Improved formatting
- Reduced ambiguity

**Cons:**
- Higher token cost
- Requires carefully curated examples

---

### 4. Chain of Thought (CoT)

<div align="center"> 
  <img src="https://gitlab.com/gil-son/useful-images-collection/-/raw/main/png/CoT.png?ref_type=heads" width="80%" />
</div>

Encourage the model to reason step by step before producing the final answer.

**Instructional Example:**
1. Access the file  
2. Remove special symbols  
3. Send the file content to: xxx@domain.com  

**Without CoT:**
```
How many letters “r” are in the word “strawberries”?
Answer: 2
```

This error happens because older or weaker models reason at the token level.

**With CoT:**
```
Split the word “strawberries” into individual characters and count how many times “r” appears.
```

**Pros:**
- Reduces reasoning errors
- Improves accuracy on complex tasks

**Cons:**
- Higher latency and token usage

---

### 5. Tree of Thought (ToT)

Explore multiple reasoning paths and compare outcomes before selecting the best one.

**Example:**
- Evaluating multiple solution strategies for a system design problem

**Pros:**
- Strong performance on complex problem-solving
- Encourages exploration

**Cons:**
- Computationally expensive
- Harder to implement

---

### 6. Batch Prompting
Send multiple prompts in a single request.

**Example:**
- Classifying thousands of customer feedback messages

**Pros:**
- Higher throughput
- Lower cost per request

**Cons:**
- Harder error isolation
- Less flexibility per prompt

---

### 7. Prompt Enrichment
Use a preprocessing LLM to improve user prompts.

**Examples:**
- Clarifying vague user input
- Adding missing context

**Pros:**
- Better downstream responses
- Improved user experience

**Cons:**
- Additional latency
- Extra model cost

---

### 8. Skeleton of Thought (SoT)
Ask the model to generate an outline before producing the full answer.

**Example:**
> First generate a bullet-point outline, then expand each point.

**Pros:**
- Better structure
- More coherent long-form outputs

**Cons:**
- Two-step generation increases latency

---

### 9. ReAct Framework
Combine **Reasoning + Acting**.

- The model reasons
- Executes actions (tools, APIs)
- Observes results
- Continues reasoning

**Pros:**
- Ideal for agents and workflows
- Enables tool usage

**Cons:**
- Complex orchestration
- Requires guardrails

---

### 10. Prompt Chaining
Break complex tasks into sequential prompts.

**Pros:**
- Easier debugging
- Modular design

**Cons:**
- More orchestration logic
- Potential error propagation

---

### 11. Least-to-Most Decomposition
Solve problems by starting with simple subtasks and gradually increasing complexity.

**Pros:**
- Reduces cognitive load
- Improves complex reasoning

**Cons:**
- Requires task decomposition logic

---

### 12. Professional Prompt Structure
A high-quality prompt usually includes:
- Role
- Task
- Context
- Constraints
- Examples (optional)
- Output format

**Pros:**
- Predictable outputs
- Easier maintenance

**Cons:**
- More upfront design effort

---

### 13. Prompt Storage and Versioning
Treat prompts as code.

**Pros:**
- Reproducibility
- Easy rollback

**Cons:**
- Requires governance

---

### 14. Prompt Management Tools
Tools like LangSmith or LangChain provide tracing, evaluation, and versioning.

**Pros:**
- Observability
- Faster iteration

**Cons:**
- Tooling dependency

---

### 15. Testing and Prompt Evaluation
- Automated tests
- Regression tests
- A/B testing
- Metrics: accuracy, latency, cost

**Pros:**
- Production reliability
- Safer deployments

**Cons:**
- Requires test datasets

---

### 16. Design Documentation
Document goals, assumptions, and failure cases.

**Pros:**
- Shared understanding
- Easier onboarding

**Cons:**
- Documentation overhead

---

### 17. Repositories and References
- Prompt pattern libraries
- Open-source examples
- Experiment notebooks

**Pros:**
- Faster learning
- Reuse of proven patterns

**Cons:**
- Requires curation


## <img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="60"/> Use Cases

- Chatbots and virtual assistants: Designing a prompt that makes a customer-support bot greet users, ask clarifying questions, and provide step-by-step troubleshooting for common issues (e.g., “Reset your password” or “Track my order”), while maintaining a consistent brand tone.
- RAG (Retrieval-Augmented Generation): Creating a prompt that instructs an AI to answer questions using only retrieved company policy documents, and to respond with “I don’t have that information” if the answer is not found in the provided context.
- AI agents and workflows: Prompting an agent to break a complex task (e.g., “Plan a marketing campaign”) into subtasks like research, copywriting, budgeting, and scheduling—then coordinating outputs between multiple tools or agents.
- Data extraction and transformation: Building a prompt that extracts structured fields (name, date, total amount) from unstructured invoices or emails and outputs them as clean JSON or a CSV-ready format.
- Code generation and review: Writing a prompt that asks the model to generate a REST API in Python, include unit tests, follow a specific style guide, and then review the code for security issues and performance improvements.
- Decision support systems: Designing a prompt that summarizes key metrics from sales data, compares different strategies, highlights risks, and recommends the best option with a short justification.



---

### <img src="https://cdn-icons-png.flaticon.com/512/2112/2112889.png" width="80"> Videos

A few recommended resources to visualize:

<div align="center">
  <a href="https://www.youtube.com/watch?v=sW5xoicq5TY" target="_blank">
      <img width="640" height="360" src="https://i.ytimg.com/vi/sW5xoicq5TY/hq720.jpg?sqp=-oaymwEnCNAFEJQDSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLAZD_GK6Y-d4_POvKW6xTNj1duPQQ"/>
  </a>
</div>

---

<div align="center">
  <a href="https://www.youtube.com/watch?v=1c9iyoVIwDs" target="_blank">
      <img width="640" height="360" src="https://i.ytimg.com/vi/1c9iyoVIwDs/hq720.jpg?sqp=-oaymwEnCNAFEJQDSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLDX-KjQUVawkSqObSHDBOgrihqKDw"/>
  </a>
</div>
