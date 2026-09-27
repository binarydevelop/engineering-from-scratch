# Packet Capture Exercise: TCP Connection Teardown (FIN-ACK)

> **Motto**: Understand it. Predict it. Send it. Capture it. Dissect it.

---

## 1. Objective
Gracefully terminate connection.

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
sudo tcpdump -i <interface> -nn -vvv -s0 "tcp[tcpflags] & (tcp-fin|tcp-ack) != 0"
```

## 4. Annotated Wire Dissection
```text
1. Client > Server: Flags [F.], seq 1051, ack 2001
2. Server > Client: Flags [.], ack 1052
3. Server > Client: Flags [F.], seq 2001, ack 1052
4. Client > Server: Flags [.], ack 2002
```

## 5. Mastery Reasoning Question
> **Question**: Which side enters the TIME_WAIT state, and why?

Document your empirical findings in `outputs/evidence-template.md`.
