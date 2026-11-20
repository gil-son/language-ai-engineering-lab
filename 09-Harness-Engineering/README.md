# 09. Harness Engineering

## <img src="https://cdn-icons-png.flaticon.com/512/8592/8592294.png" width="10%"/> Overview

A **test harness** is the machinery that **runs** LLM tests and evaluations reliably, repeatably, and automatically. If [Evaluation](https://github.com/gil-son/language-ai-engineering-lab/tree/main/08-Evaluation-and-Benchmarks) defines *what* to measure, **Harness Engineering** builds the scaffolding that *actually runs the tests*, captures every input and output, handles failures, and plugs the whole thing into CI/CD.

> **"How do I run, capture, and automate LLM tests so results are reliable and reproducible?"**

A harness turns evaluation from a manual, copy-paste ritual into an engineered pipeline: define cases once, run them on every change, and get a report and a pass/fail gate automatically.

| Aspect | Manual Prompting | Test Harness |
|--------|------------------|--------------|
| Execution | By hand, one at a time | Automated over a suite |
| Reproducibility | Low | High (fixtures, seeds, versions) |
| Failure handling | Ad-hoc | Retries, timeouts, mocks |
| Output capture | Screenshots / memory | Structured, logged, diffable |
| Integration | None | Runs in CI/CD on every change |

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7963/7963858.png" width="80"/> Introduction

Testing LLM systems is harder than testing ordinary code: outputs are **non-deterministic**, calls are **slow and costly**, and dependencies (model APIs, vector stores, tools) are **external and flaky**. A naive test suite is either unreliable (random failures) or impractically expensive.

Harness Engineering solves this with purpose-built scaffolding: deterministic fixtures, mocking of external calls, retry and timeout logic, structured capture of inputs and outputs, and evaluators that score the results. The harness is the bridge between a pile of test ideas and a trustworthy, automated quality gate.

> **Key mindset:** treat prompts and LLM behavior as software under test — with fixtures, snapshots, retries, and CI — not as something you eyeball.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/5557/5557844.png" width="80"/> Why use it?

- **Reproducibility** — same inputs, same conditions, comparable results
- **Automation** — run the full suite on every commit, not by hand
- **Reliability** — retries, timeouts, and mocks tame flaky external calls
- **Capture** — every input/output is logged for debugging and regression
- **Cost control** — caching and mocking cut redundant API spend
- **Confidence to ship** — a green suite in CI gates releases objectively

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/2299/2299623.png" width="80"/> Components

| Component | Role |
|-----------|------|
| **Test Runner / Scaffold** | Orchestrates test cases and collects results |
| **Input/Output Capture** | Records prompts, responses, and metadata for each run |
| **Fixtures & Seeds** | Fixed inputs and settings for reproducibility |
| **Mocking Layer** | Replaces live model/tool calls with recorded responses |
| **Retry & Timeout Logic** | Handles transient API failures gracefully |
| **Evaluators** | Apply metrics / LLM-judge to score captured outputs |
| **Snapshot / Golden Files** | Detect changes by diffing against saved outputs |
| **Reporting** | Human-readable results, pass/fail, trends |
| **CI/CD Integration** | Runs the suite automatically and enforces gates |

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/7527/7527144.png" width="80"/> How it works?

```mermaid
graph TD
    A[Define Test Cases + Fixtures] --> B[Harness Runs Cases]
    B --> C{Mock or Live call?}
    C -- Mock --> D[Recorded Response]
    C -- Live --> E[Model / Tool API + Retry/Timeout]
    D --> F[Capture Input/Output]
    E --> F
    F --> G[Evaluators Score Results]
    G --> H[Report + Pass/Fail Gate]
    H --> I[CI/CD: block or allow merge]
```

1. **Define** test cases with fixed inputs and expected behavior.
2. **Run** them through the harness, mocking external calls where determinism matters.
3. **Capture** every input, output, and metric (latency, tokens, cost).
4. **Evaluate** the captured outputs with metrics or an LLM judge.
5. **Report** results and compare against snapshots/thresholds.
6. **Gate** in CI/CD — fail the build if quality regresses.

---

### <td align="center"><img src="https://cdn-icons-png.flaticon.com/512/6404/6404564.png" width="80"/> Use Cases

- **Prompt regression testing** — detect when a prompt edit breaks behavior
- **Model upgrade validation** — re-run the suite before switching models
- **RAG pipeline testing** — mock retrieval to test generation deterministically
- **Agent/tool testing** — mock tool calls to test reasoning paths
- **CI quality gates** — block merges that drop below a threshold
- **Cost/latency guardrails** — fail builds that exceed budgets
- **Snapshot testing** — catch unexpected output changes via diffs

---

### <img src="https://cdn-icons-png.flaticon.com/512/6675/6675847.png" width="80"> Limitations

- **Non-determinism** — even with fixtures, live model outputs vary
- **Mock drift** — recorded responses go stale as real models change
- **Maintenance cost** — snapshots and fixtures need upkeep
- **Flaky externals** — retries help but cannot fully hide unreliable APIs
- **Cost of live runs** — full live suites can be expensive and slow
- **Coverage gaps** — a harness only tests the cases you thought to write

---

## <img src="https://cdn-icons-png.flaticon.com/512/18310/18310876.png" width="80"/> Topics Covered

```
09-Harness-Engineering/
├── Test scaffolding and runners
├── Input/output capture and logging
├── Mocking model and tool calls
├── Retry, timeout, and rate-limit handling
├── Snapshot / golden-file testing
├── Evaluator integration (metrics, LLM-judge)
└── CI/CD integration and quality gates
```

---

### <img src="https://cdn-icons-png.flaticon.com/512/2581/2581996.png" width="80"> Related

- **[08-Evaluation-and-Benchmarks](https://github.com/gil-son/language-ai-engineering-lab/tree/main/08-Evaluation-and-Benchmarks)** — defines the metrics the harness runs
- **[15-MLOps-and-Production](https://github.com/gil-son/language-ai-engineering-lab/tree/main/15-MLOps-and-Production)** — deploying and monitoring what the harness validates
