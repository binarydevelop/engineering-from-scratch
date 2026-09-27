# Packet Capture Exercise: ICMP Destination Unreachable

> **Motto**: Understand it. Predict it. Send it. Capture it. Dissect it.

---

## 1. Objective
Handle routing/firewall drops.

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
sudo tcpdump -i <interface> -nn -vvv -s0 "icmp"
```

## 4. Annotated Wire Dissection
```text
Router > Client: ICMP 10.0.2.50 unreachable - host unreachable (Type 3 Code 1)
```

## 5. Mastery Reasoning Question
> **Question**: What is the difference between ICMP Code 1 (Host Unreachable) and Code 3 (Port Unreachable)?

Document your empirical findings in `outputs/evidence-template.md`.
