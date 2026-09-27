# Broken Lab 24: ArrayStoreException via Covariant Array

> **Failure Type:** `ArrayStoreException`  
> **Symptom:** Storing incompatible type into Object[] backing Integer[]

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as storing incompatible type into object[] backing integer[].
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab24.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab24Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab24.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab24Test
```
