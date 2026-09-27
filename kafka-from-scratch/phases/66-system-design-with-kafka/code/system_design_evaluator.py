#!/usr/bin/env python3
def display_20_questions():
    print("=== The 20-Question Kafka System Design Interrogation Framework ===\n")
    questions = [
        ("1. Why Kafka?", "Why not direct REST/gRPC or SQS? (Decoupling, replay, fanout, throughput)"),
        ("2. Topic Design", "Single fat topic vs multiple fine-grained topics?"),
        ("3. Partition Key", "What entity ID determines partition routing?"),
        ("4. Ordering Requirement", "Per-entity ordering vs global ordering vs no ordering?"),
        ("5. Expected Peak Load", "Records/sec and MB/sec throughput?"),
        ("6. Record Size", "Average and max byte size? (Apply claim-check if > 500KB)"),
        ("7. Retention Policy", "Time-based (days) or size-based (GB)?"),
        ("8. Log Compaction", "Does this represent state (compact) or event history (delete)?"),
        ("9. Replication Factor", "Standard 3 for production?"),
        ("10. min.insync.replicas", "Set to 2 to protect against data loss under acks=all?"),
        ("11. Producer Acks", "acks=all for zero loss, or acks=1 for telemetry?"),
        ("12. Consumer Group Sizing", "How many partitions needed to support required consumer concurrency?"),
        ("13. Retry Architecture", "In-process retries vs dedicated Retry Topics?"),
        ("14. Consumer Idempotency", "How does the consumer deduplicate At-Least-Once redeliveries?"),
        ("15. Lag Tolerance SLA", "How many minutes of lag is acceptable before alerting on-call?"),
        ("16. Failure Modes", "What happens when leader dies? What happens when consumer stalls?"),
        ("17. Replay Strategy", "Will consumers ever need to rewind offsets to rebuild state?"),
        ("18. Schema Contract", "Protobuf, Avro, or JSON Schema with backward compatibility?"),
        ("19. Security Controls", "SASL_SSL + ACLs + TLS wire encryption?"),
        ("20. Simpler Alternatives", "Could Postgres + Redis have solved this with 1/10th the complexity?")
    ]
    for q, desc in questions:
        print(f"{q:<28} : {desc}")

if __name__ == "__main__":
    display_20_questions()
