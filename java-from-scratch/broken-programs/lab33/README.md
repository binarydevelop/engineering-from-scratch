# Broken Lab 33: Circular Dependency in Constructor Injection

> **Failure Type:** `StackOverflowError`  
> **Symptom:** Two services require each other in constructor, causing StackOverflowError

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as two services require each other in constructor, causing stackoverflowerror.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab33.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab33Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab33.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab33Test
```
