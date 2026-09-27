# Broken Lab 25: Ternary Operator Hidden Unboxing NPE

> **Failure Type:** `NullPointerException`  
> **Symptom:** Conditional expression unboxes null wrapper when second branch is primitive

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as conditional expression unboxes null wrapper when second branch is primitive.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab25.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab25Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab25.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab25Test
```
