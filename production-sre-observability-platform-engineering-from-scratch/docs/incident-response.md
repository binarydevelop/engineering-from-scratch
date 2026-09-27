# Incident Response & Outage Operations Guide

> **Motto**: The goal of incident response is to restore customer experience as quickly and safely as possible, not to satisfy intellectual curiosity.

---

## 1. Incident Command System (ICS) Roles

During a major degradation or SEV-1 outage, clear role separation prevents chaos:

```text
                  ┌───────────────────────────────┐
                  │      Incident Commander       │
                  │  (Owns process, pace, action) │
                  └───────────────┬───────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ Operations Lead  │    │ Communications   │    │      Scribe      │
│ (Technical leads,│    │ (Status page,    │    │ (Maintains real- │
│ rollbacks, logs) │    │ exec updates)    │    │ time timeline)   │
└──────────────────┘    └──────────────────┘    └──────────────────┘
```

* **Incident Commander (IC)**: Holds the baton. Makes high-level decisions. Prevents responders from talking over each other. Solicits explicit hypotheses.
* **Operations Lead (Ops)**: Drives the command-line investigation, executes rollback commands, and coordinates technical responders.
* **Communications Lead (Comms)**: Shields technical responders from executive inquiries and updates status pages every 15-30 minutes.
* **Scribe**: Records actions, metric timestamps, and team decisions in the incident timeline.

---

## 2. The Four Immediate Triage Questions

Before changing any configuration or restarting nodes, the responder must ask:
1. **What is the user impact?** Which endpoints, error codes, and customer cohorts are degraded?
2. **When did it start?** What is the exact timestamp of the initial metric deviation?
3. **What changed?** Was there a code deployment, configuration push, feature flag flip, or cloud infrastructure event within 30 minutes of the start?
4. **Can we mitigate safely right now?** If a rollback or traffic shift is available, execute it immediately before diagnosing the root cause.

---

## 3. Severity Matrix

| Severity | Definition | Target TTD | Target TTM (Mitigate) |
|:---|:---|:---|:---|
| **SEV-1** | Critical customer outage, core revenue-generating journey blocked, active data loss. | < 5 mins | < 30 mins |
| **SEV-2** | Significant degradation of core service with partial workaround, or total loss of non-critical feature. | < 15 mins | < 2 hours |
| **SEV-3** | Minor operational defect, internal tooling impairment, no direct customer impact. | < 1 hour | Next business day |
