# Packet Capture Exercise: TCP Packet Loss & Retransmission

> **Motto**: Understand it. Predict it. Send it. Capture it. Dissect it.

---

## 1. Objective
Recover lost segment.

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
sudo tcpdump -i <interface> -nn -vvv -s0 "tcp and port 8080"
```

## 4. Annotated Wire Dissection
```text
1. Client > Server: Flags [P.], seq 1001:1021 (lost in transit)
2. Client > Server: Flags [P.], seq 1021:1041 (Server generates Dup ACK 1001)
3. Client > Server: Retransmit seq 1001:1021
```

## 5. Mastery Reasoning Question
> **Question**: How many duplicate ACKs trigger Fast Retransmit before RTO expires?

Document your empirical findings in `outputs/evidence-template.md`.
