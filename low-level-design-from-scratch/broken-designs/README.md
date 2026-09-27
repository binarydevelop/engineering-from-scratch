# Broken Designs: Antipattern Case Studies

This catalog deconstructs famous object-oriented anti-patterns observed in production systems.

1. **The Blob (God Object):** Centralizes all domain decisions into a single 2,000-line monster.
2. **Anemic Domain Model:** Strips entities of behavior, turning them into passive data bags with public getters and setters.
3. **Pattern Soup:** Forcing 5 design patterns into a simple calculation that requires 20 lines of clean code.
4. **Shotgun Surgery:** Requiring 10 file edits whenever a single business requirement changes.
5. **Divergent Change:** A class changing for multiple unrelated business actors.
6. **LSP Violations:** Subclasses overriding parent methods to throw `UnsupportedOperationException`.
7. **Temporal Coupling:** Methods that crash if not invoked in a magic implicit order.
8. **Leaky Encapsulation:** Exposing internal mutable lists directly through getters.
