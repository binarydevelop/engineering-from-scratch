# Broken Lab 32: LazyInitializationException Outside Session

> **Failure Type:** `LazyInitializationException`  
> **Symptom:** Accessing uninitialized proxy after persistence session closes

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as accessing uninitialized proxy after persistence session closes.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab32.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab32Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab32.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab32Test
```
