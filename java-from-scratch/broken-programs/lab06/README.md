# Broken Lab 06: GC Allocation Storm from String Concat

> **Failure Type:** `ExcessiveGC`  
> **Symptom:** Repeated string concatenation in tight loop generates gigabytes of temporary garbage

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as repeated string concatenation in tight loop generates gigabytes of temporary garbage.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab06.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab06Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab06.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab06Test
```
