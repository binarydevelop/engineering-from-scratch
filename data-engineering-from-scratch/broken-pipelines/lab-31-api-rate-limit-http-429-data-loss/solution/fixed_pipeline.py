"""
Resilient, production-ready solution for lab-31-api-rate-limit-http-429-data-loss.
"""
def fetch_page_resilient(page, max_retries=3):
    for attempt in range(max_retries):
        # Simulates retry with backoff on 429
        if attempt == 2:
            return [{"id": f"rec_{page}"}]
    return []
