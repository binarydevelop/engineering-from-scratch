# Lesson 09.1: Ports and Publishing (`EXPOSE` vs. `-p`)

## Motto
"`EXPOSE` is a note for humans; `-p` is a programming instruction for the kernel's network routing tables."

## Problem
Engineers frequently write `EXPOSE 8080` in a Dockerfile, run `docker run my-image`, open `http://localhost:8080` in their browser, and see "This site can't be reached" (Connection refused).
Confused, they think their application failed to start or that `EXPOSE` is broken.
Without understanding the difference between internal socket binding, documentation metadata, and host port forwarding (DNAT), port configuration will always feel like guesswork.

## Prediction
1. If an image contains `EXPOSE 8000`, does `docker run <image>` automatically open port 8000 on your laptop?
2. In `-p 8888:8000`, which number is the host port and which is the container port?
3. Can two containers publish to the exact same host port simultaneously?

## Why this matters
Port publishing mistakes lead to production outages: port collision errors (`address already in use`), services inadvertently exposed to the public internet instead of private subnets, and confusion over why reverse proxies cannot route traffic to container backends.

## First principles
1. **Internal Socket Binding**: When your code calls `server.listen("0.0.0.0", 8000)`, it creates a listening TCP socket bound to port 8000 *inside that container's private network namespace*.
2. **`EXPOSE` Instruction**: Pure metadata written to the image's JSON configuration object. It informs humans and tooling which port the application expects. It does **not** alter host firewall rules, iptables, or network routing!
3. **The `-p <HOST_PORT>:<CONTAINER_PORT>` Flag**:
   - Instructs Docker Engine to configure **Destination Network Address Translation (DNAT)** in the host's `iptables`/`nftables` (or spawn a lightweight proxy process like `docker-proxy`).
   - When incoming packets hit `host:<HOST_PORT>`, the kernel rewrites the destination IP and port to `<CONTAINER_IP>:<CONTAINER_PORT>` and routes them across the virtual bridge.

## Mental model

```text
HOST MACHINE (Laptop / Server)
┌────────────────────────────────────────────────────────┐
│  Host Port: 8888                                       │
│  (Bound by docker-proxy / iptables DNAT rule)          │
└──────────────────────────┬─────────────────────────────┘
                           │ Packets forwarded via virtual bridge
                           ▼
CONTAINER (dfs-pub)
┌────────────────────────────────────────────────────────┐
│  Container eth0 IP: 172.17.0.2                         │
│  Container Port: 8000                                  │
│  (Python server listening on 0.0.0.0:8000)             │
└────────────────────────────────────────────────────────┘

SYNTAX BREAKDOWN:
$ docker run -p 8888:8000 my-image
                 │    │
  Host Port ─────┘    └───── Container Internal Port
```

## Build it
Review `Dockerfile` and `app.py` in `code/`.
The Dockerfile declares `EXPOSE 8000`.

## Run it
Execute the experiment runner:

```bash
./phases/09-ports-and-publishing/01-port-forwarding-mechanics/experiments/run_experiment.sh
```

## Inspect it
1. Observe the failure of `dfs-unpub`: `curl localhost:8000` returns exit code 7 (`Failed to connect to localhost port 8000: Connection refused`).
2. Run `docker port dfs-pub`. Output: `8000/tcp -> 0.0.0.0:8888`.
3. Run `docker inspect dfs-pub --format '{{json .NetworkSettings.Ports}}'`.
   Notice the JSON structure mapping container port `8000/tcp` to `HostPort: "8888"`.

## Break it
Try to run two containers that publish to the exact same host port:

```bash
docker run -d --name dfs-p1 -p 9100:8000 dfs-port-demo:v1
docker run -d --name dfs-p2 -p 9100:8000 dfs-port-demo:v1
```
The second command fails immediately:
`Bind for 0.0.0.0:9100 failed: port is already allocated`
Only one process on the host can bind to a given TCP port at any time.
Clean up:
```bash
docker rm -f dfs-p1
```

## Debug it
When `curl localhost:<port>` fails:
1. Run `docker ps`: Is the port published in the `PORTS` column (`0.0.0.0:8888->8000/tcp`)? If the arrow `->` is missing, you forgot `-p`.
2. Inspect application binding: If your application binds to `127.0.0.1:8000` inside the container rather than `0.0.0.0:8000`, forwarded packets arriving on `eth0` will be rejected!
3. Check host port conflicts with `lsof -i :<HOST_PORT>`.

## Modify it
Publish port 8000 dynamically to a random available high-numbered host port using `-P` (uppercase) or `-p 8000`:
```bash
docker run -d --name dfs-random -P dfs-port-demo:v1
docker port dfs-random
```
Discover which host port Docker assigned automatically.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- The exit code of curl against the un-published container.
- The output of `docker port dfs-pub`.
- The port collision error observed when binding two containers to the same host port.

## Questions for mastery
1. Why does `-p 127.0.0.1:8080:80` behave differently from `-p 8080:80`? (Hint: Public internet exposure vs local loopback).
2. What is `docker-proxy`, and what role does it play alongside `iptables`?
3. If two containers are on the same internal Docker network, do they need `-p` to communicate with each other?

## What comes next
We now understand how host traffic reaches a single container via port forwarding. But how do two containers communicate directly without exposing every internal port to the host? Proceed to **Phase 10: Docker Bridge Networks**.
