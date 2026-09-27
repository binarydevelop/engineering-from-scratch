#!/usr/bin/env python3

def generate_ngrams(word, min_n=3, max_n=5):
    ngrams = []
    L = len(word)
    for n in range(min_n, max_n + 1):
        for i in range(L - n + 1):
            ngrams.append(word[i:i+n])
    return ngrams

def generate_edge_ngrams(word, min_n=2, max_n=6):
    return [word[:n] for n in range(min_n, min(max_n + 1, len(word) + 1))]

if __name__ == "__main__":
    word = "elasticsearch"
    ng = generate_ngrams(word, 3, 4)
    eng = generate_edge_ngrams(word, 2, 6)
    print(f"Original word: '{word}' (1 term)")
    print(f"Standard N-grams (3-4): {len(ng)} terms -> {ng}")
    print(f"Edge N-grams (2-6):     {len(eng)} terms -> {eng}")
