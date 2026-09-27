# Packet Capture Exercise: TCP 3-Way Handshake

> **Motto**: Understand it. Predict it. Send it. Capture it. Dissect it.

---

## 1. Objective
Establish TCP connection.

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
sudo tcpdump -i <interface> -nn -vvv -s0 "tcp[tcpflags] & (tcp-syn|tcp-ack) != 0"
```

## 4. Annotated Wire Dissection
```text
1. Client > Server: Flags [S], seq 1000, win 65495, options [mss 1460,sackOK]
2. Server > Client: Flags [S.], seq 2000, ack 1001, win 65483
3. Client > Server: Flags [.], ack 2001, win 65495
```

## 5. Mastery Reasoning Question
> **Question**: Why does the SYN packet consume 1 sequence number even though it carries 0 bytes of payload?

Document your empirical findings in `outputs/evidence-template.md`.
