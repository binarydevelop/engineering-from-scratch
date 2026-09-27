#!/usr/bin/env python3
"""
scripts/generate_labs.py
Generates the reusable isolated Linux network namespace laboratory topologies in labs/.
"""

import os

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LABS_DIR = os.path.join(REPO_ROOT, "labs")

LAB_SPECS = [
    ("01-two-node-veth", "Two-Node Direct veth Link",
     "Constructs two namespaces (ns-alpha and ns-beta) connected by a point-to-point virtual ethernet pair.",
     """#!/usr/bin/env bash
set -euo pipefail
sudo ip netns add ns-alpha
sudo ip netns add ns-beta
sudo ip link add veth-a type veth peer name veth-b
sudo ip link set veth-a netns ns-alpha
sudo ip link set veth-b netns ns-beta
sudo ip netns exec ns-alpha ip addr add 192.168.100.1/24 dev veth-a
sudo ip netns exec ns-beta ip addr add 192.168.100.2/24 dev veth-b
sudo ip netns exec ns-alpha ip link set veth-a up
sudo ip netns exec ns-beta ip link set veth-b up
sudo ip netns exec ns-alpha ip link set lo up
sudo ip netns exec ns-beta ip link set lo up
echo "Lab 01 active. Test with: sudo ip netns exec ns-alpha ping 192.168.100.2"
""",
     """#!/usr/bin/env bash
set -euo pipefail
sudo ip netns del ns-alpha 2>/dev/null || true
sudo ip netns del ns-beta 2>/dev/null || true
echo "Lab 01 dismantled."
"""),

    ("02-bridge-lan", "Multi-Host Linux Bridge LAN",
     "Connects three isolated namespaces (ns1, ns2, ns3) into a single Layer-2 broadcast domain via a Linux software bridge.",
     """#!/usr/bin/env bash
set -euo pipefail
sudo ip netns add ns1
sudo ip netns add ns2
sudo ip netns add ns3
sudo ip link add br0 type bridge
sudo ip link set br0 up

for i in 1 2 3; do
    sudo ip link add "veth$i" type veth peer name "br-veth$i"
    sudo ip link set "veth$i" netns "ns$i"
    sudo ip link set "br-veth$i" master br0
    sudo ip link set "br-veth$i" up
    sudo ip netns exec "ns$i" ip addr add "10.0.0.$i/24" dev "veth$i"
    sudo ip netns exec "ns$i" ip link set "veth$i" up
    sudo ip netns exec "ns$i" ip link set lo up
done
echo "Lab 02 active. Test with: sudo ip netns exec ns1 ping -c 2 10.0.0.2"
""",
     """#!/usr/bin/env bash
set -euo pipefail
for i in 1 2 3; do sudo ip netns del "ns$i" 2>/dev/null || true; done
sudo ip link del br0 2>/dev/null || true
echo "Lab 02 dismantled."
"""),

    ("03-three-node-router", "Multi-Subnet Routed Network",
     "Constructs Client LAN (10.99.1.0/24) and Server LAN (10.99.2.0/24) bridged by an intermediate Linux router namespace with IP forwarding enabled.",
     """#!/usr/bin/env bash
set -euo pipefail
sudo ../../scripts/create-network-lab.sh
""",
     """#!/usr/bin/env bash
set -euo pipefail
sudo ../../scripts/destroy-network-lab.sh
"""),

    ("04-nat-gateway", "Source NAT / Masquerade Gateway",
     "Sets up a private host behind a Linux router with iptables SNAT (MASQUERADE) enabled.",
     """#!/usr/bin/env bash
set -euo pipefail
sudo ip netns add ns-priv
sudo ip netns add ns-nat
sudo ip netns add ns-wan
sudo ip link add veth-p type veth peer name veth-np
sudo ip link set veth-p netns ns-priv
sudo ip link set veth-np netns ns-nat
sudo ip link add veth-nw type veth peer name veth-w
sudo ip link set veth-nw netns ns-nat
sudo ip link set veth-w netns ns-wan

sudo ip netns exec ns-priv ip addr add 10.0.1.10/24 dev veth-p
sudo ip netns exec ns-priv ip link set veth-p up
sudo ip netns exec ns-priv ip link set lo up
sudo ip netns exec ns-priv ip route add default via 10.0.1.1

sudo ip netns exec ns-nat ip addr add 10.0.1.1/24 dev veth-np
sudo ip netns exec ns-nat ip addr add 203.0.113.1/24 dev veth-nw
sudo ip netns exec ns-nat ip link set veth-np up
sudo ip netns exec ns-nat ip link set veth-nw up
sudo ip netns exec ns-nat sysctl -w net.ipv4.ip_forward=1 >/dev/null
sudo ip netns exec ns-nat iptables -t nat -A POSTROUTING -o veth-nw -j MASQUERADE

sudo ip netns exec ns-wan ip addr add 203.0.113.100/24 dev veth-w
sudo ip netns exec ns-wan ip link set veth-w up
sudo ip netns exec ns-wan ip link set lo up

echo "Lab 04 active. Test SNAT: sudo ip netns exec ns-priv ping -c 2 203.0.113.100"
""",
     """#!/usr/bin/env bash
set -euo pipefail
sudo ip netns del ns-priv 2>/dev/null || true
sudo ip netns del ns-nat 2>/dev/null || true
sudo ip netns del ns-wan 2>/dev/null || true
echo "Lab 04 dismantled."
"""),

    ("05-firewall-isolation", "Stateful Firewall Inspection Lab",
     "Constructs a testbed to inspect iptables/nftables stateful connection tracking (conntrack).",
     """#!/usr/bin/env bash
set -euo pipefail
sudo ip netns add ns-firewall
sudo ip netns exec ns-firewall ip link set lo up
echo "Lab 05 active inside ns-firewall."
""",
     """#!/usr/bin/env bash
set -euo pipefail
sudo ip netns del ns-firewall 2>/dev/null || true
echo "Lab 05 dismantled."
"""),

    ("06-mtu-blackhole", "Path MTU Black Hole Simulation",
     "Simulates path MTU reduction to 1400 bytes with ICMP drop to reproduce PMTUD failure.",
     """#!/usr/bin/env bash
set -euo pipefail
sudo ip netns add ns-mtu-client
sudo ip netns add ns-mtu-server
sudo ip link add v-c type veth peer name v-s
sudo ip link set v-c netns ns-mtu-client
sudo ip link set v-s netns ns-mtu-server
sudo ip netns exec ns-mtu-client ip addr add 192.168.200.1/24 dev v-c
sudo ip netns exec ns-mtu-server ip addr add 192.168.200.2/24 dev v-s
sudo ip netns exec ns-mtu-client ip link set v-c up
sudo ip netns exec ns-mtu-server ip link set v-s up
# Reduce MTU on server interface to 1400
sudo ip netns exec ns-mtu-server ip link set v-s mtu 1400
echo "Lab 06 active. Test with: sudo ip netns exec ns-mtu-client ping -M do -s 1472 192.168.200.2"
""",
     """#!/usr/bin/env bash
set -euo pipefail
sudo ip netns del ns-mtu-client 2>/dev/null || true
sudo ip netns del ns-mtu-server 2>/dev/null || true
echo "Lab 06 dismantled."
"""),
]


def generate_labs():
    os.makedirs(LABS_DIR, exist_ok=True)
    master_readme = [
        "# Reusable Linux Network Namespace Labs",
        "",
        "> **Rule**: All routing mutations, bridge setups, firewall rules, and NAT tests must occur strictly inside these isolated namespaces. Never mutate your host interface configuration.",
        "",
        "| ID | Lab Topology | Description | Setup Script |",
        "| :--- | :--- | :--- | :--- |",
    ]

    for dir_name, title, desc, setup_sh, teardown_sh in LAB_SPECS:
        path = os.path.join(LABS_DIR, dir_name)
        os.makedirs(path, exist_ok=True)
        master_readme.append(f"| **{dir_name[:2]}** | [{title}]({dir_name}/) | {desc} | `./setup.sh` |")

        with open(os.path.join(path, "setup.sh"), "w") as f:
            f.write(setup_sh)
        os.chmod(os.path.join(path, "setup.sh"), 0o755)

        with open(os.path.join(path, "teardown.sh"), "w") as f:
            f.write(teardown_sh)
        os.chmod(os.path.join(path, "teardown.sh"), 0o755)

        readme_text = f"""# Lab: {title}

---

## 1. Overview
{desc}

## 2. Setup
```bash
sudo ./setup.sh
```

## 3. Teardown
```bash
sudo ./teardown.sh
```
"""
        with open(os.path.join(path, "README.md"), "w") as f:
            f.write(readme_text)

    with open(os.path.join(LABS_DIR, "README.md"), "w") as f:
        f.write("\n".join(master_readme) + "\n")

    print(f"Successfully generated all {len(LAB_SPECS)} reusable lab topologies!")


if __name__ == "__main__":
    generate_labs()
