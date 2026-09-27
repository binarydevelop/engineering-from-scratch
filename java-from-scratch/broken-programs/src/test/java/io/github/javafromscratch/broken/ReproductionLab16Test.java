package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 16 Reproduction: ThreadLocal Leak in Recycled Thread Pool")
class ReproductionLab16Test {

    @Test
    @DisplayName("Should deterministically reproduce DataPollution")
    void shouldReproduceFailure() {
        BuggyLab16 buggy = new BuggyLab16();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("DataPollution"));
    }
}
