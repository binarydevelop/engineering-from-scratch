#!/usr/bin/env python3
# Standalone Server Health Inspector
# Reads raw data directly from /proc virtual filesystems
import json
import os
import sys

def get_cpu_info():
    cores = 0
    with open("/proc/cpuinfo") as f:
        for line in f:
            if line.startswith("processor"):
                cores += 1
    with open("/proc/loadavg") as f:
        load = f.read().split()[:3]
    return {"cores": cores, "load_1m": float(load[0]), "load_5m": float(load[1]), "load_15m": float(load[2])}

def get_memory_info():
    mem = {}
    with open("/proc/meminfo") as f:
        for line in f:
            parts = line.split(":")
            if len(parts) == 2:
                key = parts[0].strip()
                val = parts[1].strip().split()[0]
                mem[key] = int(val) / 1024  # MB
    total = mem.get("MemTotal", 0)
    avail = mem.get("MemAvailable", 0)
    used = total - avail
    pct = (used / total * 100) if total > 0 else 0
    return {"total_mb": round(total, 1), "used_mb": round(used, 1), "available_mb": round(avail, 1), "used_percent": round(pct, 1)}

def get_disk_info(path="/"):
    st = os.statvfs(path)
    total = (st.f_blocks * st.f_frsize) / (1024 * 1024 * 1024)
    free = (st.f_bavail * st.f_frsize) / (1024 * 1024 * 1024)
    used = total - free
    pct = (used / total * 100) if total > 0 else 0
    return {"mount": path, "total_gb": round(total, 2), "used_gb": round(used, 2), "free_gb": round(free, 2), "used_percent": round(pct, 1)}

def main():
    cpu = get_cpu_info()
    mem = get_memory_info()
    disk = get_disk_info()

    data = {"cpu": cpu, "memory": mem, "storage": disk}

    if "--json" in sys.argv:
        print(json.dumps(data, indent=2))
        return

    print("==================================================")
    print("        LINUX HEALTH AUDIT METRICS (/proc)        ")
    print("==================================================")
    print(f"CPU Cores    : {cpu['cores']}")
    print(f"Load Average : 1m={cpu['load_1m']}, 5m={cpu['load_5m']}, 15m={cpu['load_15m']}")
    print(f"RAM Usage    : {mem['used_mb']} MB / {mem['total_mb']} MB ({mem['used_percent']}%)")
    print(f"Disk Usage   : {disk['used_gb']} GB / {disk['total_gb']} GB ({disk['used_percent']}%) on {disk['mount']}")

    # Threshold alerts
    alerts = []
    if mem['used_percent'] > 90:
        alerts.append("CRITICAL: Available Memory below 10%!")
    if disk['used_percent'] > 85:
        alerts.append("WARNING: Disk utilization above 85%!")
    if cpu['load_1m'] > (cpu['cores'] * 2):
        alerts.append("WARNING: High CPU saturation!")

    print("--------------------------------------------------")
    if alerts:
        print("ACTIVE ALERTS:")
        for a in alerts:
            print(f"  [!] {a}")
    else:
        print("[✓] All resource metrics within normal operating bounds.")
    print("==================================================")

if __name__ == "__main__":
    main()
