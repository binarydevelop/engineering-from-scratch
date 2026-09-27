# Broken Lab 23: Generics Heap Pollution via Raw Types

> **Failure Type:** `ClassCastException`  
> **Symptom:** Assigning raw type to parameterized variable throws ClassCastException later

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as assigning raw type to parameterized variable throws classcastexception later.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab23.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab23Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab23.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab23Test
```
