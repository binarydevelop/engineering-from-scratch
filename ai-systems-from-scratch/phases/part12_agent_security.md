# Part XII — Agent Security & Trust Boundaries (Phases 155 – 163)

> **Motto:** The model is not a security boundary. Authorization and sandboxing must be enforced by trusted application code.

---

## Phases 155 – 159: Prompt Injections & Permission Boundaries
- **Phase 155 — Prompt Injection:** Direct adversarial overrides: extracting system instructions and altering logic.
- **Phase 156 — Indirect Prompt Injection:** Untrusted documents and web pages hijacking agent execution flow (`SECURITY.md`).
- **Phase 157 — Tool Permission Boundaries:** Implementing least privilege: restricting dangerous system capabilities (`tools/permission_manager.py`).
- **Phase 158 — Read vs Write Tools:** Enforcing distinct authorization pipelines for queries vs external state mutations.
- **Phase 159 — Human-in-the-Loop Approval:** Two-phase commit: agent proposes high-stakes action; user approves before execution.

---

## Phases 160 – 163: Sandboxing, Secrets & Exfiltration
- **Phase 160 — Execution Sandboxing:** Running code generation tools in restricted ephemeral containers (`tools/sandboxed_executor.py`).
- **Phase 161 — Secret Isolation:** Preventing API keys, passwords, and sensitive session tokens from entering model context.
- **Phase 162 — Multi-Tenant Authorization:** Enforcing tenant data isolation in deterministic application code, not prompts.
- **Phase 163 — Data Exfiltration Defenses:** Blocking exfiltration channels (markdown image beacons, outbound webhook abuse).
