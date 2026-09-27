"""
Prefix Caching Engine (Phase 58).
Implements a prefix trie / hash table allowing multiple requests
sharing an identical system prompt or document prefix to reuse
precomputed KV cache representations rather than recomputing prefill.
"""

from typing import List, Dict, Tuple, Optional
import hashlib

class PrefixCacheNode:
    def __init__(self, token_hash: str):
        self.token_hash = token_hash
        self.children: Dict[str, "PrefixCacheNode"] = {}
        self.cached_kv_ref: Optional[str] = None
        self.hit_count = 0

class PrefixCacheEngine:
    def __init__(self):
        self.root = PrefixCacheNode("ROOT")
        self.total_queries = 0
        self.total_tokens_saved = 0

    def _hash_tokens(self, tokens: List[int]) -> str:
        s = ",".join(str(t) for t in tokens)
        return hashlib.sha256(s.encode()).hexdigest()[:16]

    def insert_prefix(self, token_ids: List[int], cache_handle: str):
        curr = self.root
        for tok in token_ids:
            key = str(tok)
            if key not in curr.children:
                curr.children[key] = PrefixCacheNode(key)
            curr = curr.children[key]
        curr.cached_kv_ref = cache_handle

    def match_longest_prefix(self, token_ids: List[int]) -> Tuple[int, Optional[str]]:
        """
        Traverses trie to find longest matching prefix.
        Returns: (matched_length, cached_kv_handle)
        """
        self.total_queries += 1
        curr = self.root
        matched_len = 0
        last_valid_handle = None

        for tok in token_ids:
            key = str(tok)
            if key in curr.children:
                curr = curr.children[key]
                matched_len += 1
                curr.hit_count += 1
                if curr.cached_kv_ref:
                    last_valid_handle = curr.cached_kv_ref
            else:
                break

        if last_valid_handle:
            self.total_tokens_saved += matched_len

        return matched_len, last_valid_handle
