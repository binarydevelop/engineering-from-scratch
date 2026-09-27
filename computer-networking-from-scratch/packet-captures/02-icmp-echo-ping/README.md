# Packet Capture Exercise: ICMP Echo Request & Reply

> **Motto**: Understand it. Predict it. Send it. Capture it. Dissect it.

---

## 1. Objective
Verify Layer-3 reachability.

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
Packet 1: IP 10.0.1.10 > 10.0.1.20: ICMP echo request, id 1234, seq 1
Packet 2: IP 10.0.1.20 > 10.0.1.10: ICMP echo reply, id 1234, seq 1
```

## 5. Mastery Reasoning Question
> **Question**: What field links an ICMP Echo Reply to its corresponding Request?

Document your empirical findings in `outputs/evidence-template.md`.
