#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0

check_file() {
    local rel_path="$1"
    local desc="$2"
    if [ -f "${REPO_DIR}/${rel_path}" ]; then
        echo " [OK] ${desc}: ${rel_path}"
    else
        echo " [ERROR] Missing ${desc}: ${rel_path}"
        ERRORS=$((ERRORS + 1))
    fi
}

check_count() {
    local dir_rel="$1"
    local pattern="$2"
    local min_count="$3"
    local desc="$4"

    local actual_count
    actual_count=$(find "${REPO_DIR}/${dir_rel}" -maxdepth 2 -name "${pattern}" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$actual_count" -ge "$min_count" ]; then
        echo " [OK] ${desc}: found ${actual_count} (expected >= ${min_count})"
    else
        echo " [ERROR] ${desc}: found ${actual_count} (expected >= ${min_count})"
        ERRORS=$((ERRORS + 1))
    fi
}

echo "======================================================================"
echo "  nosql-databases-and-query-languages-from-scratch Verification       "
echo "======================================================================"

echo ""
echo "Checking Root Documents & Canonical Templates:"
check_file "README.md" "Repository Manifesto & Quickstart"
check_file "ROADMAP.md" "Exhaustive Curriculum Roadmap"
check_file "LEARNING.md" "The 10-Step Learning Cycle & Rules"
check_file "LESSON_TEMPLATE.md" "Canonical Lesson Template"
check_file "QUERY_TEMPLATE.md" "Canonical Query Template"
check_file "VERSIONS.md" "Pinned Versions Matrix"
check_file "COST_SAFETY.md" "Cost Safety & Local First Guide"
check_file "CONTRIBUTING.md" "Contribution Guidelines"
check_file "LICENSE" "MIT License"
check_file ".gitignore" "Git Ignore File"
check_file ".env.example" "Environment Configuration Template"
check_file "Makefile" "Repository Makefile"
check_file "docker-compose.yml" "Multi-Profile Compose File"
check_file "outputs/evidence-template.md" "Evidence Log Template"

echo ""
echo "Checking Authoritative Guides (docs/):"
check_file "docs/glossary.md" "NoSQL Engineering Glossary"
check_file "docs/mental-models.md" "Physical Storage Realities"
check_file "docs/query-thinking.md" "18-Question Query Thinking Framework"
check_file "docs/access-patterns.md" "Access Pattern Catalog"
check_file "docs/database-selection.md" "Database Selection Framework"
check_file "docs/consistency.md" "Distributed Consistency & Quorums"
check_file "docs/troubleshooting.md" "Operational Troubleshooting Playbook"
check_file "docs/anti-patterns.md" "The 17 Fatal NoSQL Anti-Patterns"

echo ""
echo "Checking Core Simulators (simulations/):"
check_file "simulations/hash_partitioning_sim.py" "Hash Partitioning Simulator"
check_file "simulations/consistent_hashing_sim.py" "Consistent Hashing Ring Simulator"
check_file "simulations/quorum_sim.py" "Quorum Consistency Simulator"
check_file "simulations/tiny_kv.py" "Tiny Key-Value Store with WAL"
check_file "simulations/tiny_lsm.py" "Tiny LSM Tree Storage Engine"
check_file "simulations/conflict_resolution_sim.py" "Conflict Resolution Simulator"
check_file "simulations/hot_partition_sim.py" "Hot Partition Skew Simulator"

echo ""
echo "Checking Curriculum Modules & Sub-Directories:"
check_count "phases" "README.md" 264 "Curriculum Phases (Phase 00 to 263)"
check_count "drills" "drill-*.md" 140 "Query Muscle-Memory Drills"
check_count "exercises" "exercise-*.md" 260 "Query Exercises (Beginner to Challenge)"
check_count "broken-databases" "broken-lab-*.md" 45 "Broken NoSQL Failure Labs"
check_count "projects" "README.md" 10 "Substantial Engineering Projects"
check_count "capstones" "README.md" 9 "Comprehensive Capstone Defenses"

echo ""
echo "Checking Datasets (datasets/):"
check_file "datasets/ecommerce/orders.json" "E-Commerce Dataset"
check_file "datasets/social/users.json" "Social Network Dataset"
check_file "datasets/iot/readings.json" "IoT Telemetry Dataset"
check_file "datasets/knowledge-graph/relationships.json" "Knowledge Graph Dataset"

echo ""
echo "Checking Solutions (solutions/):"
check_count "solutions/drills" "solution-drill-*.md" 140 "Drill Solutions"
check_count "solutions/exercises" "solution-exercise-*.md" 260 "Exercise Solutions"
check_count "solutions/broken-databases" "solution-broken-lab-*.md" 45 "Broken Lab Solutions"

echo ""
echo "======================================================================"
if [ "$ERRORS" -eq 0 ]; then
    echo "  All Curriculum Components Verified Successfully! (0 Errors)         "
    echo "======================================================================"
    exit 0
else
    echo "  Verification Failed with $ERRORS Error(s)!                          "
    echo "======================================================================"
    exit 1
fi
