# Java & JVM Repetition Katas

Practice these 10 katas repeatedly until you can implement them flawlessly from memory on a blank screen.

| Kata | Title | Objective |
| :--- | :--- | :--- |
| **kata-01-dynamic-array** | [Dynamic Array Implementation](kata-01-dynamic-array.md) | Re-implement ArrayList with 1.5x growth factor and element shifting on remove |
| **kata-02-hash-bucket** | [Hash Bucket & Collision Resolution](kata-02-hash-bucket.md) | Implement separate chaining bucket hashing from scratch without using Map |
| **kata-03-spin-lock** | [Lock-Free CAS SpinLock](kata-03-spin-lock.md) | Build a spinlock using AtomicBoolean and VarHandle |
| **kata-04-bounded-queue** | [Bounded Blocking Queue](kata-04-bounded-queue.md) | Implement a thread-safe bounded buffer using wait() and notifyAll() |
| **kata-05-lru-eviction** | [LRU Eviction Policy](kata-05-lru-eviction.md) | Build an LRU cache eviction mechanism combining a Doubly-Linked list with a Map |
| **kata-06-rate-limiter-bucket** | [Token Bucket Rate Limiter](kata-06-rate-limiter-bucket.md) | Implement token replenishment rate limiter with nanosecond precision |
| **kata-07-bytecode-disassembler** | [Reading Bytecode Opcodes](kata-07-bytecode-disassembler.md) | Decode raw classfile bytes to extract magic number and constant pool count |
| **kata-08-immutable-money** | [Defensive Value Object (Money)](kata-08-immutable-money.md) | Design an immutable Money class with currency validation and defensive copying |
| **kata-09-thread-safe-singleton** | [Double-Checked Locking Singleton](kata-09-thread-safe-singleton.md) | Implement thread-safe singleton using volatile and intrinsic monitor |
| **kata-10-virtual-thread-fanout** | [Virtual Thread Task Fanout](kata-10-virtual-thread-fanout.md) | Fan out 10,000 simulated blocking HTTP calls using virtual threads |
