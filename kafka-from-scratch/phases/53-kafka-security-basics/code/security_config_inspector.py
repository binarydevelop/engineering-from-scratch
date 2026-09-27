#!/usr/bin/env python3
def explain_kafka_security():
    print("=== Apache Kafka Production Security Architecture ===\n")
    protocols = [
        ("PLAINTEXT", "No encryption, no authentication. (Local lab only!)"),
        ("SSL / TLS", "Wire encryption via TLS. Optional client certificate authentication (mTLS)."),
        ("SASL_PLAINTEXT", "Authentication via SASL (SCRAM/Kerberos), but wire bytes unencrypted."),
        ("SASL_SSL", "GOLD STANDARD: Full TLS wire encryption + SASL identity authentication.")
    ]
    for proto, desc in protocols:
        print(f" {proto:<16}: {desc}")

    print("\nSample Kafka ACL Definition:")
    print("  Principal: User:order-fulfillment-service")
    print("  Resource:  Topic:orders")
    print("  Operation: READ")
    print("  Permission: ALLOW")

if __name__ == "__main__":
    explain_kafka_security()
