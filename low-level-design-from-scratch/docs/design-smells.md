# Design Smells in Object-Oriented Software

A **design smell** is a symptom in code that frequently indicates a deeper architectural or object-oriented flaw. Smells do not mean code is immediately broken; they mean the code is **fragile, resists change, or is prone to regression**.

This document catalogs the most frequent design smells encountered in Low-Level Design, complete with code examples and refactoring directions.

---

## 1. God Object (Blob / Monster Class)

### The Smell
A single class that knows too much or does too much. It centralizes control, gathers dozens of fields, and turns all other classes into passive data holders.

### Code Example
```java
// ❌ SMELL: God Object handling parking, payment, receipts, tickets, notifications, and security
public class ParkingLotManager {
    private List<Spot> spots;
    private List<Ticket> tickets;
    private DatabaseConnection db;
    private SmtpMailer mailer;
    private PaymentGateway paymentGateway;

    public void parkVehicle(String plate, String type) { /* ... */ }
    public double calculateFee(String ticketId) { /* ... */ }
    public void processPayment(String ticketId, String cardNumber) { /* ... */ }
    public void sendEmailReceipt(String email, double amount) { /* ... */ }
    public void backupToDatabase() { /* ... */ }
}
```

### The Cure
Apply the **Single Responsibility Principle (SRP)**. Extract:
- `ParkingLot` (tracks spot occupancy and vehicle placement)
- `PricingPolicy` (calculates fees from ticket duration)
- `PaymentService` (delegates to `PaymentProcessor`)
- `NotificationService` (dispatches receipts)

---

## 2. Primitive Obsession

### The Smell
Using primitive data types (`String`, `int`, `double`, `UUID`) to represent domain concepts that carry rules, invariants, and behaviors.

### Code Example
```java
// ❌ SMELL: Primitive obsession for money, zip codes, and emails
public void transferMoney(String senderEmail, String receiverEmail, double amount, String currency) {
    if (amount <= 0) throw new IllegalArgumentException();
    // Currency conversions, email format regex checks scattered in every caller
}
```

### The Cure
Introduce **Value Objects**:
- `EmailAddress` (validates syntax once at creation)
- `Money(BigDecimal amount, Currency currency)` (enforces currency consistency and rounding math)

---

## 3. Feature Envy

### The Smell
A method in class `A` is more interested in the data of class `B` than its own data. It repeatedly queries `B`'s getters to perform calculations that belong inside `B`.

### Code Example
```java
// ❌ SMELL: OrderSummary reaches inside Customer and Address to format a shipping label
public class OrderSummary {
    public String generateShippingLabel(Order order) {
        Customer c = order.getCustomer();
        Address a = c.getAddress();
        return c.getFirstName() + " " + c.getLastName() + "\n" +
               a.getStreet() + ", " + a.getCity() + " " + a.getZipCode();
    }
}
```

### The Cure
Apply **Tell, Don't Ask** or Move Method. Move the formatting logic to `Address` or `Customer`:
```java
// ✅ REFACTORED:
String label = order.getShippingLabel();
```

---

## 4. Flag Arguments (Boolean Parameters Smell)

### The Smell
Passing a `boolean` parameter into a method to determine which branch of logic to execute. This signals the method is doing at least two different things.

### Code Example
```java
// ❌ SMELL: What does true mean? Is it VIP? Is it weekend? Is it premium?
ticketService.bookTicket(user, show, true, false);
```

### The Cure
Split into two distinct, descriptive methods or use a domain enum / strategy:
```java
// ✅ REFACTORED:
ticketService.bookVipTicket(user, show);
ticketService.bookStandardTicket(user, show);
```

---

## 5. Giant Switch / Conditional Chains

### The Smell
Repeated `switch` or `if-else` chains switching on a type code or enum throughout the codebase. Every time a new type is introduced, every switch statement must be hunted down and edited.

### Code Example
```java
// ❌ SMELL: Giant switch on vehicle type
public double calculateFee(VehicleType type, long hours) {
    switch (type) {
        case MOTORCYCLE: return hours * 1.5;
        case CAR: return hours * 3.0;
        case TRUCK: return hours * 6.0;
        case BUS: return hours * 8.0;
        default: throw new IllegalArgumentException("Unknown type");
    }
}
```

### The Cure
**Replace Conditional with Polymorphism** or introduce the **Strategy Pattern**:
```java
public interface ParkingRate {
    double calculate(long hours);
}
```

---

## 6. Shotgun Surgery

### The Smell
A single change in business requirements forces you to make dozens of small modifications across many different classes.

### The Contrast with Divergent Change:
- **Divergent Change:** One class suffers many changes for *different reasons* (violates SRP).
- **Shotgun Surgery:** One requirement change causes ripples across *many classes* (indicates poor cohesion and scattered responsibilities).

### The Cure
Consolidate related logic into a single cohesive class or module.

---

## 7. Inappropriate Intimacy

### The Smell
Two classes know far too much about each other’s internal private details or package-private state, frequently reaching across boundaries.

### The Cure
Introduce an explicit interface or mediator to decouple them.

---

## 8. Excessive Inheritance (Fragile Base Class)

### The Smell
Subclassing solely for code reuse rather than modeling a genuine polymorphic behavioral substitution (`is-a`). Subclasses inherit methods that make no sense in their context.

### Code Example
```java
// ❌ SMELL: ReadOnlyList extends ArrayList and throws UnsupportedOperationException in add()
public class ReadOnlyList<E> extends ArrayList<E> {
    @Override
    public boolean add(E e) {
        throw new UnsupportedOperationException("Read only!");
    }
}
```

### The Cure
**Favor Composition over Inheritance**:
Wrap the list inside a dedicated class that exposes only query methods.

---

## 9. Anemic Domain Model

### The Smell
Domain entities are stripped of all logic, consisting strictly of fields and public getters/setters. All business logic is pushed into bloated procedural `*Service` or `*Manager` classes.

### The Cure
Push business logic and invariant validation back into the entities where the data lives.

---

## 10. Speculative Generality (Premature Abstraction / YAGNI Violation)

### The Smell
Adding complex abstract base classes, generic hooks, and factory registries for requirements that do not currently exist and may never exist.

### Code Example
```java
// ❌ SMELL: Creating a multi-cloud distributed storage adapter for a simple local cache
public interface MultiClusterDistributedStorageProviderFactoryRegistryManager { ... }
```

### The Cure
**KISS & YAGNI**: Write the minimal sufficient implementation for current verified requirements. Refactor only when new requirements demand variation.
