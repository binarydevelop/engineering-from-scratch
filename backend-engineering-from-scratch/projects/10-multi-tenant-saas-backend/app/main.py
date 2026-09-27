"""
Project: Multi-Tenant SaaS Backend
"""
from typing import Optional, Dict, Any, List, Set, Tuple, Union, Callable
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
