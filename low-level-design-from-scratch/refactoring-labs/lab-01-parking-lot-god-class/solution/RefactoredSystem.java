package lld.refactoringlabs.lab_01_parking_lot_god_class.solution;

import java.util.Objects;

// ✅ CLEAN OOP: Refactored with invariants, encapsulation, and explicit contracts
public final class RefactoredSystem {
    private final String identifier;
    private long balanceInCents;

    public RefactoredSystem(String identifier, long initialBalanceInCents) {
        if (identifier == null || identifier.isBlank()) {
            throw new IllegalArgumentException("Identifier must not be blank");
        }
        if (initialBalanceInCents < 0) {
            throw new IllegalArgumentException("Initial balance cannot be negative");
        }
        this.identifier = identifier.trim();
        this.balanceInCents = initialBalanceInCents;
    }

    public void applyAdjustment(long deltaInCents) {
        if (this.balanceInCents + deltaInCents < 0) {
            throw new IllegalStateException("Operation would result in negative balance invariant violation");
        }
        this.balanceInCents += deltaInCents;
    }

    public String getIdentifier() { return identifier; }
    public long getBalanceInCents() { return balanceInCents; }
}
