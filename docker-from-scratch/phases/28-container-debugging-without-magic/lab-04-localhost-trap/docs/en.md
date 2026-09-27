# Lesson 28.4: Debugging Lab 04 — The Localhost Binding Trap

## Motto
"Bind to `0.0.0.0` (INADDR_ANY) inside containers; binding to `127.0.0.1` drops all packets arriving from the bridge network interface."

## Problem
**Symptom:**
A developer builds a FastAPI, Express, or Flask container.
They publish the port with `-p 8080:8080`.
`docker ps` shows the container is `Up` and port `8080` is published.
They run `curl http://localhost:8080` from their host laptop and receive:
`curl: (52) Empty reply from server` or `Connection reset by peer` or `Connection refused`.
Yet when they open an interactive shell inside the container (`docker exec`), `curl http://127.0.0.1:8080` works perfectly!
Why does it work inside the container but fail from the host?

## Prediction
1. What interface does `127.0.0.1` represent inside a container?
2. When the host forwards packets via `-p 8080:8080`, which container interface receives them (`lo` or `eth0`)?
3. What is the difference between binding to `127.0.0.1` and binding to `0.0.0.0`?

## Why this matters
Default development frameworks (Vite, Next.js, Flask, Django) bind strictly to `127.0.0.1` for local host security. When containerized without changing the host setting to `0.0.0.0`, the container is completely unreachable from the outside world.

## First principles
1. **The Loopback Boundary**:
   Binding to `127.0.0.1` tells the Linux kernel network stack: *Only accept packets originating from this exact same network namespace on the loopback (`lo`) interface.*
2. **The Forwarded Packet Arrival**:
   When host traffic hits `-p 8080:8080`, Docker's iptables NAT forwards the packet across the virtual bridge into the container's virtual ethernet interface: `eth0`.
3. **The Kernel Drop**:
   The container kernel receives packets on `eth0` with destination port 8080. It checks listening sockets: no socket is listening on `eth0`! The only socket is listening on `lo`. The kernel drops the packet or returns `RST`.
4. **The `0.0.0.0` Fix**:
   `0.0.0.0` (`INADDR_ANY`) instructs the kernel to bind the socket to **all** network interfaces (`lo`, `eth0`, `eth1`).

## Mental model

```text
TRAFFIC PATH WHEN BOUND TO 127.0.0.1:
Host: curl localhost:8080
      │
      ▼
Host Forwarder (-p 8080:8080)
      │
      ▼ Packets arrive on container interface eth0
CONTAINER:
      ├── eth0 (172.17.0.2) ──► PACKET DROPPED! (No listener on eth0)
      │
      └── lo (127.0.0.1)    ──► Server listening here (Only hears local traffic!)
```

## Build it
Review `server_broken.py` and `server_fixed.py` in `code/`.

## Run it
Execute the lab runner:

```bash
./phases/28-container-debugging-without-magic/lab-04-localhost-trap/experiments/run_experiment.sh
```

## Inspect it
1. Observe that host `curl http://localhost:8080` fails.
2. Inside the container, `curl http://127.0.0.1:8080` returns success.
3. Check `netstat -tuln` inside the container:
   `tcp 0 0 127.0.0.1:8080 0.0.0.0:* LISTEN`
   Notice the IP column says `127.0.0.1`, not `0.0.0.0`.

## Break it
Configure an Nginx or Python app to bind only to its container IP (e.g. `172.17.0.2`). Notice that local container curls to `127.0.0.1` now fail! Always bind to `0.0.0.0`.

## Debug it
1. Hypothesis: The service is listening, but bound to `127.0.0.1` instead of `0.0.0.0`.
2. Inspect listening sockets inside container:
   ```bash
   docker exec <c> ss -tuln (or netstat -tuln)
   ```
3. Look at Local Address: If it shows `127.0.0.1:<port>`, change the application server host argument to `0.0.0.0`.

## Modify it
Update a Flask or Node app with `HOST=0.0.0.0`. Verify external connectivity.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- Error observed from host curl.
- Success observed from internal curl.
- Confirmation after updating to `0.0.0.0`.

## Questions for mastery
1. Why do frameworks default to binding `127.0.0.1` when developing on bare metal laptops?
2. Does binding to `0.0.0.0` inside a container expose your port to the public internet automatically? (Hint: No; the host still requires `-p`).

## What comes next
In the next lab, a non-root container fails to write logs or state because of host permission mismatches. Proceed to **Lab 05: Permissions and Mounts**.
