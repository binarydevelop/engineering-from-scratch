#!/usr/bin/env python3
import json
import urllib.request
import sys

def check_es(url="http://localhost:9200"):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            print("Successfully connected to Elasticsearch!")
            print(f"Cluster Name: {data.get('cluster_name')}")
            print(f"Node Name:    {data.get('name')}")
            print(f"ES Version:   {data.get('version', {}).get('number')}")
            print(f"Lucene Ver:   {data.get('version', {}).get('lucene_version')}")
            return True
    except Exception as e:
        print(f"Failed to connect to {url}: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = check_es()
    sys.exit(0 if success else 1)
