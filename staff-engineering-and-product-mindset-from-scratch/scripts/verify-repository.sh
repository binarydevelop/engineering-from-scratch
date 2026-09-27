#!/usr/bin/env bash
# ==============================================================================
# staff-engineering-and-product-mindset-from-scratch Repository Verifier
# Validates presence, structure, and integrity of all curriculum components
# ==============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
RESET="\033[0m"

echo -e "${BOLD}${BLUE}======================================================================${RESET}"
echo -e "${BOLD}${BLUE}  staff-engineering-and-product-mindset-from-scratch Verification   ${RESET}"
echo -e "${BOLD}${BLUE}======================================================================${RESET}\n"

BASE_DIR="/Users/tushar/desktop/private/repos/staff-engineering-and-product-mindset-from-scratch"
cd "$BASE_DIR"

ERRORS=0

check_file() {
    local file="$1"
    local desc="$2"
    if [ -f "$file" ]; then
        echo -e " [${GREEN}OK${RESET}] $desc: ${BOLD}$file${RESET}"
    else
        echo -e " [${RED}FAIL${RESET}] Missing $desc: ${BOLD}$file${RESET}"
        ERRORS=$((ERRORS + 1))
    fi
}

check_count() {
    local dir="$1"
    local pattern="$2"
    local expected="$3"
    local desc="$4"
    local count
    count=$(find "$dir" -maxdepth 1 -name "$pattern" | wc -l | tr -d ' ')
    if [ "$count" -ge "$expected" ]; then
        echo -e " [${GREEN}OK${RESET}] $desc: found ${BOLD}$count${RESET} (expected >= $expected)"
    else
        echo -e " [${RED}FAIL${RESET}] $desc: found ${BOLD}$count${RESET} (expected >= $expected)"
        ERRORS=$((ERRORS + 1))
    fi
}

check_projects_and_capstones() {
    local dir="$1"
    local expected="$2"
    local desc="$3"
    local count
    count=$(find "$dir" -maxdepth 1 -type d \( -name "project-*" -o -name "capstone-*" \) | wc -l | tr -d ' ')
    if [ "$count" -ge "$expected" ]; then
        echo -e " [${GREEN}OK${RESET}] $desc: found ${BOLD}$count${RESET} (expected >= $expected)"
    else
        echo -e " [${RED}FAIL${RESET}] $desc: found ${BOLD}$count${RESET} (expected >= $expected)"
        ERRORS=$((ERRORS + 1))
    fi
}

echo -e "${BOLD}Checking Root Documents & Canonical Templates:${RESET}"
check_file "README.md" "Repository Manifesto & Quickstart"
check_file "ROADMAP.md" "Exhaustive Curriculum Roadmap"
check_file "LEARNING.md" "The 10-Step Learning Cycle & Rules"
check_file "LESSON_TEMPLATE.md" "Canonical Lesson Template"
check_file "CASE_STUDY_TEMPLATE.md" "Case Study Template"
check_file "DECISION_TEMPLATE.md" "ADR / Decision Journal Template"
check_file "RFC_TEMPLATE.md" "Request for Comments Template"
check_file "STRATEGY_TEMPLATE.md" "Technical Strategy Template"
check_file "PROJECT_BRIEF_TEMPLATE.md" "Project Brief Template"
check_file "POSTMORTEM_TEMPLATE.md" "Blameless Postmortem Template"
check_file "STAKEHOLDER_MAP_TEMPLATE.md" "Stakeholder Map Template"
check_file "CONTRIBUTING.md" "Contribution Guidelines"
check_file "LICENSE" "MIT License"
check_file "outputs/evidence-template.md" "Evidence Log Template"

echo ""
echo -e "${BOLD}Checking Authoritative Guides (docs/):${RESET}"
check_file "docs/glossary.md" "Technical Leadership Glossary"
check_file "docs/staff-mental-models.md" "Staff Mental Models & 12 Anti-Patterns"
check_file "docs/product-thinking.md" "Product Mindset & Customer Funnels"
check_file "docs/decision-making.md" "Decision Framework & Reversibility"
check_file "docs/communication.md" "Executive & Technical Communication"
check_file "docs/influence.md" "Influence Without Authority"
check_file "docs/execution.md" "Execution Leadership & Risk Management"
check_file "docs/career-framework.md" "Career Framework & Staff Archetypes"

echo ""
echo -e "${BOLD}Checking Curriculum Modules & Sub-Directories:${RESET}"
check_count "phases" "phase-*" 201 "Phases (Phase 00 - 200)"
check_count "case-studies" "case-*.md" 65 "Case Studies"
check_count "simulations" "sim-*.md" 32 "Multi-Stage Simulations"
check_count "writing-drills" "writing-drill-*.md" 50 "Writing Drills"
check_count "decision-drills" "decision-drill-*.md" 50 "Decision Drills"
check_count "stakeholder-scenarios" "stakeholder-scenario-*.md" 30 "Stakeholder Scenarios"
check_count "product-exercises" "product-exercise-*.md" 50 "Product Thinking Exercises"
check_count "architecture-reviews" "architecture-review-*.md" 30 "Architecture Reviews"
check_count "incident-exercises" "incident-exercise-*.md" 15 "Incident Exercises"
check_projects_and_capstones "projects" 19 "Substantial Projects & Capstones"

echo ""
if [ "$ERRORS" -eq 0 ]; then
    echo -e "${BOLD}${GREEN}======================================================================${RESET}"
    echo -e "${BOLD}${GREEN}  All Curriculum Components Verified Successfully! (0 Errors)         ${RESET}"
    echo -e "${BOLD}${GREEN}======================================================================${RESET}"
    exit 0
else
    echo -e "${BOLD}${RED}Verification encountered $ERRORS errors.${RESET}"
    exit 1
fi
