# Broken Lab 18: Unclosed FileInputStream Leaking OS Handles

> **Failure Type:** `DescriptorLeak`  
> **Symptom:** Exhausting OS open file descriptors (EMFILE: Too many open files)

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as exhausting os open file descriptors (emfile: too many open files).
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab18.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab18Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab18.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab18Test
```
