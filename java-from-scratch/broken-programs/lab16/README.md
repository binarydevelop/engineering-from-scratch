# Broken Lab 16: ThreadLocal Leak in Recycled Thread Pool

> **Failure Type:** `DataPollution`  
> **Symptom:** ThreadLocal state bleeds into subsequent tasks executing on the same thread

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as threadlocal state bleeds into subsequent tasks executing on the same thread.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab16.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab16Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab16.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab16Test
```
