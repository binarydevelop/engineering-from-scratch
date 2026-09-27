# Contributing to java-from-scratch

Thank you for your interest in contributing to `java-from-scratch`! This project is an open-source, first-principles curriculum designed to teach Java and JVM internals with complete engineering depth.

---

## 1. Core Philosophy

Every contribution (lesson, lab, exercise, benchmark, or project) must uphold the motto:

> **Understand it. Compile it. Run it. Inspect it. Break it. Debug it. Measure it. Ship it.**

Contributions that merely list syntax, provide copy-paste solutions without mental models, or use framework magic without demystifying the core Java layer will be rejected.

---

## 2. Contribution Standards

1. **Version Discipline**:
   * Target **Java 21 LTS** syntax and APIs.
   * Do not use legacy patterns (e.g., `Vector`, `Hashtable`, `java.util.Date`, `Thread.stop()`, raw `HttpURLConnection`).
   * Clearly state whether an observed effect is a JLS requirement, a JVMS specification rule, or a HotSpot implementation artifact.
2. **Template Compliance**:
   * Any new or modified lesson must strictly adhere to [`LESSON_TEMPLATE.md`](LESSON_TEMPLATE.md).
   * All sections (Problem, Prediction, Mental Model, Implement, Inspect, Break, Debug, Measure, Evidence, Mastery Questions) must be populated.
3. **Reproducibility**:
   * Code must compile cleanly with `javac --release 21` with zero warnings under `-Xlint:all`.
   * Unit tests must execute under JUnit 5 (`mvn test`).
   * Reproduction steps for broken programs must be deterministic.
4. **Code Quality**:
   * Clean, standard Java conventions.
   * Explicit imports (no wildcard imports like `import java.util.*;`).
   * Descriptive identifiers that reinforce domain and JVM concepts.

---

## 3. Pull Request Process

1. Fork the repository and create your branch from `main`:
   ```bash
   git checkout -b feature/phase-xx-enhancement
   ```
2. Run the environment check and full verification suite:
   ```bash
   ./scripts/check-environment.sh
   ./scripts/build-all.sh
   ./scripts/run-tests.sh
   ```
3. Commit with concise, descriptive commit messages adhering to Conventional Commits:
   * `feat(phase-39): add collision chaining benchmark to hashmap lab`
   * `fix(broken-programs): correct reproduction timeout in lab 04 deadlock`
   * `docs(jvm-guide): clarify C2 scalar replacement vs true stack allocation`
4. Submit a Pull Request clearly stating the problem addressed and attaching the evidence log from `./outputs/`.
