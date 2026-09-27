"""
Project: Authentication Microservice
"""
from typing import Optional, Dict, Any, List, Set, Tuple, Union, Callable
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
