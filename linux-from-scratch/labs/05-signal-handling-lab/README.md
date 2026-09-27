# Lab 05: Signal Handling Sandbox

## Objective
Trace and experiment with Unix signal delivery: `SIGINT`, `SIGTERM`, `SIGHUP`, and `SIGKILL`, contrasting catchable signals with uncatchable kernel terminations.

## Setup Procedure
```bash
# 1. Create a signal trapping Python script
cat << 'EOF' > /tmp/lfs-lab/sig_trap.py
import signal, time, sys, os

def handler(signum, frame):
    sig_name = signal.Signals(signum).name
    print(f"\n[PID {os.getpid()}] Caught signal: {sig_name} ({signum}). Graceful cleanup initiated...")
    sys.exit(0)

signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGHUP, handler)

print(f"Process running (PID: {os.getpid()}). Waiting for signals...")
while True:
    time.sleep(1)
EOF

# 2. Run in background
python3 /tmp/lfs-lab/sig_trap.py &
PID=$!
echo "Launched PID: $PID"

# 3. Test sending catchable SIGTERM
kill -15 "$PID"

# 4. Observe graceful exit
wait "$PID" 2>/dev/null || true
echo "Process terminated gracefully."
```

## Teardown
```bash
rm -f /tmp/lfs-lab/sig_trap.py
```
