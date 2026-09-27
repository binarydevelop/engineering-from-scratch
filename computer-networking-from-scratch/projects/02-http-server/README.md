# Project 02: HTTP/1.1 Server From Scratch

> **Motto**: HTTP is not an opaque binary protocol; it is a stream of ASCII lines and CRLF delimiters framed directly over a TCP socket connection.

---

## 1. Overview
In this project, you build an HTTP/1.1 compliant server without using any HTTP libraries. The server reads directly from POSIX stream sockets, parses request lines and headers, routes URIs, and handles Keep-Alive connections.

## 2. Request Parsing Flow
```text
Raw TCP Stream ──► Read until b"\r\n\r\n"
                    ├─ Request Line: "GET /api/status HTTP/1.1"
                    ├─ Headers: Host, Connection, Content-Length
                    ├─ Optional Body: (Read Content-Length bytes)
                    └─ Response: Format Status Line + Headers + Body
```

## 3. Running the Server
```bash
python3 http_server.py 8080

# In another terminal:
curl -v http://127.0.0.1:8080/
curl -v http://127.0.0.1:8080/api/status
curl -v -X POST -d "sample body" http://127.0.0.1:8080/api/echo
```

## 4. Automated Tests
```bash
python3 test_http.py
```
