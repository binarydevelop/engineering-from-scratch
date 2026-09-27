# Broken Lab 02: ConcurrentModificationException in Loop

> **Failure Type:** `ConcurrentModificationException`  
> **Symptom:** Modifying collection structure while iterating with fail-fast iterator

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as modifying collection structure while iterating with fail-fast iterator.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab02.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab02Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab02.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab02Test
```
