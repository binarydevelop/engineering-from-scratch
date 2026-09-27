# Project 01: Multi-User Raw TCP Chat Server

> **Motto**: A chat server is simply a broadcast multiplexer sitting over a collection of connected TCP stream sockets.

---

## 1. Overview
In this project, you construct a multi-user conversational chat system directly on top of the POSIX socket API without external frameworks.

## 2. Architecture & File Descriptors
```text
                       SERVER EVENT LOOP (select)
                           server_sock (fd 3)
                                  │
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
  Client 1 (fd 4)          Client 2 (fd 5)          Client 3 (fd 6)
  [ "Hello all!" ] ──► Server receives on fd 4
                       Server iterates {fd 5, fd 6}
                       Server broadcast sends payload
```

## 3. How to Run
```bash
# Terminal 1: Start Server
python3 chat_server.py 9001

# Terminal 2: Connect Client A
python3 chat_client.py 127.0.0.1 9001

# Terminal 3: Connect Client B
python3 chat_client.py 127.0.0.1 9001
```

## 4. Test Suite
```bash
python3 test_chat.py
```
