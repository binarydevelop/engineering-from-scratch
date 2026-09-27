# The Low-Level Design Interview & Problem-Solving Framework

A repeatable, 13-step battle-tested methodology for solving any Low-Level Design problem in an interview, architecture review, or production engineering project.

---

## The Fatal Mistake
When an interviewer says:
> *"Design a Movie Ticket Booking System."*

The amateur candidate says:
> *"I will use the State Pattern for seat status, Factory Pattern to create seats, and Observer Pattern to notify users."*

This immediately reveals a junior mindset. An LLD problem is not an anagram game where you find which Gang of Four pattern fits the prompt. It is an exercise in **translating ambiguous requirements into cohesive, testable, invariant-protecting software components**.

---

## The 13-Step Framework

### Step 1: Clarify Requirements (5 mins)
Never assume anything. Ask targeted questions to narrow the domain:
- What are the core user operations?
- Are bookings permanent or held temporarily with an expiration window?
- Can a cinema have multiple screens, or just one?
- What payment methods are supported?

### Step 2: Define Scope & Boundaries (3 mins)
Explicitly list what is **in-scope** and what is **out-of-scope**:
- **In Scope:** Seat inventory, hold reservation (10-minute lock), fee calculation, booking confirmation.
- **Out of Scope:** Credit card payment gateway protocol, video streaming, mobile UI, multi-region distributed consensus.

### Step 3: Identify Use Cases (5 mins)
Enumerate the concrete actor workflows:
1. `SearchShows(cinemaId, date)`
2. `SelectSeats(showId, seatIds, userId)`
3. `HoldSeats(showId, seatIds, holdDuration)`
4. `ConfirmBooking(bookingId, paymentConfirmation)`
5. `ExpireReservation(bookingId)`

### Step 4: Identify Entities and Value Objects (5 mins)
Distinguish objects by identity vs value:
- **Entities:** `Cinema`, `Screen`, `Show`, `Seat`, `Booking` (defined by unique IDs).
- **Value Objects:** `SeatNumber(row, col)`, `Money(amount, currency)`, `TimeRange(start, end)`.

### Step 5: Assign Responsibilities (GRASP / Information Expert) (5 mins)
Fill the responsibility table:
| Responsibility | Owner | Justification |
|:---|:---|:---|
| Determine if seat is available | `ShowSeat` | Owns the individual seat status and hold timestamp |
| Reserve multiple seats atomically | `BookingService` | Coordinates across multiple seats to prevent partial reservation |
| Compute ticket price | `PricingStrategy` | Isolates tariff rules (matinee, weekend, 3D surcharge) |

### Step 6: Model Relationships & Object Graph (5 mins)
Establish clear object associations:
- `Cinema` has 1..* `Screens` (Composition)
- `Screen` has 1..* `Seats` (Composition)
- `Show` has 1..* `ShowSeats` (Stateful representation of seat for a specific show)
- `Booking` references `User`, `Show`, and `List<ShowSeat>`

### Step 7: Define Interfaces & Behavioral Contracts (5 mins)
Draft method signatures with explicit inputs and outputs:
```java
public interface BookingService {
    ReservationHold holdSeats(String showId, List<String> seatIds, String userId);
    Booking confirmBooking(String holdId, PaymentDetails payment);
    void releaseExpiredHolds();
}
```

### Step 8: Model Key Workflows & State Transitions (5 mins)
Map out states and legal transitions:
```text
[AVAILABLE] ──(hold)──> [HELD] ──(confirm)──> [BOOKED]
                          │
                   (timeout/cancel)
                          │
                          ▼
                     [AVAILABLE]
```

### Step 9: Handle Edge Cases & Failures (3 mins)
- Two users attempt to hold the exact same seat at the exact same millisecond.
- Payment fails halfway through confirmation.
- User closes browser after seats are held.

### Step 10: Implement Core Path (15 mins)
Write clean, idiomatic code for the core classes.
- Use private final fields.
- Validate invariants at constructor.
- Never write dummy getters/setters without behavior.

### Step 11: Discuss Extensibility (3 mins)
Show how the design accommodates future changes without rewriting:
- *"If the business wants dynamic pricing based on occupancy, we implement `OccupancyBasedPricingStrategy` without touching `BookingService`."*

### Step 12: Address Concurrency & Thread Safety (3 mins)
Identify shared mutable state:
- Where is the race condition? (`ShowSeat.hold()`)
- How do we protect it? (`synchronized`, `ReentrantLock`, `AtomicReference`, or versioned optimistic locking).

### Step 13: Test Strategy (3 mins)
Outline key tests:
- Happy path: hold -> confirm -> seat marked booked.
- Invariant test: holding an already held seat throws `SeatUnavailableException`.
- Timeout test: expired hold allows a second user to book.
