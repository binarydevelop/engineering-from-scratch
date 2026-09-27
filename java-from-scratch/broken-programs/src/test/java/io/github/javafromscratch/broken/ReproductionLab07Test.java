package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 07 Reproduction: Thread Pool Exhaustion / Starvation")
class ReproductionLab07Test {

    @Test
    @DisplayName("Should deterministically reproduce ThreadStarvation")
    void shouldReproduceFailure() {
        BuggyLab07 buggy = new BuggyLab07();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("ThreadStarvation"));
    }
}
