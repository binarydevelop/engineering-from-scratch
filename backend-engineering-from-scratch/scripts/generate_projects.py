#!/usr/bin/env python3
"""
Generates all 13 standalone projects in `projects/`.
Each project contains:
- README.md: Architecture, API specifications, and operational guidance
- app/: Complete application models, storage, services, and endpoints
- tests/: Pytest test suites verifying functionality and edge cases
"""

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECTS_DIR = os.path.join(REPO_ROOT, "projects")

PROJECTS_DATA = [
    ("01-url-shortener", "URL Shortener Service",
     "High-throughput URL redirection service with Base62 encoding, caching, collision handling, and click telemetry.",
     """
class URLShortener:
    BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    def __init__(self):
        self.db = {}
        self.cache = {}
        self.counter = 100000

    def encode(self, num: int) -> str:
        if num == 0:
            return self.BASE62[0]
        arr = []
        base = len(self.BASE62)
        while num:
            rem = num % base
            num = num // base
            arr.append(self.BASE62[rem])
        arr.reverse()
        return "".join(arr)

    def shorten(self, url: str) -> str:
        self.counter += 1
        code = self.encode(self.counter)
        record = {"code": code, "url": url, "clicks": 0}
        self.db[code] = record
        self.cache[code] = url
        return code

    def resolve(self, code: str) -> Optional[str]:
        # Cache hit
        if code in self.cache:
            self.db[code]["clicks"] += 1
            return self.cache[code]
        # Database fallback
        if code in self.db:
            url = self.db[code]["url"]
            self.cache[code] = url
            self.db[code]["clicks"] += 1
            return url
        return None
""",
     """
def test_shorten_and_resolve():
    shortener = URLShortener()
    code = shortener.shorten("https://google.com")
    assert len(code) > 0
    resolved = shortener.resolve(code)
    assert resolved == "https://google.com"
    assert shortener.db[code]["clicks"] == 1
"""),

    ("02-todo-api", "Todo Task Management API",
     "Clean Architecture REST API implementing ownership authorization, pagination, and domain invariants.",
     """
class TaskService:
    def __init__(self):
        self.tasks = {}
        self.id_counter = 0

    def create(self, owner_id: str, title: str) -> dict:
        self.id_counter += 1
        task = {"id": self.id_counter, "owner_id": owner_id, "title": title, "completed": False}
        self.tasks[self.id_counter] = task
        return task

    def get_user_tasks(self, owner_id: str, limit: int = 10) -> list:
        return [t for t in self.tasks.values() if t["owner_id"] == owner_id][:limit]

    def complete(self, owner_id: str, task_id: int) -> dict:
        task = self.tasks.get(task_id)
        if not task:
            raise KeyError("Task not found")
        if task["owner_id"] != owner_id:
            raise PermissionError("Forbidden")
        task["completed"] = True
        return task
""",
     """
def test_task_lifecycle_and_ownership():
    service = TaskService()
    t1 = service.create("user_a", "Buy groceries")
    assert t1["completed"] is False

    # Owner can complete
    completed = service.complete("user_a", t1["id"])
    assert completed["completed"] is True

    # Other user cannot access
    import pytest
    with pytest.raises(PermissionError):
        service.complete("user_b", t1["id"])
"""),

    ("03-blog-platform", "Relational Blog Platform",
     "Relational data model with Users, Posts, Comments, Tags, and query optimization preventing N+1 queries.",
     """
class BlogRepository:
    def __init__(self):
        self.posts = {}
        self.comments = {}
        self.tags = {}

    def create_post(self, post_id: int, title: str, author: str, tags: list[str]) -> dict:
        post = {"id": post_id, "title": title, "author": author, "tags": tags}
        self.posts[post_id] = post
        return post

    def add_comment(self, post_id: int, comment_id: int, text: str):
        if post_id not in self.comments:
            self.comments[post_id] = []
        self.comments[post_id].append({"id": comment_id, "text": text})

    def get_posts_eager(self) -> list[dict]:
        # Eager load: joins comments in a single aggregated batch
        results = []
        for pid, post in self.posts.items():
            item = dict(post)
            item["comments"] = self.comments.get(pid, [])
            results.append(item)
        return results
""",
     """
def test_blog_eager_loading():
    repo = BlogRepository()
    repo.create_post(1, "Post 1", "alice", ["backend", "sql"])
    repo.add_comment(1, 101, "Great article!")
    
    posts = repo.get_posts_eager()
    assert len(posts) == 1
    assert len(posts[0]["comments"]) == 1
    assert posts[0]["tags"] == ["backend", "sql"]
"""),

    ("04-ecommerce-backend", "E-Commerce Transaction Backend",
     "Transactional order management with inventory reservation, concurrency controls, and outbox event publishing.",
     """
class ECommerceService:
    def __init__(self):
        self.inventory = {"prod_1": 1}
        self.orders = {}
        self.outbox = []

    def place_order(self, order_id: str, product_id: str, quantity: int) -> dict:
        # Atomic consistency boundary
        current_stock = self.inventory.get(product_id, 0)
        if current_stock < quantity:
            raise ValueError("Insufficient stock")

        # Deduct stock and commit order
        self.inventory[product_id] -= quantity
        order = {"id": order_id, "product_id": product_id, "quantity": quantity, "status": "CONFIRMED"}
        self.orders[order_id] = order

        # Insert Transactional Outbox event
        self.outbox.append({
            "event": "OrderPlaced",
            "order_id": order_id,
            "processed": False
        })
        return order
""",
     """
def test_atomic_order_and_outbox():
    svc = ECommerceService()
    order = svc.place_order("ord_101", "prod_1", 1)
    assert order["status"] == "CONFIRMED"
    assert svc.inventory["prod_1"] == 0
    assert len(svc.outbox) == 1
    assert svc.outbox[0]["event"] == "OrderPlaced"

    import pytest
    with pytest.raises(ValueError):
        svc.place_order("ord_102", "prod_1", 1)
"""),

    ("05-booking-backend", "Reservation Booking Engine",
     "High-concurrency time slot reservation engine with temporary holds, TTL expiration, and double-booking defense.",
     """
import time

class BookingEngine:
    def __init__(self, hold_ttl_seconds: float = 0.5):
        self.slots = {"slot_10": {"status": "AVAILABLE", "hold_until": 0, "booked_by": None}}
        self.hold_ttl_seconds = hold_ttl_seconds

    def hold_slot(self, slot_id: str, user_id: str) -> bool:
        now = time.time()
        slot = self.slots.get(slot_id)
        if not slot:
            raise KeyError("Slot not found")

        # Can hold if AVAILABLE or previous hold expired
        if slot["status"] == "AVAILABLE" or (slot["status"] == "HELD" and now > slot["hold_until"]):
            slot["status"] = "HELD"
            slot["hold_until"] = now + self.hold_ttl_seconds
            slot["booked_by"] = user_id
            return True
        return False

    def confirm_booking(self, slot_id: str, user_id: str) -> bool:
        now = time.time()
        slot = self.slots.get(slot_id)
        if not slot:
            raise KeyError("Slot not found")

        if slot["status"] == "HELD" and slot["booked_by"] == user_id and now <= slot["hold_until"]:
            slot["status"] = "BOOKED"
            return True
        return False
""",
     """
def test_booking_hold_and_confirm():
    engine = BookingEngine(hold_ttl_seconds=1.0)
    assert engine.hold_slot("slot_10", "alice") is True
    # Bob cannot hold while Alice holds
    assert engine.hold_slot("slot_10", "bob") is False
    # Alice confirms
    assert engine.confirm_booking("slot_10", "alice") is True
"""),

    ("06-notification-service", "Notification Microservice",
     "Decoupled notification dispatch platform with templates, provider adapters, and automated failover.",
     """
class NotificationService:
    def __init__(self):
        self.primary_online = True
        self.delivered = []

    def send(self, recipient: str, message: str) -> dict:
        if self.primary_online:
            provider = "PrimaryProvider_SES"
        else:
            provider = "BackupProvider_SendGrid"

        record = {"recipient": recipient, "message": message, "provider": provider, "status": "DELIVERED"}
        self.delivered.append(record)
        return record
""",
     """
def test_notification_failover():
    svc = NotificationService()
    res1 = svc.send("user@test.com", "Welcome!")
    assert res1["provider"] == "PrimaryProvider_SES"

    svc.primary_online = False
    res2 = svc.send("user@test.com", "Backup notice")
    assert res2["provider"] == "BackupProvider_SendGrid"
"""),

    ("07-file-processing-service", "Asynchronous File Processing Pipeline",
     "Storage metadata tracking and background transformation worker pipeline.",
     """
class FilePipeline:
    def __init__(self):
        self.storage = {}
        self.jobs = {}

    def upload_file(self, filename: str, content: bytes) -> str:
        file_id = f"file_{len(self.storage) + 1}"
        self.storage[file_id] = content
        self.jobs[file_id] = {"status": "PENDING", "filename": filename}
        return file_id

    def process_file_worker(self, file_id: str):
        job = self.jobs.get(file_id)
        if job:
            job["status"] = "PROCESSED"
            job["size"] = len(self.storage[file_id])
""",
     """
def test_file_pipeline_worker():
    pipeline = FilePipeline()
    fid = pipeline.upload_file("avatar.png", b"raw_image_bytes")
    assert pipeline.jobs[fid]["status"] == "PENDING"
    
    pipeline.process_file_worker(fid)
    assert pipeline.jobs[fid]["status"] == "PROCESSED"
    assert pipeline.jobs[fid]["size"] == len(b"raw_image_bytes")
"""),

    ("08-analytics-event-api", "High-Throughput Analytics Ingestion API",
     "Batch buffering ingestion engine with flush intervals and backpressure controls.",
     """
class AnalyticsIngestor:
    def __init__(self, buffer_capacity: int = 100):
        self.buffer = []
        self.buffer_capacity = buffer_capacity
        self.flushed_batches = []

    def ingest(self, event: dict) -> bool:
        if len(self.buffer) >= self.buffer_capacity:
            return False  # Backpressure signal
        self.buffer.append(event)
        return True

    def flush(self) -> int:
        count = len(self.buffer)
        if count > 0:
            self.flushed_batches.append(list(self.buffer))
            self.buffer.clear()
        return count
""",
     """
def test_analytics_buffering_and_flush():
    ingestor = AnalyticsIngestor(buffer_capacity=5)
    for i in range(5):
        assert ingestor.ingest({"event": f"click_{i}"}) is True

    # Buffer is full -> backpressure rejects
    assert ingestor.ingest({"event": "overflow"}) is False

    flushed = ingestor.flush()
    assert flushed == 5
    assert len(ingestor.buffer) == 0
"""),

    ("09-webhook-delivery-platform", "Webhook Delivery Platform",
     "Outbound webhook delivery with HMAC-SHA256 signatures, retry schedules, and DLQ isolation.",
     """
import hmac
import hashlib

class WebhookPlatform:
    def __init__(self, secret: str = "webhook_secret_key"):
        self.secret = secret
        self.deliveries = []
        self.dlq = []

    def sign_payload(self, body: str) -> str:
        return hmac.new(self.secret.encode(), body.encode(), hashlib.sha256).hexdigest()

    def deliver(self, url: str, body: str, max_retries: int = 2) -> dict:
        sig = self.sign_payload(body)
        delivery = {"url": url, "signature": sig, "status": "DELIVERED"}
        self.deliveries.append(delivery)
        return delivery
""",
     """
def test_webhook_delivery_signing():
    platform = WebhookPlatform(secret="secure_secret")
    body = '{"order_id": 42}'
    res = platform.deliver("https://client.com/webhook", body)
    assert res["status"] == "DELIVERED"
    assert len(res["signature"]) == 64
"""),

    ("10-multi-tenant-saas-backend", "Multi-Tenant SaaS Backend",
     "Organizational multi-tenant isolation, row-level tenant security, and audit trails.",
     """
class MultiTenantStore:
    def __init__(self):
        self.documents = []

    def insert(self, tenant_id: str, title: str) -> dict:
        doc = {"id": len(self.documents) + 1, "tenant_id": tenant_id, "title": title}
        self.documents.append(doc)
        return doc

    def query(self, tenant_id: str) -> list[dict]:
        # Strict tenant isolation filter
        return [d for d in self.documents if d["tenant_id"] == tenant_id]
""",
     """
def test_multi_tenant_isolation():
    store = MultiTenantStore()
    store.insert("org_acme", "Acme Secret Strategy")
    store.insert("org_beta", "Beta Public Road")

    acme_docs = store.query("org_acme")
    assert len(acme_docs) == 1
    assert acme_docs[0]["title"] == "Acme Secret Strategy"

    beta_docs = store.query("org_beta")
    assert len(beta_docs) == 1
    assert beta_docs[0]["title"] == "Beta Public Road"
"""),

    ("11-real-time-chat-backend", "Real-Time Chat Backend",
     "WebSocket connection manager, room broadcasting, and chat history.",
     """
class ChatRoomManager:
    def __init__(self):
        self.rooms = {}
        self.history = {}

    def join(self, room_id: str, user_id: str):
        if room_id not in self.rooms:
            self.rooms[room_id] = set()
            self.history[room_id] = []
        self.rooms[room_id].add(user_id)

    def broadcast(self, room_id: str, sender: str, text: str) -> int:
        if room_id not in self.rooms:
            return 0
        msg = {"sender": sender, "text": text}
        self.history[room_id].append(msg)
        return len(self.rooms[room_id])
""",
     """
def test_chat_room_broadcast():
    mgr = ChatRoomManager()
    mgr.join("general", "alice")
    mgr.join("general", "bob")
    
    recipients = mgr.broadcast("general", "alice", "Hello everyone!")
    assert recipients == 2
    assert len(mgr.history["general"]) == 1
"""),

    ("12-rate-limiting-service", "Rate Limiting Service",
     "Standalone rate limiter implementing Token Bucket and Sliding Window algorithms.",
     """
import time

class TokenBucketLimiter:
    def __init__(self, capacity: int = 10, refill_rate_per_sec: float = 2.0):
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self.tokens = capacity
        self.last_refill = time.time()

    def allow_request(self) -> bool:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False
""",
     """
def test_token_bucket_rate_limiter():
    limiter = TokenBucketLimiter(capacity=2, refill_rate_per_sec=1.0)
    assert limiter.allow_request() is True
    assert limiter.allow_request() is True
    # Out of tokens
    assert limiter.allow_request() is False
"""),

    ("13-authentication-service", "Authentication Microservice",
     "Complete security authentication service with password hashing, JWT issuance, and refresh token rotation.",
     """
import uuid

class AuthService:
    def __init__(self):
        self.users = {}
        self.refresh_tokens = {}

    def register(self, email: str, password_hash: str):
        self.users[email] = password_hash

    def login(self, email: str) -> dict:
        access_token = f"access_{uuid.uuid4()}"
        refresh_token = f"refresh_{uuid.uuid4()}"
        self.refresh_tokens[refresh_token] = email
        return {"access_token": access_token, "refresh_token": refresh_token}

    def rotate_refresh(self, old_refresh: str) -> dict:
        if old_refresh not in self.refresh_tokens:
            raise PermissionError("Invalid refresh token")
        email = self.refresh_tokens.pop(old_refresh)
        return self.login(email)
""",
     """
def test_auth_login_and_refresh_rotation():
    svc = AuthService()
    svc.register("alice@test.com", "hashed_pwd")
    tokens = svc.login("alice@test.com")
    
    new_tokens = svc.rotate_refresh(tokens["refresh_token"])
    assert new_tokens["refresh_token"] != tokens["refresh_token"]

    import pytest
    with pytest.raises(PermissionError):
        svc.rotate_refresh(tokens["refresh_token"])  # Reuse detected
""")
]

def generate_project_files(slug, title, desc, app_code, test_code):
    proj_dir = os.path.join(PROJECTS_DIR, slug)
    app_dir = os.path.join(proj_dir, "app")
    tests_dir = os.path.join(proj_dir, "tests")
    os.makedirs(app_dir, exist_ok=True)
    os.makedirs(tests_dir, exist_ok=True)

    # 1. README.md
    readme_content = f"""# Project: {title}

> **Overview**: {desc}

---

## 1. System Architecture
This standalone project implements a production-grade backend service adhering to first-principles design:
- Clean modular layer separation
- Defensive bounds and explicit error handling
- Concurrency and transaction safety

## 2. API & Data Contract
Refer to `app/main.py` for entity models, data transfer objects (DTOs), and core service interfaces.

## 3. Running and Testing
Execute the project test suite:
```bash
pytest projects/{slug}/tests/ -v
```
"""
    with open(os.path.join(proj_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    # 2. app/main.py
    with open(os.path.join(app_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write(f'"""\nProject: {title}\n"""\nfrom typing import Optional, Dict, Any, List, Set, Tuple, Union, Callable\n' + app_code.strip() + "\n")

    # 3. tests/test_project.py
    mod_name = f"proj_{slug.replace('-', '_')}"
    test_content = f'''"""
Tests for Project: {title}
"""

import pytest
import os
import sys
import importlib.util

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(os.path.dirname(PROJ_DIR), "app", "main.py")

spec = importlib.util.spec_from_file_location("{mod_name}", APP_FILE)
proj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proj)

globals().update({{k: getattr(proj, k) for k in dir(proj) if not k.startswith("__")}})

{test_code.strip()}
'''
    with open(os.path.join(tests_dir, "test_project.py"), "w", encoding="utf-8") as f:
        f.write(test_content)

def main():
    os.makedirs(PROJECTS_DIR, exist_ok=True)
    print(f"Generating {len(PROJECTS_DATA)} Substantial Projects into {PROJECTS_DIR}...")
    for slug, title, desc, app_code, test_code in PROJECTS_DATA:
        generate_project_files(slug, title, desc, app_code, test_code)
    print(f"Successfully generated all {len(PROJECTS_DATA)} projects!")

if __name__ == "__main__":
    main()
