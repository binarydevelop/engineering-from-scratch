#!/usr/bin/env python3
"""
scripts/generate_all_phases.py
Imports curriculum data from Part 1, Part 2, and Part 3 and generates
the complete 86-phase lesson files in phases/<module>/<slug>/docs/en.md
strictly formatted according to LESSON_TEMPLATE.md.
"""

import os
import sys

from curriculum_part1 import PART1_LESSONS
from curriculum_part2 import PART2_LESSONS
from curriculum_part3 import PART3_LESSONS

ALL_LESSONS = PART1_LESSONS + PART2_LESSONS + PART3_LESSONS
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PHASES_DIR = os.path.join(BASE_DIR, "phases")

def render_lesson(data):
    return f"""# Phase {data['num']}: {data['title']}

## Motto
> {data['motto']}

**Type:** {data['type']}  
**Time Estimate:** ~{data['time']} minutes  
**Prerequisites:** {data['prereqs']}  
**AWS Services Involved:** {data['services']}  
**Cost Vector:** {data['cost']}  

---

## Problem
{data['problem']}

---

## Prediction
{data['prediction']}

---

## Why this matters
{data['why_matters']}

---

## First principles
{data['first_principles']}

---

## Mental model
```text
{data['diagram']}
```

---

## Architecture before AWS
{data['before_aws']}

---

## Build the primitive
```python
{data['primitive_code']}
```

---

## Use AWS
```bash
{data['aws_cmd']}
```

---

## Inspect it
```bash
{data['inspect']}
```

---

## Measure it
{data['measure']}

---

## Break it
{data['break_desc']}

---

## Diagnose it
{data['diagnose']}

---

## Recover it
{data['recover']}

---

## Security
{data['security']}

---

## Cost
### Cost Warning
{data['cost']}

### Resources Created
- Documented in lesson steps above.

### How to Verify Them
```bash
./scripts/list-lab-resources.sh
```

---

## Modify it
Experiment by tuning parameters, increasing capacity, changing timeouts, or tweaking security group rules. Observe metric changes in CloudWatch.

---

## Cleanup
```bash
{data['cleanup']}
```

---

## Verify cleanup
```bash
{data['verify_cleanup']}
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-{data['num']}-evidence.md`.

---

## Questions for mastery
1. {data['mastery_q1']}
2. {data['mastery_q2']}
3. {data['mastery_q3']}

---

## When to use this
{data['when_use']}

---

## When not to use this
{data['when_not']}

---

## What comes next
{data['next_step']}
"""

def main():
    print(f"Generating full curriculum: {len(ALL_LESSONS)} phases...")
    count = 0
    for lesson in ALL_LESSONS:
        lesson_dir = os.path.join(PHASES_DIR, lesson['module'], lesson['slug'])
        docs_dir = os.path.join(lesson_dir, "docs")
        outputs_dir = os.path.join(lesson_dir, "outputs")
        os.makedirs(docs_dir, exist_ok=True)
        os.makedirs(outputs_dir, exist_ok=True)

        md_path = os.path.join(docs_dir, "en.md")
        content = render_lesson(lesson)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(content)

        evidence_symlink = os.path.join(outputs_dir, "evidence-template.md")
        if not os.path.exists(evidence_symlink):
            # Write a pointer to the main evidence template
            with open(evidence_symlink, "w", encoding="utf-8") as f:
                f.write("# Lab Evidence Template\n\nRefer to the master template at `outputs/evidence-template.md`.\n")

        count += 1

    print(f"✓ Successfully generated {count} complete lesson documentation files across 13 modules!")

if __name__ == "__main__":
    main()
