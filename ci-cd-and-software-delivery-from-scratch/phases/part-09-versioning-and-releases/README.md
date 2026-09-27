# Part IX: Versioning & Releases (Phases 63–69)

## Motto
> "A build is a technical artifact. A release is a business decision. A deployment is an operational event. Keep them clearly distinct, and make every release immutable."

---

## Delivery Problem
A developer makes a hotfix and pushes it directly over the existing `v1.2.0` Git tag: `git tag -f v1.2.0 && git push -f --tags`. 

Customer A downloads `v1.2.0` at 09:00 AM; Customer B downloads `v1.2.0` at 11:00 AM. 
When Customer A files a bug report, the support and engineering teams cannot reproduce it because their local environment contains Customer B's code. Version numbers have lost all meaning, and customer trust is destroyed.

---

## Prediction
1. Overwriting an existing release tag breaks supply-chain reproducibility and client expectations.
2. Generating release notes by blindly dumping raw Git commit messages produces unreadable noise for operators.
3. Decoupling build, release, and deployment allows teams to prepare and verify releases days before exposing them to users.

---

## First Principles
1. **The Core Triad: Build vs Release vs Deployment**:
   - **Build**: Compiles source into a binary or container image. (Technical machine process).
   - **Release**: Designates an immutable package as intended for distribution/production use, assigning version numbers, changelogs, and signed metadata. (Business milestone).
   - **Deployment**: The act of running that release package inside an operational environment and connecting network routing. (Operational event).
2. **Semantic Versioning (SemVer: `MAJOR.MINOR.PATCH`)**:
   - **MAJOR**: Incompatible API changes (breaking consumer contracts).
   - **MINOR**: Backward-compatible new functionality.
   - **PATCH**: Backward-compatible bug fixes.
3. **The Immutability Invariant**:
   Once a release tag (`v1.4.0`) is published, it must **never** be modified, deleted, or re-pointed. If a defect is found 5 minutes after release, publish `v1.4.1`.

---

## Manual Process
Generate a release package manually:

```bash
# 1. Inspect the release script
cat scripts/release.sh

# 2. Generate release v1.0.0 bundle
bash scripts/release.sh 1.0.0

# 3. Inspect the generated release notes and manifest
cat outputs/release-v1.0.0/RELEASE_NOTES.md
cat outputs/release-v1.0.0/sbom.json
```

---

## Mental Model

```text
[ Git Commit SHA: c477286... ]
              │
              ▼ Tagged as 'v1.4.0'
[ Annotated Git Tag (Signed) ]
              │
              ▼ Automated Release Workflow
      ┌───────┴──────────────────────┐
      ▼                              ▼
[ Release Artifact: app-1.4.0.tgz ] [ Signed Release Ledger ]
- SHA-256 Checksum                 - CycloneDX SBOM
- OCI Container Digest             - SLSA Provenance Attestation
- Human-Readable Changelog         - Compatibility Invariants
```

---

## Automate It (Phase 68: Automated Release on Tag Push)

```yaml
# .github/workflows/release.yml
on:
  push:
    tags:
      - 'v[0-9]+.[0-9]+.[0-9]+'

jobs:
  release:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4.1.7
      - run: bash scripts/release.sh "${GITHUB_REF_NAME#v}"
```

---

## Run It
Execute `scripts/release.sh` from the repository root:

```bash
bash scripts/release.sh 1.0.0
```

---

## Break It (Phase 69: Release Immutability Violation)
1. Re-run `scripts/release.sh 1.0.0` after a release tag exists.
2. Observe how the script detects that the release tag already exists and exits with code 1, protecting the release from being overwritten!

---

## Debug It
When a release fails:
- Check if the tag already exists in local Git or remote origin (`git ls-remote --tags origin`).
- Ensure the version string strictly adheres to Semantic Versioning (`vMAJOR.MINOR.PATCH`).

---

## Security
- Sign Git release tags with GPG or SSH (`git tag -s v1.0.0`).
- Attach cryptographically verifiable SLSA provenance attestations to all release bundles.

---

## Optimize It
- Use automated Conventional Commits (`feat:`, `fix:`, `feat!:`) to automatically calculate the next SemVer bump and generate structured changelogs.

---

## Deployment Implication
Deployments should reference immutable release bundles or container digests rather than arbitrary Git commit SHAs, giving operators clear human-readable context during incidents.

---

## Recovery
If a release is broken:
- Do NOT delete the Git tag.
- Cut a patch release (`v1.0.1`) containing the fix, update the changelog with post-mortem notes, and deploy `v1.0.1`.

---

## Practical Exercises (Part IX)
1. **Exercise 9.1**: Create an annotated Git tag with a multi-line release message and verify it using `git show v1.0.0`.
2. **Exercise 9.2**: Write a Python script that parses Conventional Commit messages since the last tag and categorizes them into Features, Fixes, and Breaking Changes.
3. **Exercise 9.3**: Implement SemVer calculation logic that determines whether the next release is MAJOR, MINOR, or PATCH based on commit messages.
4. **Exercise 9.4**: Test release immutability by configuring a simulated Git hook that rejects `git push --delete` or `git push --force` targeting release tags.
5. **Exercise 9.5**: Generate a release notes document following [`RELEASE_TEMPLATE.md`](../../RELEASE_TEMPLATE.md) for a simulated hotfix release.
6. **Exercise 9.6**: Verify that the generated release tarball contains the exact Git commit SHA embedded inside its build manifest.
7. **Exercise 9.7**: Write a script that checks whether an API change is backward-compatible before allowing a MINOR version bump.
8. **Exercise 9.8**: Calculate the Mean Time to Release (MTTRel) for your team's typical release workflow.

---

## Questions for Mastery
1. *What is the difference between a build artifact, a release package, and a deployment?*
2. *Why is `git tag -f` (force-moving a release tag) considered an unacceptable anti-pattern in production engineering?*
3. *How do Conventional Commits automate the release generation process?*

---

## What Comes Next
In **Part X (Phases 70–74)**, we explore Environments: Dev, Staging, Production parity, Twelve-Factor configuration injection, and GitHub Environment protection rules.
