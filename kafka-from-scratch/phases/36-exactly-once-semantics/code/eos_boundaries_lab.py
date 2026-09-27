#!/usr/bin/env python3
def explain_eos_boundaries():
    print("=== The Reality of Exactly-Once Semantics (EOS) ===\n")
    print("1. Kafka-to-Kafka Stream:")
    print("   Input Topic -> Stream Processor -> Output Topic")
    print("   Guarantee: EXACTLY-ONCE (via Idempotent Producer + Transactions)\n")

    print("2. Kafka to External Non-Transactional API:")
    print("   Input Topic -> Consumer -> HTTP POST https://api.stripe.com/charges")
    print("   Guarantee: AT-LEAST-ONCE (Network can drop response after card charged!)")
    print("   Solution: Must send Idempotency-Key header to external API!\n")

    print("3. Kafka to SQL Database:")
    print("   Input Topic -> Consumer -> INSERT INTO orders VALUES (...)")
    print("   Guarantee: AT-LEAST-ONCE (Crash between DB commit and Kafka offset commit!)")
    print("   Solution: Idempotent Consumer (Phase 15) or Outbox Pattern (Phase 60)!\n")

if __name__ == "__main__":
    explain_eos_boundaries()
