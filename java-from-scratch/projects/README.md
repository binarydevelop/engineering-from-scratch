# 16 Substantial Production Java Projects

Real-world, multi-class systems built from first principles without heavy framework magic.

## Project Catalog

| Project ID | Directory | Description | Key Mechanism |
| :--- | :--- | :--- | :--- |
| **cli-application** | [CLI Application Engine](cli-application/README.md) | Production CLI with arguments parsing, configuration files, and exit codes | `CliApp` |
| **banking-domain** | [Banking Domain & Ledger](banking-domain/README.md) | BigDecimal Money value object, Account invariants, deadlock-free concurrent transfers | `BankingService` |
| **library-system** | [Library Management System](library-system/README.md) | Domain state modeling, sequenced collections, custom exceptions, loan tracking | `LibraryService` |
| **task-runner** | [Resilient Task Runner](task-runner/README.md) | ThreadPoolExecutor, priority queue, exponential backoff retries, metrics | `TaskRunner` |
| **file-indexer** | [High-Performance File Indexer](file-indexer/README.md) | NIO path walking, inverted search index, concurrent search engine | `FileIndexer` |
| **http-server** | [Lightweight HTTP/1.1 Server](http-server/README.md) | Raw ServerSocket, HTTP request parser, route dispatch, Virtual Threads | `HttpServerEngine` |
| **jdbc-crud** | [Raw JDBC Transactional Service](jdbc-crud/README.md) | Raw JDBC, PreparedStatements, connection pool, rollback on failure | `JdbcService` |
| **lru-cache** | [Generic Thread-Safe LRU Cache](lru-cache/README.md) | HashMap + DoublyLinkedList, generic <K,V>, ReentrantLock mutual exclusion | `LruCache` |
| **rate-limiter** | [Distributed-Ready Rate Limiter](rate-limiter/README.md) | Token Bucket and Sliding Window rate limiters using AtomicLong | `RateLimiter` |
| **message-queue** | [In-Memory Message Broker](message-queue/README.md) | Pub/Sub engine, topics, bounded blocking queues, poison pill shutdown | `MessageBroker` |
| **mini-di** | [Mini Dependency Injection Container](mini-di/README.md) | Custom @Inject/@Service annotations, reflection constructor injection | `MiniContainer` |
| **mini-orm** | [Mini Object-Relational Mapper](mini-orm/README.md) | Custom @Entity/@Id annotations, reflection row mapping, dynamic SQL | `MiniOrm` |
| **mini-test-framework** | [Mini Test Discovery & Runner](mini-test-framework/README.md) | Custom @Test/@Before annotations, reflective discovery and execution | `MiniTestRunner` |
| **web-crawler** | [Concurrent Asynchronous Web Crawler](web-crawler/README.md) | HttpClient, Virtual Threads, concurrent visited set, rate limit | `WebCrawler` |
| **log-analyzer** | [Streaming Log Analyzer](log-analyzer/README.md) | Streaming I/O, parallel computation, latency percentiles (p50, p95, p99) | `LogAnalyzer` |
| **in-memory-db** | [In-Memory Relational Engine](in-memory-db/README.md) | Table storage, primary key index, table scan, mini transaction log | `InMemoryDatabase` |
