#!/usr/bin/env python3
"""
Generates ROADMAP.md for NoSQL Databases & Query Languages From Scratch
Maps all 264 phases across Parts I through XXIII.
"""

import os
from generate_phases import PHASE_DEFS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROADMAP_FILE = os.path.join(BASE_DIR, "ROADMAP.md")

PARTS = [
    ("PART I — NOSQL FOUNDATIONS", 0, 20),
    ("PART II — DOCUMENT DATABASE QUERY LANGUAGE (MONGODB)", 21, 37),
    ("PART III — MONGODB AGGREGATION LANGUAGE", 38, 53),
    ("PART IV — DOCUMENT INDEXES", 54, 62),
    ("PART V — DOCUMENT MODELING", 63, 70),
    ("PART VI — WIDE-COLUMN & CQL (CASSANDRA)", 71, 88),
    ("PART VII — LSM TREE INTERNALS", 89, 98),
    ("PART VIII — PARTITIONING & REPLICATION", 99, 108),
    ("PART IX — DYNAMODB QUERY MODEL", 109, 127),
    ("PART X — PARTIQL", 128, 137),
    ("PART XI — REDIS ACCESS & QUERY MODEL", 138, 145),
    ("PART XII — GRAPH DATABASES & CYPHER (NEO4J)", 146, 163),
    ("PART XIII — SEARCH QUERY LANGUAGE (ELASTICSEARCH)", 164, 173),
    ("PART XIV — CROSS-DATABASE QUERY THINKING", 174, 179),
    ("PART XV — DATA MODELING CHALLENGES", 180, 187),
    ("PART XVI — DISTRIBUTED NOSQL INTERNALS", 188, 205),
    ("PART XVII — TRANSACTIONS IN NOSQL", 206, 211),
    ("PART XVIII — PERFORMANCE & MEASUREMENT", 212, 221),
    ("PART XIX — FAILURE & OPERATIONS", 222, 230),
    ("PART XX — NOSQL QUERY MASTERY", 231, 236),
    ("PART XXI — DATABASE SELECTION", 237, 244),
    ("PART XXII — PROJECTS", 245, 254),
    ("PART XXIII — CAPSTONES & FINAL CHALLENGES", 255, 263)
]

def main():
    phase_dict = {p[0]: p for p in PHASE_DEFS}

    content = """# The Exhaustive NoSQL & Query Languages Roadmap (Phases 00 – 263)

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

This roadmap maps all **264 curriculum phases** across 23 parts. Every single phase requires formulating access patterns, writing queries, inspecting physical plans via `explain`, measuring read amplification, deliberately breaking the design, and recording evidence.

---

## Curriculum Overview

| Part | Title | Phase Range | Primary Focus |
| :--- | :--- | :--- | :--- |
"""
    for title, start_p, end_p in PARTS:
        content += f"| **{title.split(' — ')[0]}** | {title.split(' — ')[1]} | Phase {start_p:02d} – {end_p:02d} | Core principles & queries |\n"

    content += "\n---\n\n"

    for part_title, start_p, end_p in PARTS:
        content += f"## {part_title}\n\n"
        content += "| Phase | Title | Primary Problem / Question | Core First Principle | Required Artifact |\n"
        content += "| :--- | :--- | :--- | :--- | :--- |\n"
        for p_idx in range(start_p, end_p + 1):
            if p_idx in phase_dict:
                _, slug, title, prob, princ, art = phase_dict[p_idx]
                link = f"[Phase {p_idx:02d}](file:///Users/tushar/desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-{p_idx:02d}-{slug}/docs/en.md)"
                content += f"| {link} | **{title}** | {prob} | {princ} | `{art}` |\n"
        content += "\n---\n\n"

    with open(ROADMAP_FILE, "w") as f:
        f.write(content)

    print(f"Successfully generated {ROADMAP_FILE}")

if __name__ == "__main__":
    main()
