package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 27 Reproduction: Virtual Thread Pinned to Carrier in synchronized")
class ReproductionLab27Test {

    @Test
    @DisplayName("Should deterministically reproduce CarrierPinning")
    void shouldReproduceFailure() {
        BuggyLab27 buggy = new BuggyLab27();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("CarrierPinning"));
    }
}
