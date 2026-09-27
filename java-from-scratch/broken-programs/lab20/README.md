# Broken Lab 20: Financial Arithmetic Error with double

> **Failure Type:** `PrecisionLoss`  
> **Symptom:** 0.1 + 0.2 produces 0.30000000000000004 in account balance

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as 0.1 + 0.2 produces 0.30000000000000004 in account balance.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab20.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab20Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab20.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab20Test
```
