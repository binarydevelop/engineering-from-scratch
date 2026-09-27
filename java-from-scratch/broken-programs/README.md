# 35 Realistic Broken-Java Debugging Labs

Master diagnostic engineering and root-cause analysis by examining real production failures, reproducing them deterministically, analyzing stack traces and thread dumps, and implementing verified fixes.

## Catalog of Broken Labs

| Lab ID | Name | Failure Mechanism | Root Cause / Diagnostic Tool |
| :--- | :--- | :--- | :--- |
| **Lab 01** | [Hidden NullPointerException in Chained Call](lab01/README.md) | `NullPointerException` | Null pointer dereferenced during nested unboxing |
| **Lab 02** | [ConcurrentModificationException in Loop](lab02/README.md) | `ConcurrentModificationException` | Modifying collection structure while iterating with fail-fast iterator |
| **Lab 03** | [NoClassDefFoundError After Clinit Failure](lab03/README.md) | `NoClassDefFoundError` | Static initializer throws exception, rendering class permanently uninitializable |
| **Lab 04** | [Classic Two-Lock Deadlock](lab04/README.md) | `Deadlock` | Circular lock acquisition between two threads acquiring locks in reverse order |
| **Lab 05** | [Unbounded Static Map Memory Leak](lab05/README.md) | `OutOfMemoryError` | Static collection retains object references, preventing GC reclamation |
| **Lab 06** | [GC Allocation Storm from String Concat](lab06/README.md) | `ExcessiveGC` | Repeated string concatenation in tight loop generates gigabytes of temporary garbage |
| **Lab 07** | [Thread Pool Exhaustion / Starvation](lab07/README.md) | `ThreadStarvation` | Tasks blocking synchronously on tasks submitted to the same bounded pool |
| **Lab 08** | [Leaked Database Connection](lab08/README.md) | `PoolExhaustion` | Unclosed Connection instances exhaust the pool |
| **Lab 09** | [Blocking Network I/O in <clinit>](lab09/README.md) | `ClassInitLockup` | Class loading hangs during static initialization |
| **Lab 10** | [Mutable Key Mutates After Put in HashMap](lab10/README.md) | `KeyLoss` | Mutating key field changes hashCode, making entry unfindable |
| **Lab 11** | [equals Implemented Without hashCode](lab11/README.md) | `SetCorruption` | Two equal objects map to different hash buckets in HashSet |
| **Lab 12** | [Race Condition on Non-Synchronized Shared Counter](lab12/README.md) | `LostUpdates` | Concurrent increments lose updates due to non-atomic read-modify-write |
| **Lab 13** | [Infinite Loop Due to Lack of volatile](lab13/README.md) | `VisibilityFailure` | Reader thread caches stale value of running flag in CPU registers |
| **Lab 14** | [Non-Atomic Compound Operation on volatile](lab14/README.md) | `LostUpdates` | volatile int count; count++ still suffers from race conditions |
| **Lab 15** | [Wait Outside Loop and Solitary notify](lab15/README.md) | `LostWakeup` | Thread wakes up on spurious wakeup or missed notify |
| **Lab 16** | [ThreadLocal Leak in Recycled Thread Pool](lab16/README.md) | `DataPollution` | ThreadLocal state bleeds into subsequent tasks executing on the same thread |
| **Lab 17** | [Escaping this Reference from Constructor](lab17/README.md) | `PartiallyInitialized` | Publishing this to another thread before constructor finishes establishing invariants |
| **Lab 18** | [Unclosed FileInputStream Leaking OS Handles](lab18/README.md) | `DescriptorLeak` | Exhausting OS open file descriptors (EMFILE: Too many open files) |
| **Lab 19** | [Character Encoding Corruption on Byte Conversions](lab19/README.md) | `EncodingMismatch` | String.getBytes() using default system encoding instead of UTF-8 |
| **Lab 20** | [Financial Arithmetic Error with double](lab20/README.md) | `PrecisionLoss` | 0.1 + 0.2 produces 0.30000000000000004 in account balance |
| **Lab 21** | [Unbounded Stream Iteration Without Limit](lab21/README.md) | `HeapExhaustion` | Intermediate stream pipeline without terminal short-circuit exhausts heap |
| **Lab 22** | [Blocking I/O Inside Common ForkJoinPool](lab22/README.md) | `CommonPoolStarvation` | Parallel stream blocking all worker threads in the JVM common pool |
| **Lab 23** | [Generics Heap Pollution via Raw Types](lab23/README.md) | `ClassCastException` | Assigning raw type to parameterized variable throws ClassCastException later |
| **Lab 24** | [ArrayStoreException via Covariant Array](lab24/README.md) | `ArrayStoreException` | Storing incompatible type into Object[] backing Integer[] |
| **Lab 25** | [Ternary Operator Hidden Unboxing NPE](lab25/README.md) | `NullPointerException` | Conditional expression unboxes null wrapper when second branch is primitive |
| **Lab 26** | [StringBuilder Repeated Resizing Overhead](lab26/README.md) | `LatencyDegradation` | Default initial capacity (16) forces continuous array reallocation |
| **Lab 27** | [Virtual Thread Pinned to Carrier in synchronized](lab27/README.md) | `CarrierPinning` | Blocking socket call inside synchronized prevents unmounting from carrier |
| **Lab 28** | [Swallowed Exception in CompletableFuture](lab28/README.md) | `SilentFailure` | Missing exceptionally() or handle() leaves failure silent |
| **Lab 29** | [SQL Injection via String Concatenation](lab29/README.md) | `SecurityBreach` | Malicious SQL injected into dynamic query statement |
| **Lab 30** | [Partial Multi-Statement Failure Without Transaction](lab30/README.md) | `DataInconsistency` | First update succeeds but second fails, corrupting ledger balance |
| **Lab 31** | [N+1 Database Query Avalanche](lab31/README.md) | `DatabaseOverload` | Iterating entities fires separate select query per child record |
| **Lab 32** | [LazyInitializationException Outside Session](lab32/README.md) | `LazyInitializationException` | Accessing uninitialized proxy after persistence session closes |
| **Lab 33** | [Circular Dependency in Constructor Injection](lab33/README.md) | `StackOverflowError` | Two services require each other in constructor, causing StackOverflowError |
| **Lab 34** | [Socket Read Hanging Indefinitely Without Timeout](lab34/README.md) | `SocketHang` | Client blocks on socket read forever when server socket does not close |
| **Lab 35** | [StackOverflowError from Unbounded Recursion](lab35/README.md) | `StackOverflowError` | Method recursive call without base case exhausts 1MB thread stack |
