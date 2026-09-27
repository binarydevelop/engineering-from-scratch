#!/usr/bin/env python3
import os
import uuid
import hashlib
import json
from pathlib import Path

STORAGE_DIR = Path("/tmp/claim_check_storage")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

def upload_large_payload(payload_bytes: bytes) -> str:
    blob_id = str(uuid.uuid4())
    blob_path = STORAGE_DIR / f"{blob_id}.bin"
    with open(blob_path, "wb") as f:
        f.write(payload_bytes)
    return str(blob_path)

def produce_claim_check(payload_bytes: bytes) -> dict:
    # 1. Upload heavy data to external storage
    blob_uri = upload_large_payload(payload_bytes)
    sha256 = hashlib.sha256(payload_bytes).hexdigest()
    
    # 2. Craft lightweight Kafka event
    kafka_event = {
        "event_type": "DocumentGenerated",
        "blob_uri": blob_uri,
        "size_bytes": len(payload_bytes),
        "sha256": sha256
    }
    return kafka_event

if __name__ == "__main__":
    # Simulate 5 MB PDF document
    large_pdf_data = b"%PDF-1.4 " + (b"X" * (5 * 1024 * 1024))
    print(f"Original Payload Size: {len(large_pdf_data) / (1024*1024):.1f} MB")

    event = produce_claim_check(large_pdf_data)
    event_json = json.dumps(event)
    print(f"Kafka Event Size:      {len(event_json)} bytes")
    print(f"\nEvent published to Kafka:\n{json.dumps(event, indent=2)}")
    print(f"\nStorage Efficiency: {(1 - len(event_json)/len(large_pdf_data))*100:.4f}% reduction on Kafka wire!")
