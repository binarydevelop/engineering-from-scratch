# Broken Lab 13: Infinite Loop Due to Lack of volatile

> **Failure Type:** `VisibilityFailure`  
> **Symptom:** Reader thread caches stale value of running flag in CPU registers

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as reader thread caches stale value of running flag in cpu registers.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab13.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab13Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab13.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab13Test
```
