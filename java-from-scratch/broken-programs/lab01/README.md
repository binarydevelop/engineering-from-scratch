# Broken Lab 01: Hidden NullPointerException in Chained Call

> **Failure Type:** `NullPointerException`  
> **Symptom:** Null pointer dereferenced during nested unboxing

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as null pointer dereferenced during nested unboxing.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab01.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab01Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab01.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab01Test
```
