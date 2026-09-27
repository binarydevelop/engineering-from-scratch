# Broken Lab 11: equals Implemented Without hashCode

> **Failure Type:** `SetCorruption`  
> **Symptom:** Two equal objects map to different hash buckets in HashSet

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as two equal objects map to different hash buckets in hashset.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab11.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab11Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab11.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab11Test
```
