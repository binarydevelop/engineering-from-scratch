#!/usr/bin/env python3
import socket
import threading
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../02-build-an-append-only-log/code")))
from mini_log import MiniLog

class TCPLogServer:
    def __init__(self, host="127.0.0.1", port=9999, log_path="/tmp/tcp_log.dat"):
        self.host = host
        self.port = port
        self.log = MiniLog(log_path)
        self.lock = threading.Lock()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def handle_client(self, conn):
        with conn:
            buffer = ""
            while True:
                data = conn.recv(1024)
                if not data: break
                buffer += data.decode("utf-8", errors="ignore")
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line: continue
                    parts = line.split(" ", 2)
                    cmd = parts[0].upper()
                    
                    if cmd == "APPEND" and len(parts) >= 2:
                        payload = parts[1].encode("utf-8")
                        with self.lock:
                            offset = self.log.append(payload)
                        conn.sendall(f"OK OFFSET {offset}\n".encode())
                    elif cmd == "FETCH" and len(parts) >= 2:
                        start_offset = int(parts[1])
                        with self.lock:
                            records = self.log.read_from(start_offset)
                        serializable = [{"offset": o, "data": d.decode("utf-8", errors="ignore")} for o, d in records]
                        conn.sendall(f"OK RECORDS {json.dumps(serializable)}\n".encode())
                    elif cmd == "PING":
                        conn.sendall(b"PONG\n")
                    else:
                        conn.sendall(b"ERR UNKNOWN_COMMAND\n")

    def run(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[TCPLogServer] Listening on {self.host}:{self.port}...")
        try:
            while True:
                conn, _ = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()
        except KeyboardInterrupt:
            print("\nShutting down server.")
        finally:
            self.server_socket.close()
            self.log.close()

if __name__ == "__main__":
    server = TCPLogServer()
    server.run()
