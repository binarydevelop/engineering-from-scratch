# Contributing to `aws-from-scratch`

Thank you for contributing! This repository has a strict pedagogical standard inspired by first-principles engineering.

---

## The Core Philosophy

Our repository motto is:
> **Understand it. Build it. Observe it. Break it. Recover it. Secure it. Scale it. Cost it. Ship it.**

Before contributing a lesson or exercise, understand what we **do NOT** do:
- **We do NOT teach AWS as a service catalog.** (Do not write: "Amazon SQS is a fully managed message queue." Instead write: "Service A is producing work faster than Service B can consume it. What happens when B crashes?")
- **We do NOT optimize for passing multiple-choice certification exams.** We optimize for building deep, intuitive mental models of distributed infrastructure primitives.
- **We do NOT skip cleanup.** A cloud lab without teardown instructions and verification commands is considered broken and will be rejected.

---

## Lesson Structure Requirements

Every lesson must strictly follow [LESSON_TEMPLATE.md](LESSON_TEMPLATE.md).

Key requirements:
1. **Derive Before Using:**
   - Problem first.
   - Physical/Computer Science primitive second.
   - AWS managed service third.
2. **Local Simulation Where Possible:**
   - Write a short Python or bash script demonstrating the mechanics before touching live cloud APIs.
3. **Mandatory Cost Safety Section:**
   - Every lesson creating live cloud resources MUST include:
     - `## Cost Warning`
     - `## Resources Created`
     - `## How to Verify Them`
     - `## Cleanup`
     - `## How to Verify Cleanup`
4. **Mandatory Tagging:**
   - All AWS resources must be tagged with:
     `Project=aws-from-scratch`, `Lesson=<slug>`, `Environment=learning`.
5. **Security Discipline:**
   - Never commit credentials, private keys, or `.env` files.
   - Use IAM roles and short-lived STS tokens instead of static access keys.
   - Never recommend `0.0.0.0/0` on sensitive ports (SSH/RDP/Databases).

---

## Pull Request Checklist

Before submitting a PR:
- [ ] Ran `./scripts/check-environment.sh` and confirmed all checks pass.
- [ ] Followed the 23-point structure in `LESSON_TEMPLATE.md`.
- [ ] Tested all AWS CLI commands against live AWS CLI v2 and verified their syntax.
- [ ] Included complete `## Cleanup` and `## Verify cleanup` commands.
- [ ] Verified that code snippets run on Python 3.12+.
- [ ] Documented trade-offs under the AWS Well-Architected Framework (all 6 pillars).
