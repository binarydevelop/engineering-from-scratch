package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 31 Reproduction: N+1 Database Query Avalanche")
class ReproductionLab31Test {

    @Test
    @DisplayName("Should deterministically reproduce DatabaseOverload")
    void shouldReproduceFailure() {
        BuggyLab31 buggy = new BuggyLab31();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("DatabaseOverload"));
    }
}
