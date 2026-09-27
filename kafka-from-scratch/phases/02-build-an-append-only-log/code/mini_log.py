#!/usr/bin/env python3
import struct
import os
from pathlib import Path

class MiniLog:
    """
    A first-principles append-only log on disk.
    Record Format on Disk:
      [8 bytes: monotonic offset (uint64)]
      [4 bytes: payload length (uint32)]
      [N bytes: raw payload]
    """
    HEADER_FORMAT = ">QI" # 8-byte unsigned long long, 4-byte unsigned int
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.file = open(filepath, "a+b")
        self.next_offset = self._recover_next_offset()

    def _recover_next_offset(self) -> int:
        self.file.seek(0, os.SEEK_END)
        size = self.file.tell()
        if size == 0:
            return 0
        # Scan headers to find last offset
        self.file.seek(0, os.SEEK_SET)
        last_offset = -1
        while True:
            header_bytes = self.file.read(self.HEADER_SIZE)
            if len(header_bytes) < self.HEADER_SIZE:
                break
            offset, length = struct.unpack(self.HEADER_FORMAT, header_bytes)
            last_offset = offset
            self.file.seek(length, os.SEEK_CUR) # Skip payload
        return last_offset + 1

    def append(self, payload: bytes) -> int:
        offset = self.next_offset
        header = struct.pack(self.HEADER_FORMAT, offset, len(payload))
        self.file.seek(0, os.SEEK_END)
        self.file.write(header + payload)
        self.file.flush() # Ensure flush to OS buffer
        self.next_offset += 1
        return offset

    def read_from(self, start_offset: int = 0):
        """Sequentially reads records starting from start_offset."""
        self.file.seek(0, os.SEEK_SET)
        records = []
        while True:
            header_bytes = self.file.read(self.HEADER_SIZE)
            if len(header_bytes) < self.HEADER_SIZE:
                break
            offset, length = struct.unpack(self.HEADER_FORMAT, header_bytes)
            payload = self.file.read(length)
            if offset >= start_offset:
                records.append((offset, payload))
        return records

    def close(self):
        self.file.close()

if __name__ == "__main__":
    log_path = "/tmp/test_mini_log.dat"
    if os.path.exists(log_path):
        os.remove(log_path)

    log = MiniLog(log_path)
    print("Appending events...")
    off0 = log.append(b"user-created:alice")
    off1 = log.append(b"email-sent:alice@example.com")
    off2 = log.append(b"payment-started:amount=50")
    off3 = log.append(b"payment-completed:amount=50")

    print(f"Appended 4 records. Next offset will be: {log.next_offset}")
    log.close()

    # Re-open and read from offset 2
    log_reader = MiniLog(log_path)
    print("\nReading from offset 2:")
    for offset, data in log_reader.read_from(2):
        print(f"  Offset {offset}: {data.decode()}")
    log_reader.close()
