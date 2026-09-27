# Contributing to Low-Level Design from Scratch

Thank you for helping build the premier open-source repository for mastering object-oriented design and low-level software architecture.

---

## Pedagogical Principles for Contributions

Before contributing code, exercises, or lessons, ensure you align with our core teaching principles:

1. **Behavior First, Never Diagram First:** We never present class diagrams before walking through use cases and dynamic responsibilities.
2. **Pain-Driven Patterns:** Never introduce a design pattern (Strategy, State, Observer, etc.) upfront. Always start with a simpler naive implementation, introduce a new requirement, show the pain/design smell, and then refactor to the pattern.
3. **No Framework Magic:** Core domain lessons must run on pure Java (or Python for companion lessons) with standard JUnit 5. Do not introduce Spring, Hibernate, or runtime reflection injection in foundational phases.
4. **Tested Invariants:** Every code artifact must include automated unit tests testing both the happy path and invalid state transitions.
5. **No Vague Classes:** Classes named `*Manager`, `*Helper`, `*Utils`, `*Handler` are strictly forbidden unless accompanied by rigorous architectural justification.

---

## Lesson Structure Standard

Every new lesson must follow `LESSON_TEMPLATE.md` and reside in:

```text
phases/<phase-number>-<phase-name>/
├── docs/
│   └── en.md
├── src/
│   └── main/java/lld/...
├── tests/
│   └── test/java/lld/...
└── outputs/
    └── evidence-template.md
```

---

## Running Checks Locally

Before opening a pull request, run the complete suite:

```bash
# Verify compilation and all automated unit tests
mvn clean test
```

Ensure all tests pass and there are no compilation warnings.
