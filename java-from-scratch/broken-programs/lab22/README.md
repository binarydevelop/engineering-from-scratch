# Broken Lab 22: Blocking I/O Inside Common ForkJoinPool

> **Failure Type:** `CommonPoolStarvation`  
> **Symptom:** Parallel stream blocking all worker threads in the JVM common pool

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as parallel stream blocking all worker threads in the jvm common pool.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab22.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab22Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab22.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab22Test
```
