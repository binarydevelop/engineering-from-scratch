# Broken Lab 07: Thread Pool Exhaustion / Starvation

> **Failure Type:** `ThreadStarvation`  
> **Symptom:** Tasks blocking synchronously on tasks submitted to the same bounded pool

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as tasks blocking synchronously on tasks submitted to the same bounded pool.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab07.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab07Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab07.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab07Test
```
