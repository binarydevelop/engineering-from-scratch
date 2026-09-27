#!/usr/bin/env python3
def classify_producer_errors():
    print("=== Producer Error Classification Matrix ===\n")
    retriable = [
        ("NotLeaderOrFollowerException", "Partition leader is failing over; new leader will be elected shortly."),
        ("LeaderNotAvailableException", "Leader election currently in progress; wait for metadata refresh."),
        ("NetworkException", "Socket connection dropped; client will reconnect."),
        ("NotEnoughReplicasException", "Broker temporarily lagging; will retry until ISR catches up.")
    ]
    fatal = [
        ("RecordTooLargeException", "Payload exceeds max.message.bytes. Retrying will never help!"),
        ("SerializationException", "Data does not match schema or serializer format."),
        ("TopicAuthorizationException", "Client credentials lack WRITE permission on target topic."),
        ("UnknownTopicOrPartitionException", "Topic does not exist and auto-creation is disabled.")
    ]

    print("--- 1. RETRIABLE ERRORS (Client auto-heals via retries) ---")
    for name, desc in retriable:
        print(f" [RETRIABLE] {name:<32}: {desc}")

    print("\n--- 2. FATAL ERRORS (Immediate Application Failure / Alert) ---")
    for name, desc in fatal:
        print(f" [FATAL]     {name:<32}: {desc}")

if __name__ == "__main__":
    classify_producer_errors()
