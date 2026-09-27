#!/usr/bin/env python3
import json

def create_catalog_index_dsl():
    return {
        "settings": {
            "number_of_shards": 2,
            "number_of_replicas": 0,
            "analysis": {
                "tokenizer": {
                    "autocomplete_tokenizer": {
                        "type": "edge_ngram",
                        "min_gram": 2,
                        "max_gram": 10,
                        "token_chars": ["letter", "digit"]
                    }
                },
                "analyzer": {
                    "autocomplete_analyzer": {
                        "type": "custom",
                        "tokenizer": "autocomplete_tokenizer",
                        "filter": ["lowercase"]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "title": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword"},
                        "autocomplete": {"type": "text", "analyzer": "autocomplete_analyzer"}
                    }
                },
                "description": {"type": "text"},
                "category": {"type": "keyword"},
                "brand": {"type": "keyword"},
                "price": {"type": "double"},
                "rating": {"type": "float"},
                "in_stock": {"type": "boolean"}
            }
        }
    }

if __name__ == "__main__":
    dsl = create_catalog_index_dsl()
    print("Capstone 1: E-commerce Catalog Mapping Specification:")
    print(json.dumps(dsl, indent=2))
