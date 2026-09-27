#!/usr/bin/env python3
"""
Filesystem Crash Consistency & Journaling Simulator
Demonstrates the filesystem consistency problem when power fails midway
through multi-block metadata and data writes, and how Journaling (Write-Ahead Logging)
guarantees recovery.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import copy


@dataclass
class DiskState:
    block_bitmap: List[int] = field(default_factory=lambda: [1, 1, 0, 0, 0, 0, 0, 0])
    inode_table: Dict[int, Dict[str, any]] = field(default_factory=lambda: {
        1: {"name": "notes.txt", "size": 0, "blocks": []}
    })
    data_blocks: Dict[int, str] = field(default_factory=dict)
    journal_log: List[Dict[str, any]] = field(default_factory=list)


def naive_append_file(disk: DiskState, inode_id: int, block_id: int, content: str, crash_point: int) -> str:
    """
    Append requires 3 writes:
    Write 1: Write Data Block
    Write 2: Update Inode
    Write 3: Update Block Bitmap
    crash_point: 0 (no crash), 1 (crash after W1), 2 (crash after W2), 3 (crash after W3)
    """
    state = copy.deepcopy(disk)

    # Write 1: Data Block
    state.data_blocks[block_id] = content
    if crash_point == 1:
        return "CRASH after Write 1 (Data Block written, Inode and Bitmap untouched). Result: Leaked unreferenced data block."

    # Write 2: Inode update
    state.inode_table[inode_id]["size"] += len(content)
    state.inode_table[inode_id]["blocks"].append(block_id)
    if crash_point == 2:
        return "CRASH after Write 2 (Inode points to block, but Bitmap marks it FREE!). Result: FATAL CORRUPTION - Next write will overwrite this file's data!"

    # Write 3: Bitmap update
    state.block_bitmap[block_id] = 1
    if crash_point == 3:
        return "CRASH after Write 3 (All 3 writes committed successfully before crash)."

    return "All writes completed normally."


def journaled_append_file(disk: DiskState, inode_id: int, block_id: int, content: str, crash_point: int) -> Tuple[DiskState, str]:
    """
    Journaling (WAL):
    Step 1: Write TxBegin & Desired Changes to Journal
    Step 2: Write TxCommit to Journal (the commit point!)
    Step 3: Checkpoint to actual FS tables
    """
    state = copy.deepcopy(disk)

    # 1. Journal Transaction Descriptor
    tx = {
        "tx_id": 101,
        "committed": False,
        "changes": {
            "data_block": (block_id, content),
            "inode_update": (inode_id, block_id, len(content)),
            "bitmap_update": (block_id, 1)
        }
    }
    state.journal_log.append(tx)
    if crash_point == 1:
        # Crash before commit
        recovered_state = journal_recover(state)
        return recovered_state, "CRASH before journal TxCommit. Recovery: Transaction discarded (atomicity preserved, zero corruption)."

    # 2. TxCommit
    tx["committed"] = True
    if crash_point == 2:
        # Crash right after commit, before checkpointing
        recovered_state = journal_recover(state)
        return recovered_state, "CRASH after journal TxCommit, before checkpointing. Recovery: Journal replayed! All updates restored cleanly."

    # 3. Checkpoint to disk
    state.data_blocks[block_id] = content
    state.inode_table[inode_id]["size"] += len(content)
    state.inode_table[inode_id]["blocks"].append(block_id)
    state.block_bitmap[block_id] = 1
    state.journal_log.clear()  # Checkpoint complete, clear journal

    return state, "Normal execution: Transaction committed and checkpointed successfully."


def journal_recover(state: DiskState) -> DiskState:
    recovered = copy.deepcopy(state)
    for tx in recovered.journal_log:
        if tx["committed"]:
            # Replay transaction (redo logging)
            changes = tx["changes"]
            b_id, content = changes["data_block"]
            in_id, in_block, length = changes["inode_update"]
            bm_id, val = changes["bitmap_update"]

            recovered.data_blocks[b_id] = content
            recovered.inode_table[in_id]["size"] += length
            if in_block not in recovered.inode_table[in_id]["blocks"]:
                recovered.inode_table[in_id]["blocks"].append(in_block)
            recovered.block_bitmap[bm_id] = val
        else:
            # Uncommitted transaction, discard
            pass
    recovered.journal_log.clear()
    return recovered


if __name__ == "__main__":
    initial_disk = DiskState()
    print("================================================================")
    print("Filesystem Crash Consistency & Journaling Simulation")
    print("================================================================\n")

    print("[1] Naive Filesystem (No Journal):")
    print("Scenario A: Power fails after Data Write:")
    print("  ->", naive_append_file(initial_disk, inode_id=1, block_id=2, content="Hello OS!", crash_point=1))
    print("Scenario B: Power fails after Inode Write, before Bitmap:")
    print("  ->", naive_append_file(initial_disk, inode_id=1, block_id=2, content="Hello OS!", crash_point=2))

    print("\n[2] Journaling Filesystem (With WAL):")
    _, msg1 = journaled_append_file(initial_disk, inode_id=1, block_id=2, content="Hello OS!", crash_point=1)
    print("Scenario A: Power fails before TxCommit:")
    print("  ->", msg1)

    rec_disk, msg2 = journaled_append_file(initial_disk, inode_id=1, block_id=2, content="Hello OS!", crash_point=2)
    print("Scenario B: Power fails after TxCommit (during checkpointing):")
    print("  ->", msg2)
    print(f"  Verified State after Recovery: Inode blocks = {rec_disk.inode_table[1]['blocks']}, Bitmap = {rec_disk.block_bitmap[:4]}")
