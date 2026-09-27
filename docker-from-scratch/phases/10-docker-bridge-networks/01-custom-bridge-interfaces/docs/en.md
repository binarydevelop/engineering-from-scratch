# Lesson 10.1: Docker Bridge Networks and Network Isolation

## Motto
"A Docker network is not a magical cloud; it is a software Ethernet bridge connecting virtual interface cables."

## Problem
Suppose you have an API server container and a PostgreSQL container.
To connect them, beginner tutorials often instruct developers to publish the database port with `-p 5432:5432` and connect via host networking.
This creates a critical architectural failure:
1. The database port is inadvertently exposed to your local network or the public internet!
2. Traffic must exit the container, cross into the host network stack via NAT, and enter the database container, introducing latency and security risks.
We need a way for two isolated containers to speak privately to each other without exposing ports to the host machine.

## Prediction
1. If two containers are attached to the same custom bridge network, can they send packets to each other's IP addresses without using `-p`?
2. If container C is on network `net-1` and container D is on network `net-2`, can they ping each other?
3. Where does the bridge interface actually exist?

## Why this matters
Isolating microservices into distinct software-defined network segments is fundamental to zero-trust architecture. Database and cache layers should never be accessible from the host or public internet; only the frontend/gateway container should publish ports.

## First principles
1. **The Linux Software Bridge (`bridge`)**: A kernel-level virtual switch that operates at Layer 2 (Data Link) and Layer 3 (Network). Packets arriving on one port of the bridge are forwarded to the appropriate MAC address.
2. **Virtual Ethernet Pairs (`veth`)**: Software network cables with two ends.
   - One end is plugged into the Linux bridge interface (e.g. `br-xxx` or `docker0`).
   - The other end is moved into the container's private network namespace and renamed `eth0`.
3. **Subnet and Gateway Allocation**:
   - Each user-defined network is assigned an IP subnet CIDR block (e.g., `172.28.0.0/16`).
   - The bridge interface on the host is assigned the gateway IP (e.g., `172.28.0.1`).
   - Each container gets an IP dynamically leased by Docker's IPAM (IP Address Management) driver (e.g. `172.28.0.2`).
4. **Network Boundary Isolation**: The Linux kernel drops or rejects packets routed between different Docker bridge networks unless explicit routing/iptables rules are created to bridge them.

## Mental model

```text
HOST KERNEL (Linux / Docker VM)
┌────────────────────────────────────────────────────────────────────────┐
│  Bridge Interface: dfs-learning-net (IP: 172.28.0.1)                   │
│                                                                        │
│         ┌─────────── veth pair ───────────┐         ┌─── veth pair ───┐│
│         │                                 │         │                 ││
│         ▼                                 ▼         ▼                 ││
│  ┌──────────────┐                  ┌──────────────┐ ┌──────────────┐  ││
│  │ dfs-node-a   │                  │ dfs-node-b   │ │ dfs-isolated │  ││
│  │ IP:          │ ◄─── PING OK ──► │ IP:          │ │ (on default  │  ││
│  │ 172.28.0.2   │                  │ 172.28.0.3   │ │  bridge)     │  ││
│  └──────────────┘                  └──────────────┘ └──────┬───────┘  ││
│         ▲                                                  │          ││
│         └─────────────── BLOCKED BY KERNEL ────────────────┘          ││
└────────────────────────────────────────────────────────────────────────┘
```

## Build it
Review [inspect_bridge.py](../code/inspect_bridge.py).
It inspects the network configuration JSON to reveal:
- Subnet and Gateway CIDR blocks.
- Attached container endpoint names and MAC/IP allocations.

## Run it
Execute the experiment runner:

```bash
./phases/10-docker-bridge-networks/01-custom-bridge-interfaces/experiments/run_experiment.sh
```

## Inspect it
1. Run `docker network ls`. Notice `bridge`, `host`, `null`, and `dfs-learning-net`.
2. Inspect your custom network: `python3 inspect_bridge.py dfs-learning-net`.
3. Verify that `dfs-node-a` can ping `dfs-node-b` at `172.28.0.3` with sub-millisecond latency.

## Break it
Test inter-network isolation:
Run a container on the default bridge (`docker0`) and attempt to ping it from `dfs-node-a`.
Notice 100% packet loss! Docker's bridge networks strictly enforce isolation between subnets.

## Debug it
When two containers cannot reach each other:
1. Verify both containers are attached to the *same* network:
   ```bash
   docker inspect <c1> --format '{{range $k, $v := .NetworkSettings.Networks}}{{$k}}{{end}}'
   docker inspect <c2> --format '{{range $k, $v := .NetworkSettings.Networks}}{{$k}}{{end}}'
   ```
2. If networks differ, connect them dynamically:
   ```bash
   docker network connect <network-name> <container-name>
   ```

## Modify it
Create an internal-only network with no internet access by passing `--internal`:
```bash
docker network create --internal dfs-isolated-net
docker run --rm --network dfs-isolated-net alpine:latest ping -c 2 8.8.8.8
```
Observe that the container has internal bridge connectivity but cannot reach external internet gateways!

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- Subnet and Gateway allocated to `dfs-learning-net`.
- Ping output showing round-trip time between Node A and Node B.
- Evidence of packet loss when pinging across network boundaries.

## Questions for mastery
1. Why does service-to-service communication within a Docker network not require `-p`?
2. What happens to the `veth` interface when a container is deleted?
3. How does traffic between containers on the same bridge avoid touching your physical WiFi/Ethernet card?

## What comes next
We connected containers using raw IP addresses (`172.28.0.3`). But container IPs are volatile and change on restart! How do containers find each other by name? Proceed to **Phase 11: Docker DNS and Service Discovery**.
