# Java for Low-Level Design: The Minimalist Guide

This guide covers **only the essential Java language constructs** needed to practice Low-Level Design (LLD) from first principles. It intentionally skips enterprise framework magic (e.g., Spring Boot, JPA, Hibernate, reflection injection) so you can focus 100% on **object-oriented modeling, contracts, invariants, and behavioral boundaries**.

---

## 1. Classes: Encapsulating State & Behavior

In LLD, an object is **not** a dumb data bucket with getters and setters. An object is an **autonomous entity** that pairs internal state with behavior protecting that state.

```java
package lld.foundations.bank;

import java.util.Objects;

public class BankAccount {
    // Encapsulation rule: fields are private and final whenever possible
    private final String accountNumber;
    private long balanceInCents; // Avoid floating-point money

    public BankAccount(String accountNumber, long initialDepositInCents) {
        if (accountNumber == null || accountNumber.isBlank()) {
            throw new IllegalArgumentException("Account number must not be blank");
        }
        if (initialDepositInCents < 0) {
            throw new IllegalArgumentException("Initial deposit cannot be negative");
        }
        this.accountNumber = accountNumber;
        this.balanceInCents = initialDepositInCents;
    }

    // Behavior protects invariants
    public void deposit(long amountInCents) {
        if (amountInCents <= 0) {
            throw new IllegalArgumentException("Deposit amount must be positive");
        }
        this.balanceInCents += amountInCents;
    }

    public void withdraw(long amountInCents) {
        if (amountInCents <= 0) {
            throw new IllegalArgumentException("Withdrawal amount must be positive");
        }
        if (amountInCents > this.balanceInCents) {
            throw new IllegalStateException("Insufficient funds");
        }
        this.balanceInCents -= amountInCents;
    }

    public long getBalanceInCents() {
        return balanceInCents;
    }

    public String getAccountNumber() {
        return accountNumber;
    }
}
```

---

## 2. Interfaces: Defining Contracts

An `interface` specifies **what** an object does, not **how** it does it. It decouples high-level policy from low-level implementation details.

```java
package lld.foundations.payment;

public interface PaymentProcessor {
    PaymentResult processPayment(PaymentRequest request);
}
```

Implementations fulfill the contract:

```java
public class CreditCardPaymentProcessor implements PaymentProcessor {
    @Override
    public PaymentResult processPayment(PaymentRequest request) {
        // Concrete credit card payment gateway logic
        return PaymentResult.success("TXN-CC-" + System.currentTimeMillis());
    }
}
```

---

## 3. Enums: State, Strategies & Types

Enums in Java are full classes. They can hold fields, constructor methods, and even behavior:

```java
package lld.foundations.order;

public enum OrderStatus {
    PENDING {
        @Override
        public boolean canTransitionTo(OrderStatus next) {
            return next == PAID || next == CANCELLED;
        }
    },
    PAID {
        @Override
        public boolean canTransitionTo(OrderStatus next) {
            return next == SHIPPED || next == CANCELLED;
        }
    },
    SHIPPED {
        @Override
        public boolean canTransitionTo(OrderStatus next) {
            return next == DELIVERED;
        }
    },
    DELIVERED {
        @Override
        public boolean canTransitionTo(OrderStatus next) {
            return false; // Terminal state
        }
    },
    CANCELLED {
        @Override
        public boolean canTransitionTo(OrderStatus next) {
            return false; // Terminal state
        }
    };

    public abstract boolean canTransitionTo(OrderStatus next);
}
```

---

## 4. Records: Modern Value Objects

Java 14+ records provide immutable data carriers with automatic `equals()`, `hashCode()`, and `toString()`. They are ideal for **Value Objects** and **Data Transfer Objects (DTOs)**.

```java
package lld.foundations.money;

import java.math.BigDecimal;
import java.util.Currency;

public record Money(BigDecimal amount, Currency currency) {
    // Compact constructor for invariant validation
    public Money {
        Objects.requireNonNull(amount, "Amount cannot be null");
        Objects.requireNonNull(currency, "Currency cannot be null");
        if (amount.compareTo(BigDecimal.ZERO) < 0) {
            throw new IllegalArgumentException("Amount cannot be negative");
        }
    }

    public Money add(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new IllegalArgumentException("Currency mismatch: " + this.currency + " vs " + other.currency);
        }
        return new Money(this.amount.add(other.amount), this.currency);
    }
}
```

---

## 5. Generics: Type-Safe Abstractions

Generics allow repositories, collections, and containers to operate across types safely:

```java
package lld.foundations.repository;

import java.util.Optional;

public interface Repository<T, ID> {
    void save(T entity);
    Optional<T> findById(ID id);
    void deleteById(ID id);
}
```

---

## 6. Collections: Choosing the Right Semantics

In LLD, collection selection conveys **domain semantics**:

| Collection | Domain Semantics | Example in LLD |
|:---|:---|:---|
| `List<E>` (`ArrayList`, `CopyOnWriteArrayList`) | Ordered sequence; duplicates allowed | History of events, audit log, checkout steps |
| `Set<E>` (`HashSet`, `TreeSet`, `ConcurrentSkipListSet`) | Unique collection; no duplicates | Assigned parking spots, role permissions |
| `Map<K, V>` (`HashMap`, `ConcurrentHashMap`) | Key-value lookup; dictionary | Cache, in-memory repository, routing table |
| `Queue<E>` (`ArrayDeque`, `PriorityBlockingQueue`) | Work queues; FIFO or prioritized scheduling | Task scheduler, print spooler, event queue |

Always return unmodifiable views from entities to prevent internal state leaks:

```java
public class Cart {
    private final List<CartItem> items = new java.util.ArrayList<>();

    // Defend against caller mutating internal list
    public List<CartItem> getItems() {
        return java.util.Collections.unmodifiableList(items);
    }
}
```

---

## 7. Exceptions: Distinguishing Failures

Avoid treating exceptions as ordinary control flow. Distinguish between:
1. **Validation errors:** `IllegalArgumentException` / `NullPointerException` (client violated precondition)
2. **Domain rule rejections:** `DomainRuleViolationException` (e.g., `SpotAlreadyOccupiedException`)
3. **Infrastructure failures:** `RepositoryAccessException` (I/O, network)

```java
package lld.foundations.exception;

public class DomainException extends RuntimeException {
    public DomainException(String message) {
        super(message);
    }
    public DomainException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

---

## 8. Packages: Organizing by Feature vs Layer

We avoid dumping everything into `com.company.models` or `com.company.services`. Group by cohesive domain modules:

```text
lld/
  parkinglot/
    allocation/
    pricing/
    ticket/
    ParkingLot.java
```

---

## 9. Unit Testing with JUnit 5 & AssertJ

```java
package lld.foundations.bank;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

class BankAccountTest {

    @Test
    @DisplayName("Should withdraw funds when balance is sufficient")
    void shouldWithdrawWhenBalanceSufficient() {
        BankAccount account = new BankAccount("ACC-1001", 5000);

        account.withdraw(2000);

        assertThat(account.getBalanceInCents()).isEqualTo(3000);
    }

    @Test
    @DisplayName("Should throw exception when withdrawing more than current balance")
    void shouldThrowWhenWithdrawingOverBalance() {
        BankAccount account = new BankAccount("ACC-1001", 1000);

        assertThatThrownBy(() -> account.withdraw(2000))
                .isInstanceOf(IllegalStateException.class)
                .hasMessage("Insufficient funds");
    }
}
```

That is all the Java syntax required. Everything else in this repository is **design thinking**.
