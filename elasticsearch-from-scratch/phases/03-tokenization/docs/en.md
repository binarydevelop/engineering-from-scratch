# Lesson 03.1: Tokenization

## Motto
"Before you can index text, you must define what constitutes a word."

## Problem
Raw strings like `"Redis, Kafka and Elasticsearch!"` contain punctuation, commas, hyphens, and whitespace. If a naive index simply splits on spaces, the token `"Elasticsearch!"` will never match a query for `"Elasticsearch"`.

## Prediction
What happens if you index `"Wi-Fi 6E"` with a naive whitespace tokenizer versus a punctuation-stripping tokenizer?

## Why this matters
Search quality lives or dies on tokenization. Tokenizing too aggressively splits meaningful domain terms (like `C++` or `e-commerce`), while tokenizing too passively leaves noisy punctuation attached to words.

## First principles
A tokenizer consumes a character stream and produces a token stream, recording:
* The token string (`term`)
* Start and end character offsets in the original text
* Position in the token stream (for phrase queries)

## Mental model
```text
Raw Text: "Distributed, fault-tolerant search!"
                       │
             [ Tokenizer Stage ]
                       │
Emitted Tokens:
 1. "Distributed"  (offset: 0-11,  pos: 0)
 2. "fault"        (offset: 13-18, pos: 1)
 3. "tolerant"     (offset: 19-27, pos: 2)
 4. "search"       (offset: 28-34, pos: 3)
```

## Build it
See `code/tokenizer_experiments.py` demonstrating whitespace, regex word boundary, and punctuation-aware tokenization.

## Use Elasticsearch
Run the experiment using Elasticsearch's `_analyze` API:
```bash
./phases/03-tokenization/experiments/run_experiment.sh
```

## Inspect it
Observe the output of the standard tokenizer:
```bash
curl -X POST http://localhost:9200/_analyze -H "Content-Type: application/json" -d '{
  "tokenizer": "standard",
  "text": "Redis, Kafka and Elasticsearch!"
}'
```

## Measure it
Inspect token count and emitted offsets.

## Break it
Send email addresses (`alice@example.com`) or URLs (`https://elastic.co`) through `standard` tokenizer vs `whitespace` tokenizer and observe where standard tokenizer fractures domains.

## Recover it
Choose domain-specific tokenizers (e.g. `uax_url_email`) when indexing structured identifiers.

## Modify it
Configure custom pattern tokenizers with custom regexes.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does the standard tokenizer strip punctuation but preserve alphanumeric characters?
2. What information is lost permanently when a tokenizer discards punctuation?

## Guarantees
* Tokenization deterministically maps a character stream to discrete tokens with offsets.

## Non-guarantees
* A single generic tokenizer cannot handle natural language and code identifiers with equal fidelity.

## When to use this
* As the second mandatory stage of any text analysis pipeline.

## When not to use this
* Do not apply full text tokenization to exact identifiers (IDs, SKUs, IP addresses). Use `keyword` mapping instead.

## What comes next
In Phase 04, we introduce token normalization: lowercasing, stop words, and stemming.
