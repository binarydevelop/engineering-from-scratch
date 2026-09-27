#!/usr/bin/env python3
"""
Capstone 4: Tiny Filesystem (TinyFS)
A complete educational Unix-like filesystem implemented on a virtual block device file.

Disk Layout:
[ Block 0: Superblock ]
[ Block 1: Inode Bitmap ]
[ Block 2: Block Bitmap ]
[ Block 3..10: Inode Table (64 inodes total) ]
[ Block 11..N: Data Blocks (Files & Directory tables) ]
"""

import sys
import os
import struct
from typing import List, Dict, Optional, Tuple

BLOCK_SIZE = 512
NUM_BLOCKS = 128
NUM_INODES = 64
SUPERBLOCK_MAGIC = 0x54494E59  # "TINY"

INODE_TYPE_FREE = 0
INODE_TYPE_FILE = 1
INODE_TYPE_DIR = 2

INODE_SIZE = 64
INODES_PER_BLOCK = BLOCK_SIZE // INODE_SIZE  # 8 inodes per block
INODE_BLOCKS = NUM_INODES // INODES_PER_BLOCK  # 8 blocks (blocks 3..10)
DATA_BLOCK_START = 1 + 1 + 1 + INODE_BLOCKS   # Block 11


class TinyFS:
    def __init__(self, disk_path: str = "virtual_disk.img"):
        self.disk_path = disk_path

    def format(self):
        """Formats the virtual disk image with a clean superblock, bitmaps, and root directory."""
        with open(self.disk_path, "wb") as f:
            f.seek(NUM_BLOCKS * BLOCK_SIZE - 1)
            f.write(b"\0")

        # 1. Superblock (Block 0): magic, block_size, num_blocks, num_inodes, data_start
        sb = struct.pack("<IIIII492x", SUPERBLOCK_MAGIC, BLOCK_SIZE, NUM_BLOCKS, NUM_INODES, DATA_BLOCK_START)
        self._write_block(0, sb)

        # 2. Inode Bitmap (Block 1): Mark Inode 0 (root dir) as used
        inode_bitmap = bytearray(BLOCK_SIZE)
        inode_bitmap[0] = 0x01
        self._write_block(1, bytes(inode_bitmap))

        # 3. Block Bitmap (Block 2): Mark metadata blocks (0..10) and Root data block (11) as used
        block_bitmap = bytearray(BLOCK_SIZE)
        for b in range(DATA_BLOCK_START + 1):
            block_bitmap[b] = 1
        self._write_block(2, bytes(block_bitmap))

        # 4. Zero Inode Table (Blocks 3..10)
        zero_inodes = bytes(BLOCK_SIZE * INODE_BLOCKS)
        with open(self.disk_path, "r+b") as f:
            f.seek(3 * BLOCK_SIZE)
            f.write(zero_inodes)

        # 5. Write Inode 0 (Root Directory)
        # Inode struct: type (H), size (I), direct_blocks[4] (4I), padding (46B) = 64B
        root_inode = struct.pack("<HIIIII42x", INODE_TYPE_DIR, 0, DATA_BLOCK_START, 0, 0, 0)
        self._write_inode(0, root_inode)

        # 6. Initialize Root Directory Data Block
        empty_dir = bytes(BLOCK_SIZE)
        self._write_block(DATA_BLOCK_START, empty_dir)
        print(f"TinyFS: Formatted disk '{self.disk_path}' ({NUM_BLOCKS * BLOCK_SIZE // 1024} KB).")

    def _read_block(self, block_num: int) -> bytes:
        with open(self.disk_path, "rb") as f:
            f.seek(block_num * BLOCK_SIZE)
            return f.read(BLOCK_SIZE)

    def _write_block(self, block_num: int, data: bytes):
        assert len(data) == BLOCK_SIZE, f"Block write must be exactly {BLOCK_SIZE} bytes"
        with open(self.disk_path, "r+b") as f:
            f.seek(block_num * BLOCK_SIZE)
            f.write(data)

    def _read_inode(self, inode_idx: int) -> Tuple[int, int, List[int]]:
        block_idx = 3 + (inode_idx // INODES_PER_BLOCK)
        offset = (inode_idx % INODES_PER_BLOCK) * INODE_SIZE
        raw = self._read_block(block_idx)[offset:offset + INODE_SIZE]
        itype, size, b0, b1, b2, b3 = struct.unpack("<HIIIII42x", raw)
        return itype, size, [b0, b1, b2, b3]

    def _write_inode(self, inode_idx: int, inode_bytes: bytes):
        block_idx = 3 + (inode_idx // INODES_PER_BLOCK)
        offset = (inode_idx % INODES_PER_BLOCK) * INODE_SIZE
        block_data = bytearray(self._read_block(block_idx))
        block_data[offset:offset + INODE_SIZE] = inode_bytes
        self._write_block(block_idx, bytes(block_data))

    def _alloc_inode(self) -> int:
        bitmap = bytearray(self._read_block(1))
        for i in range(NUM_INODES):
            if bitmap[i] == 0:
                bitmap[i] = 1
                self._write_block(1, bytes(bitmap))
                return i
        raise OSError("TinyFS: Out of inodes (ENOSPC)")

    def _free_inode(self, inode_idx: int):
        bitmap = bytearray(self._read_block(1))
        bitmap[inode_idx] = 0
        self._write_block(1, bytes(bitmap))
        zero_inode = bytes(INODE_SIZE)
        self._write_inode(inode_idx, zero_inode)

    def _alloc_block(self) -> int:
        bitmap = bytearray(self._read_block(2))
        for b in range(DATA_BLOCK_START, NUM_BLOCKS):
            if bitmap[b] == 0:
                bitmap[b] = 1
                self._write_block(2, bytes(bitmap))
                self._write_block(b, bytes(BLOCK_SIZE))  # Zero block
                return b
        raise OSError("TinyFS: Out of disk space (ENOSPC)")

    def _free_block(self, block_num: int):
        bitmap = bytearray(self._read_block(2))
        bitmap[block_num] = 0
        self._write_block(2, bytes(bitmap))

    def _get_dir_entries(self, dir_inode_idx: int = 0) -> List[Tuple[str, int]]:
        itype, size, blocks = self._read_inode(dir_inode_idx)
        assert itype == INODE_TYPE_DIR
        data = self._read_block(blocks[0])
        entries = []
        # Directory entry: inode_idx (H), name (14s) = 16 bytes. (32 entries per block)
        for i in range(0, BLOCK_SIZE, 16):
            chunk = data[i:i + 16]
            in_idx, raw_name = struct.unpack("<H14s", chunk)
            if in_idx != 0 or raw_name.strip(b"\0") != b"":
                name = raw_name.split(b"\0", 1)[0].decode("utf-8")
                entries.append((name, in_idx))
        return entries

    def _add_dir_entry(self, name: str, inode_idx: int, dir_inode_idx: int = 0):
        itype, size, blocks = self._read_inode(dir_inode_idx)
        data = bytearray(self._read_block(blocks[0]))
        for i in range(0, BLOCK_SIZE, 16):
            in_idx, raw_name = struct.unpack("<H14s", data[i:i + 16])
            if in_idx == 0 and raw_name.strip(b"\0") == b"":
                # Found free slot
                entry = struct.pack("<H14s", inode_idx, name.encode("utf-8"))
                data[i:i + 16] = entry
                self._write_block(blocks[0], bytes(data))
                return
        raise OSError("Directory full")

    def _remove_dir_entry(self, name: str, dir_inode_idx: int = 0) -> int:
        itype, size, blocks = self._read_inode(dir_inode_idx)
        data = bytearray(self._read_block(blocks[0]))
        for i in range(0, BLOCK_SIZE, 16):
            in_idx, raw_name = struct.unpack("<H14s", data[i:i + 16])
            c_name = raw_name.split(b"\0", 1)[0].decode("utf-8")
            if c_name == name:
                data[i:i + 16] = bytes(16)
                self._write_block(blocks[0], bytes(data))
                return in_idx
        raise FileNotFoundError(f"File '{name}' not found")

    def create(self, filename: str):
        in_idx = self._alloc_inode()
        inode_raw = struct.pack("<HIIIII42x", INODE_TYPE_FILE, 0, 0, 0, 0, 0)
        self._write_inode(in_idx, inode_raw)
        self._add_dir_entry(filename, in_idx)
        print(f"TinyFS: Created file '{filename}' (Inode: {in_idx})")

    def write(self, filename: str, content: str):
        entries = self._get_dir_entries(0)
        match = [e for e in entries if e[0] == filename]
        if not match:
            raise FileNotFoundError(f"File '{filename}' not found")
        in_idx = match[0][1]

        itype, size, blocks = self._read_inode(in_idx)
        payload = content.encode("utf-8")
        needed_blocks = (len(payload) + BLOCK_SIZE - 1) // BLOCK_SIZE
        if needed_blocks > 4:
            raise ValueError("File exceeds maximum direct block capacity (2048 bytes)")

        allocated_blocks = []
        for i in range(needed_blocks):
            b = self._alloc_block()
            chunk = payload[i * BLOCK_SIZE:(i + 1) * BLOCK_SIZE]
            padded_chunk = chunk.ljust(BLOCK_SIZE, b"\0")
            self._write_block(b, padded_chunk)
            allocated_blocks.append(b)

        while len(allocated_blocks) < 4:
            allocated_blocks.append(0)

        # Update inode
        new_inode = struct.pack("<HIIIII42x", INODE_TYPE_FILE, len(payload), *allocated_blocks)
        self._write_inode(in_idx, new_inode)
        print(f"TinyFS: Wrote {len(payload)} bytes to '{filename}' across {needed_blocks} block(s).")

    def read(self, filename: str) -> str:
        entries = self._get_dir_entries(0)
        match = [e for e in entries if e[0] == filename]
        if not match:
            raise FileNotFoundError(f"File '{filename}' not found")
        in_idx = match[0][1]

        itype, size, blocks = self._read_inode(in_idx)
        data = bytearray()
        bytes_left = size
        for b in blocks:
            if b == 0 or bytes_left <= 0:
                break
            raw = self._read_block(b)
            to_read = min(bytes_left, BLOCK_SIZE)
            data.extend(raw[:to_read])
            bytes_left -= to_read

        return data.decode("utf-8")

    def ls(self) -> List[Dict]:
        entries = self._get_dir_entries(0)
        report = []
        for name, in_idx in entries:
            itype, size, blocks = self._read_inode(in_idx)
            t_str = "DIR" if itype == INODE_TYPE_DIR else "FILE"
            report.append({"name": name, "inode": in_idx, "type": t_str, "size": size, "blocks": [b for b in blocks if b > 0]})
        return report

    def delete(self, filename: str):
        in_idx = self._remove_dir_entry(filename, 0)
        itype, size, blocks = self._read_inode(in_idx)
        for b in blocks:
            if b > 0:
                self._free_block(b)
        self._free_inode(in_idx)
        print(f"TinyFS: Deleted '{filename}' (Freed Inode {in_idx})")


if __name__ == "__main__":
    fs = TinyFS("test_virtual_disk.img")
    fs.format()

    fs.create("hello.txt")
    fs.write("hello.txt", "Operating Systems From Scratch: Filesystem Capstone!")
    print(f"Content of 'hello.txt': \"{fs.read('hello.txt')}\"")

    fs.create("data.json")
    fs.write("data.json", '{"status": "ok", "fs": "tinyfs"}')

    print("\nDirectory Listing (ls):")
    for item in fs.ls():
        print(f"  [{item['type']:<4}] {item['name']:<12} Size: {item['size']:<4} Inode: {item['inode']} Blocks: {item['blocks']}")

    print("\nDeleting 'hello.txt'...")
    fs.delete("hello.txt")
    print("Listing after deletion:")
    for item in fs.ls():
        print(f"  [{item['type']:<4}] {item['name']:<12} Size: {item['size']:<4} Inode: {item['inode']}")

    if os.path.exists("test_virtual_disk.img"):
        os.remove("test_virtual_disk.img")
