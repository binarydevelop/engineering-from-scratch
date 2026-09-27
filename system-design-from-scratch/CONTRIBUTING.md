# Contributing to System Design From Scratch

Thank you for your interest in contributing to **`system-design-from-scratch`**!
Our mission is to replace rote architecture memorization with rigorous first-principles engineering and empirical simulations.

---

## 1. Guiding Principles

1. **Pressure Before Architecture**: Never propose a component (cache, queue, sharding) without first proving what breaks without it.
2. **Every Box Must Be Justified**: Any diagram change must include the *Component Justification Rule* (Problem solved, evidence, alternative, new failure mode).
3. **Reproducibility**: All simulations and code must be runnable with standard Python 3.12+ and pass `pytest` with zero external vendor lock-in.
4. **Tradeoffs are Mandatory**: Every design change must document at least one architectural downside (cost, latency, complexity, staleness).

---

## 2. Development Workflow

1. Fork and clone the repository.
2. Set up the development environment:
   ```bash
   make setup
   make env-check
   ```
3. Run the full test suite:
   ```bash
   make test
   ```
4. If contributing a new phase or simulation:
   - Follow [`LESSON_TEMPLATE.md`](LESSON_TEMPLATE.md) for curriculum phases.
   - Follow [`DESIGN_TEMPLATE.md`](DESIGN_TEMPLATE.md) for system design problems.
   - Add unit tests verifying functional correctness and failure modes.

---

## 3. Pull Request Guidelines

- Ensure `make test` passes cleanly.
- Keep commits atomic and descriptive.
- Include empirical evidence (measurements, latency histograms) where applicable.
