# Lesson 08.1: Container Networking: The Localhost Trap

## Motto
"Inside a container, `localhost` means *this container*, not your laptop."

## Problem
This is the single most common networking bug junior developers encounter with containers:
A developer has PostgreSQL running directly on their MacBook at `localhost:5432`. They containerize a web application, set `DATABASE_URL=postgres://localhost:5432/mydb`, and launch the container.
The application crashes immediately with `Connection refused`.
The developer tests `psql -h localhost` on their laptop terminal and it connects instantly. They assume Docker is broken.
What happened?

## Prediction
1. Does a container share the host machine's network stack by default?
2. If you run `ping localhost` inside a container, which network interface responds?
3. Can a process inside container A reach a server in container B via `localhost`?

## Why this matters
Every network connection in microservice architectures hinges on understanding network namespaces. Believing that `localhost` is universal across containers leads to failed database connections, broken microservice communication, and insecure hacks.

## First principles
1. **Network Namespaces**: When Docker creates a container, the Linux kernel assigns it an isolated **Network Namespace (`netns`)**.
2. **Dedicated Loopback**: Each network namespace has its own private loopback interface (`lo` at `127.0.0.1`).
   - On the host: `127.0.0.1` talks only to sockets bound within the host network namespace.
   - Inside the container: `127.0.0.1` talks only to sockets bound *within that specific container*.
3. **Cross-Boundary Host Resolution**:
   - To reach the host from a container on Docker Desktop (macOS/Windows), Docker provides a special internal DNS name: `host.docker.internal`.
   - On native Linux, traffic to the host must be routed to the bridge gateway IP (typically `172.17.0.1` or `--add-host=host.docker.internal:host-gateway`).

## Mental model

```text
HOST MACHINE (Mac / Linux)
┌────────────────────────────────────────────────────────┐
│  Host Network Namespace:                               │
│  - lo interface: 127.0.0.1                             │
│  - Python server listening on 127.0.0.1:8080           │
│                                                        │
│  curl http://localhost:8080 ──► REACHES SERVER!        │
└──────────────────────────┬─────────────────────────────┘
                           │ Network Namespace Boundary (Isolated)
                           ▼
CONTAINER A (alpine)
┌────────────────────────────────────────────────────────┐
│  Container Network Namespace:                          │
│  - lo interface: 127.0.0.1                             │
│  - (No process listening on port 8080 inside!)         │
│                                                        │
│  wget http://localhost:8080 ──► CONNECTION REFUSED!    │
│                                                        │
│  wget http://host.docker.internal:8080 ──► SUCCESS!    │
└────────────────────────────────────────────────────────┘
```

## Build it
Review [server.py](../code/server.py).
It starts a minimal HTTP server on the host machine listening on `0.0.0.0:8080`.

## Run it
Execute the experiment runner:

```bash
./phases/08-container-networking-start-with-localhost/01-localhost-isolation/experiments/run_experiment.sh
```

## Inspect it
1. Run `ifconfig lo0` (or `ip addr show lo`) on the host. Notice `127.0.0.1`.
2. Run `docker run --rm alpine:latest ip addr show lo`.
   Notice the container has its own independent `lo` interface!
3. Observe that `wget http://localhost:8080` inside the container immediately returns `wget: can't connect to remote host: Connection refused`.

## Break it
Launch an Nginx or web container and try to reach another container using `localhost`:
```bash
docker run -d --name dfs-s1 alpine:latest sleep 60
docker run -d --name dfs-s2 alpine:latest sleep 60
# Neither can communicate via localhost:
docker exec dfs-s1 ping -c 1 localhost
# This only pings s1 itself, never s2!
docker rm -f dfs-s1 dfs-s2
```

## Debug it
When an application inside a container cannot reach a service:
1. Verify the connection target: if it says `localhost` or `127.0.0.1`, ask: *Is the destination service running inside this exact same container?*
2. If the destination is on the host: replace `localhost` with `host.docker.internal`.
3. If the destination is another container: both containers must share a Docker network and use service discovery (covered in Phase 10 & 11).

## Modify it
Run a container using the host's actual network namespace by passing `--net=host`:
```bash
docker run --rm --net=host alpine:latest wget -qO- --timeout=2 http://localhost:8080
```
Notice that with `--net=host`, the container bypasses network isolation and shares the host's loopback interface! (Note: On macOS Docker Desktop, `--net=host` binds to the Linux VM, not macOS).

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- Output of host curl vs container wget.
- Explanation of why container wget received Connection Refused.
- The working resolution via `host.docker.internal`.

## Questions for mastery
1. Why does `localhost` inside container A never connect to container B?
2. What are the security risks of running containers with `--net=host`?
3. How does Docker Desktop route `host.docker.internal` across the hypervisor VM boundary into macOS?

## What comes next
We saw how containers talk outward to the host. But how does outside traffic from your browser reach *into* a service running inside a container? Proceed to **Phase 09: Ports and Publishing**.
