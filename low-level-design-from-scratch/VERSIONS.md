# Environment & Tooling Versions

This repository standardizes on modern, stable, long-term-support (LTS) tools to ensure reproducibility, deterministic builds, and clean object-oriented idioms without premature framework magic.

| Component | Target Version | Rationale |
|:---|:---|:---|
| **Language** | Java 21 LTS (OpenJDK) | Static typing makes behavioral contracts explicit; virtual threads, records, pattern matching for `switch`, sealed interfaces, and immutable data structures provide clean modern OOP syntax without framework baggage. |
| **Build Tool** | Apache Maven 3.9+ | Ubiquitous industry standard; strict dependency resolution and lifecycle plugins (`compile`, `test`, `package`). |
| **Test Framework** | JUnit Jupiter (JUnit 5.10.2) | Modern test engine with nested test contexts (`@Nested`), parameterized testing (`@ParameterizedTest`), dynamic tests, and explicit assertion semantics. |
| **Assertion Library** | AssertJ (3.25.3) | Fluent, readable assertions that clearly communicate expected domain invariants and test failures. |
| **Mocking / Doubles** | Self-written Fakes / Mocks | The repository deliberately avoids heavy reflection mocking libraries (e.g. Mockito) in early phases to teach test doubles from first principles. Lightweight fakes are hand-coded to keep interfaces explicit. |
| **Alternative Language** | Python 3.11+ / 3.12+ | Optional companion implementations for key lessons to demonstrate that Low-Level Design principles (SRP, Invariants, State Machines, Dependency Injection) transcend language syntax. |
| **Formatting / Linter** | Spotless / Checkstyle | Uniform coding standard enforcing clear naming, 4-space indentation, and explicit package boundaries. |

---

## Verifying Local Environment

Verify your runtime environment before running the lab:

```bash
# Check Java runtime (must be 21+)
java -version

# Check Java compiler
javac -version

# Check Maven installation
mvn -version
```

If multiple JDKs are installed on macOS, set `JAVA_HOME` explicitly:

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
```
