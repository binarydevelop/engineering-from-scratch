"""
Dataset Cleaner & Validator (Phases 82-83).
Detects and filters:
1. Exact and normalized duplicate instruction-response pairs.
2. Contradictory pairs (same input, conflicting labels).
3. Empty responses or malformed record schemas.
"""

from typing import List, Dict, Tuple, Set
import hashlib
import json

class DatasetCleaner:
    def __init__(self):
        self.seen_inputs: Dict[str, str] = {}
        self.duplicates_removed = 0
        self.contradictions_removed = 0
        self.malformed_removed = 0

    def _normalize(self, text: str) -> str:
        return " ".join(text.strip().lower().split())

    def clean_dataset(self, records: List[Dict]) -> List[Dict]:
        cleaned = []
        for r in records:
            # 1. Schema check
            if not isinstance(r, dict) or "instruction" not in r or "output" not in r:
                self.malformed_removed += 1
                continue

            inst = r["instruction"]
            out = r["output"]

            # 2. Empty check
            if not isinstance(inst, str) or not isinstance(out, str):
                self.malformed_removed += 1
                continue
            if len(inst.strip()) == 0 or len(out.strip()) == 0:
                self.malformed_removed += 1
                continue

            norm_inst = self._normalize(inst)
            norm_out = self._normalize(out)

            # 3. Duplicate and Contradiction check
            if norm_inst in self.seen_inputs:
                prev_out = self.seen_inputs[norm_inst]
                if prev_out == norm_out:
                    self.duplicates_removed += 1
                else:
                    # Contradiction: same input, conflicting output!
                    self.contradictions_removed += 1
                continue

            self.seen_inputs[norm_inst] = norm_out
            cleaned.append(r)

        return cleaned
