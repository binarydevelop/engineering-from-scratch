# Packet Capture Exercise: Persistent Database Connection Pool

> **Motto**: Understand it. Predict it. Send it. Capture it. Dissect it.

---

## 1. Objective
Amortize connection setup overhead.

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
sudo tcpdump -i <interface> -nn -vvv -s0 "tcp port 5432"
```

## 4. Annotated Wire Dissection
```text
Multiple SQL queries executed over established TCP connection with 0 SYN/FIN packets exchanged.
```

## 5. Mastery Reasoning Question
> **Question**: Why is connection pooling critical for high-throughput relational database workloads?

Document your empirical findings in `outputs/evidence-template.md`.
