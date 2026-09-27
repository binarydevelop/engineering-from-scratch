#!/usr/bin/env python3

SCENARIOS = [
    "1. E-Commerce Product Catalog Search",
    "2. Centralized Microservice Log Analytics (APM)",
    "3. Multi-Tenant SaaS Knowledge Base",
    "4. Sub-10ms Global Autocomplete Search Bar",
    "5. Security Information & Event Management (SIEM)",
    "6. Real-Time Geospatial Store & Ride Finder",
    "7. Job Portal & Resume Candidate Matching",
    "8. Audit Event Trail with Cold Tiering"
]

if __name__ == "__main__":
    print("=== The 8 Enterprise System Design Scenarios ===\n")
    for s in SCENARIOS:
        print(s)
    print("\nEvery scenario must answer the 20 fundamental architectural questions!")
