# Contributing to kafka-from-scratch

Thank you for your interest in improving `kafka-from-scratch`!

---

## 1. Pedagogical Standards

Every contribution—whether a new experiment, bug fix, or lesson refinement—must uphold the core philosophy:

* **First Principles First:** Explain *why* a mechanism exists before introducing Kafka syntax. Build a minimal Python prototype before showing the Kafka API.
* **No "Magic":** Avoid hand-waving abstractions. Unpack how bytes are framed on the wire and written to disk segments.
* **Failure-Oriented:** Every major concept must include an experiment that breaks the system (e.g. killing a broker, stalling a consumer, corrupting records) followed by diagnosis and recovery.
* **Evidence-Producing:** Provide clear steps to measure throughput, latency, lag, and disk usage.
* **Version Discipline:** All Kafka commands and configurations must strictly adhere to the pinned version in `VERSIONS.md` (Apache Kafka 3.8.0, KRaft mode, No ZooKeeper).

---

## 2. Directory Structure Conventions

When adding or updating phases:

```text
phases/<phase-name>/
├── docs/
│   └── en.md                      # Follows LESSON_TEMPLATE.md strictly
├── code/
│   └── <runnable_code>.py         # Clear, self-contained Python scripts
├── experiments/
│   └── run_experiment.sh          # Executable shell script running the lab
└── outputs/
    └── evidence-template.md       # Custom evidence capture template
```

---

## 3. Submitting Pull Requests

1. Verify environment preflight:
   ```bash
   make env-check
   ```
2. Run the test suite:
   ```bash
   make test
   ```
3. Ensure no trailing whitespace, clean markdown formatting, and clear ASCII diagrams.
