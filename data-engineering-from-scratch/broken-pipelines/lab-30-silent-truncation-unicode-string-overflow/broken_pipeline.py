"""
Broken implementation demonstrating the flaw in lab-30-silent-truncation-unicode-string-overflow.
"""
def truncate_bytes_broken(s, max_bytes=10):
    return s[:max_bytes] # Character slice != byte length in UTF-8
