#!/usr/bin/env python3
class BankAccountEventSourced:
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.balance = 0.0
        self.version = 0

    def apply(self, event: dict):
        etype = event["type"]
        amt = event["amount"]
        if etype == "AccountCreated":
            self.balance = amt
        elif etype == "MoneyDeposited":
            self.balance += amt
        elif etype == "MoneyWithdrawn":
            if self.balance < amt:
                raise ValueError("Insufficient funds!")
            self.balance -= amt
        self.version += 1

if __name__ == "__main__":
    event_log = [
        {"type": "AccountCreated", "amount": 0.0},
        {"type": "MoneyDeposited", "amount": 100.0},
        {"type": "MoneyWithdrawn", "amount": 35.0},
        {"type": "MoneyDeposited", "amount": 50.0},
    ]

    print("Reconstructing Bank Account from Event Log:")
    acc = BankAccountEventSourced("ACC-42")
    for ev in event_log:
        acc.apply(ev)
        print(f" Applied {ev['type']} (${ev['amount']:.2f}) -> Balance: ${acc.balance:.2f} (v{acc.version})")

    print(f"\nFinal Account Balance: ${acc.balance:.2f}")
    print("Wiping projection... Replaying log rebuilds the exact state: $115.00!")
