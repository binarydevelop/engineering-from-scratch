package lld.refactoringlabs.lab_01_parking_lot_god_class;

import lld.refactoringlabs.lab_01_parking_lot_god_class.solution.RefactoredSystem;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

@DisplayName("Deconstructing the Parking Lot God Class Test Suite")
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
