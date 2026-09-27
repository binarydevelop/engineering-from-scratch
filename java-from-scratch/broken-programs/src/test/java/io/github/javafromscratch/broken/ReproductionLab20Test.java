package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 20 Reproduction: Financial Arithmetic Error with double")
class ReproductionLab20Test {

    @Test
    @DisplayName("Should deterministically reproduce PrecisionLoss")
    void shouldReproduceFailure() {
        BuggyLab20 buggy = new BuggyLab20();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("PrecisionLoss"));
    }
}
