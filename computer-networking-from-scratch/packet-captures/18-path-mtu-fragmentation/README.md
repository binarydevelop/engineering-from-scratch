# Packet Capture Exercise: Path MTU Discovery (PMTUD)

> **Motto**: Understand it. Predict it. Send it. Capture it. Dissect it.

---

## 1. Objective
Detect path MTU boundaries.

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
sudo tcpdump -i <interface> -nn -vvv -s0 "icmp or (ip[6:2] & 0x3fff != 0)"
```

## 4. Annotated Wire Dissection
```text
Router > Sender: ICMP 10.0.2.20 unreachable - need to frag (mtu 1400) (Type 3 Code 4)
```

## 5. Mastery Reasoning Question
> **Question**: What happens if an upstream enterprise firewall blocks all ICMP Type 3 Code 4 packets?

Document your empirical findings in `outputs/evidence-template.md`.
