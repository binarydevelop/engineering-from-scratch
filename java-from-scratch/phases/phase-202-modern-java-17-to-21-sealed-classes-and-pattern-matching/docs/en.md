# Phase 202: Modern Java (17-21) Architecture: Sealed Classes, Pattern Matching, and Records

## 1. Why This Matters for MAANG & Senior/Staff Roles
Java has undergone its most aggressive modernization cycle in history. In senior technical interviews, writing legacy Java 8 style code (verbose boilerplate, mutable JavaBeans, nested instanceof-cast blocks) signals stagnation. Mastery of Records, Sealed Class Hierarchies, and Pattern Matching enables elegant, algebraically complete domain modeling similar to Scala, Rust, and Kotlin.

---

## 2. Core Concepts & Architecture Deep-Dive
### Core Language Evolutions
1. **Records (JEP 395)**: Immutable transparent data carriers. Compiler automatically generates immutable state fields, canonical constructor, `equals()`, `hashCode()`, and `toString()`. Records cannot extend classes (already extend `java.lang.Record`) but can implement interfaces.
2. **Sealed Classes & Interfaces (JEP 409)**: Restricts which specific subclasses/implementations are permitted to extend them via `permits` clause. Provides closed-world type hierarchies for algebraic data types.
3. **Pattern Matching for `switch` (JEP 441)**: Eliminates verbose `instanceof` cascades and unsafe casts. Supports type patterns, guarded patterns (`when`), and exhaustive completeness checks.

---

## 3. High-Value Interview Angle & Failure Modes
### Algebraic Domain Modeling Pattern
```java
// Closed algebraic hierarchy for payment processing
public sealed interface PaymentMethod 
    permits CreditCard, BankTransfer, CryptoWallet {}

public record CreditCard(String cardNumber, String cvv, int expYear) 
    implements PaymentMethod {}

public record BankTransfer(String iban, String routingCode) 
    implements PaymentMethod {}

public record CryptoWallet(String walletAddress, Network network) 
    implements PaymentMethod {
    public enum Network { ETHEREUM, BITCOIN, SOLANA }
}

// Exhaustive pattern matching without default branch
public String processPayment(PaymentMethod method, BigDecimal amount) {
    return switch (method) {
        case CreditCard cc when cc.expYear() < 2026 -> "Expired Card Rejected";
        case CreditCard cc -> "Charging CreditCard ending in " + cc.cardNumber().substring(12);
        case BankTransfer bt -> "Initiating ACH transfer via " + bt.routingCode();
        case CryptoWallet cw -> "Triggering smart contract on " + cw.network();
        // Compiler guarantees exhaustiveness: NO default clause required!
    };
}
```

---

## 4. Hands-On Practice & Implementation Drills
### Interview Significance
- Interviewers evaluate code quality and conciseness in Low-Level Design rounds.
- Demonstrates domain-driven modeling without null-pointer vulnerabilities.
- Guarantees compile-time safety: adding a new payment subtype causes a compile error in every switch statement missing that case.

---

## 5. Key Takeaways & Cheat Sheet
- Records provide clean, immutable value objects out of the box.
- Sealed interfaces enable compile-time exhaustiveness checking in switch expressions.
- Guarded patterns (`when`) combine type validation and business checks cleanly.
- Standard syntax in modern Java backend and LLD interview rounds.
