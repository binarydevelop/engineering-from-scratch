#!/usr/bin/env python3

def lowercase(tokens):
    return [t.lower() for t in tokens]

def remove_stopwords(tokens, stopwords=None):
    if stopwords is None:
        stopwords = {"the", "a", "an", "and", "in", "of", "to", "is", "for"}
    return [t for t in tokens if t not in stopwords]

def naive_suffix_stemmer(tokens):
    stemmed = []
    for t in tokens:
        if t.endswith("ing") and len(t) > 4:
            stemmed.append(t[:-3])
        elif t.endswith("ed") and len(t) > 3:
            stemmed.append(t[:-2])
        elif t.endswith("s") and len(t) > 2 and not t.endswith("ss"):
            stemmed.append(t[:-1])
        else:
            stemmed.append(t)
    return stemmed

if __name__ == "__main__":
    raw_tokens = ["The", "Distributed", "Nodes", "are", "Running", "Fast"]
    print("Raw Tokens:       ", raw_tokens)
    step1 = lowercase(raw_tokens)
    print("1. Lowercased:    ", step1)
    step2 = remove_stopwords(step1)
    print("2. Stop words out:", step2)
    step3 = naive_suffix_stemmer(step2)
    print("3. Stemmed:       ", step3)
