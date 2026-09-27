"""
Lesson 195: HTTP/2 Framing and Stream Multiplexing
Implements 9-byte HTTP/2 binary frame header encoding and stream demultiplexing.
"""
from typing import Dict, Any, List, Tuple
import struct

FRAME_TYPE_DATA = 0x0
FRAME_TYPE_HEADERS = 0x1
FRAME_TYPE_SETTINGS = 0x4

class PhaseComponent:
    def __init__(self):
        self.name = "HTTP/2 Framing and Stream Multiplexing"
        self.active_streams: Dict[int, List[bytes]] = {}
        self.metrics = {"operations_total": 0, "errors_total": 0, "frames_processed": 0}

    @staticmethod
    def pack_frame_header(length: int, frame_type: int, flags: int, stream_id: int) -> bytes:
        """Packs HTTP/2 9-byte header: Length (24-bit), Type (8-bit), Flags (8-bit), Stream ID (31-bit)."""
        header = bytearray(9)
        header[0] = (length >> 16) & 0xFF
        header[1] = (length >> 8) & 0xFF
        header[2] = length & 0xFF
        header[3] = frame_type & 0xFF
        header[4] = flags & 0xFF
        struct.pack_into(">I", header, 5, stream_id & 0x7FFFFFFF)
        return bytes(header)

    @staticmethod
    def unpack_frame_header(header: bytes) -> Tuple[int, int, int, int]:
        if len(header) < 9:
            raise ValueError("HTTP/2 frame header must be 9 bytes")
        length = (header[0] << 16) | (header[1] << 8) | header[2]
        frame_type = header[3]
        flags = header[4]
        stream_id = struct.unpack_from(">I", header, 5)[0] & 0x7FFFFFFF
        return length, frame_type, flags, stream_id

    def demux_frame(self, stream_id: int, payload: bytes):
        if stream_id not in self.active_streams:
            self.active_streams[stream_id] = []
        self.active_streams[stream_id].append(payload)
        self.metrics["frames_processed"] += 1

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.metrics["operations_total"] += 1
        if not isinstance(payload, dict):
            self.metrics["errors_total"] += 1
            raise ValueError("Payload must be a dictionary")
        if payload.get("trigger_error"):
            self.metrics["errors_total"] += 1
            raise RuntimeError("Corrupt frame header")

        stream_id = payload.get("stream_id", 1)
        data = payload.get("data", "hello").encode("utf-8")
        header = self.pack_frame_header(len(data), FRAME_TYPE_DATA, 0, stream_id)
        l, t, f, s = self.unpack_frame_header(header)
        self.demux_frame(s, data)

        return {
            "status": "success",
            "phase": 195,
            "stream_id": s,
            "header_hex": header.hex(),
            "payload_len": l,
            "active_streams_count": len(self.active_streams)
        }

    def get_telemetry(self) -> Dict[str, Any]:
        return {"component": self.name, "metrics": self.metrics}
