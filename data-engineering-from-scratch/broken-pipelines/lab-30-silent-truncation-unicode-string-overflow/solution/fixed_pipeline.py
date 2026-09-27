"""
Resilient, production-ready solution for lab-30-silent-truncation-unicode-string-overflow.
"""
def safe_utf8_truncate(s, max_bytes=10):
    encoded = s.encode("utf-8")
    if len(encoded) <= max_bytes:
        return s
    return encoded[:max_bytes].decode("utf-8", errors="ignore")
