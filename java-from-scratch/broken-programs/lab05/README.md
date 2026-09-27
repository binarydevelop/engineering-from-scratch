# Broken Lab 05: Unbounded Static Map Memory Leak

> **Failure Type:** `OutOfMemoryError`  
> **Symptom:** Static collection retains object references, preventing GC reclamation

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as static collection retains object references, preventing gc reclamation.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab05.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab05Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab05.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab05Test
```
