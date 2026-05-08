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

## 07.3. Design Document Examples — Context Management

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="80"/> Introduction

---

Context management is one of the most consequential — and most underestimated — engineering disciplines in LLM-powered systems. Every call to a language model is shaped entirely by what you put in the context window: the system prompt, conversation history, retrieved knowledge, user input, and output formatting instructions all compete for the same finite space.

Get it wrong, and your system hallucinates, loses track of the conversation, ignores instructions, or silently truncates critical information. Get it right, and you have a system that is coherent, accurate, cost-efficient, and robust at scale.

This module makes context management **concrete** by walking through real, annotated Design Document examples. Each example targets a different architectural pattern — from a stateless Q&A bot to a long-running multi-session agent — so you can see how context decisions change based on use case, model choice, and user expectations.

> **What you will learn here:** Not principles in the abstract, but actual design decisions, the tradeoffs behind them, and what the resulting context window looks like at runtime.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/11471/11471401.png" width="80"/>  Common Design Document Types

Before diving into examples, it is essential to understand that "design document" is not a single artifact — it is a family of documents, each serving a distinct purpose in the engineering lifecycle. In LLM system development, you will encounter all five of these types.

---

#### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/3344/3344877.png" width="80"/> HLD — High Level Design
*"How does the system work, overall?"*

The HLD describes the system at the architectural level. It answers: what are the main components, how do they connect, and what are the key data flows? For an LLM system, the HLD shows the relationship between the user interface, the orchestration layer, the retrieval system, the model inference endpoint, and the storage layer — without going into implementation details.

**In context management terms:** The HLD is where you declare *that* a context window strategy exists (e.g., "the system uses a sliding window for conversation history and a RAG pipeline for knowledge retrieval") but not *how* it is implemented.

**Typical length:** 3–8 pages. Audience: engineers, product managers, architects.


Referencies:

- [How to create a good High Level Design — HLD](https://medium.com/@vedmkw/how-to-create-a-good-high-level-design-hld-fddba7f6ae18)
- [MADR (Markdown ADR)](https://adr.github.io/madr/?utm_source=chatgpt.com)

Templates:

- [HLD template](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.ucl.ac.uk%2Fisd%2Fsites%2Fisd%2Ffiles%2Fmigrated-files%2FHLD_template_v3.docx&wdOrigin=BROWSELINK)
- [Prompt to Generate HLD](https://devfullcycle.notion.site/Prompt-para-gera-o-de-um-HLD-29e1423c0388802e98dec48b415a98f2)


---

#### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/4067/4067507.png" width="80"/> Feature Design Doc
*"How does this specific capability work?"*

A Feature Design Doc zooms into one feature within the system — for example, "multi-session memory" or "dynamic prompt compression." It describes the user-facing behavior, the technical approach, the edge cases, and the acceptance criteria for that feature specifically.

**In context management terms:** A Feature Design Doc for "context overflow handling" would specify exactly which slot gets truncated first, the token accounting method, the retry logic, and how overflow events are surfaced in observability tooling.

**Typical length:** 2–5 pages. Audience: the engineering team implementing the feature.

---

#### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/3344/3344790.png" width="80"/>  LLD — Low Level Design
*"How exactly will we build this?"*

The LLD is the implementation blueprint. It includes class/function signatures, database schemas, API contracts, sequence diagrams, and pseudocode. For an LLM pipeline, this is where the context assembly function is fully specified: input types, token counting logic, priority queue for overflow, error return types, and unit test cases.

**In context management terms:** The LLD for a context manager might include the full signature of a `build_context(session_id, user_query, retrieval_results) -> ContextBundle` function, with documented behavior for each edge case.

**Typical length:** 5–15 pages. Audience: engineers who will write the code.

---

#### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/5175/5175137.png" width="80"/> ADR — Architecture Decision Record
*"Why did we make this architectural choice, and what did we reject?"*

An ADR is a short, structured record of a single architectural decision. It captures the context (what problem we faced), the decision (what we chose), the alternatives considered, and the consequences (what we gain and what we trade off). ADRs are stored alongside code and updated when decisions change.

**In context management terms — example ADR:**

```
ADR-007: Use sliding window over full history for conversation context

Status: Accepted (2025-03-12)

Context:
  Conversations average 8 turns but can reach 30+. Full history
  causes latency to grow linearly with session length and exceeds
  our p95 budget of 2s for sessions longer than 15 turns.

Decision:
  Use a sliding window of the last 10 turns. Always preserve the
  first turn (establishes user intent) and the last 3 turns
  (ensures immediate coherence).

Alternatives considered:
  - Full history: rejected — latency and cost unsustainable at scale
  - Summarization: rejected for v1 — adds 300–500ms per compression
    call; revisit in Q3 when we have fine-tuned summarizer
  - Fixed token budget: rejected — turn length variance too high;
    token-based windowing requires exact counting on every request

Consequences:
  + Predictable latency regardless of session length
  + Simpler implementation, no compression model needed
  - Agent may lose context from early turns in long sessions
  - Users who revisit early topics may get inconsistent responses
```

**Typical length:** Half a page to 2 pages per decision. Audience: all engineers, archived for future reference.


Referencies:

- [ADR GitHub Organization](https://adr.github.io/?utm_source=chatgpt.com)
- [MADR (Markdown ADR)](https://adr.github.io/madr/?utm_source=chatgpt.com)

Templates:

- [ADR Templates Catalog](https://adr.github.io/adr-templates/?utm_source=chatgpt.com)
- [architecture_decision_record (kainepro)](https://github.com/kainepro/architecture_decision_record?utm_source=chatgpt.com)


---

#### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6404/6404017.png" width="80"/>  RFC — Request for Comments
*"Here is a proposal — please challenge it before we commit."*

An RFC is a pre-decision document that proposes a significant change and explicitly solicits structured feedback. It is used when a decision is large enough to warrant broad input — for example, switching the context management strategy from sliding window to hierarchical memory, or adopting a new vector store. The RFC is circulated, commented on, revised, and eventually either accepted (becoming an ADR) or rejected (with the reasoning recorded).

**In context management terms:** An RFC might propose adding a long-term memory tier to an existing agent system. It would describe the proposed architecture, estimate the implementation cost, quantify the expected accuracy improvement from evals, and ask reviewers to flag risks or alternative approaches.

**Typical RFC structure:**
- Summary (2–3 sentences)
- Motivation — why now, what problem does this solve?
- Proposed design — architecture, API changes, data model
- Alternatives considered
- Rollout plan and rollback strategy
- Open questions for reviewers
- Deadline for comments

**Typical length:** 3–10 pages. Audience: senior engineers, tech leads, affected teams.


Referencies:

- [Texto do link](https://exemplo.com)
- [Texto do link](https://exemplo.com)

Templates:

- [Rust RFCs](https://github.com/rust-lang/rfcs/blob/master/0000-template.md)
- [React RFCs](https://github.com/reactjs/rfcs/blob/main/0000-template.md)


---

### How These Five Types Work Together

In a real LLM project, these document types appear in sequence:

```
RFC (propose)  →  ADR (decide)  →  HLD (design whole system)
                                         ↓
                               Feature Design Doc (design one feature)
                                         ↓
                                    LLD (implement it)
```

The three annotated examples in the **How it works?** section below each correspond to an HLD-level description, with Feature Design Doc detail on the context management strategy and ADR-style justifications embedded inline.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/5557/5557844.png" width="80"/> Why use it?

---

Design Document Examples serve a fundamentally different purpose than design document *templates*. Templates tell you **what to fill in**. Examples show you **how engineers actually think** through context management problems — the reasoning, the tradeoffs, and the mistakes worth avoiding.

**1. Bridges theory and implementation**

Reading that "sliding window truncation is a common technique" is not the same as seeing an annotated doc that says: *"We use a 3,000-token sliding window on conversation history, dropping turns from the oldest end, and we always preserve the system prompt and the last user turn regardless of token budget."* The latter is buildable.

**2. Reveals hidden decisions**

Context management involves dozens of micro-decisions that no high-level guide surfaces: What happens when retrieved context and conversation history together exceed the budget? Who wins? How is token counting done — estimated or exact? What is the flush strategy when context is full? Examples make these visible.

**3. Gives you a vocabulary for design reviews**

When your team reviews a context management design, shared examples create a common reference point. Instead of debating abstract strategies, you can say: *"This is closer to Example 2 (session-persistent agent) than Example 1 — do we have a summarization fallback?"*

**4. Accelerates onboarding**

New engineers joining an LLM team can read three annotated design doc examples and immediately understand the context management patterns in use — far faster than reading code or attending meetings.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2299/2299623.png" width="80"/> Components

---

Each Design Document Example in this module is structured around the same six building blocks of context management. Understanding these components is prerequisite to reading any example.

#### 1. Context Budget
The total token allocation for a single model call, broken down by role:

| Slot | Typical Allocation | Notes |
|---|---|---|
| System prompt | 500–2,000 tokens | Static; version-controlled |
| Retrieved context (RAG) | 2,000–8,000 tokens | Dynamic; varies per query |
| Conversation history | 1,000–4,000 tokens | Dynamic; managed via windowing |
| User input | 100–1,000 tokens | Sanitized before insertion |
| Output buffer | 512–2,048 tokens | Reserved; not sent as input |

#### 2. History Management Strategy
How previous turns are included, compressed, or dropped:
- **Full history** — all turns, up to context limit
- **Sliding window** — last N turns only
- **Summarization** — older turns collapsed into a running summary
- **Hierarchical memory** — short-term (turns) + long-term (session summaries) + episodic (user profile)

#### 3. Retrieval Integration Point
Where retrieved chunks are injected in the prompt and how conflicts with history are resolved when both compete for tokens.

#### 4. Overflow Strategy
What happens when the assembled context exceeds the budget:
- Drop oldest history turns first
- Truncate retrieved context to fit
- Summarize and compress before dropping
- Reject the request and ask the user to simplify

#### 5. Token Counting Method
- **Estimated** — character count heuristic (fast, ±15% error)
- **Exact** — tiktoken / model-native tokenizer (slower, precise)
- **Conservative** — use exact for system prompt + history; estimate for retrieved chunks

#### 6. Observability and Logging
What context management data is captured per call:
- Tokens used per slot (system, history, retrieval, user, output)
- Truncation events (how often, which slot was dropped)
- Context hit rate (% of calls that stayed within budget without overflow)

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7527/7527144.png" width="80"/> How it works?

---

Below are four fully annotated Design Document Examples, each addressing a different context management scenario.

---

#### 📄 Example 1 — Stateless FAQ Bot (Simple)

**System:** A public-facing FAQ assistant for a SaaS product. Each conversation is a single turn — no history is preserved between sessions.

**Model:** `gpt-4o-mini` (128K context window, low cost per token)

**Context Budget:**

```
Total available:     128,000 tokens
System prompt:         1,200 tokens  (static, version-controlled)
Retrieved chunks:      6,000 tokens  (top-5 FAQ passages, BM25 retrieval)
User query:              400 tokens  (max enforced at API gateway)
Output buffer:         1,000 tokens
──────────────────────────────────
Total used (max):      8,600 tokens  (6.7% of window — intentionally conservative)
```

**Design decision — Why use only 6.7% of a 128K window?**

> *"This is a latency-sensitive public endpoint with a p95 SLA of 1.5s. Filling more of the context window increases TTFT (time to first token). For FAQ retrieval, 5 passages is empirically sufficient — our evals show no accuracy gain beyond 8 retrieved chunks for this domain. We deliberately leave headroom to absorb future system prompt growth without re-benchmarking latency."*

**History Management:** None. Stateless by design.

**Overflow Strategy:** If the user query exceeds 400 tokens, the API gateway returns a 400 error with a message asking the user to shorten their question. Retrieved context is capped at 5 chunks regardless of retrieval score.

**Token Counting:** Exact, using `tiktoken` with `cl100k_base` encoding. Run on every request.

**Observability:**
```json
{
  "call_id": "abc-123",
  "tokens_system": 1187,
  "tokens_retrieved": 5842,
  "tokens_user": 214,
  "tokens_output": 387,
  "overflow_event": false,
  "retrieval_chunks_used": 5,
  "latency_ms": 1243
}
```

---

#### 📄 Example 2 — Multi-Turn Customer Support Agent (Intermediate)

**System:** A support agent for a telecom company. Conversations span multiple turns within a single session (average 6 turns, max observed 22 turns). Session ends when the user closes the chat or is escalated to a human.

**Model:** `claude-3-5-sonnet-20241022` (200K context window)

**Context Budget:**

```
Total available:     200,000 tokens
System prompt:         2,400 tokens  (static + dynamic policy injection)
User profile:            600 tokens  (account tier, open tickets, plan)
Conversation history: 12,000 tokens  (sliding window — last 10 turns)
Retrieved context:     8,000 tokens  (top-6 KB articles, hybrid retrieval)
User query:              500 tokens
Output buffer:         2,048 tokens
──────────────────────────────────
Total used (max):     25,548 tokens  (12.8% of window)
```

**Design decision — Sliding window parameters:**

> *"We chose a 10-turn window after A/B testing against 6-turn and 14-turn windows. At 6 turns, users who revisited a sub-issue from earlier in the conversation received inconsistent responses — the agent had 'forgotten' the prior resolution attempt. At 14 turns, we saw no accuracy improvement but a 180ms median latency increase. 10 turns covers 94% of our sessions without overflow."*

**History Management:** Sliding window (last 10 turns). Turns are stored in a Redis session store keyed by `session_id`. On each request, the orchestration layer fetches the last 10 turns, assembles the context, and calls the model.

**Overflow Strategy — Priority order when budget is exceeded:**
1. Reduce retrieved context from 6 chunks to 3
2. Drop oldest conversation turns (never drop the most recent 3 turns)
3. Truncate user profile to account tier + open ticket count only
4. If still over budget: log overflow event, proceed with truncated context, flag session for review

**Dynamic Policy Injection:**

The system prompt has a slot for account-tier-specific policies:

```
[BASE SYSTEM PROMPT — 1,800 tokens]
...
[POLICY INJECTION — dynamic, 200–600 tokens]
{{#if account_tier == "enterprise"}}
  This customer has a dedicated SLA of 4-hour response. Escalate unresolved
  technical issues immediately rather than attempting a third resolution step.
{{else if account_tier == "free"}}
  Standard SLA applies. Self-service resources should be offered before
  escalation to human agents.
{{/if}}
```

**Token Counting:** Exact for system prompt + user profile + conversation history. Estimated (char / 3.5) for retrieved chunks to save latency on chunk assembly. Error margin accepted: ±8%.

**Observability:**
```json
{
  "session_id": "sess-789",
  "turn": 7,
  "tokens_system": 2389,
  "tokens_profile": 541,
  "tokens_history": 9814,
  "tokens_retrieved": 7203,
  "tokens_user": 312,
  "tokens_output": 681,
  "overflow_event": false,
  "history_turns_included": 10,
  "retrieval_chunks_used": 6
}
```

---

#### 📄 Example 3 — Long-Running Research Agent (Advanced)

**System:** An autonomous research agent that a user activates to investigate a topic over multiple sessions spanning days or weeks. The agent must remember prior findings, avoid re-researching what it already knows, and build a coherent knowledge state across sessions.

**Model:** `gemini-1.5-pro` (1M context window) with a fallback to `claude-3-5-sonnet` for cost-sensitive sub-tasks.

**Context Budget:**

```
Total available:      1,000,000 tokens
System prompt:           3,200 tokens  (static)
Long-term memory:       15,000 tokens  (compressed session summaries)
Working memory:         40,000 tokens  (current session turns, uncompressed)
Retrieved documents:    80,000 tokens  (full documents, not just chunks)
Tool call history:       8,000 tokens  (last 20 tool invocations + results)
User input:              2,000 tokens
Output buffer:          10,000 tokens
──────────────────────────────────────
Total used (max):      158,200 tokens  (15.8% of window)
```

**Design decision — Hierarchical memory architecture:**

> *"Single-window history does not work for a research agent that operates across sessions. We implement a three-tier memory model: (1) Working memory holds the current session in full. (2) At session end, a dedicated compression call summarizes the session into ~3,000 tokens and appends it to long-term memory. (3) Long-term memory is capped at 15,000 tokens — when exceeded, the oldest session summaries are re-compressed into a single archival block. This gives the agent coherent recall over 10+ sessions without ever exceeding context budget."*

**Memory Compression Call (session end):**

A separate, lightweight model call (`claude-3-haiku`) summarizes each completed session:

```
System: You are a research memory compressor. Given the full transcript
of a research session, produce a structured summary of:
- Key findings (bullet list, max 10 items)
- Hypotheses confirmed or refuted
- Sources consulted (title + URL only)
- Open threads for future sessions
- Data collected (structured, if any)
Output must not exceed 3,000 tokens.
```

**Overflow Strategy:**
1. Compress working memory early (mid-session) if approaching 50,000 tokens
2. Reduce retrieved documents from full-text to chunk-only (saves ~60,000 tokens)
3. Drop tool call history beyond last 10 invocations
4. Never compress long-term memory mid-session — only at session boundaries

**Cost Optimization:**

| Task | Model | Reason |
|---|---|---|
| Main reasoning | `gemini-1.5-pro` | Large context, strong reasoning |
| Memory compression | `claude-3-haiku` | Cheap, fast, structured output |
| Simple lookups | `gpt-4o-mini` | Low latency, low cost |
| Document summarization | `claude-3-haiku` | Handles long inputs efficiently |

**Observability:**
```json
{
  "agent_id": "research-007",
  "session": 4,
  "tokens_system": 3187,
  "tokens_long_term_memory": 14203,
  "tokens_working_memory": 38712,
  "tokens_retrieved": 71540,
  "tokens_tool_history": 6821,
  "tokens_user": 1102,
  "tokens_output": 4893,
  "overflow_events_this_session": 1,
  "compression_calls_this_session": 2,
  "total_sessions": 4
}
```

---

#### 📄 Example 4 — Deep Research Pipeline (Expert)

**System:** A multi-agent deep research pipeline that accepts a broad research question, decomposes it into sub-queries, executes parallel web searches and document retrievals, synthesizes findings across sources, and produces a structured long-form report — all within a single user-initiated run lasting minutes to hours.

**Model:** `gemini-2.5-pro` (1M context window) as the orchestrator; `gpt-4o-mini` for sub-agent search summarization; `claude-3-5-haiku` for deduplication and citation formatting.

**Architecture Overview:**

```
User query
    │
    ▼
Orchestrator agent (gemini-2.5-pro)
    ├── Decompose into N sub-queries
    ├── Dispatch to Search sub-agents (parallel, gpt-4o-mini)
    │       └── Each sub-agent: web search → chunk retrieval → local summary
    ├── Collect sub-agent summaries
    ├── Deduplicate + cite (claude-3-5-haiku)
    └── Synthesize final report (gemini-2.5-pro)
```

**Context Budget — Orchestrator:**

```
Total available:      1,000,000 tokens
System prompt:           4,500 tokens  (orchestration rules, output schema)
Research plan:           2,000 tokens  (decomposed sub-queries + status)
Sub-agent summaries:   120,000 tokens  (up to 20 summaries × 6,000 tokens each)
Synthesis scratchpad:   30,000 tokens  (intermediate reasoning, outline)
User query + constraints: 1,500 tokens
Output buffer:          20,000 tokens  (long-form report)
──────────────────────────────────────
Total used (max):      178,000 tokens  (17.8% of window)
```

**Context Budget — Search Sub-agent (per instance):**

```
Total available:        128,000 tokens  (gpt-4o-mini)
System prompt:            1,200 tokens  (search + summarize instructions)
Search results (raw):    40,000 tokens  (top-10 web results, full text)
Sub-query:                  300 tokens
Output buffer:            6,000 tokens  (structured summary for orchestrator)
──────────────────────────────────────
Total used (max):        47,500 tokens  (37.1% of window — intentionally higher
                                         to maximize recall per sub-agent)
```

**Design decision — Why run sub-agents in parallel instead of sequentially?**

> *"Sequential search would take 12–18 minutes for a 15-sub-query research plan, which is unacceptable for interactive use. Parallel execution reduces wall-clock time to ~2–3 minutes (the longest single sub-agent call). The orchestrator's context is not populated until all sub-agents complete, so there is no race condition on the shared context window. The tradeoff is cost: 15 parallel gpt-4o-mini calls vs 15 sequential calls costs the same tokens but peaks API concurrency. We rate-limit to 10 concurrent sub-agents to stay within our tier limits."*

**Design decision — Sub-agent summary size of 6,000 tokens:**

> *"We tested 2,000, 4,000, 6,000, and 10,000 token summaries. At 2,000 tokens, sub-agents truncated key evidence — the orchestrator's synthesis missed crucial details. At 10,000 tokens, the orchestrator's context filled too quickly with redundant text, and synthesis quality did not improve. 6,000 tokens was the sweet spot: enough for a sub-agent to preserve methodology, key findings, 3–5 direct quotes, and source URLs, while leaving the orchestrator with sufficient budget to hold all 20 summaries simultaneously."*

**Research Plan Slot:**

The orchestrator maintains a structured JSON plan in its context, updated after each sub-agent completes:

```json
{
  "query": "Impact of transformer architecture on NLP benchmarks 2020–2025",
  "sub_queries": [
    { "id": 1, "query": "BERT vs GPT performance on GLUE 2020", "status": "complete", "summary_tokens": 5840 },
    { "id": 2, "query": "T5 and encoder-decoder variants 2021", "status": "complete", "summary_tokens": 6100 },
    { "id": 3, "query": "Instruction tuning impact 2022", "status": "running" },
    { "id": 4, "query": "RLHF and alignment benchmarks 2023–2024", "status": "pending" }
  ],
  "total_sub_queries": 15,
  "completed": 2,
  "running": 1,
  "pending": 12
}
```

**Overflow Strategy — Orchestrator:**
1. If sub-agent summaries exceed 120,000 tokens, invoke a secondary compression pass using `claude-3-5-haiku` to reduce each summary to 3,000 tokens before loading into orchestrator context
2. If synthesis scratchpad exceeds 30,000 tokens mid-synthesis, checkpoint the partial outline, flush the scratchpad, and continue from the checkpoint
3. Never truncate the research plan — it is the orchestrator's ground truth for task completion
4. Output buffer is hard-reserved: synthesis stops and yields partial output if remaining budget drops below 20,000 tokens

**Overflow Strategy — Search Sub-agent:**
1. If raw search results exceed 40,000 tokens, score chunks by BM25 relevance to the sub-query and keep top-N fitting within budget
2. Never truncate the system prompt or sub-query
3. If a single web page exceeds 8,000 tokens, truncate to first 8,000 (typically captures the main body before boilerplate)

**Deduplication Pass (claude-3-5-haiku):**

Before loading sub-agent summaries into the orchestrator, a lightweight deduplication call identifies and collapses redundant findings:

```
System: You receive N research summaries on the same broad topic.
Identify claims that appear in 3 or more summaries and consolidate
them into a single canonical statement with all supporting citations.
Return a deduplicated summary list where each unique claim appears
exactly once, attributed to all sources that support it.
Output must not exceed [total_budget] tokens.
```

> *"Without deduplication, 40–60% of the orchestrator's context was consumed by the same 5–6 major findings repeated across every sub-agent summary. After deduplication, the orchestrator's effective information density tripled, and report quality improved measurably on factual coverage evals."*

**Token Counting:**
- **Orchestrator:** Exact counting using model-native tokenizer for all slots. The research plan and sub-agent summaries are high-value slots — estimation errors here cascade into synthesis quality degradation.
- **Sub-agents:** Estimated (char / 3.8) for raw search results (fast, low-stakes — overflow is handled by chunk scoring). Exact for system prompt and output.

**Cost Optimization:**

| Task | Model | Tokens/call (avg) | Reason |
|---|---|---|---|
| Orchestration + synthesis | `gemini-2.5-pro` | ~180,000 | Large context, strongest reasoning |
| Search + local summary | `gpt-4o-mini` | ~47,000 × 15 | Low cost per call, parallelizable |
| Deduplication + citation | `claude-3-5-haiku` | ~80,000 | Fast structured output, cheap |
| Plan status updates | `gpt-4o-mini` | ~2,000 | Minimal reasoning needed |

**Estimated cost per deep research run:** ~$0.18–0.35 USD (15 sub-queries, average complexity).

**Observability:**
```json
{
  "run_id": "deep-research-2891",
  "user_query_tokens": 312,
  "sub_queries_total": 15,
  "sub_queries_completed": 15,
  "sub_agent_calls": 15,
  "dedup_calls": 1,
  "orchestrator_calls": 2,
  "tokens_orchestrator_system": 4487,
  "tokens_research_plan": 1843,
  "tokens_sub_agent_summaries_raw": 94200,
  "tokens_sub_agent_summaries_post_dedup": 61400,
  "tokens_synthesis_scratchpad": 22100,
  "tokens_output_report": 14300,
  "overflow_events": 0,
  "compression_passes": 0,
  "wall_clock_seconds": 187,
  "total_tokens_all_calls": 892400,
  "estimated_cost_usd": 0.24
}
```

**Key lessons from this pattern:**

- **Parallel sub-agents change the cost structure, not the total token count.** You spend the same tokens whether sequential or parallel — but wall-clock time collapses dramatically. Design for concurrency from the start; retrofitting it is expensive.
- **Deduplication is not optional at scale.** Without it, the orchestrator's context becomes a hall of mirrors — the same findings echoed by every sub-agent, leaving no room for genuinely unique insights.
- **Hard-reserve the output buffer.** A synthesis that runs out of context mid-report produces a truncated, inconsistent document. Reserve the output slot before assembly begins, not after.
- **The research plan is the orchestrator's spine.** It must survive every overflow event intact. If you must drop something, drop retrieved content before dropping the plan.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="80"/> Use Cases

---

The four example patterns above map to a wide range of real-world applications. Here is how to match your use case to the right example:

#### Use Example 1 (Stateless) when:
- Each user interaction is self-contained — a search, a lookup, a single question
- Latency is critical and context size must be minimized
- There is no meaningful session concept (e.g., public APIs, embedded widgets)
- Examples: Product search assistants, document Q&A, HR policy lookup bots

#### Use Example 2 (Multi-Turn Session) when:
- Users have back-and-forth conversations with clear start and end points
- The agent must remember earlier turns to give coherent answers
- Sessions are bounded (minutes to hours, not days)
- Examples: Customer support, technical helpdesks, onboarding assistants, tutoring bots

#### Use Example 3 (Long-Running Agent) when:
- The agent operates across multiple sessions over days or weeks
- It must build and maintain a cumulative knowledge state
- Token budgets must be actively managed to avoid degradation over time
- Examples: Research assistants, autonomous coding agents, project management AIs, personal AI advisors

#### Use Example 4 (Deep Research Pipeline) when:
- A single user query requires decomposition into many parallel sub-tasks
- Research quality depends on breadth of sources, not just depth of single retrieval
- Wall-clock time matters as much as token budget
- The final output is a structured long-form artifact (report, analysis, literature review)
- Examples: Competitive intelligence platforms, academic literature review tools, due diligence automation, investigative journalism assistants

#### Hybrid Patterns:
Many production systems combine patterns. A coding assistant might use **Example 1** for single-file completions, **Example 2** for a chat-style debugging session, **Example 3** for a long-running feature branch agent, and **Example 4** when a user asks it to survey the entire codebase and produce an architecture report — all within the same product, routing to different context management strategies based on detected user intent.

---

### <img src="https://cdn-icons-png.flaticon.com/512/6675/6675847.png" width="80"> Limitations

---

Design Document Examples are invaluable references, but they carry specific risks if misused:

**1. Examples age quickly**
Context window sizes, model pricing, and tokenization behavior change with every model release. An example written for GPT-4 (8K context) may give entirely wrong intuitions for GPT-4o (128K context). Always check the model version referenced in any example you use as a template.

**2. Token estimates are environment-specific**
A "3,000-token system prompt" in one example may be 2,700 or 3,400 tokens in your environment depending on the tokenizer, the language (non-English languages often tokenize less efficiently), and whether you count special tokens. Never copy token budgets without re-measuring.

**3. Observability schemas are not standardized**
The logging structures shown in these examples are illustrative. Real systems use LangSmith, Weights & Biases, Datadog, or custom telemetry. The fields matter; the exact format will vary.

**4. Examples show the happy path**
The overflow strategies described are correct in design, but they simplify error handling. Real systems need to handle partial retrieval failures, Redis session store timeouts, model API errors mid-compression, and race conditions in multi-agent architectures. Examples sketch the architecture; they do not replace integration testing.

**5. One-size-fits-none**
No single example maps perfectly to any new use case. Treat these as starting points that require adaptation. The most dangerous thing an engineer can do is clone an example context budget without benchmarking it against their actual data distribution.

**6. Privacy and compliance are not covered here**
None of these examples address what happens when PII appears in conversation history, retrieved documents, or tool call results. In production systems, context management and data governance are inseparable — consult your compliance team before logging raw context windows.

**7. Parallel sub-agent patterns require API tier planning**
Example 4's parallel architecture assumes your API tier supports 10+ concurrent requests. Bursting beyond your rate limit causes sub-agent failures that cascade into incomplete orchestrator context. Always validate concurrency headroom before committing to parallel patterns in production.

---

### <img src="https://cdn-icons-png.flaticon.com/512/2112/2112889.png" width="80"> Video

A recommended video to visualize:

<div align="center">
  <a href="https://www.youtube.com/watch?v=KNH7hKB1rpA" target="_blank">
      <img width="640" height="360" src="https://i.ytimg.com/vi/KNH7hKB1rpA/maxresdefault.jpg"/>
  </a>
</div>

> **LangChain — Managing Memory in LLM Applications** *(Deep dive into history management, summarization strategies, and practical context window patterns — perfect complement to the examples in this module)*

---

<div align="center">

| ← Previous | Module | Next → |
|:---:|:---:|:---:|
| [05-4 Context Compression](./05-4-Context-Compression.md) | **05. Context Management** | [06 RAG Pipeline →](../06-RAG-Pipeline/) |

</div>
