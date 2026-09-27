# Broken Lab 12: Race Condition on Non-Synchronized Shared Counter

> **Failure Type:** `LostUpdates`  
> **Symptom:** Concurrent increments lose updates due to non-atomic read-modify-write

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as concurrent increments lose updates due to non-atomic read-modify-write.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab12.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab12Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab12.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab12Test
```
