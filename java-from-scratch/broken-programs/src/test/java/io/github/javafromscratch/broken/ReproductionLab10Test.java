package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 10 Reproduction: Mutable Key Mutates After Put in HashMap")
class ReproductionLab10Test {

    @Test
    @DisplayName("Should deterministically reproduce KeyLoss")
    void shouldReproduceFailure() {
        BuggyLab10 buggy = new BuggyLab10();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("KeyLoss"));
    }
}
