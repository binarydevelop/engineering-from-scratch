# Broken Lab 10: Mutable Key Mutates After Put in HashMap

> **Failure Type:** `KeyLoss`  
> **Symptom:** Mutating key field changes hashCode, making entry unfindable

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as mutating key field changes hashcode, making entry unfindable.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab10.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab10Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab10.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab10Test
```
