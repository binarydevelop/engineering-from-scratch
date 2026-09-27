package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 01 Reproduction: Hidden NullPointerException in Chained Call")
class ReproductionLab01Test {

    @Test
    @DisplayName("Should deterministically reproduce NullPointerException")
    void shouldReproduceFailure() {
        BuggyLab01 buggy = new BuggyLab01();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("NullPointerException"));
    }
}
