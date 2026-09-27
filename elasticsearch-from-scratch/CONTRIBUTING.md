# Contributing to `elasticsearch-from-scratch`

We welcome contributions that deepen the educational rigor, expand practical failure scenarios, or improve reproducibility across platforms.

---

## 1. Principles for Contributions

1. **First Principles First:** Every phase must begin with a pure Python or conceptual implementation before introducing the Elasticsearch REST API.
2. **Version Discipline:** All Elasticsearch examples and docker configurations must strictly target **Elasticsearch 8.17.0** (or compatible 8.x) as documented in `VERSIONS.md`. Never use deprecated APIs (e.g. `_type`, `mapping types`, legacy TF-IDF configs).
3. **Reproducibility:** Code and experiments must run reliably on macOS (Apple Silicon / Intel) and Linux. Memory limits should be bounded (`-Xms512m -Xmx512m` for lab nodes).
4. **No Magic:** Always show the full HTTP curl request or explicit Python client code. Avoid wrapping raw queries in excessive application boilerplate.
5. **Include Failure and Recovery:** Contributions adding new features should ideally include a "Break it" and "Recover it" section demonstrating how the feature fails in real clusters.

---

## 2. Directory Layout for New Lessons

When contributing a phase or lesson, adhere to the standard directory pattern:

```text
phases/<phase-num>-<phase-name>/
├── docs/
│   └── en.md                     # Lesson guide following LESSON_TEMPLATE.md
├── code/
│   └── <script_name>.py          # Standalone runnable implementation
├── experiments/
│   └── run_experiment.sh         # Reproducible shell test script
└── outputs/
    └── evidence-template.md      # Structured evidence log
```

---

## 3. Submitting a Pull Request

1. Fork the repository and create a descriptive feature branch (`feat/phase-xx-topic`).
2. Run `./scripts/check-environment.sh` and make sure your scripts execute cleanly.
3. Validate that markdown files conform to `LESSON_TEMPLATE.md`.
4. Ensure tests in `tests/` pass.
5. Submit your PR with a concise description of the mental model and experiment covered.
