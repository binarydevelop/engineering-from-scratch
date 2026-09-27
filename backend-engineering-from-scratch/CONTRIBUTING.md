# Contributing to Backend Engineering From Scratch

We welcome contributions that deepen understanding, improve mechanical clarity, strengthen failure scenarios, and maintain the first-principles philosophy of this curriculum.

---

## 1. Principles of Contribution

1. **First Principles First**: Do not submit PRs that simply add framework boilerplate or hide underlying protocols behind third-party packages. Every lesson must derive its abstraction from concrete requirements and fundamental mechanisms.
2. **Follow the Complete Lesson Structure**: Any new lesson or revision must strictly adhere to [LESSON_TEMPLATE.md](LESSON_TEMPLATE.md). Do not skip sections such as *First Principles*, *Break it*, *Debug it*, *Measure it*, or *Production Implications*.
3. **Runnable and Tested**: All code examples and tests must run cleanly on modern Python (>= 3.12) using standard libraries or the pinned dependencies in [requirements.txt](requirements.txt).
4. **Empirical Evidence**: Claims of performance or reliability must be accompanied by reproducible benchmarks or failure injection tests.
5. **Clear Separation of Vulnerable Code**: If adding a security lab, clearly isolate and label the vulnerability inside `broken-systems/` and provide both the broken and fixed code.

---

## 2. Development Workflow

1. Fork and clone the repository.
2. Set up the development environment:
   ```bash
   make setup
   make env-check
   ```
3. Run the existing test suite:
   ```bash
   make test
   ```
4. Create a dedicated branch for your topic or phase:
   ```bash
   git checkout -b feature/phase-xx-topic
   ```
5. Ensure your code passes all tests and conforms to the repository style.
6. Submit a pull request detailing:
   - The concept explained or failure injected
   - The verified test commands and output
   - The production relevance of the topic
