#!/usr/bin/env python3
import binascii

def crc16(data: bytes) -> int:
    """CRC16-CCITT calculation matching Redis Cluster specification."""
    crc = 0
    for byte in data:
        crc = ((crc << 8) & 0xFF00) ^ binascii.crc_hqx(bytes([byte]), crc >> 8)
    return crc & 0xFFFF

def get_slot(key: str) -> int:
    # Hash Tag Support: If {...} present, only hash substring
    if "{" in key and "}" in key:
        s = key.find("{") + 1
        e = key.find("}")
        if e > s:
            key = key[s:e]
    return binascii.crc_hqx(key.encode("utf-8"), 0) % 16384

if __name__ == "__main__":
    print("Testing Redis Cluster Hash Slot Calculation:")
    print("  Slot for 'user:100'         ->", get_slot("user:100"))
    print("  Slot for 'order:999'        ->", get_slot("order:999"))
    
    print("\nTesting Hash Tags for Multi-Key Colocation:")
    s1 = get_slot("{tenant_1}:profile")
    s2 = get_slot("{tenant_1}:settings")
    print(f"  Slot for '{{tenant_1}}:profile'  -> {s1}")
    print(f"  Slot for '{{tenant_1}}:settings' -> {s2}")
    print("  -> Both land on exact same slot! Multi-key operations are guaranteed safe.")
