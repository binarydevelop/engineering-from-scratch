"""
Lesson 35: Password Storage.
Implements salted adaptive work-factor password hashing and constant-time verification using bcrypt.
"""

import bcrypt

class PasswordHasher:
    """Secure password hasher enforcing per-user salting and configurable work factors."""

    def __init__(self, rounds: int = 12):
        self.rounds = rounds

    def hash_password(self, plaintext: str) -> str:
        """Hashes plaintext password with a unique cryptographic salt."""
        if not plaintext:
            raise ValueError("Password cannot be empty")
        # Generate salt with specified work factor
        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed_bytes = bcrypt.hashpw(plaintext.encode("utf-8"), salt)
        return hashed_bytes.decode("utf-8")

    def verify_password(self, plaintext: str, hashed_str: str) -> bool:
        """Verifies plaintext against stored hash in constant time."""
        if not plaintext or not hashed_str:
            return False
        try:
            return bcrypt.checkpw(plaintext.encode("utf-8"), hashed_str.encode("utf-8"))
        except (ValueError, TypeError):
            return False
