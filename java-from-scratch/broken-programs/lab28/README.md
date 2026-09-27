# Broken Lab 28: Swallowed Exception in CompletableFuture

> **Failure Type:** `SilentFailure`  
> **Symptom:** Missing exceptionally() or handle() leaves failure silent

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as missing exceptionally() or handle() leaves failure silent.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab28.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab28Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab28.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab28Test
```
