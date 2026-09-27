# Part III: Dependencies & Caching (Phases 18–23)

## Motto
> "A cache is an optimization, not a source of truth. If your cache key does not capture the exact hash of your dependency inputs, your build is non-deterministic."

---

## Delivery Problem
A pipeline takes 14 minutes to run. 11 of those minutes are spent repeatedly downloading and compiling Python/Node dependencies from the public internet. 

To "fix" this, an engineer adds caching with a static key: `key: my-deps`.
Three weeks later, an engineer updates a library to patch a zero-day security vulnerability. The pipeline passes, but the running application continues to use the vulnerable library because the static cache key restored the old packages! Worse, an untrusted PR writes a modified binary into the cache directory, poisoning all subsequent builds.

---

## Prediction
1. Downloading dependencies over the internet introduces network flakiness, upstream rate-limiting (`HTTP 429`), and massive feedback delays.
2. An imprecise cache key will restore stale or mismatched libraries when dependencies change.
3. Blindly restoring untrusted caches into privileged release runners allows remote code execution via cache poisoning.

---

## First Principles
1. **Lockfiles as Cryptographic Invariants**:
   A manifest (`requirements.txt`, `package.json`) declares intent (e.g. `requests>=2.28`). A lockfile (`poetry.lock`, `package-lock.json`) records the exact resolved versions and SHA-256 hashes of every direct and transitive library. Without a lockfile, builds are inherently non-reproducible.
2. **Cache Key Composition**:
   A cache key must uniquely identify the exact environment and dependency inputs:
   ```text
   Key = OS_Runner + Runtime_Version + Hash(Lockfile)
   ```
   If any character in the lockfile changes, the hash changes, automatically invalidating the old cache and creating a clean entry.
3. **Cache vs Artifact Distinction**:
   - A **Cache** is internal to the CI runner and can be dropped at any time without impacting correctness.
   - An **Artifact** is the immutable output of the build destined for production.

---

## Manual Process
Observe cache evaluation manually:

```bash
# 1. Compute hash of the lockfile
shasum -a 256 sample-apps/delivery-service/requirements.txt | awk '{print $1}'

# 2. Simulate cache lookup with local runner
python3 -c "
cache_store = {'mac-py3.12-a1b2c3d4': '/tmp/cache_hit'}
incoming_key = 'mac-py3.12-a1b2c3d4'
if incoming_key in cache_store:
    print('CACHE HIT: Restoring dependencies in 0.1s')
else:
    print('CACHE MISS: Downloading from PyPI in 18.2s')
"
```

---

## Mental Model

```text
[ Lockfile: requirements.lock ]
               │
               ▼ Compute Hash
     [ SHA-256: 7f9b8c31... ]
               │
               ▼ Construct Key
[ Cache Key: os-py3.12-7f9b8c31... ]
               │
       ┌───────┴───────┐
       ▼               ▼
 [ Cache HIT ]   [ Cache MISS ]
 (Fast Restore)  (Download & Populate Cache)
```

---

## Automate It (Phase 20, 21: GitHub Actions Cache)

```yaml
- name: Cache Python Dependencies
  uses: actions/cache@v4.0.2
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

---

## Inspect It
Run `python3 benchmarks/benchmark_pipeline.py` to inspect the performance benchmark comparing cold cache miss (18.5s) against warm cache hit (2.1s) — yielding an **8.8x speedup**.

---

## Break It (Phase 22: Stale Cache)
1. Execute broken lab `07-stale-cache-bad-key`:
   ```bash
   python3 broken-pipelines/07-stale-cache-bad-key/reproduce_failure.py
   ```
2. Observe how using a cache key that omits the lockfile hash returns stale packages.
3. Inspect `broken-pipelines/07-stale-cache-bad-key/solution/SOLUTION.md` for the fix.

---

## Debug It
When debugging cache issues:
- Verify whether the cache step printed `Cache hit` or `Cache miss`.
- Inspect the evaluated cache key string in the CI step log.
- If dependencies failed to update, compare the SHA-256 hash of the local lockfile against the hash in the CI log.

---

## Security (Phase 23: Cache Poisoning)
- Pull requests from external forks must **never** be permitted to write to base repository caches. GitHub Actions enforces this by making fork caches read-only with respect to the base branch.
- Never execute binaries directly out of an untrusted cache without hash verification.

---

## Optimize It
- Use multi-layer caching: cache both the package manager download directory (`~/.cache/pip`) and the compiled bytecode (`.venv`).
- Use fallback `restore-keys` to get partial cache hits on incremental branch updates.

---

## Deployment Implication
Deploying an artifact built with a poisoned or stale cache can result in deploying outdated or tampered libraries directly into production.

---

## Recovery
If a cache is corrupted or poisoned:
1. Immediately bump the cache key version prefix (e.g. `python-deps-v1` -> `python-deps-v2`).
2. Purge the repository cache using the GitHub API or CLI (`gh cache delete --all`).
3. Re-run the release pipeline from a clean slate.

---

## Practical Exercises (Part III)
1. **Exercise 3.1**: Write a Python script that reads a `requirements.txt` file and generates a canonical, sorted lockfile with exact package hashes.
2. **Exercise 3.2**: Benchmark the time taken to run `pip install` with a clean cache versus an existing local cache directory.
3. **Exercise 3.3**: Construct a cache key that incorporates three distinct inputs: runner OS, runtime minor version, and lockfile SHA-256.
4. **Exercise 3.4**: Write a reproduction script showing what happens when a dependency version is bumped in `requirements.txt` but the lockfile is not re-generated.
5. **Exercise 3.5**: Implement a cache validation step that computes checksums of all `.whl` files in the cache directory before unpacking them.
6. **Exercise 3.6**: Simulate a cache poisoning scenario where a malicious script modifies an installed file inside `.venv/lib/` and observe how tests fail or pass.
7. **Exercise 3.7**: Trace GitHub Actions cache scope rules: explain why a cache created on `feature-branch` cannot be accessed by `another-feature-branch`.
8. **Exercise 3.8**: Calculate the storage and network egress cost of caching 500MB container layers across 100 builds per day.

---

## Questions for Mastery
1. *Why should a dependency cache never be used as a production release artifact?*
2. *If an application uses dynamic version constraints like `fastapi>=0.95.0`, why is CI caching dangerous without a lockfile?*
3. *How does GitHub Actions isolate caches between pull request branches and the main branch?*

---

## What Comes Next
In **Part IV (Phases 24–35)**, we explore Testing in Pipelines: unit tests, integration tests, service containers, flaky test quarantine, test sharding, and API contract verification.
