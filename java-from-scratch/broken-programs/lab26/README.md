# Broken Lab 26: StringBuilder Repeated Resizing Overhead

> **Failure Type:** `LatencyDegradation`  
> **Symptom:** Default initial capacity (16) forces continuous array reallocation

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as default initial capacity (16) forces continuous array reallocation.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab26.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab26Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab26.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab26Test
```
