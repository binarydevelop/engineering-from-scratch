#!/usr/bin/env python3
class BankAccountProjection:
    def __init__(self):
        self.balance = 0.0

    def apply_event(self, event_type: str, amount: float, buggy=False):
        if buggy:
            # Buggy logic applied 10x multiplier accidentally!
            amount = amount * 10
        if event_type == "DEPOSIT":
            self.balance += amount
        elif event_type == "WITHDRAWAL":
            self.balance -= amount

if __name__ == "__main__":
    events = [
        ("DEPOSIT", 100.0),
        ("DEPOSIT", 50.0),
        ("WITHDRAWAL", 30.0),
        ("DEPOSIT", 20.0),
    ]
    # Expected: 100 + 50 - 30 + 20 = 140.0

    print("--- 1. Initial Run with Buggy Logic ---")
    buggy_proj = BankAccountProjection()
    for etype, amt in events:
        buggy_proj.apply_event(etype, amt, buggy=True)
    print(f" Corrupted Account Balance: ${buggy_proj.balance:.2f} (WRONG!)")

    print("\n--- 2. Rewinding Offset to 0 & Replaying with Fixed Logic ---")
    fixed_proj = BankAccountProjection()
    for etype, amt in events:
        fixed_proj.apply_event(etype, amt, buggy=False)
    print(f" Correct Restored Balance: ${fixed_proj.balance:.2f} (ACCURATE!)")
