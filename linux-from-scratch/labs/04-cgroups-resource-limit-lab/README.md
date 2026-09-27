# Lab 04: Cgroups Resource Limit Sandbox

## Objective
Enforce CPU quotas and memory maximums using Linux cgroups v2, observing controlled process throttling and Out-Of-Memory termination.

## Setup Procedure
```bash
# 1. Create a delegated test cgroup under /sys/fs/cgroup/
sudo mkdir -p /sys/fs/cgroup/lfs-sandbox
sudo chown -R $USER:$USER /sys/fs/cgroup/lfs-sandbox

# 2. Configure a strict memory limit of 50 Megabytes
echo "50M" > /sys/fs/cgroup/lfs-sandbox/memory.max
echo "0" > /sys/fs/cgroup/lfs-sandbox/memory.swap.max

# 3. Launch an unconstrained memory consumer inside the cgroup
python3 -c "
import os
with open('/sys/fs/cgroup/lfs-sandbox/cgroup.procs', 'w') as f:
    f.write(str(os.getpid()))
print('Joined cgroup. Allocating 100MB of RAM...')
data = bytearray(100 * 1024 * 1024)
"
# Result: Killed (Process killed by cgroup OOM-killer with Exit code 137)
```

## Teardown
```bash
sudo rmdir /sys/fs/cgroup/lfs-sandbox 2>/dev/null || true
```
