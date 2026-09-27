# Contributing to Data Engineering From Scratch

Thank you for contributing to **Data Engineering From Scratch**!

Our mission is to teach the fundamental principles of data systems through first-principles implementation, empirical measurement, deliberate failure injection, and architectural derivation.

---

## 1. Core Educational Principles

Before submitting any Pull Request, verify that your contribution obeys our three non-negotiable pedagogical rules:

1. **Problem First, Primitive Second, Tool Third**:
   - Never introduce an external tool (Airflow, Spark, dbt, Kafka, Iceberg) without first demonstrating the breakdown of a simpler manual primitive.
   - Ground every concept in concrete failure: out-of-memory errors, duplicate records, unindexed table scans, unhandled schema drift, or silent data corruption.

2. **The 12-Step Lifecycle**:
   - Every lesson and phase must implement:
     `Motto` -> `Problem` -> `Prediction` -> `First Principles` -> `Mental Model` -> `Build Simple Version` -> `Run It` -> `Inspect` -> `Validate` -> `Measure` -> `Break` -> `Recover` -> `Replay` -> `Evidence`.

3. **No Vendor Lock-In**:
   - Do not make proprietary cloud data warehouses (Snowflake, BigQuery, Redshift) or managed services the center of any lesson.
   - Use open standards: DuckDB, PostgreSQL, Apache Parquet, Apache Arrow, and pure Python.

---

## 2. Directory Layout for New Phases

When adding or expanding a phase, adhere to the standard directory layout:

```text
phases/XX-phase-name/
├── docs/
│   └── en.md                     # Comprehensive lesson guide following LESSON_TEMPLATE.md
├── code/
│   ├── main.py                   # Working, runnable Python implementation
│   └── validator.py              # Validation / quality assertion logic
├── sql/
│   ├── schema.sql                # Table definitions (DDL)
│   └── transform.sql             # SQL transformations
├── tests/
│   └── test_phase.py             # Pytest suite verifying execution & recovery
└── outputs/
    └── evidence-template.md      # Completed evidence log template
```

---

## 3. Code Standards & Tooling

- **Python**: Python 3.11+, strict type annotations where practical, PEP 8 styling, pure standard library or light dependencies (DuckDB, PyArrow, Pydantic).
- **SQL**: Standard ANSI SQL. Uppercase SQL keywords (`SELECT`, `FROM`, `WHERE`, `GROUP BY`), lowercase identifiers, explicit column aliases, and window functions formatted clearly.
- **Testing**: All code must include Pytest tests in `tests/test_phase.py`.
- **Failures Must Be Reversible**: Any script that injects a failure must provide a clean recovery mechanism that leaves the lab in a working state.

---

## 4. Submitting a Pull Request

1. Fork the repository and create your feature branch:
   ```bash
   git checkout -b feat/phase-enhancement
   ```
2. Run test suites and verify all checks pass:
   ```bash
   make check-env
   make test
   ```
3. Commit with semantic commit messages:
   ```bash
   git commit -m "feat(phase-46): add partition pruning benchmark and skew test"
   ```
4. Push to your branch and open a Pull Request against `main`.
