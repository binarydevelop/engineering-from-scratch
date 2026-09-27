# The Fine-Tuning & Model Adaptation Decision Framework

> **Motto:** Fine-tuning teaches form, style, and behavioral grammar. It is rarely the right solution for teaching facts or live private knowledge.

---

## 1. The Pre-Fine-Tuning Diagnostic Tree

Before spending GPU compute or curating training datasets, walk down this diagnostic tree:

```text
               What is the root cause of the current failure?
                                     │
      ┌──────────────────────────────┼──────────────────────────────┐
      │                              │                              │
      ▼                              ▼                              ▼
[Missing / Outdated Facts]   [Needs External Action]    [Ambiguous Instructions]
      │                              │                              │
      ▼                              ▼                              ▼
 DO NOT FINE-TUNE!              DO NOT FINE-TUNE!              DO NOT FINE-TUNE!
 Use Retrieval (RAG)           Equip Model with Tools         Fix Prompt & Workflow
 (Documents change daily;      (API calls, DB queries,        (Structured output,
  weights are frozen)           deterministic calculators)     few-shot examples)
                                     │
                                     ▼
                     [Systematic Behavioral Failure]
                     - Custom domain output grammar
                     - Unreliable tool-call syntax on small models
                     - Strict tone / stylistic alignment
                     - Latency reduction (distilling large prompt into weights)
                                     │
                                     ▼
                           PROCEED TO FINE-TUNING!
```

---

## 2. Capability Matrix: Prompting vs RAG vs Tools vs Fine-Tuning

| Capability Dimension | Prompting (Zero/Few-Shot) | Retrieval-Augmented Gen (RAG) | Function / Tool Calling | Parameter-Efficient Fine-Tuning (LoRA) |
| :--- | :--- | :--- | :--- | :--- |
| **New Private Knowledge** | ❌ Poor (Context limited) | ✅ Excellent (Dynamic indexing) | ❌ N/A | ⚠️ Risky (Prone to hallucinations) |
| **Fresh / Real-Time Data** | ❌ Impossible | ✅ Excellent | ✅ Live API calls | ❌ Static at training cutoff |
| **Stylistic Conformity** | ⚠️ Moderate (Burns tokens) | ❌ N/A | ❌ N/A | ✅ Unmatched & Token-free |
| **Strict Output Grammar** | ⚠️ Inconsistent on small models | ❌ N/A | ⚠️ Schema errors | ✅ Eliminates syntax errors |
| **Context Window Consumption** | ❌ High (Repeated examples) | ⚠️ Moderate (Chunks injected) | ⚠️ Schema overhead | ✅ Minimal (Behavior burned into weights) |
| **Engineering Maintenance** | 🟢 Minimal | 🟡 Index pipelines & chunking | 🟡 API contracts & auth | 🔴 Dataset curation & eval regressions |

---

## 3. Training Data Quality Checklist

Every fine-tuning dataset must satisfy these 6 criteria before launch:
1. **Zero Data Contamination:** Every evaluation benchmark query must be rigorously purged from training data.
2. **Deterministic Deduplication:** Exact string and MinHash deduplication to prevent model over-indexing on frequent prompts.
3. **Chat Template Consistency:** Verify formatting tokens (`<|im_start|>`, `<|start_header_id|>`) match the base model's exact tokenizer configuration.
4. **Length Distribution Check:** Ensure 95%+ of samples fall within your designated sequence length ceiling to prevent excessive truncation.
5. **Quality Review:** Randomly inspect 100 human-annotated rows manually. If 5% have errors, discard or clean the dataset.
6. **Task Representation Balance:** Ensure domain edge cases are proportionally represented, not dominated by easy repetitive rows.
