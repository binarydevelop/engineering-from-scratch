# Broken Lab 27: Virtual Thread Pinned to Carrier in synchronized

> **Failure Type:** `CarrierPinning`  
> **Symptom:** Blocking socket call inside synchronized prevents unmounting from carrier

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as blocking socket call inside synchronized prevents unmounting from carrier.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab27.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab27Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab27.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab27Test
```
