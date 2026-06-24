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

## 07.1.1 From LLMs to Systems — Design Documents

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="80"/> Introduction

---

An LLM alone is not a product. It is a capability — a powerful text-in, text-out engine. The moment you want to deploy it to serve real users, answer questions from a knowledge base, or automate a workflow, you are no longer writing prompts. You are engineering a **system**.

That transition — from experimenting with a model in a notebook to shipping a production-grade AI system — is one of the most important conceptual leaps in applied AI. And the artifact that bridges that leap is the **System Design Document** (also called a Technical Design Doc, or TDD).

This module focuses specifically on how LLMs fit inside larger systems: what architectural decisions you must make, what components you need to specify, and how to translate your understanding of LLM fundamentals into well-reasoned design choices that your team can build from.

> **Key mindset shift:** Stop thinking of the LLM as the system. Start thinking of it as one critical component inside a larger, orchestrated pipeline.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/5557/5557844.png" width="80"/> Why use it?

---

Writing a design document before building an LLM-powered system serves four distinct purposes:

**1. Forces clarity on scope and assumptions**

LLM systems involve many implicit decisions: Which model? What temperature? How much context? What happens when the model refuses? These decisions need to be surfaced and debated before they become buried in code.

**2. Creates alignment across roles**

A system design document is a shared contract between ML engineers, backend engineers, product managers, and stakeholders. It ensures everyone is solving the same problem with the same constraints.

**3. Exposes architectural risks early**

Latency bottlenecks, context window limits, cost-per-call explosions, hallucination failure modes — these are much cheaper to discover in a document than in a production incident.

**4. Enables iterative, reviewable decisions**

Unlike code, a design doc can be commented on, version-controlled, and revised without side effects. It is the only artifact in your stack that is truly cheap to change.

> Without a design doc, you build the system twice: once in chaos, and again when you realize what you actually needed.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2299/2299623.png" width="80"/> Components

---

A System Design Document for an LLM-powered application typically includes the following sections. Each section maps to a real architectural decision.

#### 1. Problem Statement and Goals
What problem does this system solve? What does success look like? Define measurable outcomes (e.g., "reduce customer support resolution time by 30%") and anti-goals (what this system will NOT do).

#### 2. System Overview
A high-level description of the system with a diagram. Shows how data flows from user input to LLM to output. Identifies all major components (API gateway, retrieval system, LLM inference endpoint, output parser, etc.).

#### 3. LLM Component Specification
This is where your fundamentals knowledge becomes directly applicable:

| Decision | Options | Design Implication |
|---|---|---|
| Model selection | GPT-4o, Claude 3.5, Gemini 1.5, open-source | Cost, latency, capability, privacy |
| Context window | 8K → 1M+ tokens | Determines retrieval strategy |
| Inference mode | API call vs self-hosted | Throughput, data residency |
| Temperature | 0.0 → 1.0 | Determinism vs creativity |
| Output format | Free text, JSON, structured schema | Parsability and reliability |

#### 4. Prompt Architecture
How is the prompt constructed at runtime? This section documents:
- System prompt content and versioning strategy
- How user input is sanitized and embedded
- Where retrieved context is injected
- How few-shot examples are selected dynamically

#### 5. Data Flow and Storage
- What data enters the system?
- What gets logged? (inputs, outputs, latency, token usage)
- How is PII handled?
- Is the conversation history persisted, and if so, where?

#### 6. Retrieval Strategy (if applicable)
If the system uses a knowledge base:
- Chunking strategy (fixed, semantic, document-aware)
- Embedding model and vector store
- Retrieval algorithm (cosine similarity, MMR, hybrid BM25 + dense)
- Reranking layer (yes/no, and which model)

#### 7. Output Handling and Validation
- How is the LLM output parsed?
- What happens on malformed output? (retry, fallback, error to user)
- Is there a guardrail layer for safety or content filtering?

#### 8. Evaluation Plan
How will you know if this system works?
- Offline evals (golden datasets, LLM-as-judge)
- Online evals (user feedback, implicit signals)
- Baseline comparisons

#### 9. Operational Considerations
- Estimated token usage and monthly cost
- Latency SLA and p95 targets
- Rate limiting strategy
- Fallback behavior under model API outage

#### 10. Open Questions and Risks
Every honest design doc ends with a section on what you don't know yet. This signals intellectual humility and surfaces blockers early.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7527/7527144.png" width="80"/> How it works?

---

Here is a step-by-step walkthrough of how a design document comes to life for a real LLM system — using a **Customer Support Automation Agent** as the running example.

#### Step 1: Start from the User Journey, Not the Model

Before writing a single technical line, trace the full user journey:

```
User types question
  → System classifies intent
  → Routes to appropriate sub-agent or knowledge base
  → LLM generates response
  → Response is validated and formatted
  → User receives answer + sources
  → Interaction is logged for future fine-tuning
```

This flow is your design doc's backbone. Every section you write maps to one of these steps.

#### Step 2: Identify All Decision Points

Go back through the flow and mark every place where you must make a technical choice. For the example above:

- `Intent classifier` → Rule-based? Another LLM? Zero-shot or fine-tuned?
- `Knowledge base` → What documents? How chunked? What embedding model?
- `Response LLM` → Which model? What system prompt? What temperature?
- `Validation` → Do you check for hallucinations? How?
- `Logging` → PII masking? What retention policy?

Each decision point becomes a subsection in your design document.

#### Step 3: Draft the Architecture Diagram

Before writing prose, draw the system. A good architecture diagram shows:

```
┌─────────────────────────────────────────────────────┐
│                  USER INTERFACE                     │
└────────────────────────┬────────────────────────────┘
                         │ HTTP request
                         ▼
┌────────────────────────────────────────────────────┐
│               API GATEWAY / AUTH LAYER             │
└────────────────────────┬───────────────────────────┘
                         │
          ┌──────────────▼──────────────┐
          │     ORCHESTRATION LAYER     │
          │  (LangGraph / custom agent) │
          └──────────────┬──────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
  ┌──────────┐   ┌──────────────┐  ┌──────────────┐
  │ RETRIEVER│   │  LLM ENGINE  │  │  GUARDRAILS  │
  │ (RAG)    │   │  (GPT-4o)    │  │  (NeMo/etc)  │
  └──────────┘   └──────────────┘  └──────────────┘
         │               │               │
         └───────────────▼───────────────┘
                  ┌──────────────┐
                  │  OUTPUT      │
                  │  FORMATTER   │
                  └──────────────┘
                         │
                  ┌──────────────┐
                  │  LOGGING &   │
                  │  OBSERVABIL. │
                  └──────────────┘
```

#### Step 4: Write the LLM Component Spec

This is the section where your knowledge of LLM fundamentals — architectures, pretraining, instruction tuning, RLHF — pays off directly. You are not just choosing a model name; you are justifying why that model's training objective, context handling, and alignment approach makes it the right tool for this job.

**Example entry:**

```
Model: claude-3-5-sonnet-20241022
Justification: Task requires long-context reasoning over support tickets
(avg 3,000 tokens). Claude's 200K context window and strong instruction-
following from Constitutional AI training aligns with our accuracy and
safety requirements. Cost-per-token is 40% lower than GPT-4o for our
expected volume of 500K tokens/day.

Temperature: 0.1
Justification: Support responses must be consistent and factual.
Low temperature reduces variance across sessions.

Max output tokens: 1,024
Justification: Empirical testing shows 98% of valid support answers
fit within 800 tokens. Cap prevents runaway completions.
```

#### Step 5: Document the Prompt Architecture

Never leave the prompt as an undocumented runtime artifact. Treat it as a versioned system component.

```
Prompt version: v2.3
Last updated: 2025-04-10
Owner: NLP Platform Team

System prompt structure:
  [1] Role and persona definition (static)
  [2] Company knowledge and tone guidelines (static)
  [3] Retrieved context from knowledge base (dynamic, max 8,000 tokens)
  [4] Conversation history (dynamic, last 5 turns)
  [5] User query (dynamic)
  [6] Output format instructions (static)

Prompt versioning: stored in Git under /prompts/, injected at deploy time
via environment variable SYSTEM_PROMPT_VERSION.
```

#### Step 6: Define the Evaluation Plan Before You Build

The evaluation plan is not a post-launch concern. Write it in the design doc, so that what you build is measurable from day one.

| Metric | Method | Target |
|---|---|---|
| Correctness | LLM-as-judge vs. golden dataset (n=500) | ≥ 87% |
| Groundedness | Citation overlap with retrieved chunks | ≥ 92% |
| Refusal rate | % of valid queries refused | ≤ 3% |
| Latency (p95) | End-to-end wall clock time | ≤ 4.5s |
| Cost per query | Tokens × model price | ≤ $0.008 |

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="80"/> Use Cases

---

System Design Documents are not just for large enterprise teams. They apply across a spectrum of LLM-powered applications:

#### Internal Knowledge Base Assistant
A company deploys an LLM over its internal Confluence/Notion pages. The design doc specifies chunking strategy, access control integration (only show docs the user has permission to see), response citation format, and PII redaction rules for logs.

#### LLM-Powered IVR / Voice Bot
An automated phone system that uses an LLM to understand caller intent and route or resolve issues. The design doc covers ASR→text pipeline, latency constraints (voice is unforgiving — sub-2s response budget), turn-taking logic, escalation triggers, and the handoff protocol to human agents. *(See module 16 for AI IVR specifics.)*

#### Code Review Assistant
A system that ingests a pull request diff and generates structured review comments. The design doc defines max diff size per call, the prompt structure for multi-file context, how to handle binary files, and how review comments are posted back via GitHub API.

#### Multi-Agent Research Pipeline
An orchestrated system where one agent plans a research task, spawns sub-agents to search and summarize, and a final agent synthesizes the outputs. The design doc is critical here — it defines inter-agent communication protocols, how state is passed, error propagation, and the human-in-the-loop checkpoints.

#### Real-Time Personalization Engine
An LLM that generates personalized content recommendations or emails. The design doc specifies how user profile data is injected into the prompt, what A/B testing framework is used, and how output quality is monitored at scale.

---

### <img src="https://cdn-icons-png.flaticon.com/512/6675/6675847.png" width="80"> Limitations

---

Design documents are powerful, but they come with real limitations you must account for:

**1. Documents go stale**
A design doc written at project inception becomes misleading as the system evolves. You must treat it as a living document with explicit versioning and ownership. Teams that treat the doc as a one-time artifact end up with documentation that contradicts reality.

**2. LLM behavior is non-deterministic by design**
Unlike a traditional API contract, an LLM's output cannot be fully specified in a design doc. The doc can define expected behavior, format, and constraints — but actual outputs will always have variance. Build your system assuming the LLM will occasionally be wrong, refuse, or produce malformed output.

**3. Cost and latency estimates are always approximations**
Token usage depends on runtime context length, which is hard to predict precisely. Real-world p95 latency depends on model API load, network conditions, and your own infrastructure. Treat design-time estimates as baselines, not guarantees.

**4. Design docs can create false confidence**
A well-written design doc can give the impression that edge cases are handled when they are only listed. "Fallback to human agent on refusal" is not a design — it is a note. The actual fallback logic must be implemented, tested, and monitored.

**5. Prompt architecture is fragile across model versions**
When the underlying model is updated or swapped, prompts that worked well may degrade. Design docs should note which model version the prompt was tuned for, and include a re-evaluation protocol for model upgrades.

**6. Security and adversarial inputs are often under-specified**
Prompt injection, jailbreaks, and data exfiltration via the LLM are real attack surfaces. Design docs in production systems must include a dedicated threat model section — something many early-stage teams skip.

---

### <img src="https://cdn-icons-png.flaticon.com/512/2112/2112889.png" width="80"> Videos

A recommended video to visualize:

<div align="center">
  <a href="https://www.youtube.com/watch?v=fFgyOucIFuk" target="_blank">
      <img width="640" height="360" src="https://i.ytimg.com/vi/fFgyOucIFuk/hqdefault.jpg?sqp=-oaymwEnCOADEI4CSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBHeCpHvfGkZzjwULYaxOiQYwk4gg"/>
  </a>
</div>

---

<div align="center">
  <a href="https://www.youtube.com/watch?v=_pEEJu-2KKM" target="_blank">
      <img width="640" height="360" src="https://i.ytimg.com/vi/_pEEJu-2KKM/hq720.jpg?sqp=-oaymwEnCNAFEJQDSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLCReKeM7dXvVhKYV6ZKdGVRWYTwHw"/>
  </a>
</div>