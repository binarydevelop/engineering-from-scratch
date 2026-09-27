"""
Broken implementation demonstrating the flaw in lab-31-api-rate-limit-http-429-data-loss.
"""
def fetch_page_broken(page):
    resp = {"status": 429}
    if resp["status"] != 200:
        return [] # Skips page! Data lost!
