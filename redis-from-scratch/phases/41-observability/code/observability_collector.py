#!/usr/bin/env python3
import socket

def parse_info(raw):
    metrics = {}
    for line in raw.split("\r\n"):
        if ":" in line and not line.startswith("#"):
            k, v = line.split(":", 1)
            metrics[k] = v
    return metrics

def scrape_metrics():
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    s.sendall(b"*1\r\n$4\r\nINFO\r\n")
    data = s.recv(16384).decode(errors="replace")
    s.close()
    
    m = parse_info(data)
    print("==================================================")
    print("         REDIS PRODUCTION HEALTH DASHBOARD        ")
    print("==================================================")
    print(f"  • Connected Clients    : {m.get('connected_clients', 'N/A')}")
    print(f"  • Ops Per Second       : {m.get('instantaneous_ops_per_sec', 'N/A')}")
    print(f"  • Used Memory (RSS)    : {m.get('used_memory_rss_human', 'N/A')}")
    print(f"  • Fragmentation Ratio  : {m.get('mem_fragmentation_ratio', 'N/A')}")
    print(f"  • Evicted Keys Count   : {m.get('evicted_keys', 'N/A')}")
    print(f"  • Expired Keys Count   : {m.get('expired_keys', 'N/A')}")
    print(f"  • Uptime (days)        : {int(m.get('uptime_in_seconds', 0)) // 86400}")
    print("==================================================")

if __name__ == "__main__":
    try: scrape_metrics()
    except Exception as e: print("Redis offline:", e)
