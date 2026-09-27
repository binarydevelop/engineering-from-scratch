# Packet Capture Exercise: DNS Standard Query & Response

> **Motto**: Understand it. Predict it. Send it. Capture it. Dissect it.

---

## 1. Objective
Resolve name to IP.

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
sudo tcpdump -i <interface> -nn -vvv -s0 "udp port 53"
```

## 4. Annotated Wire Dissection
```text
Packet 1: IP 10.0.1.10.54321 > 1.1.1.1.53: [udp sum ok] 0x1234+ A? example.com. (29)
Packet 2: IP 1.1.1.1.53 > 10.0.1.10.54321: 0x1234 1/0/0 example.com. A 93.184.216.34 (45)
```

## 5. Mastery Reasoning Question
> **Question**: How does the client know that a response packet belongs to its specific query?

Document your empirical findings in `outputs/evidence-template.md`.
