# Part IV: Testing in Pipelines (Phases 24–35)

## Motto
> "A test suite in CI is a risk-mitigation portfolio. Optimize for feedback speed, failure isolation, and deterministic confidence — never retry blindly to mask flakiness."

---

## Delivery Problem
A test suite takes 55 minutes to execute. 40 minutes of that time is spent running end-to-end Selenium browser tests that intermittently fail because of animation timing glitches. Developers re-run the pipeline 3 to 5 times until it turns green by chance ("retry until green").

Because CI feedback is agonizingly slow, developers stop running tests locally and batch massive changes together. When a real regression hits production, everyone assumes it was just another flaky test!

---

## Prediction
1. Ordering fast unit tests before heavy integration tests provides failure feedback in seconds rather than an hour.
2. Sharing database fixtures across parallel test workers causes intermittent collision errors.
3. Blindly retrying failing tests hides concurrency deadlocks and race conditions.

---

## First Principles
1. **The Test Portfolio (Speed vs. Confidence vs. Cost)**:
   - **Unit Tests**: In-memory, zero I/O, runs in milliseconds. High volume, catches logic bugs.
   - **Integration Tests**: Tests interaction with real databases, caches, or filesystems.
   - **Contract Tests**: Validates that API schemas and payload shapes match consumer expectations without spinning up full downstream systems.
   - **End-to-End (E2E) Tests**: Full system traversal. Slowest, most expensive, highest maintenance cost.
2. **Deterministic Test Isolation**:
   Every test must be an independent, self-contained unit. If Test B depends on rows inserted by Test A, parallelization will cause non-deterministic failures.
3. **Flakiness Root Causes**:
   Tests do not fail "randomly." Flakiness is always caused by:
   - Unsynchronized asynchronous operations (`time.sleep` instead of condition polling).
   - Shared mutable state (shared database rows, global singletons).
   - Order-dependent execution (tests pass in A-Z order, fail in Z-A order).
   - Environmental dependencies (timezones, system locales, network latency).

---

## Manual Process (Phases 24, 25, 33, 95)
Run each test suite tier independently:

```bash
# Tier 1: Unit Tests (< 0.1s)
python3 sample-apps/delivery-service/tests/unit/test_orders.py

# Tier 2: Integration Tests (~ 0.5s)
python3 sample-apps/delivery-service/tests/integration/test_db.py

# Tier 3: Contract Tests (< 0.1s)
python3 sample-apps/delivery-service/tests/contract/test_api_contract.py

# Tier 4: Post-Deployment Smoke Tests (~ 1s)
python3 sample-apps/delivery-service/tests/smoke/test_smoke.py
```

---

## Mental Model

```text
       ▲
      / \        End-to-End Tests   (Slow, High Cost, Broad Confidence)
     /   \       Contract Tests      (Boundary Compatibility)
    /     \      Integration Tests   (Real Database & Schema Validation)
   /───────\     Unit Tests          (Sub-second, Isolated Logic, Fast Feedback)
```

---

## Automate It (Phase 30: Test Sharding)

When test suites grow to thousands of cases, split the execution across parallel runner workers:

```yaml
jobs:
  test-shards:
    runs-on: ubuntu-24.04
    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - uses: actions/checkout@v4.1.7
      - run: pytest --shard-id=${{ matrix.shard }} --num-shards=4
```

---

## Run It
Run all test suites using the automated script:

```bash
bash scripts/test.sh
```

---

## Break It (Phase 28: Flaky Tests)
1. Run broken lab `04-flaky-test-race-condition`:
   ```bash
   python3 broken-pipelines/04-flaky-test-race-condition/reproduce_failure.py
   ```
2. Run broken lab `05-test-isolation-shared-database-leak`:
   ```bash
   python3 broken-pipelines/05-test-isolation-shared-database-leak/reproduce_failure.py
   ```
3. Observe how shared database state breaks parallel execution.

---

## Debug It
When a test fails intermittently:
1. Run the test 100 times in a tight loop to measure the failure probability:
   ```bash
   for i in {1..20}; do python3 sample-apps/delivery-service/tests/unit/test_orders.py || break; done
   ```
2. Randomize test execution order to detect state leakage from preceding tests.
3. Quarantine the flaky test immediately; do not let it block the main PR pipeline.

---

## Security
- Tests must never access production database endpoints.
- Integration tests must use ephemeral credentials generated dynamically for the test runner.

---

## Optimize It
- Run Unit Tests on PR push. Run heavy E2E suites only on merge to `main` or nightly.
- Implement test sharding to scale linearly with worker count (Phase 30).

---

## Deployment Implication
A passing test suite verifies known invariants. It does not replace post-deployment smoke tests or live canary health monitoring in production.

---

## Recovery
If a broken release passes tests and reaches staging:
- Write a failing unit or integration test reproducing the exact customer bug.
- Verify that the test fails on current code, then apply the fix and verify it turns green.

---

## Practical Exercises (Part IV)
1. **Exercise 4.1**: Implement a custom test runner that executes test methods in randomized order to detect state leakage.
2. **Exercise 4.2**: Write a condition-polling helper (`wait_until(condition, timeout)`) that replaces arbitrary `time.sleep()` calls.
3. **Exercise 4.3**: Configure an ephemeral SQLite database for each parallel test worker using `tempfile.NamedTemporaryFile`.
4. **Exercise 4.4**: Write an API contract test verifying that the `/version` response schema contains all required fields.
5. **Exercise 4.5**: Measure the runtime difference between running tests with an in-memory SQLite database (`:memory:`) vs a disk-based SQLite file.
6. **Exercise 4.6**: Build a flaky test detector that runs a specific test 50 times and calculates the flake rate percentage.
7. **Exercise 4.7**: Implement test sharding logic that splits a list of 20 test files evenly across 4 worker processes based on file index modulo.
8. **Exercise 4.8**: Write a script that parses JUnit XML test output and prints the 5 slowest tests in the suite.

---

## Questions for Mastery
1. *Why is 'retry until green' considered one of the most hazardous anti-patterns in CI/CD?*
2. *How do contract tests allow microservices to verify API compatibility without deploying all services into an integrated test environment?*
3. *What is the difference between test code coverage and test quality?*

---

## What Comes Next
In **Part V (Phases 36–42)**, we study Static Verification: automated formatting, linting, type checking, dependency vulnerability scanning, secret scanning, and manifest validation.
