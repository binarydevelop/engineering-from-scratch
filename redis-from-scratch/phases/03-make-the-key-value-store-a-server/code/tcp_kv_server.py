#!/usr/bin/env python3
import socket
import threading

class TCPServerKV:
    def __init__(self, port=9999):
        self.port = port
        self.store = {}
        self.running = True

    def handle_client(self, client_sock):
        with client_sock:
            buffer = ""
            while self.running:
                data = client_sock.recv(1024).decode("utf-8", errors="replace")
                if not data: break
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line: continue
                    parts = line.split(" ", 2)
                    cmd = parts[0].upper()
                    
                    if cmd == "SET" and len(parts) >= 3:
                        self.store[parts[1]] = parts[2]
                        client_sock.sendall(b"+OK\n")
                    elif cmd == "GET" and len(parts) >= 2:
                        val = self.store.get(parts[1], None)
                        if val is None:
                            client_sock.sendall(b"-NIL\n")
                        else:
                            client_sock.sendall(f"+{val}\n".encode())
                    elif cmd == "PING":
                        client_sock.sendall(b"+PONG\n")
                    elif cmd == "QUIT":
                        return
                    else:
                        client_sock.sendall(b"-ERR unknown command or syntax\n")

    def run_test_client(self):
        import time
        time.sleep(0.1)
        s = socket.create_connection(("localhost", self.port))
        s.sendall(b"SET username Tushar\n")
        print("Client received:", s.recv(1024).decode().strip())
        s.sendall(b"GET username\n")
        print("Client received:", s.recv(1024).decode().strip())
        s.sendall(b"QUIT\n")
        s.close()

if __name__ == "__main__":
    server = TCPServerKV(port=9998)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("localhost", 9998))
    server_sock.listen(5)
    
    t = threading.Thread(target=server.run_test_client)
    t.start()
    
    conn, _ = server_sock.accept()
    server.handle_client(conn)
    server_sock.close()
    t.join()
