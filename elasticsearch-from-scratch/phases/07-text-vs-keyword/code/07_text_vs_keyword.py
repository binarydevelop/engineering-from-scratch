#!/usr/bin/env python3

def index_entry(raw_value):
    # text pipeline: lowercase + tokenize
    text_tokens = raw_value.lower().split()
    # keyword pipeline: exact verbatim string
    keyword_token = raw_value
    return {"text_tokens": text_tokens, "keyword_token": keyword_token}

if __name__ == "__main__":
    val = "United States"
    indexed = index_entry(val)
    print("Raw Value:     ", val)
    print("Text Tokens:   ", indexed["text_tokens"])
    print("Keyword Token: ", repr(indexed["keyword_token"]))

    query_term = "United States"
    print(f"\nQuerying term '{query_term}':")
    print(f"  Matches keyword? {query_term == indexed['keyword_token']}")
    print(f"  Matches in text tokens? {query_term in indexed['text_tokens']}")
    print("  (Text tokens contain 'united' and 'states' separately!)")
