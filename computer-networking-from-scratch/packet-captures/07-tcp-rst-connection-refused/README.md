# Packet Capture Exercise: TCP RST (Connection Refused)

> **Motto**: Understand it. Predict it. Send it. Capture it. Dissect it.

---

## 1. Objective
Port closed rejection.

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
sudo tcpdump -i <interface> -nn -vvv -s0 "tcp[tcpflags] & tcp-rst != 0"
```

## 4. Annotated Wire Dissection
```text
1. Client > Server: Flags [S], seq 1000, dport 9999
2. Server > Client: Flags [R.], seq 0, ack 1001, win 0
```

## 5. Mastery Reasoning Question
> **Question**: Why does the kernel return RST with ack=seq+1 instead of silently ignoring the packet?

Document your empirical findings in `outputs/evidence-template.md`.
