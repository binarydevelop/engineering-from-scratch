# Lesson Template: docker-from-scratch

Use this template whenever creating or extending a lesson in `docker-from-scratch`.
Every lesson follows the core philosophy:

**Understand it. Build it. Inspect it. Break it. Fix it. Ship it.**

---

## Directory Structure

```text
phases/<phase>/<lesson>/
├── docs/
│   └── en.md
├── code/
│   └── (code, Dockerfile, scripts, or configs)
├── experiments/
│   └── run_experiment.sh
└── outputs/
    └── evidence-template.md
```

---

## Documentation Structure (`docs/en.md`)

```markdown
# Lesson [Number]: [Title]

## Motto
[A memorable one-line mental model anchor]

## Problem
[What engineering challenge or boundary are we hitting? Why can't we solve it with what we already know? Never introduce Docker behavior as magic.]

## Prediction
[What do you predict will happen before typing any commands?
1. Predict question 1
2. Predict question 2]

## Why this matters
[Real-world failure scenarios, production impact, or architectural consequence of misunderstanding this concept.]

## First principles
[Kernel, OS, networking, or filesystem mechanics underlying this topic. Explain the mechanism, not just the Docker CLI flag.]

## Mental model
[ASCII diagram explaining the actors, interfaces, boundaries, and data flow.]

```text
[Insert ASCII Diagram]
```

## Build it
[Step-by-step creation of code, configuration, or environment from scratch.]

## Run it
[Exact commands to execute. Show the commands, working directories, and expected outputs.]

```bash
# Commands to run
```

## Inspect it
[How to inspect the resulting state using docker inspect, ps, logs, netstat, curl, etc. Do not trust what a command claims to do; verify the state.]

```bash
# Inspection commands
```

## Break it
[Inject a deliberate fault. Change a port, kill a dependency, break a path, simulate network failure, or exceed resources.]

## Debug it
[Systematic diagnostic steps. Formulate hypothesis, inspect state, find root cause, and apply remedy.]

## Modify it
[One hands-on challenge or alteration the learner must complete before considering the lesson finished.]

## Evidence
[Required proof of completion. Record outputs, exit codes, and answers in `outputs/evidence-template.md`.]

## Questions for mastery
1. [Mastery question 1]
2. [Mastery question 2]
3. [Mastery question 3]

## What comes next
[How this lesson directly connects to the problem solved in the next lesson.]
```

---

## Evidence Template (`outputs/evidence-template.md`)

```markdown
# Lesson Evidence Record

**Lesson:** [Lesson Name]
**Date:** [YYYY-MM-DD]
**Host OS / Platform:** [macOS (Apple Silicon/Intel) / Linux / Windows WSL2]

## 1. Prediction
*What did I expect to happen before running the experiment?*

## 2. Commands Executed
*Exact commands executed in order:*
```bash

```

## 3. Working Directory
```text

```

## 4. Important Output
*Key outputs or logs observed:*
```text

```

## 5. Exit Codes
```text

```

## 6. What Actually Happened?
*Did behavior match prediction? What differed?*

## 7. What Surprised Me?
*Any unexpected outputs, warnings, or mechanics:*

## 8. What Did I Break?
*The deliberate failure injected:*

## 9. How Did I Diagnose It?
*The exact diagnostic commands and reasoning used:*

## 10. How Did I Fix It?
*The fix applied and verification:*

## 11. What Did I Modify?
*The hands-on modification completed:*

## 12. Artifact Produced
*Files, images, volumes, or scripts created:*

## 13. Explain the Concept in My Own Words
*3-5 sentences explaining what happened underneath without jargon or memorized phrases:*

## 14. Remaining Questions
*Any open questions to investigate in subsequent lessons:*
```
