# Part VI: Build Systems (Phases 43–48)

## Motto
> "A build system is a dependency-driven DAG evaluator. A hermetic build ensures that identical source inputs, built on any machine at any time, yield bit-for-bit identical outputs."

---

## Delivery Problem
A project compiles fine on an engineer's laptop running macOS with Homebrew packages in `/usr/local`. When the CI runner attempts to compile on an Ubuntu Linux container, the build crashes with `header file not found`.

Later, an engineer builds the service twice from the exact same Git commit. Build 1 has SHA `10313939...`, while Build 2 has SHA `5ebf656d...`. Because the hashes differ, caching engines cannot verify whether the binary was tampered with, and release managers cannot verify provenance!

---

## Prediction
1. Build tools like `make`, `bazel`, or `cargo` rely on DAG graphs to avoid redundant work.
2. Embedding timestamps, randomized archive order, or host paths makes builds non-reproducible.
3. Hermetic builds isolate the build environment from global host state.

---

## First Principles
1. **The Build Graph (Directed Acyclic Graph)**:
   A target $T$ depends on a set of inputs $I = \{i_1, i_2, \dots\}$ and dependencies $D = \{d_1, d_2, \dots\}$. The build engine calculates the fingerprint of all inputs:
   $$\text{Fingerprint}(T) = \text{Hash}(\text{Command} + \text{Inputs} + \sum \text{Fingerprint}(D))$$
   If the fingerprint has not changed since the last build, the target is up-to-date and execution is skipped.
2. **Hermeticity**:
   A build is hermetic if it depends **only** on explicitly declared inputs and tools. It does not read unpinned system libraries, user home directories, network resources, or system timezones.
3. **Reproducibility (Bit-for-Bit Identity)**:
   A build is reproducible if executing it multiple times on different hardware, operating systems, and dates produces the exact same cryptographic SHA-256 output.

---

## Manual Process
Run the build graph DAG engine and inspect incremental caching:

```bash
python3 build-labs/dag_builder.py
```

Run the reproducible build check:

```bash
python3 build-labs/reproducible_build_check.py
```

---

## Mental Model

```text
[ Inputs: app.py, schema.sql ]
              │
              ▼ Topological Sort
      ┌───────────────┐
      │ schema_parser │
      └───────┬───────┘
              │
              ▼
      ┌───────────────┐
      │  core_binary  │  ◄── Is input hash changed?
      └───────┬───────┘      NO  ──► [ CACHE HIT: Skip ]
              │              YES ──► [ RECOMPILE ]
              ▼
    [ distribution_bundle ]
```

---

## Automate It (Phase 48: Enforcing Reproducibility)

In scripts, set `SOURCE_DATE_EPOCH` to normalize timestamps, zero out user IDs, and normalize gzip compression:

```python
# build-labs/reproducible_build_check.py
with gzip.GzipFile(filename="", mode="wb", fileobj=compressed, mtime=epoch) as gz:
    gz.write(raw_tar.getvalue())
```

---

## Run It
Execute the reproducible build validator:

```bash
python3 build-labs/reproducible_build_check.py
```

Output:
```text
=== REPRODUCIBLE BUILD EXPERIMENT (Phase 48) ===
1. Testing Naive Builds:
  Build 1 SHA-256: 5de12521...
  Build 2 SHA-256: 3b2efd46...
  ✗ FAILURE: Artifacts are NON-REPRODUCIBLE! (Timestamps embedded in header)

2. Testing Hermetic Reproducible Builds (SOURCE_DATE_EPOCH enforced):
  Reproducible Build 1 SHA-256: 46ede60c...
  Reproducible Build 2 SHA-256: 46ede60c...
  ✓ SUCCESS: Bit-for-bit identical hashes achieved across separate builds!
```

---

## Break It (Phase 44: Breaking Incremental Caching)
1. In `build-labs/dag_builder.py`, modify an input file in Target `core_binary`.
2. Re-run `python3 build-labs/dag_builder.py`.
3. Observe how `schema_parser` is cached, while `core_binary` and dependent target `distribution_bundle` are invalidated and rebuilt!

---

## Debug It
When two builds produce different hashes:
1. Extract both archives to separate directories.
2. Compare file modification times (`stat -f "%m"`).
3. Check file order inside the tarball (`tar -tzf archive.tar.gz`).
4. Inspect embedded compiler flags and absolute file paths (`strings binary | grep /Users/`).

---

## Security
- Non-reproducible builds make it impossible to prove that a published binary was compiled from a specific open-source commit.
- An attacker with access to the build runner could inject backdoors without altering the source code. Reproducible builds allow independent auditors to verify the binary by rebuilding it from source.

---

## Optimize It
- Use distributed compilation caches (e.g. `ccache`, `sccache`, Bazel remote caching) so work completed by one developer or CI worker is shared with the entire team.

---

## Deployment Implication
If builds are reproducible, you can safely skip rebuilding artifacts when promoting from staging to production, guaranteeing that the exact tested binary moves forward.

---

## Recovery
If non-reproducibility is detected:
1. Identify the source of non-determinism (timestamps, random seeds, path leaks).
2. Set `SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)`.
3. Sort tar entries alphabetically and enforce fixed UIDs before packing.

---

## Practical Exercises (Part VI)
1. **Exercise 6.1**: Run `stat` on two compiled files and inspect the modification timestamp (`mtime`).
2. **Exercise 6.2**: Modify `build-labs/dag_builder.py` to support parallel execution of independent build targets using a Python `ThreadPoolExecutor`.
3. **Exercise 6.3**: Write a script that checks whether any compiled `.pyc` files contain absolute path references from the local workstation.
4. **Exercise 6.4**: Package a tarball using standard `tar -czf` and compare its SHA-256 hash when run 5 seconds apart. Explain the discrepancy.
5. **Exercise 6.5**: Create an automated test that asserts that `SOURCE_DATE_EPOCH` is respected across all packaging scripts in `scripts/`.
6. **Exercise 6.6**: Implement target cycle detection in `build-labs/dag_builder.py` using DFS coloring (White, Gray, Black).
7. **Exercise 6.7**: Compare the build speed of a clean build vs an incremental build on a project with 50 mock source files.
8. **Exercise 6.8**: Write a script that inspects container image layer creation dates and verifies that timestamps are normalized.

---

## Questions for Mastery
1. *Why does embedding the current build timestamp into a binary destroy build reproducibility?*
2. *How does `SOURCE_DATE_EPOCH` provide a standardized solution for reproducible archiving?*
3. *What is the relationship between build DAG topological sorting and parallel compilation?*

---

## What Comes Next
In **Part VII (Phases 49–54)**, we study Artifacts: build outputs, the "Build Once, Promote Many" principle, artifact identities, storage registries, retention lifecycles, and workflow diagnostic outputs.
