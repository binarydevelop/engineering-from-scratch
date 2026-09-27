"""
Lesson 37: Token-Based Authentication (JWT).
Implements RFC 7519 JSON Web Token issuance and signature verification with expiration and alg:none rejection.
"""

import time
import jwt
from typing import Dict, Any, Optional

class TokenService:
    """Issues and verifies cryptographically signed JWT tokens."""

    def __init__(self, secret_key: str, algorithm: str = "HS256", token_ttl_seconds: int = 900):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_ttl_seconds = token_ttl_seconds

    def issue_token(self, subject: str, claims: Optional[Dict[str, Any]] = None) -> str:
        """Issues a signed JWT containing subject, iat, and exp claims."""
        now = int(time.time())
        payload = {
            "sub": subject,
            "iat": now,
            "exp": now + self.token_ttl_seconds,
        }
        if claims:
            payload.update(claims)
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token_str: str) -> Dict[str, Any]:
        """
        Verifies token signature, expiration, and algorithm.
        Rejects 'none' algorithm and tampered signatures.
        """
        try:
            # Explicitly enforce the allowed algorithm to prevent 'alg: none' attacks
            decoded = jwt.decode(
                token_str,
                self.secret_key,
                algorithms=[self.algorithm],
                options={"require": ["exp", "iat", "sub"]}
            )
            return decoded
        except jwt.ExpiredSignatureError:
            raise PermissionError("Token has expired")
        except jwt.InvalidSignatureError:
            raise PermissionError("Invalid token signature")
        except jwt.PyJWTError as e:
            raise PermissionError(f"Invalid token: {e}")
