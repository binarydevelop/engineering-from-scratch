# Broken Lab 04: Classic Two-Lock Deadlock

> **Failure Type:** `Deadlock`  
> **Symptom:** Circular lock acquisition between two threads acquiring locks in reverse order

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as circular lock acquisition between two threads acquiring locks in reverse order.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab04.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab04Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab04.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab04Test
```
