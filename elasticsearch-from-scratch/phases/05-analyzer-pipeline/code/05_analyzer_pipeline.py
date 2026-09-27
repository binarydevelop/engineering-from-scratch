#!/usr/bin/env python3
import re
import html

class AnalysisPipeline:
    def __init__(self, char_filters=None, tokenizer=None, token_filters=None):
        self.char_filters = char_filters or []
        self.tokenizer = tokenizer or (lambda text: text.split())
        self.token_filters = token_filters or []

    def analyze(self, text):
        # Stage 1: Char filters
        current_text = text
        for cf in self.char_filters:
            current_text = cf(current_text)
        
        # Stage 2: Tokenizer
        tokens = self.tokenizer(current_text)

        # Stage 3: Token filters
        current_tokens = tokens
        for tf in self.token_filters:
            current_tokens = tf(current_tokens)

        return current_tokens

if __name__ == "__main__":
    def strip_html(t): return re.sub(r'<[^>]+>', '', t)
    def decode_entities(t): return html.unescape(t)
    def word_tokenizer(t): return re.findall(r'\b\w+\b', t)
    def lowercase(tokens): return [t.lower() for t in tokens]
    def remove_stopwords(tokens): return [t for t in tokens if t not in {"is", "and", "the"}]

    pipeline = AnalysisPipeline(
        char_filters=[strip_html, decode_entities],
        tokenizer=word_tokenizer,
        token_filters=[lowercase, remove_stopwords]
    )

    sample = "<h2>Elasticsearch &amp; Lucene</h2> are <b>FAST</b>!"
    terms = pipeline.analyze(sample)
    print("Input: ", sample)
    print("Terms: ", terms)
