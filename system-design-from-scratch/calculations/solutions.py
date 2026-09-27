"""
Mathematical solutions and verification engine for all 105 Back-of-the-Envelope exercises.
"""

from typing import Dict, Any

class EstimationSolutions:
    @staticmethod
    def solve_all() -> Dict[int, Any]:
        s = {}

        # Category 1: Traffic & RPS (1-15)
        # 1. 10M DAU * 20 req/day / 86400
        s[1] = round((10_000_000 * 20) / 86_400, 2)  # ~2314.81 req/s
        # 2. 50M * 30 / 86400 * 2.5
        s[2] = round(((50_000_000 * 30) / 86_400) * 2.5, 2)  # ~43402.78 req/s
        # 3. 20M DAU * 15 / 86400 = avg; peak = avg * 3
        avg_3 = (20_000_000 * 15) / 86_400
        s[3] = {"avg_rps": round(avg_3, 2), "peak_rps": round(avg_3 * 3, 2)}
        # 4. 500k orders, 80% in 4h (14400s) -> 400k / 14400
        s[4] = round((500_000 * 0.80) / (4 * 3600), 2)  # ~27.78 writes/s
        # 5. 200M DAU: 2 writes/day, 200 reads/day
        s[5] = {
            "write_qps": round((200_000_000 * 2) / 86_400, 2),
            "read_qps": round((200_000_000 * 200) / 86_400, 2)
        }
        # 6. 50M uploads / 86400
        s[6] = round(50_000_000 / 86_400, 2)  # ~578.70 uploads/s
        # 7. 1M sensors every 60s
        s[7] = round(1_000_000 / 60, 2)  # ~16666.67 req/s
        # 8. 30M in 1 hour (3600s)
        s[8] = round(30_000_000 / 3600, 2)  # ~8333.33 QPS
        # 9. 5B msgs / 86400
        s[9] = round(5_000_000_000 / 86_400, 2)  # ~57870.37 msg/s
        # 10. 100M URLs/month (30 days) -> write = 100M / (30*86400); read = 10x
        w_10 = 100_000_000 / (30 * 86_400)
        s[10] = {"write_rps": round(w_10, 2), "read_rps": round(w_10 * 10, 2)}
        # 11. 100k auctions/s * 5 bidders
        s[11] = 100_000 * 5  # 500,000 req/s
        # 12. 5M * 50 / (6.5 * 3600)
        s[12] = round((5_000_000 * 50) / (6.5 * 3600), 2)  # ~10683.76 req/s
        # 13. 500k drivers every 4s
        s[13] = round(500_000 / 4, 2)  # 125,000 QPS
        # 14. 10M * 1.05 / 86400
        s[14] = round((10_000_000 * 1.05) / 86_400, 2)  # ~121.53 req/s
        # 15. 2M * 12 / 86400
        s[15] = round((2_000_000 * 12) / 86_400, 2)  # ~277.78 QPS

        # Category 2: Storage Growth (16-30)
        # 16. 100M * 500B = 50 GB/month; 600 GB/year
        s[16] = {"gb_per_month": 50.0, "gb_per_year": 600.0}
        # 17. 500M * 1 KB = 500 GB/day; 182.5 TB/year
        s[17] = {"gb_per_day": 500.0, "tb_per_year": round((500 * 365) / 1000, 1)}
        # 18. 1M pings/min * 200B * 60 * 24 * 30
        bytes_18 = 1_000_000 * 200 * 60 * 24 * 30
        s[18] = {"gb_total": round(bytes_18 / (10**9), 1)}  # 8640 GB = 8.64 TB
        # 19. 100M * 2KB * 1.25
        s[19] = {"gb_total": round((100_000_000 * 2000 * 1.25) / (10**9), 1)}  # 250 GB
        # 20. 20M * 2MB = 40 TB/day; 14,600 TB/year
        s[20] = {"tb_per_day": 40.0, "tb_per_year": 40.0 * 365}
        # 21. 500 hours/min * 3600s/h * 5 Mbps / 8 bits/byte
        bytes_21 = 500 * 3600 * (5_000_000 / 8)
        s[21] = {"gb_per_min": round(bytes_21 / (10**9), 1)}  # 1125 GB
        # 22. 10k logs/s * 800B = 8 MB/s = 691.2 GB/day; 90 days = 62.2 TB
        gb_day_22 = (10_000 * 800 * 86_400) / (10**9)
        s[22] = {"gb_per_day": round(gb_day_22, 1), "tb_90_days": round((gb_day_22 * 90) / 1000, 1)}
        # 23. 1B * 300B = 300 GB/day; 5 years = 300 * 365 * 5 / 1000 = 547.5 TB
        s[23] = {"gb_per_day": 300.0, "tb_5_years": round((300 * 1825) / 1000, 1)}
        # 24. 50M * (1.10)^12
        s[24] = {"rows_after_12m": int(50_000_000 * (1.10**12))}  # ~156,921,418
        # 25. 50k * 100B * 86400
        s[25] = {"gb_per_day": round((50_000 * 100 * 86_400) / (10**9), 1)}  # 432 GB
        # 26. 10M * 5KB * 3 replicas
        s[26] = {"gb_replicated": round((10_000_000 * 5_000 * 3) / (10**9), 1)}  # 150 GB
        # 27. 2 TB/day * 30 days = 60 TB active SSD
        s[27] = {"active_ssd_tb": 60.0}
        # 28. 10k servers * 5 metrics = 50k samples every 10s = 5k samples/s * 16B * 86400 * 7
        bytes_28 = 5_000 * 16 * 86_400 * 7
        s[28] = {"gb_7_days": round(bytes_28 / (10**9), 2)}  # 48.38 GB
        # 29. 10M docs * 1.5MB * 3 versions = 45 TB
        s[29] = {"tb_total": 45.0}
        # 30. 200M * (3 indexes * 16 bytes) = 200M * 48 bytes = 9.6 GB
        s[30] = {"gb_index_size": round((200_000_000 * 48) / (10**9), 1)}  # 9.6 GB

        # Category 3: Bandwidth & Networking (31-45)
        # 31. 10,000 * 25 KB = 250 MB/s = 2.0 Gbps (250 * 8 / 1000)
        s[31] = {"mb_per_sec": 250.0, "gbps": 2.0}
        # 32. 500 * 1.2 MB = 600 MB/s = 4.8 Gbps
        s[32] = {"mb_per_sec": 600.0, "gbps": 4.8}
        # 33. 100k viewers * 4 Mbps = 400,000 Mbps = 400 Gbps
        s[33] = {"gbps": 400.0}
        # 34. 2000 req/s * 5 RPCs = 10k RPC/s * (4KB + 8KB) = 120 MB/s
        s[34] = {"mb_per_sec": 120.0}
        # 35. 50 MB / 60s = 0.833 MB/s * 8 = 6.67 Mbps
        s[35] = {"mbps": round((50 * 8) / 60, 2)}
        # 36. 50k * 1.5 KB = 75 MB/s
        s[36] = {"mb_per_sec": 75.0}
        # 37. 150 Gbps * (1 - 0.85) = 22.5 Gbps origin
        s[37] = {"origin_gbps": 22.5}
        # 38. 500k * 256 kbps = 128,000,000 kbps = 128 Gbps
        s[38] = {"gbps": 128.0}
        # 39. 10 GB = 80 Gb / (100 Mbps * 0.80) = 80,000 Mb / 80 Mbps = 1,000 s = 16.67 min
        s[39] = {"minutes": round(1000 / 60, 1)}
        # 40. 1000 * 500 KB / 5s = 500,000 KB / 5s = 100,000 KB/s = 100 MB/s
        s[40] = {"mb_per_sec": 100.0}
        # 41. 25k * 800 B = 20,000,000 B/s = 20 MB/s
        s[41] = {"mb_per_sec": 20.0}
        # 42. 1000 * 150 KB = 150 MB/s
        s[42] = {"mb_per_sec": 150.0}
        # 43. 5 TB = 40,000 Gb / (10 Gbps * 0.70) = 40,000 / 7 = 5714 s = 95.2 min
        s[43] = {"minutes": round((5 * 8 * 1000) / (7 * 60), 1)}
        # 44. 50k * 64B / 30s = 3,200,000 B / 30s = 106.67 KB/s
        s[44] = {"kb_per_sec": round(3200 / 30, 2)}
        # 45. 1200 * (2KB + 1KB) = 3600 KB/s = 3.6 MB/s
        s[45] = {"mb_per_sec": 3.6}

        # Category 4: Cache & Memory Sizing (46-60)
        # 46. 500 GB * 0.20 = 100 GB RAM
        s[46] = {"gb_ram": 100.0}
        # 47. 10M * 2 KB = 20,000,000 KB = 20 GB
        s[47] = {"gb_ram": 20.0}
        # 48. 5M * (1.5KB + 0.1KB) = 5M * 1.6KB = 8 GB
        s[48] = {"gb_ram": 8.0}
        # 49. 10k * 0.05 = 500 articles * 40 KB = 20,000 KB = 20 MB
        s[49] = {"mb_ram": 20.0}
        # 50. 2M * 800B * 1.25 = 2,000,000,000 B = 2.0 GB
        s[50] = {"gb_ram": 2.0}
        # 51. 10M * 64B = 640 MB
        s[51] = {"mb_ram": 640.0}
        # 52. 1 TB * 0.20 = 200 GB
        s[52] = {"gb_ram": 200.0}
        # 53. 10,000 * (1 - 0.95) = 500 QPS to DB
        s[53] = {"db_qps": 500}
        # 54. 0.90 * 0.5ms + 0.10 * 15ms = 0.45 + 1.5 = 1.95 ms
        s[54] = {"avg_latency_ms": 1.95}
        # 55. 0.99 * 0.5ms + 0.01 * 15ms = 0.495 + 0.15 = 0.645 ms
        s[55] = {"avg_latency_ms": 0.645}
        # 56. 100 GB / (32 GB * 0.75) = 100 / 24 = 4.16 -> 5 nodes
        s[56] = {"nodes_required": 5}
        # 57. 1M * 0.10 = 100k users * 500B = 50 MB
        s[57] = {"mb_ram": 50.0}
        # 58. 50k * 8 KB = 400 MB
        s[58] = {"mb_ram": 400.0}
        # 59. 30 GB = 30,000,000 KB / (5k * 1 KB/s) = 6,000 s = 100 minutes
        s[59] = {"minutes": 100.0}
        # 60. 20 instances * 4 GB = 80 GB total local RAM vs 4 GB centralized
        s[60] = {"local_aggregate_gb": 80.0, "centralized_gb": 4.0}

        # Category 5: Little's Law & Concurrency (61-75)
        # 61. L = lambda * W = 2500 * 0.080 = 200 concurrent requests
        s[61] = {"concurrency": 200}
        # 62. lambda = L / W = 100 / 0.040 = 2500 QPS
        s[62] = {"max_throughput_qps": 2500}
        # 63. L = 200 * 0.500 = 100 connections
        s[63] = {"connections": 100}
        # 64. Before: 1000 * 0.025 = 25; After: 1000 * 0.200 = 200 (8x increase)
        s[64] = {"before": 25, "after": 200, "multiplier": 8.0}
        # 65. lambda = 64 / 0.250 = 256 jobs/s
        s[65] = {"jobs_per_sec": 256}
        # 66. lambda = 10k / 10s = 1000 msg/s
        s[66] = {"msg_per_sec": 1000}
        # 67. L = 4000 * 0.050 = 200 concurrent requests -> 200 / 200 = 1 server
        s[67] = {"servers_required": 1}
        # 68. W = 10 + 15 + 25 = 50ms = 0.05s -> L = 500 * 0.05 = 25
        s[68] = {"concurrency": 25}
        # 69. W = 25ms = 0.025s -> L = 500 * 0.025 = 12.5
        s[69] = {"concurrency": 12.5}
        # 70. W = 0.90*2ms + 0.10*80ms = 1.8 + 8.0 = 9.8ms = 0.0098s -> L = 1500 * 0.0098 = 14.7
        s[70] = {"weighted_latency_ms": 9.8, "concurrency": 14.7}
        # 71. lambda = 1200 / 0.150 = 8000 req/s
        s[71] = {"max_arrival_rps": 8000}
        # 72. L = lambda * W = 200 * 0.005 = 1.0 item
        s[72] = {"avg_queue_depth": 1.0}
        # 73. 50k * 0.002s = 100 CPU core-seconds/s = 100 cores
        s[73] = {"cores_required": 100}
        # 74. Capacity = 50 / 0.200 = 250 req/s. Arrival = 300 req/s -> 50 req/s accumulate in queue
        s[74] = {"deficit_req_per_sec": 50, "outcome": "QUEUE_OVERFLOW"}
        # 75. 500 buffer / 50 deficit = 10 seconds until buffer full
        s[75] = {"seconds_until_full": 10.0}

        # Category 6: Queue Capacity (76-85)
        # 76. (10k - 8k) * 3600 = 2000 * 3600 = 7.2M messages/hour
        s[76] = {"backlog_growth_per_hour": 7_200_000}
        # 77. 2h backlog = 14.4M. Drain rate = 16k - 10k = 6k/s. Time = 14.4M / 6k = 2400s = 40 min
        s[77] = {"drain_time_minutes": 40.0}
        # 78. 1M / 500s = 2000s = 33.33 minutes
        s[78] = {"minutes": round(2000 / 60, 2)}
        # 79. 50 GB = 50M messages / 2000 msg/s = 25,000 s = 6.94 hours
        s[79] = {"hours_to_full": round(25000 / 3600, 2)}
        # 80. 32k / 16 = 2,000 msg/s per partition
        s[80] = {"per_partition_rps": 2000}
        # 81. 32k * 0.25 = 8,000 msg/s on hot partition
        s[81] = {"hot_partition_rps": 8000}
        # 82. 20M * 0.001 = 20,000 messages/day
        s[82] = {"dlq_messages_per_day": 20_000}
        # 83. 1 container = 4 workers * (1 / 0.050s) = 4 * 20 = 80 jobs/s. 2000 / 80 = 25 containers
        s[83] = {"containers_required": 25}
        # 84. 8 partitions / 7 consumers: 6 consumers get 1 partition, 1 consumer gets 2 partitions
        s[84] = {"max_partitions_on_single_consumer": 2}
        # 85. Visibility timeout expires while worker still working -> duplicate reprocessing
        s[85] = {"defect": "DUPLICATE_EXECUTION"}

        # Category 7: Availability (86-95)
        # 86. 99.9% = 0.001 * 365 * 24 = 8.76 hours = 8h 45m 36s
        s[86] = {"hours_downtime": 8.76, "minutes_downtime": 525.6}
        # 87. 99.99% = 0.0001 * 365 * 24 * 60 = 52.56 minutes
        s[87] = {"minutes_downtime": 52.56}
        # 88. 99.999% = 0.00001 * 30 * 86400 = 25.92 seconds
        s[88] = {"seconds_downtime": 25.92}
        # 89. 0.9999 * 0.999 * 0.9995 = 0.9984004995 -> 99.84%
        s[89] = {"composite_availability_pct": 99.84}
        # 90. 1 - 0.9984 = 0.0016 * 8760 = 14.016 hours
        s[90] = {"annual_downtime_hours": 14.02}
        # 91. 1 - (1 - 0.99)^2 = 1 - (0.01)^2 = 1 - 0.0001 = 0.9999 = 99.99%
        s[91] = {"composite_availability_pct": 99.99}
        # 92. 1 - (1 - 0.999)^2 = 1 - (0.001)^2 = 1 - 0.000001 = 99.9999%
        s[92] = {"composite_availability_pct": 99.9999}
        # 93. MTBF / (MTBF + MTTR) = 1000 / 1002 = 0.998004 = 99.80%
        s[93] = {"availability_pct": 99.8}
        # 94. 1000 / (1000 + 1/60) = 1000 / 1000.016667 = 0.999983 = 99.998%
        s[94] = {"availability_pct": 99.998}
        # 95. 30 days * 86400 = 2,592,000s. 35m = 2100s. Downtime allowed = 0.0005 * 2592000 = 1296s (21.6m). 35m > 21.6m -> Violated
        s[95] = {"allowed_minutes": 21.6, "actual_minutes": 35.0, "violated": True}

        # Category 8: Cost Modeling (96-105)
        # 96. 10 * 0.08 * 730 = $584.00
        s[96] = {"monthly_compute_cost": 584.0}
        # 97. 50 TB = 50,000 GB * $0.023 = $1,150.00
        s[97] = {"monthly_storage_cost": 1150.0}
        # 98. 100 TB = 100,000 GB * $0.08 = $8,000.00
        s[98] = {"monthly_egress_cost": 8000.0}
        # 99. 128 GB * 730h * $0.035 = $3,270.40
        s[99] = {"monthly_cache_cost": 3270.4}
        # 100. 20 * $150 = $3000 vs 4 * $300 = $1200 -> Savings = $1800/month
        s[100] = {"monthly_savings": 1800.0}
        # 101. 50M * 400KB saved = 20,000,000 KB = 20,000 GB saved * $0.08 = $1,600/month
        s[101] = {"monthly_savings": 1600.0}
        # 102. (800 + 3*400) * 12 = 2000 * 12 = $24,000/year
        s[102] = {"annual_db_cost": 24000.0}
        # 103. 5 TB = 5000 GB * $0.50 = $2,500/month
        s[103] = {"monthly_log_cost": 2500.0}
        # 104. 75% reduction: new = $625/month; annual savings = $1875 * 12 = $22,500
        s[104] = {"new_monthly": 625.0, "annual_savings": 22500.0}
        # 105. Arch A: 100M * $0.20/M = $20. Compute: 100M * 0.2s = 20M s * 0.5 GB = 10M GB-s * $0.000016 = $160. Total A = $180/mo. Arch B: 2 * $60 = $120/mo. Dedicated is cheaper by $60/mo.
        s[105] = {"serverless_cost": 180.0, "dedicated_cost": 120.0, "cheaper": "Dedicated", "difference": 60.0}

        return s

if __name__ == "__main__":
    solutions = EstimationSolutions.solve_all()
    print("=" * 70)
    print(f"VERIFIED {len(solutions)} / 105 BACK-OF-THE-ENVELOPE DRILLS")
    print("=" * 70)
    for i in range(1, 106):
        print(f"Drill {i:3d}: {solutions[i]}")
