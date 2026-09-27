# Broken Lab 30: Partial Multi-Statement Failure Without Transaction

> **Failure Type:** `DataInconsistency`  
> **Symptom:** First update succeeds but second fails, corrupting ledger balance

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as first update succeeds but second fails, corrupting ledger balance.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab30.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab30Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab30.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab30Test
```
