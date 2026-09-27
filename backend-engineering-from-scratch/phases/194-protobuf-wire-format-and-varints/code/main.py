"""
Lesson 194: Protocol Buffers Wire Format and Varints
Implements pure Python LEB128 Varint encoding, ZigZag encoding, and tag header packing.
"""
from typing import Dict, Any, Tuple

class PhaseComponent:
    def __init__(self):
        self.name = "Protocol Buffers Wire Format and Varints"
        self.metrics = {"operations_total": 0, "errors_total": 0}

    @staticmethod
    def encode_varint(value: int) -> bytes:
        """LEB128 varint encoding: 7 data bits per byte with MSB continuation bit."""
        out = bytearray()
        while value > 0x7F:
            out.append((value & 0x7F) | 0x80)
            value >>= 7
        out.append(value & 0x7F)
        return bytes(out)

    @staticmethod
    def decode_varint(buffer: bytes) -> Tuple[int, int]:
        """Decodes LEB128 varint, returning (value, bytes_read)."""
        res = 0
        shift = 0
        for i, byte in enumerate(buffer):
            res |= (byte & 0x7F) << shift
            if not (byte & 0x80):
                return res, i + 1
            shift += 7
        raise ValueError("Buffer ended without terminating varint")

    @staticmethod
    def zigzag_encode(n: int) -> int:
        """ZigZag maps signed integers to unsigned: 0=0, -1=1, 1=2, -2=3."""
        return (n << 1) ^ (n >> 63)

    @staticmethod
    def make_tag(field_number: int, wire_type: int) -> int:
        """Key = (field_number << 3) | wire_type."""
        return (field_number << 3) | wire_type

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.metrics["operations_total"] += 1
        if not isinstance(payload, dict):
            self.metrics["errors_total"] += 1
            raise ValueError("Payload must be a dictionary")
        if payload.get("trigger_error"):
            self.metrics["errors_total"] += 1
            raise RuntimeError("Varint serialization error")

        num = payload.get("value", 300)
        encoded = self.encode_varint(num)
        decoded, length = self.decode_varint(encoded)

        return {
            "status": "success",
            "phase": 194,
            "original": num,
            "encoded_hex": encoded.hex(),
            "bytes_used": length,
            "decoded": decoded
        }

    def get_telemetry(self) -> Dict[str, Any]:
        return {"component": self.name, "metrics": self.metrics}
