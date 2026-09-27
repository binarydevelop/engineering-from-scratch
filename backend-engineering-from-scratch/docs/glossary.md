# Backend Engineering Glossary

A precise reference mapping common industry jargon to concrete mechanical definitions.

| Term | What People Say | What It Mechanically Means |
| :--- | :--- | :--- |
| **Socket** | "A connection to a server" | An operating system file descriptor representing a local endpoint of a bidirectional network communication channel (IP + Port + Protocol buffer). |
| **HTTP Request** | "An API call" | A structured stream of bytes formatted according to RFC 9112, starting with a Request-Line (`METHOD /path HTTP/1.1\r\n`), followed by headers (`Key: Value\r\n`), an empty line separator (`\r\n`), and an optional body. |
| **Router** | "URL mapping in FastAPI" | A dispatch data structure (hash map, trie, or regex matcher) that maps an incoming `(HTTP Method, Path)` tuple to a callable request handler function. |
| **Middleware** | "Plugins for the web server" | An onion-style chain of wrapper functions executing sequentially before and after the core route handler, sharing request/response context (e.g., logging, auth, CORS). |
| **Idempotency** | "Safe to run multiple times" | A mathematical property where applying an operation $f(x)$ multiple times produces the exact same system state as applying it once: $f(f(x)) = f(x)$. For APIs, sending the same request twice must not create duplicate side effects. |
| **ACID Transaction** | "Saving data to SQL" | A database consistency boundary guaranteeing Atomicity (all-or-nothing), Consistency (invariants preserved), Isolation (concurrent operations do not interfere), and Durability (committed data survives power loss). |
| **Connection Pool** | "Fast database access" | A bounded cache of pre-established, persistent TCP connections to a database server, avoiding the latency and resource overhead of repeated 3-way handshakes and authentication handshakes per request. |
| **Cache Stampede** | "Too much traffic" | A catastrophic concurrency failure where an expired hot cache key causes hundreds of simultaneous requests to experience a cache miss and hammer the underlying database with identical expensive queries at the exact same millisecond. |
| **Transactional Outbox** | "Sending Kafka events from SQL" | An architectural pattern that solves the dual-write problem by inserting an event message into an `outbox` table in the *same* local database transaction as the business entity, ensuring the event is guaranteed to be published asynchronously if and only if the business write commits. |
| **Circuit Breaker** | "Fault tolerance" | A state machine (Closed, Open, Half-Open) wrapping calls to an external dependency that automatically stops sending traffic to a failing downstream service after a threshold of errors, returning fast fallback responses instead of exhausting caller worker threads. |
| **Bulkhead** | "Resource limits" | An isolation pattern that partitions thread pools, connection pools, or worker processes so that a complete failure or slow down in one subsystem cannot consume 100% of the entire application's resources. |
| **Backpressure** | "System slowdown" | A feedback mechanism signaling an upstream producer to slow down or stop sending data when a downstream consumer's processing queue or buffer reaches capacity, preventing memory exhaustion and crashes. |
| **Event Loop** | "Async Python" | A single-threaded runtime loop that continuously polls operating system non-blocking I/O multiplexers (`epoll`, `kqueue`, `select`) and resumes paused coroutines when socket read/write buffers become ready. |
| **N+1 Problem** | "Slow ORM query" | A data-access anti-pattern where an application executes 1 query to fetch $N$ parent records, followed by $N$ individual separate queries to fetch related child records, turning a single operation into $N+1$ database roundtrips. |
| **Dead-Letter Queue (DLQ)** | "Where bad jobs go" | A secondary queue where messages or background tasks that repeatedly fail processing after a bounded number of retry attempts are isolated for manual inspection and debugging without blocking normal queue processing. |
| **RED Method** | "Monitoring" | An observability framework focusing on three core microservice metrics: Rate (requests per second), Errors (number of failed requests), and Duration (distribution of request latency). |
