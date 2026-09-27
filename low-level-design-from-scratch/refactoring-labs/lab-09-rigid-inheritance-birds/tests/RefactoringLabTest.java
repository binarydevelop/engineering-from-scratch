package lld.refactoringlabs.lab_09_rigid_inheritance_birds;

import lld.refactoringlabs.lab_09_rigid_inheritance_birds.solution.RefactoredSystem;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

@DisplayName("Refactoring Rigid Inheritance (Fragile Base Class) Test Suite")
class RefactoringLabTest {

    @Test
    @DisplayName("Should successfully construct refactored system and apply valid adjustments")
    void shouldMaintainInvariants() {
        RefactoredSystem system = new RefactoredSystem("SYS-001", 1000);
        system.applyAdjustment(500);

        assertThat(system.getBalanceInCents()).isEqualTo(1500);
    }

    @Test
    @DisplayName("Should guard invariants and throw when balance drops below zero")
    void shouldGuardNegativeBalanceInvariant() {
        RefactoredSystem system = new RefactoredSystem("SYS-001", 1000);

        assertThatThrownBy(() -> system.applyAdjustment(-2000))
                .isInstanceOf(IllegalStateException.class)
                .hasMessageContaining("invariant violation");
    }
}
