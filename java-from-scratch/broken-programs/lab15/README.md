# Broken Lab 15: Wait Outside Loop and Solitary notify

> **Failure Type:** `LostWakeup`  
> **Symptom:** Thread wakes up on spurious wakeup or missed notify

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as thread wakes up on spurious wakeup or missed notify.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab15.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab15Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab15.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab15Test
```
