# Phase 264: Apache HBase: BigTable Architecture, RegionServers, and LSM on HDFS

## 1. Why This Matters for MAANG & Senior/Staff Roles
Apache HBase (modeled directly on Google BigTable) was the foundational distributed wide-column database that powered massive systems at Facebook (Messages), Uber (driver/rider tracking), and Pinterest. While managed alternatives like DynamoDB and Bigtable exist, HBase remains the gold standard for understanding master-slave distributed storage architectures running on append-only filesystems (HDFS).

---

## 2. Core Concepts & Architecture Deep-Dive
### Architectural Components
- **HMaster**: Coordinates cluster metadata, manages region splits, handles failover, and assigns regions to RegionServers. Does NOT participate in the data read/write path.
- **RegionServer**: Serves reads and writes for assigned Regions. A Region is a horizontal range of keys (`[start_key, end_key)`).
- **ZooKeeper**: Maintains consensus, tracks live RegionServers, and stores root region catalog locations.

### Internal Storage Engine (LSM on HDFS)
Each Region contains multiple Stores (one Store per Column Family):
1. **Write Path**: Write arrives -> appended to HDFS Write-Ahead Log (`HLog` / WAL) for durability -> written to in-memory `MemStore`. Client receives ACK immediately (fast write).
2. **Flush**: When `MemStore` reaches threshold (typically 128MB), it is flushed to an immutable `HFile` on HDFS.
3. **Compaction**:
   - *Minor Compaction*: Merges small HFiles into fewer, larger HFiles.
   - *Major Compaction*: Rewrites all HFiles in a Store into a single HFile, permanently purging deleted rows (tombstones) and expired TTL versions.
4. **Read Path**: Checks `BlockCache` (L1/L2 in-memory cache) -> `MemStore` -> filters HFiles using Bloom Filters -> reads matching blocks from HDFS.

---

## 3. High-Value Interview Angle & Failure Modes
### Interview Trade-Offs: HBase vs Cassandra
| Dimension | Apache HBase | Apache Cassandra |
|---|---|---|
| **Architecture** | Master-Slave (HMaster + RegionServers) | Masterless (Peer-to-peer ring / Dynamo) |
| **Consistency** | Strong Consistency (Single region primary) | Tunable Consistency (Quorum R+W > N) |
| **Storage Layer** | HDFS (Decoupled compute and storage) | Local ephemeral/attached NVMe disks |
| **Coordination** | Heavy ZooKeeper reliance | Gossip protocol + Paxos for LWT |
| **Sweet Spot** | Sequential range scans on row keys | High-write random lookups across multiple data centers |

---

## 4. Hands-On Practice & Implementation Drills
### Row Key Design Principles (Golden Rule)
Because HBase indexes rows strictly in lexicographical order:
- **Avoid Monotonic Keys**: Using timestamps (`2026-10-11-12:00:00`) causes all writes to hit a single RegionServer (Region Hotspotting).
- **Salting & Hashing**: Prefix row keys with a hash or reverse the domain name (`com.company.api`) to distribute writes uniformly across all RegionServers.

---

## 5. Key Takeaways & Cheat Sheet
- HBase is an open-source implementation of Google's BigTable.
- Writes write to WAL + MemStore in memory before flushing immutable HFiles to HDFS.
- Provides strong consistency per row key by routing all writes for a key range to one RegionServer.
- Monotonic row keys cause write hotspotting; salt or hash row keys to distribute load.
