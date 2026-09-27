# Project 04: Durable Background Task Pipeline with Redis Streams

Demonstrates reliable asynchronous task processing using Redis Streams Consumer Groups, solving the durability and failure-recovery limitations of Redis Lists and Pub/Sub.

---

## Comparison: List vs Pub/Sub vs Streams

| Capability | Redis List (`LPUSH` / `RPOP`) | Redis Pub/Sub (`PUBLISH`) | Redis Streams (`XADD`) |
| :--- | :--- | :--- | :--- |
| **Durability** | Yes (in memory / persistence) | **NO** (fire-and-forget; dropped if offline) | **YES** (persistent append-only log) |
| **Consumer Groups** | No (competing consumers, no offset) | No (every subscriber receives everything) | **YES** (`XGROUP` partitions stream) |
| **Crash Recovery** | If worker dies after `RPOP`, item is lost! | Impossible (no historical replay) | **YES** (tracked in Pending Entries List) |
| **Dead-Letter Claiming**| Requires secondary recovery list (`RPOPLPUSH`)| Not supported | **YES** (`XCLAIM` re-assigns idle jobs) |
| **Message Deduplication**| Manual | None | Native via millisecond-sequence ID |

---

## Running the Pipeline

```bash
make up
python3 projects/04-task-queue/worker_queue.py
```
