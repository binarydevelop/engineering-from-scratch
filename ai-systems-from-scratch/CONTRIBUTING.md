# Contributing to AI Systems From Scratch

Thank you for contributing to **AI Systems From Scratch**!

## Core Teaching Philosophy
Before proposing changes, understand our fundamental methodology:
1. **Understand it. Build it. Train it. Compile it. Serve it. Evaluate it. Break it. Debug it. Optimize it. Operate it.**
2. **Never start with high-level libraries.** Problem first. Primitive second. Tool third.
3. **No magic abstractions.** If you introduce an agent, implement the while loop first. If you introduce LoRA, show $\Delta W = A \cdot B$ on raw tensors first.
4. **Hardware democratization:** All core concepts must run on Tier 1 (CPU/Universal) with simulated or scaled equivalents for GPU/cloud-specific operations.
5. **Separation of Concerns:** Solutions for broken-system labs and exercises must remain strictly in `broken-systems/solutions/` or dedicated solution directories.

## Pull Request Guidelines
- Verify code against Python 3.12+ and PyTorch 2.x.
- Run `make test` and ensure all tests pass.
- If adding a lesson, follow `LESSON_TEMPLATE.md` precisely.
- Include evidence logs following the Evidence Template specified in `LEARNING.md`.
