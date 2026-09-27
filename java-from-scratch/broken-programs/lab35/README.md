# Broken Lab 35: StackOverflowError from Unbounded Recursion

> **Failure Type:** `StackOverflowError`  
> **Symptom:** Method recursive call without base case exhausts 1MB thread stack

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as method recursive call without base case exhausts 1mb thread stack.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab35.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab35Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab35.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab35Test
```
