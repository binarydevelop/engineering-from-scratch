# Broken Lab 09: Blocking Network I/O in <clinit>

> **Failure Type:** `ClassInitLockup`  
> **Symptom:** Class loading hangs during static initialization

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as class loading hangs during static initialization.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab09.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab09Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab09.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab09Test
```
