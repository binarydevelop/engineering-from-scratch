# Broken Lab 14: Non-Atomic Compound Operation on volatile

> **Failure Type:** `LostUpdates`  
> **Symptom:** volatile int count; count++ still suffers from race conditions

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as volatile int count; count++ still suffers from race conditions.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab14.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab14Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab14.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab14Test
```
