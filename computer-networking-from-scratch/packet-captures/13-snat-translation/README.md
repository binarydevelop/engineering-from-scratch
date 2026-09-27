# Packet Capture Exercise: Source NAT (SNAT / Masquerade)

> **Motto**: Understand it. Predict it. Send it. Capture it. Dissect it.

---

## 1. Objective
Translate private client IP.

## 2. Hypothesis & Packet Prediction
Before running the capture, predict the sequence of frames:
```text
┌───────────────────────┬────────────────────────────────────────────────────────┐
│ Header Layer          │ Predicted Values / Flags                               │
├───────────────────────┼────────────────────────────────────────────────────────┤
│ Layer 2 (Ethernet II) │ Source MAC, Destination MAC, EtherType                 │
│ Layer 3 (IP)          │ Source IP, Destination IP, TTL, Protocol               │
│ Layer 4 (Transport)   │ Source Port, Destination Port, Flags, Seq/Ack          │
│ Layer 7 (Application) │ Command / Payload / Delimiters                         │
└───────────────────────┴────────────────────────────────────────────────────────┘
```

## 3. tcpdump Capture Command
```bash
sudo tcpdump -i <interface> -nn -vvv -s0 "ip and port 80"
```

## 4. Annotated Wire Dissection
```text
Before NAT: 10.0.1.10:54321 > 93.184.216.34:80
After NAT:  203.0.113.1:61000 > 93.184.216.34:80
```

## 5. Mastery Reasoning Question
> **Question**: What Linux kernel table maintains the mapping between internal and external IP:Port tuples?

Document your empirical findings in `outputs/evidence-template.md`.
