# Project 02: Reverse Proxy Server

## Objective
Configure an Nginx reverse proxy fronting the backend Python service from Project 01.
- Public traffic enters on port `80` (or `8000` in non-root lab)
- Proxies requests to backend application at `127.0.0.1:8080`
- Configures custom proxy headers (`X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`)
- Enforces HTTP connection timeouts and client body limits
- Sets up dedicated access and error logs with structured formatting

---

## Architecture
```text
Client (curl / browser)
         │
         ▼ (Port 80/8000)
    Nginx Reverse Proxy
         │
         ▼ (127.0.0.1:8080)
   Python Backend Service
```
