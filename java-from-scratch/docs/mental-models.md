# Core Java and JVM Mental Models

> "Java is a statically typed programming language executed by the JVM, with strong runtime services for memory management, concurrency, dynamic optimization, and portability."

This guide establishes the foundational mental models required to reason accurately about Java systems under execution.

---

## 1. The Grand Execution Pipeline

When you execute a Java application, your code transitions through distinct representations across physical and virtual layers:

```text
 ┌───────────────┐
 │   Main.java   │   Human-readable source text
 └───────┬───────┘
         │
         ▼  (javac compiler: lexical analysis, parsing, semantic attribution, desugaring)
 ┌───────────────┐
 │  Main.class   │   Classfile: Constant pool, field/method descriptors, bytecode opcodes
 └───────┬───────┘
         │
         ▼  (ClassLoader: Loading, Linking [Verification, Preparation, Resolution], Initialization)
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │                            JVM Runtime Engine                               │
 │                                                                             │
 │  ┌────────────────┐     invoke     ┌────────────────────────┐               │
 │  │ Bytecode Interp│ ─────────────► │ C1 / C2 JIT Compilers  │               │
 │  │  (Stack Loop)  │ ◄───────────── │ (Inlining, Escape Anal)│               │
 │  └───────┬────────┘    deoptimize  └───────────┬────────────┘               │
 │          │                                     │                            │
 │          ▼                                     ▼                            │
 │  ┌──────────────────────────────────────────────────────────┐               │
 │  │                 Native Machine Code (CPU)                │               │
 │  └─────────────────────────────┬────────────────────────────┘               │
 └────────────────────────────────┼────────────────────────────────────────────┘
                                  ▼
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │                         Operating System & Hardware                         │
 │   Kernel Threads  •  Virtual Memory Pages  •  L1/L2/L3 Caches  •  RAM       │
 └─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Memory Architecture: Stack vs. Heap vs. Metaspace

Memory in Java is divided into distinct operational regions:

```text
+-----------------------------------------------------------------------------------------+
|                                    JVM PROCESS (OS MEMORY)                              |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  THREAD 1 (Main)                       THREAD 2 (Worker)               METASPACE (Native)|
|  +---------------------------+         +---------------------------+   +---------------+|
|  | Stack Frame: bar()        |         | Stack Frame: run()        |   | Class Models  ||
|  | - Locals: [x=42, refA]    |         | - Locals: [y=10, refB]    |   | Method VTables||
|  | - Operand Stack: [42, 1]  |         | - Operand Stack: [...]    |   | Constant Pools||
|  +---------------------------+         +---------------------------+   | Bytecodes     ||
|  | Stack Frame: main()       |                                         +---------------+|
|  | - Locals: [args, refA]    |                                                          |
|  +---------------------------+                                         CODE CACHE       |
|                                                                        +---------------+|
|                                                                        | JIT Native    ||
|                                                                        | Machine Code  ||
|                                                                        +---------------+|
|                                                                                         |
|  SHARED HEAP (Allocated via -Xms / -Xmx)                                                |
|  +-----------------------------------------------------------------------------------+  |
|  |                                                                                   |  |
|  |   Object A (e.g. Account)                      Object B (e.g. Transaction)        |  |
|  |   +------------------------------------+       +--------------------------------+ |  |
|  |   | Mark Word (hash, lock, age) (8B)   |       | Mark Word (8B)                 | |  |
|  |   | Klass Word (-> Metaspace)   (4B)*  |       | Klass Word (4B)*               | |  |
|  |   | balance = $1,500.00         (8B)   |       | amount = $50.00          (8B)  | |  |
|  |   | ownerRef = -> String        (4B)*  |       | targetAccountRef = -> ObjA(4B)*| |  |
|  |   +------------------------------------+       +--------------------------------+ |  |
|  |                                                                                   |  |
|  +-----------------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------------+
* With Compressed OOPs enabled (<32GB heap)
```

### Critical Rules:
1. **Primitives live where they are declared**:
   * Local primitives (`int x = 10;`) live directly in the thread's stack frame.
   * Instance primitives (`class Account { int balance; }`) live directly inside the object on the heap.
2. **Objects ALWAYS live on the heap**:
   * A variable holding an object only holds a **reference value** (memory address handle).
   * Stack frames only store the reference value, never the object's body.
3. **Metaspace lives outside the Java heap**:
   * Stored in native OS virtual memory; class definitions do not compete with object allocations for heap space.

---

## 3. Pass-By-Value Mechanics

Java is strictly **pass-by-value**. There are NO exceptions to this rule.

```text
SCENARIO A: Primitive Parameter Pass-by-Value
caller(): int x = 50 ──(copy bits 00110010)──► callee(int val): val = 100
Result: caller's x remains 50.

SCENARIO B: Reference Parameter Pass-by-Value
caller(): Account acc = [0x7FF0] ──(copy bits 0x7FF0)──► callee(Account a):
                                                            │
    Option 1: a.setBalance(200);                            │
              Follows pointer 0x7FF0 into heap.             │
              Heap object modified! Caller sees change.     │
                                                            │
    Option 2: a = new Account(999); [0x8BA0]                │
              Reassigns local stack variable 'a'.           │
              Original pointer in caller remains [0x7FF0]!  │
              Caller sees NO change to acc.
```

---

## 4. Dynamic Method Dispatch (vtable lookup)

When `animal.speak()` executes:

```text
Bytecode: invokevirtual #4 <Animal.speak:()V>

1. Read object reference from top of operand stack.
2. If null, throw NullPointerException.
3. Read Klass pointer from object header:
   Dog instance ──► Dog.class (in Metaspace)
4. Look up method index 3 in Dog's vtable:
   Animal vtable:          Dog vtable:
   0: equals()             0: equals()
   1: hashCode()           1: hashCode()
   2: toString()           2: toString()
   3: Animal.speak()  ──►  3: Dog.speak() [OVERRIDDEN]
5. Jump to native address or bytecode of Dog.speak().
```

---

## 5. The Java Memory Model (JMM) & Visibility

Without explicit synchronization, CPU cores cache values in L1/L2 caches and the JIT compiler reorders independent statements:

```text
   CORE 1 (Writer Thread)                          CORE 2 (Reader Thread)
+---------------------------+                   +---------------------------+
| Local L1 Cache            |                   | Local L1 Cache            |
| running = false; (Dirty)  |                   | running = true; (Stale!)  |
+-------------┬-------------+                   +-------------▲-------------+
              │                                               │
              │ (No flush without memory barrier)             │ (No reload!)
              ▼                                               │
+-------------------------------------------------------------┴-------------+
|                                MAIN RAM                                   |
|                          running = true (OLD)                             |
+---------------------------------------------------------------------------+

FIX: Declare 'volatile boolean running;'
- Generates StoreLoad / DMB (Data Memory Barrier) instructions.
- Writer flushes immediately to coherent bus.
- Reader is forced to invalidate stale cache line.
- Establishes a formal Happens-Before edge: Write(running) -> Read(running).
```

---

## 6. Garbage Collection: Reachability & The Weak Generational Hypothesis

```text
                     GC ROOTS
   (Thread Locals, Static References, JNI Registers)
             │                    │
             ▼                    ▼
        [Object A]           [Object D]
             │                    │
             ▼                    ▼
        [Object B]           [Object E]
             │
             ▼
        [Object C]          [Object F] ◄─── UNREACHABLE (Dead)
                            (No path from any root)
```

### The Weak Generational Hypothesis:
* *Observation*: Most allocated objects die very shortly after creation (temporary buffers, iterators, string builders).
* *Architectural response*:
  * **Eden / Young Generation**: Fast, bump-the-pointer linear allocation. Minor GCs scavenge surviving survivors rapidly.
  * **Tenured / Old Generation**: Long-lived objects (caches, singletons, thread pools) are promoted after surviving multiple aging cycles.

---

## 7. Virtual Threads: Carrier Thread Mounting

```text
1,000,000 Virtual Threads (Heap Continuations)
[VT 1: waiting on DB]  [VT 2: parsing JSON]  [VT 3: sleeping]  [VT 4: waiting on socket]
       │                       │
       ▼ (Unmounted to Heap)   ▼ (Mounted)
+-------------------------------------------------------------+
|              ForkJoinPool Carrier OS Threads                |
|  [ Carrier Thread 1 (Core 1) ]    [ Carrier Thread 2 (Core 2) ]
+-------------------------------------------------------------+
                                │
                                ▼
                       Operating System Kernel
```

When a Virtual Thread invokes a blocking socket read:
1. The standard library intercepts the blocking call.
2. The virtual thread's stack frames are copied from the carrier stack onto the heap.
3. The carrier OS thread is immediately freed to execute other virtual threads.
4. When the OS network poll event completes, the virtual thread is re-scheduled on any available carrier.
