# Packet Capture Exercise: TCP Data Transfer & ACKs

> **Motto**: Understand it. Predict it. Send it. Capture it. Dissect it.

---

## 1. Objective
Transmit application stream.

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
sudo tcpdump -i <interface> -nn -vvv -s0 "tcp and port 80"
```

## 4. Annotated Wire Dissection
```text
Packet 1: Client > Server: Flags [P.], seq 1001:1051, ack 2001 (50 bytes HTTP GET)
Packet 2: Server > Client: Flags [.], ack 1051 (ACK acknowledging 50 bytes)
```

## 5. Mastery Reasoning Question
> **Question**: What does the PSH (Push) flag instruct the receiving kernel stack to do?

Document your empirical findings in `outputs/evidence-template.md`.
