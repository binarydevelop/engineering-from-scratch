"""
Lesson 198: Storage Engine Write-Ahead Log
Implements binary WAL format with CRC32 checksum verification and crash recovery replay.
"""
from typing import Dict, Any, List, Tuple
import zlib
import struct

class PhaseComponent:
    def __init__(self):
        self.name = "Storage Engine Write-Ahead Log"
        self.wal_entries: List[bytes] = []
        self.metrics = {"operations_total": 0, "errors_total": 0, "replays_total": 0}

    @staticmethod
    def serialize_record(key: str, value: str) -> bytes:
        """Format: CRC32(4 bytes) + KeyLen(2 bytes) + ValLen(4 bytes) + Key + Value."""
        k_bytes = key.encode("utf-8")
        v_bytes = value.encode("utf-8")
        body = struct.pack(">HI", len(k_bytes), len(v_bytes)) + k_bytes + v_bytes
        crc = zlib.crc32(body)
        return struct.pack(">I", crc) + body

    @staticmethod
    def deserialize_record(data: bytes) -> Tuple[str, str]:
        expected_crc = struct.unpack_from(">I", data, 0)[0]
        body = data[4:]
        actual_crc = zlib.crc32(body)
        if expected_crc != actual_crc:
            raise ValueError("WAL record CRC checksum mismatch! Data corruption detected.")
        k_len, v_len = struct.unpack_from(">HI", body, 0)
        key = body[6:6+k_len].decode("utf-8")
        value = body[6+k_len:6+k_len+v_len].decode("utf-8")
        return key, value

    def append(self, key: str, value: str) -> bytes:
        rec = self.serialize_record(key, value)
        self.wal_entries.append(rec)
        return rec

    def replay(self) -> Dict[str, str]:
        """Reconstructs state machine by replaying WAL."""
        state = {}
        for rec in self.wal_entries:
            k, v = self.deserialize_record(rec)
            state[k] = v
        self.metrics["replays_total"] += 1
        return state

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.metrics["operations_total"] += 1
        if not isinstance(payload, dict):
            self.metrics["errors_total"] += 1
            raise ValueError("Payload must be a dictionary")
        if payload.get("trigger_error"):
            self.metrics["errors_total"] += 1
            raise RuntimeError("WAL disk I/O error")

        k = payload.get("key", "user_101")
        v = payload.get("value", "active")
        rec = self.append(k, v)

        return {
            "status": "success",
            "phase": 198,
            "record_size_bytes": len(rec),
            "total_wal_records": len(self.wal_entries)
        }

    def get_telemetry(self) -> Dict[str, Any]:
        return {"component": self.name, "metrics": self.metrics}
