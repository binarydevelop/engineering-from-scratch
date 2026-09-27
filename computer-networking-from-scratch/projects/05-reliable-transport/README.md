# Project 05: Reliable Transport Protocol From Scratch

> **Motto**: A reliable byte stream does not exist in nature; it is a software fiction maintained by sequence tracking, cumulative acknowledgments, sliding windows, and retransmission timeouts across an unreliable packet world.

---

## 1. Overview
In this project, you construct a complete Layer-4 transport protocol from scratch on top of an intentionally lossy datagram channel.

## 2. Key Mechanisms Implemented
1. **3-Way Handshake**: `SYN` -> `SYN-ACK` -> `ACK` establishing Initial Sequence Numbers (ISN).
2. **Byte Sequence Tracking**: Mapping application payloads into indexed segment chunks.
3. **Sliding Window Pipelining**: Transmitting multiple segments concurrently without waiting for per-packet stop-and-wait ACKs.
4. **Cumulative ACKs**: Receiver advertises the exact next expected byte index.
5. **Retransmission Timers (RTO)**: Detecting lost segments and re-injecting them into the pipe.

## 3. Running & Testing
```bash
python3 transport.py
python3 test_transport.py
```
