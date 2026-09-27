# Capstone 3: Mini Search Engine From Scratch

A complete, dependency-free information retrieval and search engine implemented in pure Python 3 standard library.

---

## 1. Core Architecture
* **Text Analysis:** Lowercase normalization, boundary tokenization, and stop-word filtering.
* **Positional Inverted Index:** Maps terms to document IDs and token offsets for adjacent phrase matching.
* **Columnar Doc Values:** Column-oriented disk storage emulation for $O(1)$ attribute filtering and sorting.
* **Probabilistic BM25 Scorer:** Exact implementation of Term Frequency saturation ($k_1=1.2$) and Field Length Normalization ($b=0.75$).
* **Boolean Compound Engine:** Supports `must`, `filter`, `should` (boosting), and `must_not` clauses.
* **Phrase Matcher:** Positional intersection with configurable `slop`.

---

## 2. Running Unit Tests

```bash
python3 projects/mini_search_engine/test_engine.py
```
