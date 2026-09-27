#!/usr/bin/env python3
import re

def naive_whitespace(text):
    return text.split()

def regex_word_tokenizer(text):
    # Match alphanumeric words, discarding punctuation
    return re.findall(r'\b\w+\b', text)

if __name__ == "__main__":
    sample = "Redis, Kafka, and Elasticsearch 8.17! Email: user@elastic.co, Cost: $49.99"
    print("Input Text:", sample)
    print("\n1. Naive Whitespace Tokens:")
    print(naive_whitespace(sample))
    print("\n2. Regex Word Tokens:")
    print(regex_word_tokenizer(sample))
