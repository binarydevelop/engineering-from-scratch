# Part VII — Preference Optimization (Phases 103 – 111)

> **Motto:** Some tasks cannot be taught by imitation alone. When multiple outputs are syntactically valid, optimization requires pairwise preferences.

---

## Phases 103 – 107: Direct Preference Optimization (DPO)
- **Phase 103 — Why Supervised Data Is Not Enough:** The limit of imitation learning: subtle nuances, verbosity, and style.
- **Phase 104 — Preference Dataset Construction:** Triplet representations: prompt ($x$), chosen ($y_w$), rejected ($y_l$).
- **Phase 105 — Reward Modeling Intuition:** Bradley-Terry model: training a scalar reward model on pairwise rankings.
- **Phase 106 — DPO From First Principles:** Direct Preference Optimization: expressing the reward implicitly via policy and reference.
- **Phase 107 — DPO Practical Lab:** Training an adapter with `DPOTrainer` and evaluating win rates against the SFT baseline.

---

## Phases 108 – 111: Online RL, Reward Hacking & Alignment
- **Phase 108 — Online RL-Style Training Concepts:** Policy gradients, rollout generation, reward computation, PPO updates.
- **Phase 109 — GRPO / Contemporary RL Methods:** Group Relative Policy Optimization: normalizing rewards within sampled groups.
- **Phase 110 — Reward Hacking Lab:** Injecting a flawed reward proxy (e.g., length reward) and observing pathological policy outputs.
- **Phase 111 — Alignment Evaluation:** Multi-dimensional evaluations: helpfulness, truthfulness, safety boundaries, toxicity.
