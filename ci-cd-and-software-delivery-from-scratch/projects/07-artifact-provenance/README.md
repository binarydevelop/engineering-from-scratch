# Project: Supply-Chain SBOM & SLSA Build Provenance Attestation (Phase 212)

## 1. Project Goal
Generate verifiable cryptographic Software Bill of Materials (SBOM) and SLSA Level 2/3 provenance attestations for all release artifacts.

---

## 2. Core Architectural Deliverables
- [ ] CycloneDX v1.5 SBOM generator recording component hashes
- [ ] SLSA Provenance v1.0 statement linking artifact digest to source Git SHA
- [ ] Cosign / Sigstore signature verification harness
- [ ] Attestation verification script

---

## 3. Verification Command
To verify your project implementation, execute:
```bash
python3 projects/07-artifact-provenance/verify.py
```
