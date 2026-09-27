#!/usr/bin/env python3
def evaluate_scenarios():
    print("=== Architectural Fit Evaluation: Is Kafka the Right Tool? ===\n")
    scenarios = [
        ("Task: Send 50 password reset emails per day", "WRONG TOOL", "Use AWS SES / SQS or background worker. Kafka is extreme overkill."),
        ("Task: Real-time fraud detection on 50,000 credit card txns/sec with replay", "PERFECT FIT", "Kafka's partitioned log, acks=all, and multi-consumer fanout shine here."),
        ("Task: Key-value lookup for user profile by user_id", "WRONG TOOL", "Kafka is an append-only log. Use Redis or Postgres."),
        ("Task: Synchronous checkout payment authorization", "WRONG TOOL", "Use direct gRPC/REST. Kafka adds async complexity to synchronous flows."),
        ("Task: CDC event stream from Postgres to Elastic, Redis, and Data Lake", "PERFECT FIT", "Kafka is the ideal central nervous system for change data capture.")
    ]
    for task, verdict, reason in scenarios:
        print(f"Scenario: {task}")
        print(f" Verdict: [{verdict}] -> {reason}\n")

if __name__ == "__main__":
    evaluate_scenarios()
