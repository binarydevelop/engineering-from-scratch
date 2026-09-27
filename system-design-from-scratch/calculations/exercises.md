# 105 Back-of-the-Envelope Estimation Exercises

Test your mental math and quantitative modeling. Complete these exercises without viewing `solutions.py`.

---

## Category 1: Traffic & RPS Estimation (Exercises 1–15)

1. A service has 10 million Daily Active Users (DAU). Each user performs 20 actions per day. Calculate the average Requests Per Second (RPS).
2. Given 50M DAU with 30 requests/day, assuming a peak traffic factor of 2.5x, what is the peak RPS?
3. A video platform has 100M monthly active users (MAU). Assume 20% visit daily (20M DAU). Each user requests 15 video feeds/day. Calculate average and peak RPS (peak factor = 3x).
4. An e-commerce service expects 500,000 orders on Black Friday over a 12-hour period. If 80% of orders occur during a 4-hour peak window, what is the peak order write RPS?
5. A social media app has 200M DAU. Read-to-write ratio is 100:1. Each user creates 2 posts/day and views 200 posts/day. Calculate read QPS and write QPS.
6. A photo-sharing platform receives 50 million image uploads per day. What is the average upload write RPS?
7. An IoT fleet contains 1,000,000 connected temperature sensors. Each sensor pings telemetry once every 60 seconds. What is the steady-state ingestion RPS?
8. An authentication service authenticates 30M users during the morning peak between 8:00 AM and 9:00 AM (1 hour). What is the peak authentication QPS?
9. A messaging app handles 5 billion messages per day. What is the average message delivery RPS?
10. A URL shortener generates 100 million new short URLs per month (assume 30 days). Read-to-write ratio is 10:1. Calculate average read RPS and write RPS.
11. An ad-bidding exchange evaluates 100,000 auctions per second. Each auction invites 5 bidders. What is the total outgoing RPC request rate?
12. A financial news platform has 5M users who refresh their portfolio page 50 times during the 6.5-hour trading day. What is the trading-day average RPS?
13. A ride-sharing app has 500,000 active drivers sending GPS coordinates every 4 seconds. What is the driver location write QPS?
14. A webhook notification system sends 10M notifications per day. 5% fail on the first try and are retried once. What is the total delivery RPS including retries?
15. A food delivery app serves 2M orders per day. Each order involves 12 status-change transitions throughout its lifecycle. What is the status update QPS?

---

## Category 2: Storage Growth & Retention (Exercises 16–30)

16. A URL shortener writes 100M URLs/month. Each URL mapping record takes 500 bytes. How much storage is added per month and per year?
17. A social network stores 500M posts per day. Each post metadata record is 1 KB. How many GB/day and TB/year are written?
18. An IoT sensor service collects 1,000,000 sensor pings/minute. Each ping is 200 bytes. How much storage is needed for 30 days of raw telemetry?
19. A database table stores 100 million customer records. The primary data is 2 KB per record. Indexes add an additional 25% overhead. What is the total database disk requirement?
20. A photo service receives 20M images per day. Average compressed image size is 2 MB. How many TB of object storage are required per day and per year?
21. Video platform users upload 500 hours of video every minute. Video is encoded at an average bitrate of 5 Mbps (megabits per second). How many GB of storage are ingested per minute?
22. An audit logging system ingests 10,000 log events/second. Each JSON log is 800 bytes. How much storage is accumulated per day and per 90-day retention window?
23. A chat application stores 1 billion messages per day. Average text message size is 300 bytes. Calculate storage per day and per 5 years.
24. A relational database table has 50 million rows and grows by 10% each month. How many rows will it have after 12 months (compound growth)?
25. An analytics database stores clickstream events. 50,000 events/second are ingested. Each event is 100 bytes compressed in columnar format. How much storage is consumed per 24 hours?
26. A user metadata database stores 10M user profiles at 5 KB each. To ensure disaster recovery, 3 replicas are maintained across 3 availability zones. What is the total replicated storage?
27. A system retains 100 TB of active data on NVMe SSDs and archives data older than 30 days to cold object storage. If 2 TB of data is generated daily, what is the steady-state SSD storage requirement?
28. A time-series database stores CPU metrics for 10,000 servers. Each server reports 5 metrics every 10 seconds. Each metric sample takes 16 bytes. How much storage is consumed in 7 days?
29. A document management platform stores 10M PDF documents averaging 1.5 MB each. Documents have 3 historical versions on average. What is the total object storage footprint?
30. A database table has 200 million rows. Each row has a primary key (8 bytes) and 3 secondary B-Tree indexes (averaging 16 bytes per entry per index). What is the total index size alone?

---

## Category 3: Bandwidth & Networking (Exercises 31–45)

31. An API serves 10,000 read requests per second. The average JSON response payload is 25 KB. What is the egress network bandwidth in MB/s and Gbps?
32. An image upload service receives 500 uploads/second at an average of 1.2 MB per image. What is the inbound ingress bandwidth in MB/s and Gbps?
33. A streaming service delivers video to 100,000 concurrent viewers at 4 Mbps per stream. What is the total egress bandwidth in Gbps?
34. A microservice makes 5 downstream RPC calls per incoming HTTP request. Inbound traffic is 2,000 req/s. Each RPC payload is 4 KB request and 8 KB response. What is the internal network traffic generated?
35. A database replica asynchronously replicates a write-ahead log (WAL) from the primary. Write traffic generates 50 MB of WAL logs per minute. What is the minimum required replication link bandwidth in Mbps?
36. An ad-exchange gateway receives 50,000 bid requests per second. Request payload is 1.5 KB. What is the ingress bandwidth in Megabytes per second?
37. A CDN serves 85% of traffic from edge cache. Total origin traffic is 150 Gbps without CDN. What is the remaining egress bandwidth required from the origin datacenter?
38. A music streaming platform has 500,000 concurrent listeners streaming audio at 256 kbps (kilobits per second). What is the aggregate network egress in Gbps?
39. A file synchronization client uploads a 10 GB file over a 100 Mbps uplink. Assuming 80% effective network utilization, how long does the upload take in minutes?
40. An internal metrics daemon sends batches of 500 KB metrics data every 5 seconds from 1,000 servers to a central collector. What is the inbound bandwidth at the collector in MB/s?
41. A search autocomplete service receives 25,000 queries per second. Average response payload is 800 bytes. What is the egress bandwidth in MB/s?
42. A web crawler downloads 1,000 web pages per second. Average HTML page size is 150 KB. What is the ingress network bandwidth in MB/s?
43. A backup job transfers a 5 TB database snapshot across regions over a dedicated 10 Gbps direct connect link. Assuming 70% throughput efficiency, how many minutes will the transfer take?
44. A WebSocket chat gateway maintains 50,000 open connections. Each connection sends a 64-byte heartbeat ping every 30 seconds. What is the heartbeat network bandwidth in KB/s?
45. A payment gateway receives 1,200 transactions/second. Request payload is 2 KB and response payload is 1 KB. What is the total bi-directional network throughput in MB/s?

---

## Category 4: Cache & Memory Sizing (Exercises 46–60)

46. An application processes 50 million read requests per day. The total dataset is 500 GB. Applying the 80/20 rule, how much RAM is required to cache 20% of the daily active data?
47. An e-commerce catalog has 10 million products. Each cached product object is 2 KB in Redis. What is the total memory required to cache the entire catalog?
48. A social media profile cache stores profiles for 5 million active users. Each profile is 1.5 KB. Redis overhead per key is approximately 100 bytes. How many GB of RAM are required?
49. A news website has 10,000 articles published per month. The top 5% of articles receive 90% of all page views. Each article HTML payload is 40 KB. How much cache memory is needed to hold the top 5%?
50. A session cache holds session state for 2,000,000 concurrent logged-in users. Each session payload is 800 bytes. How much memory is needed with a 25% safety buffer for Redis memory fragmentation?
51. A rate limiter uses Redis to track request counters per IP address. It tracks 10,000,000 distinct IP addresses in a sliding window. Each IP counter requires 64 bytes. How much RAM is needed?
52. A URL shortener receives 200M read requests per day. The database contains 2 billion URLs (totaling 1 TB). If 20% of the URLs generate 80% of the traffic, how much cache memory is needed to cache the hot URLs?
53. An in-memory cache has a 95% hit ratio on a service handling 10,000 QPS. How many requests per second still reach the database?
54. If a cache miss incurs a 15 ms database query, while a cache hit takes 0.5 ms, what is the average latency with a 90% cache hit ratio?
55. What is the average latency from exercise 54 if the cache hit ratio improves to 99%?
56. A Redis cluster stores 100 GB of active cached keys. Each Redis node has 32 GB of RAM, and best practice dictates keeping memory utilization below 75% for background snapshotting (BGSAVE). How many nodes are required?
57. An API gateway caches user permissions. There are 1,000,000 users. Each permission set is 500 bytes. Cache TTL is 15 minutes. If only 10% of users are active in any 15-minute window, how much RAM is required?
58. A video metadata cache stores 50,000 popular video records. Each record is 8 KB. What is the total memory footprint in MB?
59. A cache eviction policy uses LRU. Under peak load, new keys are written at 5,000 keys/second. Each key is 1 KB. If the cache is sized at 30 GB, what is the maximum time a key can remain in the cache without being accessed before being evicted?
60. A microservice uses local in-process memory caching. There are 20 application server instances. The shared cache dataset is 4 GB. What is the aggregate RAM consumed across all instances compared to a centralized Redis instance?

---

## Category 5: Little's Law & Concurrency (Exercises 61–75)

61. An API receives 2,500 requests per second. The average response time is 80 milliseconds. According to Little's Law ($L = \lambda \times W$), how many requests are in-flight concurrently?
62. A database query takes an average of 40 ms. The database connection pool has 100 connections. What is the maximum throughput (queries per second) the pool can sustain before queueing begins?
63. An external payment gateway has an average latency of 500 ms. Your service needs to handle 200 payment requests per second. How many concurrent outgoing HTTP connections must your client maintain?
64. If downstream database latency degrades from 25 ms to 200 ms under load, and arrival rate remains 1,000 req/s, how does the concurrent in-flight request count change?
65. A worker pool has 64 worker threads. Each job takes 250 ms to execute. What is the maximum sustained throughput in jobs per second?
66. An async Python service handles 10,000 concurrent WebSocket connections. Each connection sends a message every 10 seconds. What is the incoming message arrival rate ($\lambda$)?
67. A web service handles 4,000 requests/sec with an average latency of 50 ms. It runs on application servers where each server can handle 200 concurrent requests without thread exhaustion. How many application servers are required?
68. A backend endpoint executes 3 database queries sequentially: Query 1 (10 ms), Query 2 (15 ms), Query 3 (25 ms). At 500 req/s, what is the average concurrency in this endpoint?
69. If the 3 database queries in exercise 68 are refactored to run concurrently in parallel, the total latency drops to 25 ms (the slowest query). What is the new concurrency at 500 req/s?
70. A search service handles 1,500 queries/second. 90% of queries hit the cache (latency = 2 ms), while 10% miss and execute a full index scan (latency = 80 ms). What is the weighted average latency and concurrent in-flight queries?
71. A checkout service is designed for a target SLA of 150 ms. The architecture supports a maximum of 1,200 concurrent requests before memory pressure triggers GC pauses. What is the maximum arrival rate ($\lambda$) it can support within SLA?
72. A disk drive can perform 200 random I/O operations per second (IOPS). Average disk seek and read time is 5 ms. What is the average queue depth at maximum capacity?
73. An event processing pipeline receives 50,000 events/second. Processing each event takes 2 ms of CPU time. How many CPU cores are required to process the stream in real-time?
74. A microservice thread pool has 50 threads. If requests arrive at 300 req/s and each request takes 200 ms, what happens to incoming requests?
75. Calculate the average request queue wait time in exercise 74 if arrival rate is 300 req/s, capacity is 250 req/s, and a queue buffer holds 500 requests before rejecting.

---

## Category 6: Queue Capacity & Backlog (Exercises 76–85)

76. A message queue receives 10,000 messages/second. Consumers process messages at 8,000 messages/second. By how many messages does the queue backlog grow per hour?
77. In exercise 76, consumer capacity is scaled to 16,000 messages/second after 2 hours of backlog accumulation. How many minutes will it take the workers to drain the accumulated backlog?
78. An email dispatch queue receives 1,000,000 emails during a marketing campaign blast over 10 minutes. The email provider enforces a rate limit of 500 emails/second. How many minutes will it take to deliver all emails?
79. A message queue broker has 50 GB of disk dedicated to message storage. Each message is 1 KB. If consumer workers go down completely while producers continue writing at 2,000 messages/second, how many hours until the disk fills up?
80. An event bus partitions messages across 16 partitions. Traffic is 32,000 messages/second. Assuming uniform hashing, what is the ingestion rate per partition?
81. If one partition in exercise 80 receives a hot key representing 25% of all traffic, what is the ingestion rate on that single partition?
82. A dead-letter queue (DLQ) receives 0.1% of all processed messages. The system processes 20 million messages per day. How many messages enter the DLQ daily?
83. A worker takes 50 ms to process a job. A single worker container runs 4 worker processes. How many worker containers are needed to process a steady stream of 2,000 jobs/second?
84. An event streaming consumer group has 8 consumers reading from 8 partitions. One consumer crashes. How do the remaining 7 consumers rebalance the 8 partitions?
85. A queue has a maximum visibility timeout of 30 seconds. A worker takes 35 seconds to process a heavy job. What defect occurs in the queue?

---

## Category 7: Availability & Downtime (Exercises 86–95)

86. A cloud service advertises 99.9% ("three nines") availability. What is the maximum allowed downtime per year (365 days) in hours and minutes?
87. A critical payment service requires 99.99% ("four nines") availability. What is the maximum allowed downtime per year in minutes?
88. An ultra-reliable database guarantees 99.999% ("five nines") availability. What is the maximum allowed downtime per month (30 days) in seconds?
89. A request path traverses 3 independent services in series: API Gateway (99.99%), Auth Service (99.9%), and Database (99.95%). Assuming independent failures, what is the overall system availability?
90. If the overall availability in exercise 89 is 99.84%, what is the expected annual downtime in hours?
91. A service uses two redundant load balancers in an active-passive configuration. Each load balancer has 99.0% individual availability. Assuming independent failure modes, what is the composite availability of the pair?
92. A service runs across 2 Availability Zones (AZs). Each AZ has 99.9% availability. What is the composite availability against total datacenter loss?
93. A single primary database has an MTBF (Mean Time Between Failures) of 1,000 hours and an MTTR (Mean Time to Recover) of 2 hours. What is its availability percentage?
94. An automated failover mechanism reduces MTTR from 2 hours to 1 minute. What is the new availability percentage with MTBF = 1,000 hours?
95. A SaaS company signs an SLA with a customer promising 99.95% monthly uptime. During a 30-day month, an outage lasts 35 minutes. Did the company violate the SLA?

---

## Category 8: Infrastructure Cost Modeling (Exercises 96–105)

96. A service runs 10 virtual machine instances. Each instance costs $0.08 per hour. What is the total compute cost per month (730 hours)?
97. A service stores 50 TB of standard object storage costing $0.023 per GB per month. What is the monthly storage bill?
98. An application transfers 100 TB of egress data out to the internet each month. The cloud provider charges $0.08 per GB for egress. What is the monthly data transfer cost?
99. A Redis cache cluster requires 128 GB of RAM. Managed in-memory cache instances cost $0.035 per GB-hour. What is the monthly cache cost?
100. A microservice architecture has 40 small services running on 20 Kubernetes nodes costing $150/month each. Consolidating into a modular monolith allows running on 4 larger nodes costing $300/month each. What is the monthly cost savings?
101. An unoptimized API transfers 500 KB JSON payloads. Compressing responses with gzip reduces payload size by 80% to 100 KB. At 50 million requests per month and $0.08/GB egress, what is the monthly cost reduction?
102. A primary database instance costs $800/month. Each read replica costs $400/month. Sizing requires 1 primary and 3 read replicas. What is the annual database cost?
103. A logging system ingests 5 TB of uncompressed logs per month. Log management SaaS charges $0.50 per GB ingested. What is the monthly ingestion charge?
104. Introducing client-side sampling (retaining only 10% of debug logs) reduces ingestion in exercise 103 by 75%. What is the new monthly charge and annual savings?
105. Comparing architectures: Architecture A (Serverless: $0.20 per million requests + $0.000016 per GB-second; 100M requests, 200 ms execution, 512 MB RAM) vs Architecture B (2 Dedicated VMs at $60/month each). Which is cheaper and by how much?
