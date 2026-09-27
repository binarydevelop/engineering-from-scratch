# Part VIII — Model Evaluation Rigor (Phases 112 – 120)

> **Motto:** No evaluation = No reliable claim of improvement. "It feels better" is disqualified as engineering evidence.

---

## Phases 112 – 116: Deterministic & Model-Based Evaluators
- **Phase 112 — Evaluation Before Optimization:** Establishing the baseline contract before touching a single line of model code.
- **Phase 113 — Deterministic Evaluations:** Exact match, normalized token F1, JSON schema validation, unit test runners (`evaluation/deterministic_evals.py`).
- **Phase 114 — Semantic Evaluations:** Embedding similarity, BERTScore, and reference-guided grading.
- **Phase 115 — LLM-as-Judge & Bias Mitigation:** Building an LLM judge; measuring and neutralizing position and verbosity biases (`evaluation/llm_as_judge.py`).
- **Phase 116 — Human Evaluation & Rubrics:** Designing annotation rubrics, computing inter-annotator agreement (Cohen's Kappa).

---

## Phases 117 – 120: Gating, Slices & Statistical Power
- **Phase 117 — Pairwise Blind Evaluation:** Blinded, randomized pairwise comparisons with confidence intervals.
- **Phase 118 — Regression Test Suite:** Automated gating suite preventing regressions across critical business tasks (`evaluation/regression_suite.py`).
- **Phase 119 — Slice Evaluation:** Dissecting performance across input length, domain categories, and edge cases (`evaluation/slice_evaluator.py`).
- **Phase 120 — Statistical Significance:** Calculating Wilson score intervals, p-values, and statistical power for AI evals (`evaluation/statistical_significance.py`).
