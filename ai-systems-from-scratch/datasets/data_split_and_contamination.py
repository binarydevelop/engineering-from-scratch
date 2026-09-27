"""
Data Splitting & Contamination Checker (Phases 84-85).
Implements:
1. Leak-free train / validation / test partitioning.
2. N-gram overlap and exact match contamination detector to prevent
   training models on evaluation benchmark prompts.
"""

from typing import List, Dict, Tuple, Set
import random

def split_dataset(
    records: List[Dict],
    train_ratio: float = 0.8,
    val_ratio: float = 0.1,
    test_ratio: float = 0.1,
    seed: int = 42
) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-5
    rng = random.Random(seed)
    shuffled = list(records)
    rng.shuffle(shuffled)

    n = len(shuffled)
    n_train = int(n * train_ratio)
    n_val = int(n * val_ratio)

    train_set = shuffled[:n_train]
    val_set = shuffled[n_train:n_train + n_val]
    test_set = shuffled[n_train + n_val:]
    return train_set, val_set, test_set

def get_ngrams(text: str, n: int = 5) -> Set[str]:
    words = text.lower().strip().split()
    if len(words) < n:
        return {" ".join(words)}
    return {" ".join(words[i:i+n]) for i in range(len(words) - n + 1)}

def check_contamination(
    train_records: List[Dict],
    eval_records: List[Dict],
    ngram_size: int = 5,
    threshold: float = 0.5
) -> List[Dict]:
    """
    Returns list of contaminated evaluation items where n-gram overlap
    with any training record exceeds threshold.
    """
    contaminated = []
    # Build train n-gram index
    train_ngrams = set()
    for tr in train_records:
        text = tr.get("instruction", "") + " " + tr.get("input", "")
        train_ngrams.update(get_ngrams(text, n=ngram_size))

    for idx, ev in enumerate(eval_records):
        text = ev.get("instruction", "") + " " + ev.get("input", "")
        ev_ngrams = get_ngrams(text, n=ngram_size)
        if not ev_ngrams:
            continue
        overlap = len(ev_ngrams.intersection(train_ngrams))
        overlap_ratio = overlap / len(ev_ngrams)
        if overlap_ratio >= threshold:
            contaminated.append({
                "eval_index": idx,
                "overlap_ratio": overlap_ratio,
                "text_snippet": text[:80]
            })

    return contaminated
