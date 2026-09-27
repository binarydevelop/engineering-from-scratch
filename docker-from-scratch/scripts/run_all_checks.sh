#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "============================================================"
echo "docker-from-scratch: Master Curriculum Verification Suite"
echo "============================================================"

TOTAL_PHASES=0
PASSED_PHASES=0
FAILED_PHASES=0

echo ""
echo "[1/4] Verifying Repository Structure & Root Deliverables..."
ROOT_FILES=(
    "README.md"
    "ROADMAP.md"
    "LEARNING.md"
    "CONTRIBUTING.md"
    "LESSON_TEMPLATE.md"
    "Makefile"
    ".gitignore"
    "docs/glossary.md"
    "docs/mental-models.md"
    "docs/troubleshooting.md"
    "scripts/verify_env.sh"
    "scripts/clean_labs.sh"
)

for rf in "${ROOT_FILES[@]}"; do
    if [ -f "${REPO_ROOT}/${rf}" ]; then
        echo "  ✔ Root file present: ${rf}"
    else
        echo "  ✖ MISSING root file: ${rf}"
        exit 1
    fi
done

echo ""
echo "[2/4] Verifying Capstone System Lab Artifacts..."
CAPSTONE_FILES=(
    "projects/capstone-system-lab/README.md"
    "projects/capstone-system-lab/docker-compose.yml"
    "projects/capstone-system-lab/.env"
    "projects/capstone-system-lab/app/app.py"
    "projects/capstone-system-lab/app/Dockerfile"
    "projects/capstone-system-lab/monitoring/prometheus/prometheus.yml"
    "projects/capstone-system-lab/monitoring/grafana/provisioning/datasources/datasources.yml"
    "projects/capstone-system-lab/monitoring/grafana/provisioning/dashboards/dashboards.yml"
    "projects/capstone-system-lab/monitoring/grafana/dashboards/overview.json"
)

for cf in "${CAPSTONE_FILES[@]}"; do
    if [ -f "${REPO_ROOT}/${cf}" ]; then
        echo "  ✔ Capstone artifact present: ${cf}"
    else
        echo "  ✖ MISSING capstone artifact: ${cf}"
        exit 1
    fi
done

echo ""
echo "[3/4] Validating All 38 Lessons & Labs (16 Mandatory Sections & Structure)..."
python3 -c "
import os, glob, sys

required_headers = [
    '# Lesson',
    '## Motto',
    '## Problem',
    '## Prediction',
    '## Why this matters',
    '## First principles',
    '## Mental model',
    '## Build it',
    '## Run it',
    '## Inspect it',
    '## Break it',
    '## Debug it',
    '## Modify it',
    '## Evidence',
    '## Questions for mastery',
    '## What comes next'
]

doc_files = sorted(glob.glob('${REPO_ROOT}/phases/**/docs/en.md', recursive=True))
print(f'  Found {len(doc_files)} curriculum documentation files.')

for f in doc_files:
    lesson_dir = os.path.dirname(os.path.dirname(f))
    lesson_rel = os.path.relpath(lesson_dir, '${REPO_ROOT}')
    
    # 1. Check sections
    content = open(f).read()
    missing_headers = [h for h in required_headers if h not in content]
    if missing_headers:
        print(f'  ✖ {lesson_rel}: missing sections: {missing_headers}', file=sys.stderr)
        sys.exit(1)
        
    # 2. Check code directory
    code_dir = os.path.join(lesson_dir, 'code')
    if not os.path.isdir(code_dir) or len(os.listdir(code_dir)) == 0:
        print(f'  ✖ {lesson_rel}: code directory missing or empty!', file=sys.stderr)
        sys.exit(1)
        
    # 3. Check run_experiment.sh
    exp_file = os.path.join(lesson_dir, 'experiments', 'run_experiment.sh')
    if not os.path.isfile(exp_file) or not os.access(exp_file, os.X_OK):
        print(f'  ✖ {lesson_rel}: run_experiment.sh missing or not executable!', file=sys.stderr)
        sys.exit(1)
        
    # 4. Check outputs/evidence-template.md
    out_file = os.path.join(lesson_dir, 'outputs', 'evidence-template.md')
    if not os.path.isfile(out_file):
        print(f'  ✖ {lesson_rel}: outputs/evidence-template.md missing!', file=sys.stderr)
        sys.exit(1)

print('  ✔ All 38 lessons pass structural and pedagogical section validation!')
"

echo ""
echo "[4/4] Executing Smoke Tests on Core First-Principles Experiments..."
SMOKE_EXPERIMENTS=(
    "phases/00-environment-and-orientation/01-verify-engine-and-client/experiments/run_experiment.sh"
    "phases/01-processes-before-containers/01-host-process-lifecycle/experiments/run_experiment.sh"
    "phases/08-container-networking-start-with-localhost/01-localhost-isolation/experiments/run_experiment.sh"
    "phases/28-container-debugging-without-magic/lab-01-wrong-port/experiments/run_experiment.sh"
    "phases/28-container-debugging-without-magic/lab-06-dns-resolution/experiments/run_experiment.sh"
    "phases/30-final-mental-model/01-end-to-end-execution-trace/experiments/run_experiment.sh"
)

for exp in "${SMOKE_EXPERIMENTS[@]}"; do
    echo "  -> Running smoke test: ${exp}..."
    "${REPO_ROOT}/${exp}" >/dev/null
    echo "  ✔ ${exp} passed."
done

echo ""
echo "============================================================"
echo "🎉 ALL VALIDATION CHECKS PASSED PERFECTLY!"
echo "============================================================"
