# Lesson [Number]: [Lesson Title]

## Motto
> "[A single memorable sentence summarizing the core engineering principle taught in this lesson.]"

---

## Delivery Problem
Describe the concrete failure mode or delivery bottleneck this lesson solves. What goes wrong in production or during team collaboration when this concept is missing or misunderstood? Provide a realistic scenario (e.g., failed release, merge dispute, silent data corruption, unauthorized deployment).

---

## Prediction
Before executing any command or reading the implementation, predict:
1. What will happen when we run the manual process?
2. What exit code will the terminal emit?
3. What artifact or state mutation will be left behind on the system?
4. How would an automated pipeline detect a failure in this step?

---

## Why This Matters
Explain the operational, business, and architectural impact:
- How does this step reduce lead time for changes?
- What risk does it eliminate before reaching staging or production?
- Why can this step not be skipped or deferred to post-release?

---

## First Principles
Deconstruct the core engineering mechanism behind the tooling:
- What operating system primitive is being exercised (process exit codes, file descriptors, signals, inodes, environment variables)?
- What mathematical or cryptographic invariant applies (SHA-256 digests, acyclic dependency graphs, Merkle trees)?
- Why is vendor YAML merely an abstraction over this primitive?

---

## Manual Process
Execute the exact step by hand in the terminal without any CI platform or automation framework:

```bash
# Step 1: Run the command manually
<command>

# Step 2: Inspect the exit status immediately
echo $?

# Step 3: Verify the output files or side effects
<verification-command>
```

What tedious manual tasks, human omissions, or environment assumptions did you notice?

---

## Mental Model
Present an ASCII diagram, flowchart, or state transition diagram clarifying the boundaries, inputs, and outputs of this stage.

```text
[ Input: Source Revision / State ]
               │
               ▼
      [ Transformation ]
               │
       ┌───────┴───────┐
       ▼               ▼
[ Exit 0: Success ]  [ Exit Non-Zero: Failure ]
       │               │
       ▼               ▼
[ Output Artifact ]  [ Diagnostic Evidence ]
```

---

## Automate It
Write the deterministic script or configuration that encapsulates this manual step into a repeatable unit:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Script implementation
```

Explain how this script behaves when running locally on a developer laptop versus inside an ephemeral CI runner container.

---

## Run It
Provide the exact command to execute from the repository root:

```bash
bash scripts/<script-name>.sh
```

Show the expected standard output and standard error streams.

---

## Inspect It
What specific files, logs, exit codes, and process behaviors should the learner inspect?
- Which file contains the output or artifact?
- What SHA-256 hash or identity was recorded?
- What temporary resources were created, and were they cleaned up?

---

## Break It
Deliberately inject a realistic failure:
1. Alter an input, corrupt a dependency, break a test assertion, or tamper with an environment variable.
2. Re-run the automated command.
3. Observe how the failure presents itself.

---

## Debug It
Follow the evidence-based troubleshooting loop:
- Did the failure happen during input acquisition, execution, or validation?
- What exact line of standard error revealed the root cause?
- Why should you never blindly retry without checking the failure log?

---

## Security
Analyze the security boundaries and attack vectors of this step:
- What credentials or tokens does this step require?
- Could untrusted user input (e.g., Pull Request branch name, commit message) trigger arbitrary command execution?
- How is secret exfiltration prevented?

---

## Optimize It
How do we improve feedback time and resource efficiency?
- What is the critical path duration?
- Can this step be cached, parallelized, or avoided via change detection?
- What is the trade-off between isolation and speed?

---

## Deployment Implication
Connect this stage to production software delivery:
- Does this step affect the running service immediately, or produce an immutable artifact for promotion?
- If this step fails in CI, what happens to ongoing deployments?
- How does this protect customer-facing service level objectives (SLOs)?

---

## Recovery
If a defect bypasses this step and reaches staging or production:
- How do you detect that the defect originated here?
- What is the rollback or roll-forward runbook?
- How do you add a regression check so this failure mode is caught automatically in the future?

---

## Evidence
Record your verification proof for this lesson:

```text
Lesson Number:
Date & Timestamp:
Commit SHA:
Operating System:
Command Executed:
Exit Code:
Artifact Hash (SHA-256):
Failure Injected:
Error Message Captured:
Recovery Verified (Yes/No):
```

---

## Questions for Mastery
1. *Deep architectural inquiry*: [Scenario with trade-offs between speed, cost, and safety.]
2. *Failure diagnosis inquiry*: [Log snippet or unexpected symptom — identify root cause.]
3. *First-principles inquiry*: [Explain mechanism without referencing specific vendor brand names.]

---

## When Not to Use This
Identify edge cases, architectures, or scales where this technique is counterproductive or over-engineering.

---

## What Comes Next
Brief preview of how the outputs or concepts of this lesson feed into the subsequent lesson.
