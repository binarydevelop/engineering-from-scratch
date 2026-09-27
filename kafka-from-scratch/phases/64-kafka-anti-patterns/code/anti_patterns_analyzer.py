#!/usr/bin/env python3
def analyze_anti_patterns():
    print("=== The 14 Catastrophic Kafka Anti-Patterns ===\n")
    patterns = [
        ("1. Single Partition Bottleneck", "Expecting 100k msgs/s on 1 partition", "Size partitions based on throughput math (Phase 47)."),
        ("2. Unkeyed Causal Events", "Sending banking/order updates without keys", "Key events by entity ID to preserve partition order (Phase 08)."),
        ("3. Commit Before Processing", "Committing offset before DB write commits", "Process first, commit second (At-Least-Once) + Idempotency (Phase 14)."),
        ("4. Commit Per Record", "Calling commitSync() after every single msg", "Batch commits at end of poll loop (Phase 13)."),
        ("5. Ignoring Consumer Lag", "No alerting on unread record growth", "Alert on Consumer Lag before disk saturation (Phase 31)."),
        ("6. acks=all with min_isr=1", "Believing acks=all prevents loss alone", "Set min.insync.replicas=2 on 3-replica topics (Phase 23)."),
        ("7. Giant Payloads (20 MB)", "Sending raw video/PDF files through Kafka", "Apply the Claim-Check Pattern with Object Storage (Phase 45)."),
        ("8. Silent Dead-Letter Queue", "Quarantining poison pills with no alerts", "DLT must trigger PagerDuty alerts for triage (Phase 44)."),
        ("9. Sync Request-Reply", "Forcing synchronous RPC patterns onto Kafka", "Use gRPC or REST for synchronous workflows (Phase 63)."),
        ("10. Partition Explosion", "5,000 tiny topics on 3 small brokers", "Consolidate event streams; avoid micro-partitioning (Phase 47)."),
        ("11. Non-Idempotent Consumer", "Charging credit cards without event_id check", "Implement idempotency store in database transaction (Phase 15)."),
        ("12. Auto Topic Creation", "Typos create unintended 1-partition topics", "Disable auto.create.topics.enable in broker config (Phase 05)."),
        ("13. In-Process Sleep Retries", "time.sleep(60) inside poll loop", "Use non-blocking Retry Topics with backoff (Phase 43)."),
        ("14. Assuming Global EOS", "Believing Kafka EOS protects Postgres/Stripe", "Understand Kafka EOS boundaries; use Outbox pattern (Phase 36/60).")
    ]
    for title, err, fix in patterns:
        print(f"❌ {title:<32}")
        print(f"   Mistake: {err}")
        print(f"   Fix:     {fix}\n")

if __name__ == "__main__":
    analyze_anti_patterns()
