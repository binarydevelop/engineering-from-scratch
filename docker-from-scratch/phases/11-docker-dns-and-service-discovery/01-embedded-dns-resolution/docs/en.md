# Lesson 11.1: Docker DNS and Service Discovery

## Motto
"Hardcoding IP addresses is fragile; user-defined networks give you an embedded DNS resolver at `127.0.0.11` for free."

## Problem
In Phase 10, we connected containers using raw IP addresses like `172.28.0.3`.
In production, containers restart, scale, crash, and redeploy constantly. Every time a container restarts, Docker assigns it the next available free IP from the subnet pool.
If your API server has `REDIS_HOST=172.28.0.3` hardcoded, your system breaks the moment Redis restarts with IP `172.28.0.4`.
Why does `curl http://redis:6379` work seamlessly in modern setups, but fails when you run `docker run redis` and `docker run app` without creating a network?

## Prediction
1. Does Docker provide DNS resolution for container names on the default bridge network?
2. When you query a hostname inside a container, what DNS server answers?
3. What happens if a container IP changes? Does DNS update automatically or does it cache the old IP forever?

## Why this matters
DNS is the backbone of service discovery in all container platforms (Docker, Docker Compose, Docker Swarm, and Kubernetes). If you don't understand how Docker's embedded DNS resolves names, you will waste hours debugging connection timeouts, stale DNS cache entries, and `getaddrinfo ENOTFOUND` errors.

## First principles
1. **The Four Networking Contexts**:
   - `localhost`: Loops back strictly within the current container namespace.
   - `container IP` (e.g. `172.18.0.2`): Direct Layer 3 address within the bridge subnet. Volatile across restarts!
   - `container name` (e.g. `redis`, `api`): Persistent logical identifier resolved dynamically by DNS.
   - `host IP` / `host.docker.internal`: Address of the machine hosting the Docker daemon.
2. **The Embedded DNS Server (`127.0.0.11`)**:
   - When a container connects to a **user-defined network**, Docker alters its `/etc/resolv.conf` to point to `nameserver 127.0.0.11`.
   - Any DNS query sent to `127.0.0.11:53` is trapped and handled by the Docker daemon's internal DNS service.
   - The daemon looks up the container name in its internal routing table and returns the current private IP.
3. **The Default Bridge Legacy Limitation**:
   - The default bridge (`docker0`) was built in 2013 and does **not** support automatic DNS resolution. Containers on the default bridge see the host's external DNS server in `/etc/resolv.conf`, which knows nothing about Docker container names.

## Mental model

```text
CONTAINER: "dfs-client" (/etc/resolv.conf -> nameserver 127.0.0.11)
┌─────────────────────────────────────────────────────────────────┐
│  Application calls: socket.gethostbyname("dfs-cache")           │
│       │                                                         │
│       │ 1. DNS Query: "Who is dfs-cache?" (UDP port 53)         │
│       ▼                                                         │
│  IP: 127.0.0.11 (Embedded Docker DNS Engine)                    │
└───────┬─────────────────────────────────────────────────────────┘
        │
        │ 2. Query intercepted by dockerd inside namespace
        ▼
DOCKER ENGINE ROUTING TABLE:
┌─────────────────────────────────────────────────────────────────┐
│  Registry:                                                      │
│  - "dfs-cache"  ──► 172.18.0.4                                  │
│  - "dfs-client" ──► 172.18.0.3                                  │
└───────┬─────────────────────────────────────────────────────────┘
        │
        │ 3. DNS Response: "dfs-cache is at 172.18.0.4"
        ▼
TCP Connection established directly to 172.18.0.4 across the bridge!
```

## Build it
Review [experiments/run_experiment.sh](../experiments/run_experiment.sh) and [code/dns_lookup.py](../code/dns_lookup.py).
We test:
1. DNS resolution on a user-defined network (`dfs-dns-net`).
2. Absence of DNS on the default bridge.
3. Dynamic IP reallocation when `dfs-cache` is recreated.

## Run it
Execute the experiment runner:

```bash
./phases/11-docker-dns-and-service-discovery/01-embedded-dns-resolution/experiments/run_experiment.sh
```

## Inspect it
1. Compare `/etc/resolv.conf`:
   - On `dfs-dns-net`: `nameserver 127.0.0.11`.
   - On default bridge: Host external nameserver (e.g. `192.168.65.7` or `8.8.8.8`).
2. Run `docker exec -it dfs-client ping dfs-cache`. Notice it resolves to `172.18.0.x`.
3. Test using python: `docker exec dfs-client python3 -c "import socket; print(socket.gethostbyname('dfs-cache'))"`.

## Break it
Run two containers on the default bridge and attempt to ping one from the other by name:
```bash
docker run -d --name c-one alpine:latest sleep 30
docker run --rm alpine:latest ping -c 1 c-one
```
Fails immediately: `ping: bad address 'c-one'`.
This proves why production microservices must NEVER run on the default bridge!
Clean up:
```bash
docker rm -f c-one
```

## Debug it
When `getaddrinfo ENOTFOUND <service>` occurs:
1. Check `/etc/resolv.conf`:
   ```bash
   docker exec <container> cat /etc/resolv.conf
   ```
   If `127.0.0.11` is missing, the container is attached to the default bridge or has custom `--dns` flags overriding Docker's resolver.
2. Check network membership:
   ```bash
   docker network inspect <network> --format '{{range .Containers}}{{.Name}} {{end}}'
   ```
   If both containers are not in this list, they cannot resolve each other.

## Modify it
Use container network aliases to give a container multiple DNS names:
```bash
docker run -d --name dfs-multi --network dfs-dns-net --network-alias primary-db --network-alias replica-db alpine:latest sleep 60
```
Run `docker exec dfs-client ping -c 1 primary-db` and `docker exec dfs-client ping -c 1 replica-db`. Verify both resolve to the exact same IP!
Clean up: `docker rm -f dfs-multi`.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- Content of `/etc/resolv.conf` on user-defined network vs. default bridge.
- The `ping: bad address` failure on default bridge.
- The dynamic IP reassignment output showing seamless DNS updates.

## Questions for mastery
1. Why did the Docker team not enable embedded DNS on the default bridge? (Hint: backwards compatibility with legacy 2013 Docker).
2. What is `127.0.0.11`? Why is it chosen in the loopback subnet?
3. How do multiple containers sharing the same `--network-alias` provide round-robin DNS load balancing?

## What comes next
We have mastered container processes, filesystems, images, ports, bridges, and DNS. Now we tackle stateful systems: **How do we persist database state when containers are destroyed?** Proceed to **Phase 12: Volumes and Persistence**.
