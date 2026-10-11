# Phase 139: WebRTC Architecture, NAT Traversal (STUN/TURN/ICE), and SFU Media Servers

## 1. Why This Matters for MAANG & Senior/Staff Roles
In modern distributed architectures, designing video conferencing (Zoom, Google Meet, Discord), peer-to-peer data replication, or cloud gaming requires sub-200ms latency. Traditional HTTP or TCP streaming introduces severe head-of-line blocking and buffer delays. WebRTC (Web Real-Time Communication) provides the global standard for encrypted, low-latency, real-time media and arbitrary data streaming.

---

## 2. Core Concepts & Architecture Deep-Dive
### WebRTC Connection Establishment Lifecycle
1. **Signaling**: WebRTC does NOT define a signaling protocol. Applications use WebSockets, SIP, or HTTP to exchange metadata:
   - **Session Description Protocol (SDP)**: Describes media codecs, resolutions, encryption keys, and network capabilities (Offer/Answer model).
2. **Interactive Connectivity Establishment (ICE)**: Solves NAT traversal:
   - **STUN (Session Traversal Utilities for NAT)**: Discovers the client's public reflexive IP address and port mapping.
   - **TURN (Traversal Using Relays around NAT)**: Fallback relay server when symmetric NATs prevent direct peer-to-peer communication (~15-20% of enterprise connections).
   - **ICE Candidates**: List of potential IP/port endpoints (host, srflx, relay) exchanged via signaling.
3. **DTLS & SRTP Encryption**: WebRTC mandates encryption. DTLS performs the handshake and exchanges keys; SRTP (Secure Real-time Transport Protocol) encrypts media payloads.
4. **SCTP over DTLS (Data Channels)**: Enables unreliable/unordered or reliable/ordered binary data transfer with sub-millisecond overhead.

### Topology Architectures: Mesh vs SFU vs MCU
- **Mesh (Full P2P)**: Each participant sends media to every other participant. Bandwidth explodes at O(N^2). Unusable beyond 3-4 users.
- **SFU (Selective Forwarding Unit)**: Clients send 1 stream to the SFU; SFU selectively forwards it to other participants without transcoding. Highly scalable (hundreds of participants). Standard in Zoom, Discord, Google Meet.
- **MCU (Multipoint Control Unit)**: Server decodes, composites all videos into a single grid video, re-encodes, and sends to clients. CPU intensive, high latency, expensive.

---

## 3. High-Value Interview Angle & Failure Modes
### Interview Questions & Design Scenarios
- **"Why does WebRTC use UDP instead of TCP for voice and video?"**:
  In real-time audio/video, an outdated packet (e.g., audio from 300ms ago) is worthless. TCP retransmission mechanisms cause Head-of-Line blocking and latency spirals. WebRTC drops lost packets and uses error concealment techniques instead.
- **"How does Simulcast and SVC (Scalable Video Coding) adapt to changing bandwidth?"**:
  A client encodes and uploads 3 video streams simultaneously (High: 1080p, Medium: 720p, Low: 360p). The SFU forwards 1080p to gigabit desktop users and dynamically switches to 360p for mobile users with spotty cellular reception without re-encoding.

---

## 4. Hands-On Practice & Implementation Drills
### Connection Flow State Machine Drill
```
Client A (Browser)          Signaling Server           Client B (Browser)
     |                             |                           |
     |--- 1. Create Offer (SDP) -->|                           |
     |                             |--- 2. Forward Offer ----->|
     |                             |<-- 3. Create Answer (SDP)-|
     |<-- 4. Forward Answer -------|                           |
     |                             |                           |
     |======== 5. ICE Candidate Gathering (STUN/TURN) =========|
     |                             |                           |
     |<----------------- 6. Direct P2P Media Stream ---------->|
     |                     (SRTP Encrypted via DTLS)           |
```

---

## 5. Key Takeaways & Cheat Sheet
- WebRTC delivers sub-200ms latency real-time voice, video, and data channels.
- NAT traversal uses STUN for reflection and TURN as relay fallback via the ICE framework.
- Modern video conferencing platforms use SFU (Selective Forwarding Unit) media architectures.
- Essential for system design interviews covering video calling, live streaming, and real-time collaboration.
