# The Complete AI Evaluation Engineering Guide

---

## 1. Metric Taxonomy

| Metric Category | Target Property | Measurement Method | Primary Vulnerability / Flaw |
| :--- | :--- | :--- | :--- |
| **Deterministic** | Exact token string, JSON schema, Python syntax | Regex, JSON parser, AST compiler, unit test | Misses semantically valid paraphrasing |
| **Lexical Overlap** | Surface-level word similarity | ROUGE-L, BLEU, METEOR | High scores on gibberish with matching n-grams |
| **Embedding Similarity** | Semantic closeness in vector space | Cosine distance of dense vectors | Insensitive to negated truth or inverted logic |
| **Model-Based Judge** | Nuanced reasoning & quality adherence | Structured LLM prompt with rubric | Position bias, verbosity bias, self-enhancement |
| **Human Annotator** | Ground truth preference & domain validity | Double-blind human review | High cost, slow turnaround, annotator variance |

---

## 2. Gating and Regression Matrix

```text
Every Candidate Checkpoint / Agent Release Must Pass:
┌────────────────────────────────────────────────────────┐
│ 1. Zero regression on Critical Safety & Policy slice   │
│ 2. >= 90% validity on Deterministic JSON schema slice  │
│ 3. Statistically significant gain on Core Task eval    │
│    (p < 0.05, 95% CI completely above baseline)       │
│ 4. No more than 5% regression on general eval slice   │
│ 5. Latency p95 within agreed SLA (e.g., TTFT <= 50ms)  │
│ 6. Cost per request strictly below budget cap ($0.01)  │
└────────────────────────────────────────────────────────┘
```
