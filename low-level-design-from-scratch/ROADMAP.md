# Low-Level Design Roadmap: From First Principles to Production Mastery

> **Repository Motto:**  
> **Understand it. Model it. Build it. Break it. Refactor it. Test it. Extend it. Ship it.**

---

## Pedagogical Philosophy

Low-Level Design (LLD) is **not** the art of memorizing class diagrams, reciting design patterns, or drawing UML boxes in an interview. 

**Low-Level Design is the systematic discipline of translating ambiguous requirements into collaborating software components with explicit responsibilities, inviolable state invariants, decoupled interfaces, and automated behavioral tests.**

This roadmap spans **147 total phases (Phase 00 through Phase 146)** organized into 17 foundational tiers.

```text
Requirements & Use Cases
          ↓
Responsibilities & Invariants (GRASP)
          ↓
Domain Modeling (Entities & Value Objects)
          ↓
Decoupling & Behavioral Contracts (Interfaces & DI)
          ↓
The SOLID Heuristics & Anti-Patterns
          ↓
Pain-Driven Design Patterns
          ↓
State, Errors & Concurrency
          ↓
Architectural Boundaries & Persistence
          ↓
Canonical LLD Interview Problems (30+ Systems)
          ↓
Refactoring Labs, Concurrency Challenges & Capstones
          ↓
Autonomous Design Mastery
```

---

## Tier 1: The LLD Lab & First Principles (Phases 00 – 05)

| Phase | Phase Name | Focus & Motto | Key Deliverables & Concepts |
|:---|:---|:---|:---|
| **Phase 00** | **LLD Lab** | *"A design that cannot be compiled and tested is only an opinion."* | Java 21 LTS, Maven, JUnit 5 environment setup. Implementation of `HelloDomain` test suite. Verified compile-test-run pipeline. |
| **Phase 01** | **What Is Low-Level Design?** | *"HLD draws the city map; LLD engineers the plumbing and electrical circuits inside each building."* | Distinguishing HLD (distributed topology, services, protocols, databases) from LLD (object boundaries, contracts, invariants, thread safety). Scope boundaries. |
| **Phase 02** | **Requirements Before Classes** | *"The quickest way to fail an LLD interview is to start drawing class diagrams in minute two."* | Requirements decomposition. Functional vs Non-functional requirements. The Coffee Machine exercise: extracting constraints, actors, and ambiguity handling without code. |
| **Phase 03** | **Use Cases** | *"Software is an engine of state transitions triggered by use case flows."* | Modeling happy paths, alternate paths, and failure paths. Beverage selection, payment validation, dispensing, and coin return sequence analysis. |
| **Phase 04** | **Entities vs Behaviors** | *"Noun extraction is not class design."* | The danger of blindly turning every English noun into a class. Identifying dynamic operations that deserve first-class behavioral abstractions. |
| **Phase 05** | **Responsibilities** | *"The central question of OOP: Who should know this, and who should do this?"* | Responsibility assignment via GRASP Information Expert. Constructing Responsibility Tables before writing a single line of class definition. |

---

## Tier 2: Object-Oriented Fundamentals & Domain Modeling (Phases 06 – 11)

| Phase | Phase Name | Focus & Motto | Key Deliverables & Concepts |
|:---|:---|:---|:---|
| **Phase 06** | **Encapsulation** | *"An object is state paired with the behavior that protects that state."* | Demonstrating data corruption via public mutable fields. Encapsulating state behind behavioral methods. Eliminating dummy getters and setters. |
| **Phase 07** | **Invariants** | *"Make invalid states impossible at birth."* | Enforcing domain invariants at construction. Factory validation. Bank balance non-negativity and domain boundary guards. |
| **Phase 08** | **Value Objects** | *"Primitives have no domain semantics."* | Curing Primitive Obsession. Implementing `Money`, `EmailAddress`, `Coordinate`, and `TimeRange` with structural equality and immutability. |
| **Phase 09** | **Entities** | *"Value is transient; identity is perpetual."* | Distinguishing identity equality from attribute equality. Contrast `Money(100)` vs `User(id=42)`. Entity lifecycle and mutation boundaries. |
| **Phase 10** | **Composition** | *"Favor composition as your default collaboration mechanism."* | The Fragile Base Class problem. Modeling `Car has Engine` and `Order has Items`. Assembling complex behavior via object graphs. |
| **Phase 11** | **Inheritance** | *"Inherit behavior only when the is-a relationship is substitutable under all observable operations."* | When inheritance helps (framework skeletons, template hooks) and when it hurts (deep hierarchies, LSP violations, code-reuse-only subclassing). |

---

## Tier 3: Behavioral Contracts, Decoupling & Heuristics (Phases 12 – 18)

| Phase | Phase Name | Focus & Motto | Key Deliverables & Concepts |
|:---|:---|:---|:---|
| **Phase 12** | **Interfaces** | *"An interface is a contract between a caller and a provider."* | Moving from concrete coupling to interface contracts. `PaymentProcessor` with `CardPaymentProcessor` and `WalletPaymentProcessor`. Dependency direction. |
| **Phase 13** | **Dependency Injection** | *"Never let an object reach into the global namespace to construct its own dependencies."* | Manual Constructor Injection. Refactoring `OrderService` from hardcoded `new SmtpSender()` to explicit injection. Testability seams. |
| **Phase 14** | **Cohesion** | *"Things that change together must live together."* | Deconstructing bloated, scattered classes into tightly focused, single-purpose domain components. |
| **Phase 15** | **Coupling** | *"High coupling turns every single-line feature request into a 10-file refactoring nightmare."* | Measuring and reducing afferent and efferent coupling. Decoupling tight peer networks via events and interfaces. |
| **Phase 16** | **Information Hiding** | *"Expose what to do; conceal how it is done."* | Hiding internal collections, data structures, and third-party library bindings. Defending against encapsulation leaks. |
| **Phase 17** | **Tell, Don't Ask** | *"Tell an object what behavior to perform; do not interrogate its state to make decisions externally."* | Eliminating procedural service logic that pulls data from anemic objects. Moving calculations adjacent to data. |
| **Phase 18** | **Law of Demeter** | *"Talk only to your immediate friends; do not navigate through strangers' intestines."* | Refactoring `order.getCustomer().getAddress().getCity()`. Balancing Demeter with practical pragmatic query modeling. |

---

## Tier 4: The SOLID Heuristics & Simplicity (Phases 19 – 28)

| Phase | Phase Name | Focus & Motto | Key Deliverables & Concepts |
|:---|:---|:---|:---|
| **Phase 19** | **SOLID Overview** | *"SOLID is not a set of religious commandments; it is a catalog of heuristics for managing the cost of change."* | Introduction to change vectors. Why SOLID exists to prevent code rot, fragility, and rigidity. |
| **Phase 20** | **Single Responsibility Principle** | *"A class should have one, and only one, reason to change."* | Decomposing a class doing business logic, database SQL, email dispatch, and PDF generation into 4 cohesive collaborators. |
| **Phase 21** | **Open/Closed Principle** | *"Open for extension, closed for modification."* | Experiencing the pain of repeated modifications to a giant `switch(type)`. Refactoring to polymorphic extension points. |
| **Phase 22** | **Liskov Substitution Principle** | *"Subtypes must honor every behavioral promise made by their supertype."* | The Square/Rectangle and Flying Bird dilemmas. Contract pre-conditions cannot be strengthened; post-conditions cannot be weakened. |
| **Phase 23** | **Interface Segregation Principle** | *"Clients should not be forced to depend upon methods they do not call."* | Splitting a fat `MultiFunctionPrinter` interface into `Printer`, `Scanner`, and `Fax` client-specific interfaces. |
| **Phase 24** | **Dependency Inversion Principle** | *"High-level policy must never depend on low-level technological plumbing."* | Inverting dependency direction: `OrderService` depends on `OrderRepository` interface; `PostgresOrderRepository` implements it. |
| **Phase 25** | **DRY (Don't Repeat Yourself)** | *"Duplication of knowledge is evil; superficial duplication of syntax is harmless."* | The peril of premature DRY. When two similar-looking code blocks actually represent different domain concepts that evolve independently. |
| **Phase 26** | **KISS (Keep It Simple, Stupid)** | *"Simplicity is a prerequisite for reliability."* | De-engineering an over-abstracted architecture. Stripping away unnecessary generic layers and factories. |
| **Phase 27** | **YAGNI (You Aren't Gonna Need It)** | *"Build for today's concrete verified variations, not tomorrow's imaginary requirements."* | Measuring the maintenance tax of speculative generic hooks and unused configuration knobs. |
| **Phase 28** | **Design Smells** | *"Smells are early warnings of architectural degradation."* | In-depth exploration of God Object, Long Method, Feature Envy, Shotgun Surgery, Inappropriate Intimacy, and Flag Arguments. |

---

## Tier 5: Safe Refactoring Mechanics (Phases 29 – 32)

| Phase | Phase Name | Focus & Motto | Key Deliverables & Concepts |
|:---|:---|:---|:---|
| **Phase 29** | **Refactoring Fundamentals** | *"Refactoring changes internal structure without altering external behavior, backed by an iron wall of tests."* | The Red-Green-Refactor discipline. Step-by-step mechanical transformations. |
| **Phase 30** | **Extract Method / Class** | *"Small, well-named methods turn code into executable prose."* | Decomposing 200-line monolithic methods into cohesive, isolated functions and collaborating domain classes. |
| **Phase 31** | **Replace Conditional With Polymorphism** | *"Polymorphism is the object-oriented cure for branching epidemic."* | Replacing type-code conditionals with strategy hierarchies. Benchmarking before and after readability. |
| **Phase 32** | **Replace Primitive With Value Object** | *"Give your domain concepts a proper home in the type system."* | Systematic refactoring from raw strings and doubles to validated, immutable domain value objects. |

---

## Tier 6: State, Errors, Collections & Lifecycles (Phases 33 – 41)

| Phase | Phase Name | Focus & Motto | Key Deliverables & Concepts |
|:---|:---|:---|:---|
| **Phase 33** | **State Modeling** | *"A domain object is defined as much by what transitions it forbids as what it allows."* | Modeling order lifecycle: `CREATED -> PAID -> SHIPPED -> DELIVERED` and `CANCELLED`. Invariant transition matrix. |
| **Phase 34** | **Finite State Machines** | *"State + Event = Transition + Action."* | Implementing a generic, type-safe deterministic Finite State Machine from scratch. Transition tables vs object-oriented states. |
| **Phase 35** | **State Pattern** | *"When behavior diverges radically across lifecycle states, let state become an object."* | State pattern in a Vending Machine context. Comparing enum state machines vs polymorphic State objects. |
| **Phase 36** | **Error Modeling** | *"Errors are first-class domain outcomes, not unexpected anomalies."* | Categorizing errors: invalid inputs, domain rule rejections, missing resources, and system crashes. Result types vs exceptions. |
| **Phase 37** | **Exceptions** | *"Use exceptions for exceptional circumstances, never for normal algorithmic branching."* | Checked vs unchecked exceptions in Java. Domain exception hierarchies. Preserving root causes. Eliminating catch-all swallowers. |
| **Phase 38** | **Null Handling** | *"Null is a billion-dollar mistake; banish defensive null checks from your domain model."* | Leveraging `Optional<T>`, constructor validation, and the Null Object pattern. When to throw vs when to return empty. |
| **Phase 39** | **Collections and Domain Modeling** | *"Collections convey semantics; choose your data structures to enforce invariants."* | Semantic collection choices: `List` (ordered sequence), `Set` (unique membership), `Map` (keyed lookup), `Queue` (FIFO work). Unmodifiable defensive copies. |
| **Phase 40** | **Immutability** | *"What cannot change cannot be corrupted or raced."* | Java records, immutable collections, thread-safe value objects, and copy-on-write state evolution. |
| **Phase 41** | **Object Lifecycle** | *"Who creates it? Who owns it? How long does it live? Who tears it down?"* | Ephemeral value objects vs long-lived domain services vs scoped sessions. Memory and ownership discipline. |

---

## Tier 7: Design Patterns from First Principles (Phases 42 – 55)

| Phase | Phase Name | Focus & Motto | Key Deliverables & Concepts |
|:---|:---|:---|:---|
| **Phase 42** | **Factory Method** | *"When construction logic involves domain decision-making, encapsulate creation."* | Moving beyond `new`. Static factory methods (`Money.ofCents()`) and polymorphic factory methods. |
| **Phase 43** | **Abstract Factory** | *"Families of related objects must stay compatible without coupling callers to concrete suites."* | Cross-platform UI widget factories or multi-provider cloud resource suites. Appropriate use cases vs overengineering. |
| **Phase 44** | **Builder** | *"Build complex immutable aggregates step by step without constructor explosion."* | The Telescoping Constructor anti-pattern. Fluent type-safe builder with mandatory vs optional parameter validation. |
| **Phase 45** | **Singleton** | *"The most overused and abused pattern in software engineering."* | Singleton as a testing and concurrency bottleneck. Distinguishing 'single instance in DI container' from 'global static state'. |
| **Phase 46** | **Strategy Pattern** | *"Swap algorithms at runtime without modifying the context executing them."* | Problem-driven parking tariff calculation: `HourlyPricing`, `WeekendPricing`, `EventPricing`. Open/Closed in action. |
| **Phase 47** | **Observer Pattern** | *"Decouple the occurrence of an event from the multitude of side effects reacting to it."* | Event-listener dispatching in an Order Checkout context. Error isolation, synchronous vs asynchronous notification, and memory leak prevention. |
| **Phase 48** | **Command Pattern** | *"Encapsulate a request as an object, enabling undo, logging, and transactional queues."* | Building an undoable text editor / transaction engine with `execute()` and `undo()` contracts. |
| **Phase 49** | **Template Method** | *"Fix the invariant algorithm skeleton in the superclass; defer variable steps to subclasses."* | Report generation / ETL processing pipelines. Comparing Template Method (inheritance) with Strategy (composition). |
| **Phase 50** | **Adapter** | *"Convert the interface of a class into another interface clients expect."* | Integrating an incompatible third-party payment gateway into your domain's `PaymentProcessor` interface. |
| **Phase 51** | **Facade** | *"Provide a unified, simple interface to a complex subsystem."* | Wrapping audio/video encoding, security token validation, and storage subsystems behind a clean `MediaConversionFacade`. |
| **Phase 52** | **Decorator** | *"Attach additional responsibilities to an object dynamically without subclassing."* | Composable notification wrappers: `EmailNotifier` + `LoggingDecorator` + `MetricsDecorator` + `RetryDecorator`. |
| **Phase 53** | **Proxy** | *"Control and mediate access to another object."* | Protection proxies (authorization check), virtual proxies (lazy-loading large domain aggregates), and caching proxies. |
| **Phase 54** | **Chain of Responsibility** | *"Pass a request along a chain of handlers until one handles it or all validate it."* | Request authentication, rate limiting, and input sanitization pipeline. Pros and hidden-flow cons. |
| **Phase 55** | **Mediator** | *"Reduce chaotic N-to-N dependencies between classes to 1-to-N mediator interactions."* | Chat room or airport runway traffic control mediator. Preventing peer-to-peer coupling explosions. |

---

## Tier 8: Architectural Boundaries & Layering (Phases 56 – 63)

| Phase | Phase Name | Focus & Motto | Key Deliverables & Concepts |
|:---|:---|:---|:---|
| **Phase 56** | **Repository Pattern** | *"Mediate between the domain logic and data mapping layers using a collection-like interface."* | In-memory vs persistent repository contracts. Decoupling SQL queries from domain entity invariants. |
| **Phase 57** | **Service Layer** | *"Distinguish domain logic from application use case orchestration."* | Entity methods vs Domain Services (pure domain math spanning entities) vs Application Services (transactions, repositories, mailers). |
| **Phase 58** | **Layering** | *"Strict dependency rules keep high-level business rules pure and untainted by delivery mechanisms."* | Presentation -> Application -> Domain -> Infrastructure. Clean architecture boundaries without enterprise bloat. |
| **Phase 59** | **Domain Modeling** | *"Model the business reality accurately before considering database schemas."* | Identifying aggregates, entities, value objects, and domain events in a complex subscription domain. |
| **Phase 60** | **Aggregate Boundaries** | *"An aggregate is a cluster of objects treated as a single transactional consistency boundary."* | Order and OrderItems. The Aggregate Root guards all child entity mutations and guarantees atomic invariants. |
| **Phase 61** | **Persistence Boundary** | *"Never let database column constraints dictate your domain object model."* | The impedance mismatch: object graphs vs relational tables. Clean decoupling between persistence schemas and rich domain objects. |
| **Phase 62** | **DTOs (Data Transfer Objects)** | *"Do not leak internal domain representations across public network boundaries."* | Request/Response DTOs vs Domain Entities. Preventing accidental mass-assignment vulnerabilities. |
| **Phase 63** | **Mapping Layers** | *"Explicit mappers maintain clean boundaries at the cost of boilerplate."* | Manual mapper functions vs reflection mappers. Testing mapping fidelity and handling missing fields. |

---

## Tier 9: Test-Driven Design & Testability (Phases 64 – 70)

| Phase | Phase Name | Focus & Motto | Key Deliverables & Concepts |
|:---|:---|:---|:---|
| **Phase 64** | **Testing From First Principles** | *"Tests verify observable behavior, not internal implementation mechanics."* | The Arrange-Act-Assert structure. Testing public contracts rather than private methods. |
| **Phase 65** | **Unit Tests** | *"Fast, isolated, deterministic checks of domain invariants."* | Writing comprehensive domain unit tests in JUnit 5 and AssertJ. Testing edge cases, boundary conditions, and overflow risks. |
| **Phase 66** | **Test Doubles** | *"Know your test doubles: Dummy, Stub, Fake, Mock, and Spy."* | Hand-coding test doubles from scratch. Building in-memory fake repositories without Mockito magic. |
| **Phase 67** | **Dependency Injection for Testing** | *"Code designed for testability is code designed for maintainability."* | Swapping live network adapters with deterministic fakes to verify failure recovery and timeout behavior. |
| **Phase 68** | **Integration Tests** | *"Verify that independently tested components collaborate correctly across real boundaries."* | Testing repository implementations, serialization, and end-to-end use case orchestration. |
| **Phase 69** | **Contract Tests Concept** | *"Ensure that both the provider and consumer agree on interface semantics."* | Designing reusable test suites that execute against both In-Memory Fake and Production adapters. |
| **Phase 70** | **Testable Design** | *"If an object is painful to test, its design is defective."* | Eliminating static state, hidden clocks, singletons, and deep inheritance chains to achieve effortless testability. |

---

## Tier 10: Real-World Forces: Concurrency, Time & Boundaries (Phases 71 – 80)

| Phase | Phase Name | Focus & Motto | Key Deliverables & Concepts |
|:---|:---|:---|:---|
| **Phase 71** | **Concurrency in LLD** | *"When multiple threads enter an object, shared mutable state becomes a race hazard."* | The Java Memory Model basics, visibility, and mutual exclusion in domain objects. |
| **Phase 72** | **Thread Safety** | *"Who owns synchronization? Guard the invariant at the object boundary."* | Reproducing lost updates in a seat booking / inventory counter. Fixing with `AtomicInteger`, `ReentrantLock`, and synchronized blocks. |
| **Phase 73** | **Immutable Design and Concurrency** | *"Immutable objects are inherently thread-safe without synchronization locks."* | Eliminating lock contention through functional state transitions and immutable records. |
| **Phase 74** | **Idempotency in Object Design** | *"A command executed twice must leave the system in the exact same state as executed once."* | Idempotency keys in payment processing and order cancellations. Deduplication caches and state checks. |
| **Phase 75** | **Time as a Dependency** | *"Calling `Instant.now()` inside domain logic makes your code untestable."* | Injecting `java.time.Clock`. Fast-forwarding time in unit tests to verify ticket expiration and late fees deterministically. |
| **Phase 76** | **Randomness as a Dependency** | *"Inject your randomness generators to achieve 100% reproducible tests."* | Decoupling UUID generation and dice rolling via interfaces (`IdGenerator`, `DiceRollProvider`). |
| **Phase 77** | **External Services as Boundaries** | *"Third-party systems are slow, flaky, and outside your control."* | Isolating external Stripe, SendGrid, and Twilio APIs behind domain-owned interfaces and resilient adapters. |
| **Phase 78** | **Retry Responsibility** | *"Where does retry belong? Never hide retries inside low-level domain entities."* | Placing retry policies in application service orchestrators or decorators. Combining retry with idempotency. |
| **Phase 79** | **Logging Boundary** | *"Logging is an operational side effect; domain entities are not logging pipelines."* | Keeping domain models free of SLF4J logger bloat. Emitting domain events or letting application services log. |
| **Phase 80** | **Configuration** | *"Separate business policy from dynamic deployment parameters."* | Strongly-typed configuration objects. Validating timeouts, pool sizes, and pricing tariffs at startup. |

---

## Tier 11: API Design, Granularity & UML (Phases 81 – 89)

| Phase | Phase Name | Focus & Motto | Key Deliverables & Concepts |
|:---|:---|:---|:---|
| **Phase 81** | **API Design** | *"Make interfaces easy to use correctly and hard to use incorrectly."* | Method naming, parameter constraints, null defense, return types, and side-effect expectations. |
| **Phase 82** | **Boolean Parameters Smell** | *"What does `true, false` mean? Eliminate mystery boolean arguments."* | Refactoring flag arguments to expressive method names, enums, or strategy parameter objects. |
| **Phase 83** | **Method Granularity** | *"A method should do one conceptual task at a consistent level of abstraction."* | Balancing coarse-grained facade APIs with fine-grained domain logic. Avoiding micro-method fragmentation. |
| **Phase 84** | **Naming** | *"Naming is the primary mechanism of domain communication in code."* | Ubiquitous Language: eliminating developer jargon (`processData()`, `handleThing()`) in favor of domain terms (`reconcileInvoice()`, `expireReservation()`). |
| **Phase 85** | **Package / Module Boundaries** | *"Package by feature, not by technical layer."* | Organizing packages by cohesive domain modules rather than technical dumping grounds (`controllers`, `services`, `models`). |
| **Phase 86** | **UML Basics** | *"Diagrams are communication tools, not bureaucratic artifacts."* | Using class, sequence, and state diagrams strictly to clarify design and communicate intent. |
| **Phase 87** | **Class Diagrams** | *"Accurate representation of contracts, associations, and cardinalities."* | Class diagrams in Mermaid and ASCII matching real production code. |
| **Phase 88** | **Sequence Diagrams** | *"Visualizing dynamic collaboration and message flow over time."* | Tracing caller -> service -> domain -> repository interactions during complex use cases. |
| **Phase 89** | **State Diagrams** | *"Visualizing state spaces and guard conditions."* | Statecharts for elevator movement, order lifecycles, and vending machine mechanics. |

---

## Tier 12: Canonical LLD Interview Problems (Phases 90 – 120)

Every problem in this tier follows the complete 13-step methodology with runnable code, domain invariants, and automated tests.

| Phase | Problem | Core Design Challenge |
|:---|:---|:---|
| **Phase 90** | **LLD Problem-Solving Framework** | Master 13-step blueprint for 45-minute interviews. |
| **Phase 91** | **Tic-Tac-Toe** | Board representation, dynamic grid sizing, winning strategies (Rows, Cols, Diagonals). |
| **Phase 92** | **Snake and Ladder** | Board entity, configurable dice strategies, jump chains, turn-based game loop. |
| **Phase 93** | **Vending Machine** | State pattern vs Enum FSM: Item selection, coin validation, dispensing, change return. |
| **Phase 94** | **Parking Lot** | Spot allocation strategies, multi-floor layout, vehicle dimensions, dynamic pricing tariffs. |
| **Phase 95** | **Elevator System** | Car state, hall vs car requests, SCAN/LOOK dispatching scheduling algorithms. |
| **Phase 96** | **Library Management** | Book title vs Book Copy identity, lending limits, reservation queues, fine calculation. |
| **Phase 97** | **Chess Game** | 8x8 Board, piece movement rules, check/checkmate detection, turn validation. |
| **Phase 98** | **ATM System** | Session state, PIN authentication, cash dispenser chain of responsibility, balance check. |
| **Phase 99** | **Splitwise** | Users, groups, expense splitting strategies (Exact, Equal, Percentage), balance graph simplification. |
| **Phase 100** | **Movie Ticket Booking** | Seat inventory, concurrency locks, temporary reservation holds, payment timeout release. |
| **Phase 101** | **Hotel Booking** | Room type inventory, date range overlaps, seasonal pricing policies, cancellation rules. |
| **Phase 102** | **Car Rental System** | Vehicle fleets, branch reservations, rental duration calculation, damage inspection log. |
| **Phase 103** | **Food Delivery System** | Restaurant menus, cart calculation, order aggregate, driver assignment strategy. |
| **Phase 104** | **Ride Sharing (Uber/Lyft)** | Rider/Driver matching strategies, trip state machine, surge pricing policies. |
| **Phase 105** | **Logging Framework** | Logger hierarchy, Log levels, Chain of appenders (Console, File), formatters. |
| **Phase 106** | **Cache System (LRU / LFU)** | Eviction strategies (LRU via Doubly Linked List + Map), thread safety, generic storage. |
| **Phase 107** | **Rate Limiter** | Token Bucket, Fixed Window, Sliding Window Log algorithms encapsulated cleanly. |
| **Phase 108** | **Task Scheduler** | One-time and recurring cron tasks, priority scheduling queue, execution worker pool. |
| **Phase 109** | **Notification Service** | Multi-channel dispatch (Email, SMS, Push), provider failover adapters, template rendering. |
| **Phase 110** | **Payment System** | Payment methods, idempotency keys, processor interfaces, refund state machines. |
| **Phase 111** | **Inventory Management** | Stock SKU quantities, atomic reservation, release on timeout, fulfillment verification. |
| **Phase 112** | **Shopping Cart** | Cart aggregate, line item quantity invariants, coupon discount pricing strategies. |
| **Phase 113** | **Order Management** | Comprehensive order lifecycle, domain event emission, cancellation state invariants. |
| **Phase 114** | **File Storage Abstraction** | `FileStore` interface, `LocalFileStore`, `InMemoryFileStore`, cloud S3 adapter concepts. |
| **Phase 115** | **In-Memory Database** | Key-value store with secondary indexing, filter predicates, and light transactional rollback. |
| **Phase 116** | **Message Queue** | In-memory topic partitions, consumer group offsets, message acknowledge semantics. |
| **Phase 117** | **Pub/Sub System** | Topics, subscribers, filter criteria, broadcast dispatch vs queue point-to-point. |
| **Phase 118** | **Metrics Library** | In-memory Counter, Gauge, Timer metrics collectors and console/Prometheus formatters. |
| **Phase 119** | **Feature Flag System** | User context targeting rules, percentage rollouts, override strategy chain. |
| **Phase 120** | **Access Control (RBAC)** | Users, Roles, Permissions, Resources, and authorization evaluation engine. |

---

## Tier 13: Refactoring Labs & Advanced Design Skills (Phases 121 – 132)

| Phase | Challenge | Focus & Learning Outcome |
|:---|:---|:---|
| **Phase 121** | **Refactoring Challenge I** | Deconstruct a 600-line God-Class Parking Lot into clean, testable, decoupled components. |
| **Phase 122** | **Refactoring Challenge II** | Eliminate Shotgun Surgery in an existing Notification system by creating clean provider extension seams. |
| **Phase 123** | **Refactoring Challenge III** | Fix broken domain invariants and public setters in an Order Management system. |
| **Phase 124** | **Testing Challenge** | Discover and pin down the behavior of an untested legacy component using characterization tests. |
| **Phase 125** | **Concurrency Challenge** | Detect and eliminate a critical double-booking race condition under multi-threaded load. |
| **Phase 126** | **Persistence Challenge** | Migrate an in-memory repository to a simulated relational schema without rewriting domain logic. |
| **Phase 127** | **API Evolution Challenge** | Evolve a public interface contract with new optional parameters without breaking existing client callers. |
| **Phase 128** | **Design Review Skill** | Critique existing production designs, spotting coupling, hidden assumptions, and design smells. |
| **Phase 129** | **Tradeoff Thinking** | Explicitly compare Simplicity vs Extensibility, Concrete vs Abstract, and Rich vs Anemic models. |
| **Phase 130** | **Pattern Selection** | Train pattern restraint: Given 10 real scenarios, decide which pattern fits or if NO PATTERN is best. |
| **Phase 131** | **Anti-Patterns Catalog** | Deep dive into Pattern Soup, Inappropriate Intimacy, God Objects, and Vague Managers with refactoring fixes. |
| **Phase 132** | **When Not to Abstract** | Why the wrong abstraction is far more costly than code duplication. The rule of three. |

---

## Tier 14: LLD in the Real World & System Design (Phases 133 – 136)

| Phase | Phase Name | Focus & Concepts |
|:---|:---|:---|
| **Phase 133** | **LLD and Databases** | Domain entities vs Database rows. Unit of Work and transaction boundaries. |
| **Phase 134** | **LLD and HTTP APIs** | Mapping HTTP Controllers and DTOs into Application Services and Domain Aggregates. |
| **Phase 135** | **LLD and Event-Driven Systems** | Publishing Domain Events (`OrderPlaced`, `PaymentFailed`) to decouple secondary side effects. |
| **Phase 136** | **LLD and System Design** | Connecting the Macro to the Micro: How High-Level Design services decompose into Low-Level Design components. |

---

## Tier 15: Interview Simulations (Phases 137 – 139)

Timed, realistic 45-minute mock interview challenges where requirements evolve under pressure:
- **Phase 137: Interview Simulation I (Unseen Problem):** Move from vague prompt to verified domain model without looking at solutions.
- **Phase 138: Interview Simulation II (Mid-Interview Requirement Shift):** Handle a radical requirement change introduced halfway through implementation.
- **Phase 139: Interview Simulation III (Late-Stage Concurrency Pressure):** Re-evaluate design assumptions when thread safety and high contention are demanded at the last minute.

---

## Tier 16: Capstone Projects (Phases 140 – 144)

Comprehensive, multi-stage enterprise domains built incrementally from scratch:
- **Phase 140: Capstone: Parking Platform:** Multi-floor, multi-gate, dynamic tariffs, EV charging stations, VIP reservations, and concurrent access.
- **Phase 141: Capstone: Booking Engine:** Generic resource reservation system with temporary locks, expiration timers, and cancellation policies.
- **Phase 142: Capstone: Extensible Notification Platform:** Multi-channel notification pipeline with priority queues, template engines, and resilient provider failovers.
- **Phase 143: Capstone: Order Domain:** Full e-commerce aggregate root with inventory reservations, payment processing seams, and domain event publishing.
- **Phase 144: Capstone: Build a Mini Framework:** Educational IoC dependency injection container and event dispatcher built from scratch to demystify what enterprise frameworks do under the hood.

---

## Tier 17: Mastery & Final Challenges (Phases 145 – 146)

- **Phase 145: Final Design Challenge Set:** 25 unseen, un-solved production LLD problems across beginner, intermediate, and advanced tiers.
- **Phase 146: Final Mental Model:** The culmination of your journey. An unseen problem solved effortlessly using first-principles reasoning from behavior to responsibilities to shipping code.
