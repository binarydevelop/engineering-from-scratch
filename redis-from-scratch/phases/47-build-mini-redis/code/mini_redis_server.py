#!/usr/bin/env python3
"""
phases/47-build-mini-redis/code/mini_redis_server.py — Educational Mini-Redis Server
Connect with real redis-cli: redis-cli -p 6388 PING
"""
import socket
import threading
import time

class MiniRedisServer:
    def __init__(self, port=6388):
        self.port = port
        self.db = {}       # key -> value
        self.expires = {}  # key -> expire_timestamp
        self.running = True

    def parse_resp(self, data):
        """Simple parser for RESP array commands."""
        lines = data.split(b"\r\n")
        if not lines or not lines[0].startswith(b"*"): return []
        num_args = int(lines[0][1:])
        args = []
        idx = 1
        for _ in range(num_args):
            if idx >= len(lines): break
            if lines[idx].startswith(b"$"):
                length = int(lines[idx][1:])
                idx += 1
                args.append(lines[idx][:length].decode("utf-8", errors="replace"))
                idx += 1
        return args

    def handle_client(self, client_sock):
        with client_sock:
            while self.running:
                data = client_sock.recv(4096)
                if not data: break
                args = self.parse_resp(data)
                if not args: continue
                
                cmd = args[0].upper()
                now = time.time()

                # Passive expiration check
                if len(args) > 1 and args[1] in self.expires:
                    if self.expires[args[1]] <= now:
                        del self.expires[args[1]]
                        if args[1] in self.db: del self.db[args[1]]

                # Dispatch
                if cmd == "PING":
                    client_sock.sendall(b"+PONG\r\n")
                elif cmd == "SET" and len(args) >= 3:
                    self.db[args[1]] = args[2]
                    if len(args) >= 5 and args[3].upper() == "EX":
                        self.expires[args[1]] = now + float(args[4])
                    client_sock.sendall(b"+OK\r\n")
                elif cmd == "GET" and len(args) >= 2:
                    val = self.db.get(args[1])
                    if val is None: client_sock.sendall(b"$-1\r\n")
                    else: client_sock.sendall(f"${len(val.encode())}\r\n{val}\r\n".encode())
                elif cmd == "DEL" and len(args) >= 2:
                    count = 0
                    for k in args[1:]:
                        if k in self.db: del self.db[k]; count += 1
                        if k in self.expires: del self.expires[k]
                    client_sock.sendall(f":{count}\r\n".encode())
                elif cmd == "INCR" and len(args) >= 2:
                    curr = int(self.db.get(args[1], 0)) + 1
                    self.db[args[1]] = str(curr)
                    client_sock.sendall(f":{curr}\r\n".encode())
                elif cmd == "TTL" and len(args) >= 2:
                    k = args[1]
                    if k not in self.db: client_sock.sendall(b":-2\r\n")
                    elif k not in self.expires: client_sock.sendall(b":-1\r\n")
                    else:
                        rem = max(0, int(self.expires[k] - now))
                        client_sock.sendall(f":{rem}\r\n".encode())
                else:
                    client_sock.sendall(b"-ERR unknown command\r\n")

    def run_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", self.port))
        s.listen(10)
        print(f"Mini-Redis Server listening on port {self.port} (Connect with redis-cli -p {self.port})")
        while self.running:
            conn, _ = s.accept()
            threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    server = MiniRedisServer(port=6388)
    server.run_server()
