package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 22 Reproduction: Blocking I/O Inside Common ForkJoinPool")
class ReproductionLab22Test {

    @Test
    @DisplayName("Should deterministically reproduce CommonPoolStarvation")
    void shouldReproduceFailure() {
        BuggyLab22 buggy = new BuggyLab22();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("CommonPoolStarvation"));
    }
}
