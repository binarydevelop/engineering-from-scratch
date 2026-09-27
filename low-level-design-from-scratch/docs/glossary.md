# Low-Level Design Glossary

A precise conceptual glossary for Low-Level Design (LLD). In LLD interviews and architecture reviews, ambiguous terminology leads to broken boundaries. Use these definitions to anchor discussions.

---

| Term | What People Say (Misconception) | What It Actually Means |
|:---|:---|:---|
| **Low-Level Design (LLD)** | "Writing class diagrams and choosing design patterns." | Translating requirements into collaborating software components with clear responsibilities, explicit boundaries, state invariants, and tested contracts. |
| **High-Level Design (HLD)** | "Drawing architecture boxes for microservices." | Defining system topology, network boundaries, data storage models, communication protocols, and scaling strategies across independent deployed processes. |
| **Object** | "An instance of a class with getters and setters." | A computational entity combining private internal state with behavior that enforces invariants on that state. |
| **Encapsulation** | "Making fields private and adding public getters/setters." | Bundling data with the code that manipulates it while hiding the internal representation to maintain inviolable rules (invariants). |
| **Abstraction** | "Creating an abstract class or interface." | Simplifying complexity by exposing only the essential behavioral characteristics to a caller while concealing implementation mechanisms. |
| **Information Hiding** | "Not letting other classes see your variables." | Hiding design decisions (data structures, algorithms, third-party libraries) that are most likely to change, preventing ripple effects. |
| **In-variant** | "A validation rule on input." | A condition that must *always* remain true for an object throughout its entire lifecycle (pre-conditions, post-conditions, and during transitions). |
| **Value Object** | "A data class or DTO." | An immutable object whose equality is determined solely by its structural attribute values rather than an identity token (e.g., `Money`, `Coordinates`, `EmailAddress`). |
| **Entity** | "A database table row model." | A domain object defined by its distinct identity that persists continuously across time and state changes (e.g., `User(id=42)`, `Order(id=TX-99)`). |
| **Aggregate** | "A big parent class." | A cluster of domain objects (entities and value objects) treated as a single unit for data changes, bounded by an Aggregate Root that guards all internal invariants. |
| **Coupling** | "How many classes you import." | The degree of interdependence between software modules. High coupling means changing module A breaks module B. |
| **Cohesion** | "Putting related files in the same folder." | The degree to which elements within a single module belong together and serve a single well-defined purpose. |
| **Tell, Don't Ask** | "Never call getters." | A design heuristic suggesting callers should tell an object *what behavior to execute* rather than asking for its state and making decisions externally. |
| **Law of Demeter** | "Never use more than one dot (`a.b.c()`)." | Principle of Least Knowledge: an object should only talk to its immediate collaborators, method parameters, and self-instantiated objects, avoiding navigation through deep object graphs. |
| **Single Responsibility Principle (SRP)**| "A class should do only one thing." | A module should have one, and only one, reason to change (i.e., should be responsible to one specific actor or stakeholder). |
| **Open/Closed Principle (OCP)** | "Never edit existing code." | Software artifacts should be open for extension (new behavior can be added) but closed for modification (existing stable caller contracts remain untouched). |
| **Liskov Substitution Principle (LSP)** | "Subclasses must implement all parent methods." | Objects of a superclass should be replaceable with objects of a subclass without altering the correctness of the program (preserving behavioral contracts). |
| **Interface Segregation Principle (ISP)** | "Make interfaces as small as possible." | Clients should not be forced to depend upon interfaces that have methods they do not consume. Prefer focused, client-specific role interfaces. |
| **Dependency Inversion Principle (DIP)** | "Using Spring `@Autowired`." | High-level modules should not depend on low-level modules; both should depend on abstractions. Abstractions should not depend on details; details should depend on abstractions. |
| **Dependency Injection (DI)** | "A framework like Guice or Spring." | A technique where an object receives its dependencies from the outside (typically via constructor) rather than creating them internally with `new`. |
| **Design Pattern** | "A reusable template to copy-paste." | A named, documented solution to a recurring architectural problem within a specific context, balancing competing design forces. |
| **Idempotency** | "Caching an HTTP response." | The property of an operation whereby performing it multiple times produces the identical side effect as performing it exactly once. |
| **Test Double** | "A Mockito mock." | A generic term for any surrogate object used in place of a production collaborator during automated tests (Dummy, Stub, Fake, Mock, Spy). |
| **Fake** | "A broken test." | A working implementation of an interface that takes shortcuts making it unsuitable for production (e.g., in-memory hash map repository). |
| **Mock** | "Any test helper object." | A pre-programmed test double configured with expectations about the specific method calls it should receive, verifying interactions rather than state. |
| **Anemic Domain Model** | "A clean model with just data." | An anti-pattern where domain classes contain only fields and getters/setters, while all business logic is stripped out into external procedural "services". |
