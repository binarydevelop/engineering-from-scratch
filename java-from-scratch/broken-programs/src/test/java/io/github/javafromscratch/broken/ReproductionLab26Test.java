package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 26 Reproduction: StringBuilder Repeated Resizing Overhead")
class ReproductionLab26Test {

    @Test
    @DisplayName("Should deterministically reproduce LatencyDegradation")
    void shouldReproduceFailure() {
        BuggyLab26 buggy = new BuggyLab26();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("LatencyDegradation"));
    }
}
