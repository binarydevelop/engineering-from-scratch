# Contributing to Operating Systems From Scratch

Thank you for your interest in improving and expanding `operating-systems-from-scratch`!

---

## 1. Guiding Principles

1. **First Principles First:** Never explain an OS concept through syntax or terminology alone. Always ground the explanation in physical hardware limitations, kernel data structures, and state transitions.
2. **Zero Inaccessible Magic:** Code must be concise, readable, and written in standard ISO C11 or Python 3 standard library.
3. **Safety First:** Never introduce an exercise that runs an uncontrolled fork bomb or corrupts a host system disk. All high-privilege operations must be contained in containers or disposable VMs.
4. **Follow the Lesson Template:** All new lessons or major revisions must adhere strictly to the 17-section structure defined in `LESSON_TEMPLATE.md`.

---

## 2. Coding Standards

### C Code
* Standard: ISO C11 (`-std=c11`).
* Compiles cleanly with `-Wall -Wextra -pedantic -pthread`.
* Check return values of all system calls (`open`, `read`, `write`, `fork`, `socket`, `malloc`).
* Handle errors gracefully using `perror()` or `strerror(errno)`.
* Clean up open file descriptors and dynamically allocated heap memory before exiting.

### Python Code
* Standard: Python 3.9+.
* Standard library only (no mandatory PyPI packages unless strictly optional).
* Include clear docstrings explaining data structures and simulation algorithms.

---

## 3. Pull Request Checklist

Before submitting a PR:
1. Run `./scripts/check-environment.sh`.
2. Run `make build` to verify all C binaries compile cleanly without warnings.
3. Run `make test` to verify all unit tests, simulations, and capstone tests pass.
4. Ensure solutions to new labs or exercises are placed in the appropriate `solutions/` directory.
