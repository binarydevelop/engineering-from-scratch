# Java and JVM Debugging Playbook

A systematic guide to diagnosing crashes, exceptions, deadlocks, memory leaks, and silent failures in Java applications.

---

## 1. The Scientific Debugging Loop

```text
 ┌─────────────────┐
 │ Observe Symptom │  Exception log, 100% CPU, stuck request, OutOfMemoryError
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │Deterministic Rep│  Write a minimal test case reproducing the failure.
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │ Inspect Runtime │  Thread dump (jstack), Heap histogram, Bytecode (javap), GC logs
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │ Form Hypothesis │  Connect symptoms to specific JLS, JVMS, or OS rules.
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │ Verify with Test│  Run test before and after fix; verify failure disappears.
 └─────────────────┘
```

---

## 2. Inspecting Live JVM Processes with `jcmd`

The `jcmd` utility (included with all JDK distributions) sends diagnostic commands directly to a running JVM process.

```bash
# List all running Java processes
jcmd -l

# Print complete thread stack dump (detects Java-level deadlocks automatically!)
jcmd <PID> Thread.print

# Generate class histogram to spot memory leaks (shows instance counts and bytes)
jcmd <PID> GC.class_histogram

# Trigger an immediate on-demand heap dump
jcmd <PID> GC.heap_dump /tmp/heap_dump.hprof

# Print all active JVM flags
jcmd <PID> VM.flags -all

# Check native memory tracking (if enabled with -XX:NativeMemoryTracking=summary)
jcmd <PID> VM.native_memory summary
```

---

## 3. Dissecting Java Stack Traces

Always read stack traces from the **bottom-most "Caused by:"** clause upward to find the primary root cause.

```text
Exception in thread "main" java.lang.RuntimeException: Failed to process order
    at io.github.javafromscratch.OrderService.process(OrderService.java:42)
    at io.github.javafromscratch.Main.main(Main.java:15)
Caused by: java.sql.SQLException: Connection refused
    at org.postgresql.core.v3.ConnectionFactoryImpl.openConnection(ConnectionFactoryImpl.java:230)
    ... 12 more
Caused by: java.net.ConnectException: Connection refused (Connection refused)
    at java.base/sun.nio.ch.Net.pollConnect(Native Method)
    at java.base/sun.nio.ch.Net.pollConnectNow(Net.java:318)
    ... 18 more
```
* **Top Layer**: High-level application abstraction failure (`OrderService`).
* **Middle Layer**: Library/driver translation (`SQLException`).
* **Root Cause**: Operating system socket error (`ConnectException: Connection refused`) occurring at line 318 in `Net.java`.

---

## 4. Diagnosing Deadlocks with Thread Dumps

When threads hang indefinitely, generate a thread dump. Modern HotSpot automatically prints deadlock analysis at the bottom of `Thread.print`:

```text
Found one Java-level deadlock:
=============================
"Worker-1":
  waiting to lock monitor 0x00006000028a1100 (object 0x000000070fed4320, a java.lang.Object),
  which is held by "Worker-2"

"Worker-2":
  waiting to lock monitor 0x00006000028a1200 (object 0x000000070fed4310, a java.lang.Object),
  which is held by "Worker-1"

Java stack information for the threads listed above:
===================================================
"Worker-1":
    at io.github.javafromscratch.DeadlockDemo.lambda$0(DeadlockDemo.java:22)
    - waiting to lock <0x000000070fed4320> (a java.lang.Object)
    - locked <0x000000070fed4310> (a java.lang.Object)
"Worker-2":
    at io.github.javafromscratch.DeadlockDemo.lambda$1(DeadlockDemo.java:33)
    - waiting to lock <0x000000070fed4310> (a java.lang.Object)
    - locked <0x000000070fed4320> (a java.lang.Object)
```
* **Solution**: Enforce a global **lock ordering discipline** (always acquire Lock A before Lock B across all code paths) or use `lock.tryLock(timeout)` with backoff.

---

## 5. Critical Exception Diagnoses

### A. `ClassNotFoundException` vs. `NoClassDefFoundError`
* **`ClassNotFoundException`** (Checked Exception): Occurs at runtime when an application attempts to dynamically load a class via string name (e.g., `Class.forName("org.example.MyClass")`) and the `.class` file cannot be located on the classpath.
* **`NoClassDefFoundError`** (Unchecked Error): Occurs when the class was present at compile time (the compiler successfully verified references), but is missing at runtime, OR when a static initializer (`<clinit>`) failed during initialization, rendering the class permanently unusable.

### B. `ConcurrentModificationException`
* Occurs when a collection (e.g., `ArrayList`, `HashMap`) detects structural modification (elements added or removed) while an active iterator is traversing it without using the iterator's own `remove()` method.
* **Mechanism**: Every modification increments an internal `modCount` counter. The iterator verifies `expectedModCount == modCount` on every call to `next()`.

### C. `OutOfMemoryError: Java heap space` vs. `Metaspace`
* **Heap Space**: The application created more live objects on the heap than `-Xmx` allows, or leaked references in a static collection or thread pool queue.
* **Metaspace**: The JVM generated or loaded too many dynamic classes (e.g., unbounded CGLIB proxy generation, classloader leaks in hot-reloading containers).
