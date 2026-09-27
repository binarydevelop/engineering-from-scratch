package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab 30 Reproduction: Partial Multi-Statement Failure Without Transaction")
class ReproductionLab30Test {

    @Test
    @DisplayName("Should deterministically reproduce DataInconsistency")
    void shouldReproduceFailure() {
        BuggyLab30 buggy = new BuggyLab30();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("DataInconsistency"));
    }
}
