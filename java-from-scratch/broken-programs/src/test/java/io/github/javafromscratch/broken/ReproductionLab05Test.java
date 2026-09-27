package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 05 Reproduction: Unbounded Static Map Memory Leak")
class ReproductionLab05Test {

    @Test
    @DisplayName("Should deterministically reproduce OutOfMemoryError")
    void shouldReproduceFailure() {
        BuggyLab05 buggy = new BuggyLab05();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("OutOfMemoryError"));
    }
}
