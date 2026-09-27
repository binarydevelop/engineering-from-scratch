#!/usr/bin/env python3
"""
projects/04-task-queue/worker_queue.py — Durable Background Worker Pipeline with Redis Streams

Demonstrates:
1. Producer publishing jobs to a Stream (XADD)
2. Consumer Groups with multiple workers (XGROUP, XREADGROUP)
3. Explicit acknowledgment (XACK)
4. Worker crash simulation leaving jobs in the Pending Entries List (PEL)
5. Dead-letter recovery worker claiming abandoned tasks (XPENDING, XCLAIM)
"""

import socket
import time
import json
import random

REDIS_HOST = "localhost"
REDIS_PORT = 6379

def redis_cmd(*args):
    s = socket.create_connection((REDIS_HOST, REDIS_PORT), timeout=3.0)
    msg = f"*{len(args)}\r\n"
    for arg in args:
        s_arg = str(arg)
        msg += f"${len(s_arg.encode('utf-8'))}\r\n{s_arg}\r\n"
    s.sendall(msg.encode("utf-8"))
    
    chunks = []
    while True:
        data = s.recv(4096)
        if not data: break
        chunks.append(data)
        if len(data) < 4096: break
    s.close()
    return b"".join(chunks).decode("utf-8", errors="replace")

STREAM_KEY = "stream:email_tasks"
GROUP_NAME = "email_workers"

def init_stream():
    # Create stream & group if not exists
    res = redis_cmd("XGROUP", "CREATE", STREAM_KEY, GROUP_NAME, "0", "MKSTREAM")
    if "BUSYGROUP" not in res:
        print(f"Created Consumer Group '{GROUP_NAME}' on stream '{STREAM_KEY}'.")

def produce_task(task_type, recipient, payload):
    task_json = json.dumps(payload)
    raw = redis_cmd("XADD", STREAM_KEY, "*", "type", task_type, "recipient", recipient, "data", task_json)
    msg_id = raw.strip().split("\r\n")[-1]
    return msg_id

def parse_stream_entries(raw_resp):
    """Parses raw RESP stream output into structured (msg_id, fields_dict) list."""
    lines = [l for l in raw_resp.split("\r\n") if l and not l.startswith("*") and not l.startswith("$")]
    entries = []
    # Lines contain nested stream response
    for i, line in enumerate(lines):
        if "-" in line and len(line) >= 15: # Looks like stream ID e.g. 1711234567890-0
            msg_id = line
            # Next tokens contain field-value pairs
            field_dict = {}
            for j in range(i+1, min(i+10, len(lines)), 2):
                if j+1 < len(lines) and "-" not in lines[j]:
                    field_dict[lines[j]] = lines[j+1]
            entries.append((msg_id, field_dict))
    return entries

def simulate_pipeline():
    init_stream()

    print("\n--- 1. Producer Enqueuing Tasks ---")
    ids = []
    for i in range(1, 4):
        msg_id = produce_task("WELCOME_EMAIL", f"user{i}@example.com", {"user_id": i, "template": "v2"})
        print(f"  [Producer] Enqueued Task {i} -> Stream ID: {msg_id}")
        ids.append(msg_id)

    print("\n--- 2. Worker Alpha Reading Tasks (and acknowledging) ---")
    raw = redis_cmd("XREADGROUP", "GROUP", GROUP_NAME, "worker-alpha", "COUNT", "1", "STREAMS", STREAM_KEY, ">")
    entries = parse_stream_entries(raw)
    if entries:
        msg_id, fields = entries[0]
        print(f"  [Worker Alpha] Processing Task {msg_id}: {fields}")
        time.sleep(0.1) # Simulate work
        redis_cmd("XACK", STREAM_KEY, GROUP_NAME, msg_id)
        print(f"  [Worker Alpha] Completed and Acknowledged (XACK) {msg_id}")

    print("\n--- 3. Worker Beta Reading Task and CRASHING Before Acknowledgment ---")
    raw = redis_cmd("XREADGROUP", "GROUP", GROUP_NAME, "worker-beta", "COUNT", "1", "STREAMS", STREAM_KEY, ">")
    entries = parse_stream_entries(raw)
    if entries:
        crashed_id, fields = entries[0]
        print(f"  [Worker Beta] Picked up Task {crashed_id}: {fields}")
        print(f"  💥 [Worker Beta] Simulating FATAL PROCESS CRASH (SIGKILL) before sending XACK!")

    print("\n--- 4. Inspecting Pending Entries List (PEL) ---")
    pel = redis_cmd("XPENDING", STREAM_KEY, GROUP_NAME)
    print(f"  PEL Status Summary:\n  {pel.strip()}")

    print("\n--- 5. Supervisor / Sentinel Claiming Abandoned Task ---")
    print(f"  [Supervisor] Claiming crashed task {crashed_id} from worker-beta to supervisor-node...")
    # Claim message if idle for > 0ms
    claim_resp = redis_cmd("XCLAIM", STREAM_KEY, GROUP_NAME, "supervisor-node", "0", crashed_id)
    print(f"  [Supervisor] Task re-assigned. Completing and sending XACK...")
    redis_cmd("XACK", STREAM_KEY, GROUP_NAME, crashed_id)
    print(f"  ✓ Abandoned task {crashed_id} successfully recovered and acknowledged!")

    print("\n--- 6. Verification: Final PEL Status ---")
    final_pel = redis_cmd("XPENDING", STREAM_KEY, GROUP_NAME)
    print(f"  Remaining Pending Tasks:\n  {final_pel.strip()}")

if __name__ == "__main__":
    simulate_pipeline()
