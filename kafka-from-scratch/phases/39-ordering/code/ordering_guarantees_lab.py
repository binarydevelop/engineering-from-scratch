#!/usr/bin/env python3
import time
from collections import defaultdict

def test_ordering():
    print("--- 1. Producing WITH Key (Targeting Same Partition) ---")
    account_partition = 1
    partition_log = []
    
    events = ["DEPOSIT_100", "WITHDRAW_80", "WITHDRAW_50"]
    for off, ev in enumerate(events):
        partition_log.append((off, ev))
        print(f" Partition {account_partition} | Offset {off}: {ev}")

    print("\nConsumer processing order:")
    balance = 0
    for off, ev in partition_log:
        if ev == "DEPOSIT_100": balance += 100
        elif ev == "WITHDRAW_80": balance -= 80
        elif ev == "WITHDRAW_50":
            if balance >= 50: balance -= 50
            else: print("  [DECLINED] Insufficient funds!")
        print(f"  Processed {ev} -> Current Balance: ${balance}")

if __name__ == "__main__":
    test_ordering()
