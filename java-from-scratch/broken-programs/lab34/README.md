# Broken Lab 34: Socket Read Hanging Indefinitely Without Timeout

> **Failure Type:** `SocketHang`  
> **Symptom:** Client blocks on socket read forever when server socket does not close

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as client blocks on socket read forever when server socket does not close.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab34.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab34Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab34.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab34Test
```
