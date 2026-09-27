# Lesson 16.1: Isolation and Linux Namespaces Under the Hood

## Motto
"Namespaces dictate what a process can *see*; a container process is just a host process wearing virtual blinders."

## Problem
Developers often believe that a container runs a complete guest operating system with a separate kernel.
Because of this misconception:
- They assume running 50 containers means running 50 operating system kernels.
- They don't understand why killing a process from the host immediately terminates the container.
- They are surprised to discover that a container running as `root` (UID 0) can potentially interact with the host kernel if misconfigured.
What kernel mechanisms make a process believe it is running alone on its own machine?

## Prediction
1. Does a container process have two different Process IDs (PIDs) simultaneously?
2. Can a container change the hostname of the host machine?
3. How many Linux kernels are executing on your computer when 10 containers are running?

## Why this matters
Understanding namespaces dispels the myth of the "container as virtual machine". It reveals that containers are lightweight precisely because they share a single host kernel. This knowledge is crucial for diagnosing container escape vulnerabilities, user namespace mapping, and inter-process debugging.

## First principles
The Linux kernel provides **Namespaces** to isolate global system resources:
1. **PID Namespace**: Isolates process IDs. The first process created in a new PID namespace becomes PID 1. Outside that namespace, on the host/VM kernel, the exact same process has a standard high PID (e.g. 4742).
2. **NET Namespace**: Isolates network interfaces (`lo`, `eth0`), IP routing tables, port bindings, and firewall rules.
3. **MNT (Mount) Namespace**: Isolates the filesystem mount table. Combined with `pivot_root`, the process sees the stacked container rootfs as `/`.
4. **UTS Namespace**: Isolates the system hostname and domain name.
5. **IPC Namespace**: Isolates inter-process communication resources (POSIX message queues, System V shared memory).
6. **USER Namespace**: Maps UIDs and GIDs. Allows a process to be `root` (UID 0) inside the container while mapping to an unprivileged UID (e.g. 10001) on the host.
7. **CGROUP Namespace**: Isolates visibility of the cgroup filesystem tree.

## Mental model

```text
LINUX KERNEL (Single Shared Kernel)
┌────────────────────────────────────────────────────────────────────────┐
│  Host Process Table:                                                   │
│  - PID 1: systemd (or init)                                            │
│  - PID 4719: containerd-shim                                           │
│  - PID 4742: sleep 120 ◄──────────────────────────────┐                │
├───────────────────────────────────────────────────────┼────────────────┤
│  Container PID Namespace (dfs-ns-demo):               │                │
│                                                       │ Dual Identity  │
│  ┌─────────────────────────────────────────────────┐  │ (Same process) │
│  │ Process: sleep 120                              │  │                │
│  │ View: PID 1                                     │ ◄┘                │
│  │ View: Hostname = "isolated-box-01"              │                   │
│  │ View: Root = /bin, /etc, /data (Container root) │                   │
│  └─────────────────────────────────────────────────┘                   │
└────────────────────────────────────────────────────────────────────────┘
```

## Build it
Review [inspect_namespaces.py](../code/inspect_namespaces.py).
It queries `ps` from inside the container and compares it with `docker top` from the host.

## Run it
Execute the experiment runner:

```bash
./phases/16-isolation-and-namespaces/01-linux-namespaces-under-the-hood/experiments/run_experiment.sh
```

## Inspect it
1. Observe UTS isolation: Host machine hostname is preserved, while the container has `isolated-box-01`.
2. Observe PID isolation: Inside the container, `sleep` is PID 1. Outside, `docker top` reports PID `4742`!
3. Notice that `PPID` is the `containerd-shim` process that supervises the container.

## Break it
Share the host's PID namespace by passing `--pid=host`:
```bash
docker run --rm --pid=host alpine:latest ps -ef | head -n 10
```
Notice what happened: The container can now see every single host process running on the system! This completely breaks PID isolation.

## Debug it
When you need to know which container owns a specific host process:
```bash
docker ps -q | xargs docker inspect --format '{{.State.Pid}} {{.Name}}' | grep "<HOST_PID>"
```
This maps host PIDs directly back to their container names.

## Modify it
Run a container that shares the network namespace of another container using `--net=container:<target>`:
```bash
docker run -d --name dfs-target alpine:latest sleep 60
docker run --rm --net=container:dfs-target alpine:latest ifconfig
docker rm -f dfs-target
```
Observe that both containers share the exact same IP and network interfaces.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- The hostname output comparing host vs container.
- The table comparing inside PID (1) with host PID.
- The Mount namespace directory listing.

## Questions for mastery
1. Why does a container take only 50 milliseconds to start, while a virtual machine takes 30 seconds?
2. If a process inside a container is killed from the host using `kill -9 <HOST_PID>`, does the container exit?
3. What is the security consequence of running a container with `--pid=host`?

## What comes next
Because PID 1 inside a container is special, how it handles signals governs whether your container shuts down gracefully in 100 milliseconds or hangs for 10 seconds. Proceed to **Phase 17: Signals, PID 1, and Container Lifecycle**.
