# Broken Lab 21: Unbounded Stream Iteration Without Limit

> **Failure Type:** `HeapExhaustion`  
> **Symptom:** Intermediate stream pipeline without terminal short-circuit exhausts heap

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as intermediate stream pipeline without terminal short-circuit exhausts heap.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab21.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab21Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab21.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab21Test
```
